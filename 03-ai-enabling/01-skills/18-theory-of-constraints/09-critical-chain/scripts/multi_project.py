#!/usr/bin/env python3
"""Stagger multi-project schedules around the drum resource.

Identifies the most contended resource across all projects (the drum),
then staggers project start dates so the drum is never double-booked.

Usage:
    python3 multi_project.py --file portfolio.json
    echo '{...}' | python3 multi_project.py --stdin

Input JSON:
{
  "projects": [
    {
      "id": "P1",
      "name": "Alpha",
      "priority": 1,
      "tasks": [
        {
          "id": "A",
          "name": "Design",
          "duration_aggressive": 5,
          "duration_safe": 10,
          "dependencies": [],
          "resource": "senior_dev"
        }
      ]
    }
  ],
  "shared_resources": ["senior_dev", "architect"]
}

Output: drum resource, staggered start dates, drum utilization, per-project schedule.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, classify_zone, pct


def build_task_map(tasks):
    return {t['id']: t for t in tasks}


def compute_es(task_id, task_map, memo):
    if task_id in memo:
        return memo[task_id]
    task = task_map[task_id]
    if not task.get('dependencies'):
        memo[task_id] = 0
        return 0
    es = max(
        compute_es(dep, task_map, memo) + task_map[dep]['duration_aggressive']
        for dep in task['dependencies']
    )
    memo[task_id] = es
    return es


def schedule_project(tasks, start_offset=0):
    """
    Schedule a single project's tasks respecting dependencies.
    Returns {task_id: {start, end, resource}}.
    """
    task_map = build_task_map(tasks)
    memo = {}
    for t in tasks:
        t.setdefault('dependencies', [])
        t.setdefault('resource', None)
        compute_es(t['id'], task_map, memo)

    return {
        tid: {
            'start': start_offset + memo[tid],
            'end': start_offset + memo[tid] + task_map[tid]['duration_aggressive'],
            'resource': task_map[tid].get('resource'),
            'name': task_map[tid]['name']
        }
        for tid in memo
    }


def project_duration(tasks):
    """Return aggressive critical path duration for a project."""
    task_map = build_task_map(tasks)
    memo = {}
    for t in tasks:
        t.setdefault('dependencies', [])
        compute_es(t['id'], task_map, memo)
    if not memo:
        return 0
    return max(memo[tid] + task_map[tid]['duration_aggressive'] for tid in memo)


def resource_load(tasks):
    """Return {resource: total_duration} for a project."""
    load = {}
    for t in tasks:
        r = t.get('resource')
        if r:
            load[r] = load.get(r, 0) + t['duration_aggressive']
    return load


def identify_drum(projects, shared_resources):
    """
    The drum is the resource with the highest total demand across all projects.
    Only considers shared_resources if provided; otherwise all resources.
    """
    total_load = {}
    for p in projects:
        for r, dur in resource_load(p['tasks']).items():
            if not shared_resources or r in shared_resources:
                total_load[r] = total_load.get(r, 0) + dur

    if not total_load:
        return None, {}

    drum = max(total_load, key=lambda r: total_load[r])
    return drum, total_load


def find_drum_windows(tasks, drum_resource):
    """Return list of (relative_start, relative_end) for drum resource tasks in a project."""
    task_map = build_task_map(tasks)
    memo = {}
    for t in tasks:
        t.setdefault('dependencies', [])
        compute_es(t['id'], task_map, memo)

    windows = []
    for t in tasks:
        if t.get('resource') == drum_resource:
            es = memo[t['id']]
            windows.append((es, es + t['duration_aggressive'], t['id'], t['name']))
    return windows


def stagger_projects(projects, drum_resource):
    """
    Assign start offsets so no two projects occupy the drum resource simultaneously.
    Projects are processed in priority order (lower priority number = higher priority).
    """
    sorted_projects = sorted(projects, key=lambda p: p.get('priority', 999))
    drum_occupied = []  # list of (global_start, global_end, project_id)
    project_starts = {}

    for project in sorted_projects:
        pid = project['id']
        drum_windows = find_drum_windows(project['tasks'], drum_resource)

        if not drum_windows:
            # No drum usage — start immediately
            project_starts[pid] = 0
            continue

        # Try start_offset = 0, then push until no overlap
        start_offset = 0
        placed = False
        max_attempts = 1000

        for _ in range(max_attempts):
            # Check if this project's drum windows (shifted by start_offset) overlap any occupied window
            conflict = False
            for (rel_s, rel_e, _, _) in drum_windows:
                global_s = start_offset + rel_s
                global_e = start_offset + rel_e
                for (occ_s, occ_e, _) in drum_occupied:
                    if global_s < occ_e and global_e > occ_s:
                        conflict = True
                        start_offset = occ_e - rel_s
                        break
                if conflict:
                    break

            if not conflict:
                placed = True
                break

        if not placed:
            # Fallback: place after all current occupied windows
            if drum_occupied:
                start_offset = max(occ_e for _, occ_e, _ in drum_occupied)
            else:
                start_offset = 0

        project_starts[pid] = start_offset

        # Register drum windows
        for (rel_s, rel_e, _, _) in drum_windows:
            drum_occupied.append((start_offset + rel_s, start_offset + rel_e, pid))

    return project_starts


def analyze_portfolio(data):
    require_fields(data, ['projects'])
    projects = data['projects']
    shared_resources = data.get('shared_resources', [])

    for p in projects:
        require_fields(p, ['id', 'name', 'tasks'], context=f"project '{p.get('id', '?')}'")
        for t in p['tasks']:
            require_fields(t, ['id', 'name', 'duration_aggressive', 'duration_safe'],
                           context=f"task '{t.get('id', '?')}' in project '{p.get('id', '?')}'")
            t.setdefault('dependencies', [])
            t.setdefault('resource', None)

    drum, total_load = identify_drum(projects, shared_resources)

    if not drum:
        return {'error': 'No shared resources found across projects'}, 'Error: no shared resources'

    project_starts = stagger_projects(projects, drum)

    # Build per-project output
    project_schedules = []
    for p in projects:
        pid = p['id']
        start_offset = project_starts.get(pid, 0)
        sched = schedule_project(p['tasks'], start_offset)
        dur = project_duration(p['tasks'])
        p_end = start_offset + dur

        # Size project buffer for this project
        total_safety = sum(
            t['duration_safe'] - t['duration_aggressive']
            for t in p['tasks']
        )
        pb = round(total_safety * 0.5, 2)

        project_schedules.append({
            'id': pid,
            'name': p['name'],
            'priority': p.get('priority', None),
            'start_offset': start_offset,
            'chain_end': p_end,
            'project_buffer': pb,
            'delivery_date': round(p_end + pb, 2),
            'drum_windows': [
                {
                    'task': name,
                    'global_start': start_offset + rel_s,
                    'global_end': start_offset + rel_e
                }
                for (rel_s, rel_e, _, name) in find_drum_windows(p['tasks'], drum)
            ],
            'task_schedule': [
                {
                    'id': tid,
                    'name': sched[tid]['name'],
                    'resource': sched[tid]['resource'],
                    'start': sched[tid]['start'],
                    'end': sched[tid]['end']
                }
                for tid in sorted(sched, key=lambda x: sched[x]['start'])
            ]
        })

    # Drum utilization
    if project_schedules:
        span = max(ps['chain_end'] for ps in project_schedules)
        drum_busy = total_load.get(drum, 0)
        drum_utilization = drum_busy / span if span > 0 else 0
    else:
        span = 0
        drum_utilization = 0

    result = {
        'drum_resource': drum,
        'drum_total_demand': total_load.get(drum, 0),
        'drum_utilization_pct': round(drum_utilization, 4),
        'portfolio_span': span,
        'resource_load_summary': dict(sorted(total_load.items(), key=lambda x: -x[1])),
        'projects': project_schedules
    }

    summary_lines = [
        f"Drum Resource: {drum} (total demand: {total_load.get(drum, 0)} periods)",
        f"Drum Utilization: {pct(drum_utilization)} over portfolio span of {span} periods",
        f"\nStaggered Project Starts:"
    ]
    for ps in project_schedules:
        summary_lines.append(
            f"  {ps['name']}: start={ps['start_offset']}, delivery={ps['delivery_date']} (incl. buffer)"
        )

    return result, '\n'.join(summary_lines)


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    result, summary = analyze_portfolio(data)
    format_output(result, summary)


if __name__ == '__main__':
    main()
