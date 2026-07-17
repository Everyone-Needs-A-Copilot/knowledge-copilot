#!/usr/bin/env python3
"""Identify the critical chain and size project buffers using CCPM.

Finds the critical path by aggressive duration, resolves resource contention
to produce the critical chain, sizes project and feeding buffers using the
50% rule, and outputs a full schedule.

Usage:
    python3 critical_chain.py --file project.json
    echo '{...}' | python3 critical_chain.py --stdin

Input JSON:
{
  "tasks": [
    {
      "id": "A",
      "name": "Requirements",
      "duration_aggressive": 3,
      "duration_safe": 6,
      "dependencies": [],
      "resource": "analyst"
    }
  ]
}

Output: critical chain, project buffer, feeding buffers, total duration, schedule.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, classify_zone, currency, pct


def build_task_map(tasks):
    return {t['id']: t for t in tasks}


def compute_earliest_start(task_id, task_map, memo):
    """Compute earliest start time using aggressive durations (forward pass)."""
    if task_id in memo:
        return memo[task_id]
    task = task_map[task_id]
    if not task.get('dependencies'):
        memo[task_id] = 0
        return 0
    es = max(
        compute_earliest_start(dep, task_map, memo) + task_map[dep]['duration_aggressive']
        for dep in task['dependencies']
    )
    memo[task_id] = es
    return es


def find_critical_path(tasks, task_map):
    """Find the critical path by aggressive durations. Returns list of task IDs."""
    memo = {}
    # Compute earliest finish for every task
    ef = {}
    for t in tasks:
        es = compute_earliest_start(t['id'], task_map, memo)
        ef[t['id']] = es + t['duration_aggressive']

    # Terminal tasks: tasks that are not a dependency of any other task
    all_deps = set()
    for t in tasks:
        all_deps.update(t.get('dependencies', []))
    terminal_ids = [t['id'] for t in tasks if t['id'] not in all_deps]

    # Critical path ends at the task with the latest EF among terminals
    end_id = max(terminal_ids, key=lambda tid: ef[tid])
    project_duration = ef[end_id]

    # Trace back: for each task, its predecessor on the critical path is the
    # dependency with the highest EF (latest-finish = longest path contribution)
    cp = []
    current = end_id
    while current:
        cp.append(current)
        task = task_map[current]
        deps = task.get('dependencies', [])
        if not deps:
            break
        # Choose the predecessor whose EF equals current task's ES
        current_es = memo[current]
        current = next(
            (d for d in deps if ef[d] == current_es),
            max(deps, key=lambda d: ef[d])
        )

    cp.reverse()
    return cp, project_duration, memo, ef


def resolve_resource_contention(tasks, task_map, es_memo, cp_ids):
    """
    Detect resource contention: if two tasks could run in parallel but share a resource,
    serialize them (the critical chain task goes first).
    Returns adjusted early starts that respect resource constraints.
    """
    # Build time windows for each task using aggressive durations
    scheduled_start = dict(es_memo)  # copy
    resource_schedule = {}  # resource -> list of (start, end, task_id)

    # Process tasks in topological order (sort by earliest start, then by whether they're on CP)
    cp_set = set(cp_ids)
    sorted_tasks = sorted(tasks, key=lambda t: (scheduled_start[t['id']], 0 if t['id'] in cp_set else 1))

    for task in sorted_tasks:
        tid = task['id']
        resource = task.get('resource')
        if not resource:
            continue

        desired_start = scheduled_start[tid]
        duration = task['duration_aggressive']

        if resource not in resource_schedule:
            resource_schedule[resource] = []

        # Check for overlap with already-scheduled tasks on this resource
        adjusted_start = desired_start
        changed = True
        while changed:
            changed = False
            for (s, e, other_tid) in resource_schedule[resource]:
                # Overlap if [adjusted_start, adjusted_start+dur) overlaps [s, e)
                if adjusted_start < e and adjusted_start + duration > s:
                    # Push to after this block
                    adjusted_start = e
                    changed = True

        scheduled_start[tid] = adjusted_start
        resource_schedule[resource].append((adjusted_start, adjusted_start + duration, tid))

    return scheduled_start, resource_schedule


def find_critical_chain(tasks, task_map, scheduled_start):
    """
    After resource resolution, find the longest path using scheduled starts.
    Returns critical chain task IDs.
    """
    ef_resolved = {
        t['id']: scheduled_start[t['id']] + t['duration_aggressive']
        for t in tasks
    }

    all_deps = set()
    for t in tasks:
        all_deps.update(t.get('dependencies', []))
    terminal_ids = [t['id'] for t in tasks if t['id'] not in all_deps]

    end_id = max(terminal_ids, key=lambda tid: ef_resolved[tid])
    project_end = ef_resolved[end_id]

    # Trace back through scheduled starts
    cc = []
    current = end_id
    while current:
        cc.append(current)
        task = task_map[current]
        deps = task.get('dependencies', [])
        if not deps:
            break
        # Predecessor whose EF (resolved) equals current task's scheduled start
        current_ss = scheduled_start[current]
        predecessor = next(
            (d for d in deps if ef_resolved[d] == current_ss),
            max(deps, key=lambda d: ef_resolved[d])
        )
        current = predecessor

    cc.reverse()
    return cc, project_end


def size_buffer(task_ids, task_map):
    """50% of sum of (safe - aggressive) for the given task IDs."""
    total_safety = sum(
        task_map[tid]['duration_safe'] - task_map[tid]['duration_aggressive']
        for tid in task_ids
    )
    return round(total_safety * 0.5, 2)


def find_feeding_chains(tasks, task_map, cc_ids):
    """
    Identify feeding chains: paths that feed into the critical chain but are not on it.
    Returns list of dicts: {merge_point, tasks: [task_ids], buffer_size}.
    """
    cc_set = set(cc_ids)
    feeding_buffers = []
    visited_in_feeding = set()

    for cc_task_id in cc_ids:
        cc_task = task_map[cc_task_id]
        for dep_id in cc_task.get('dependencies', []):
            if dep_id in cc_set:
                continue
            # Trace back the feeding chain from dep_id
            feeding_chain = []
            queue = [dep_id]
            while queue:
                tid = queue.pop()
                if tid in visited_in_feeding or tid in cc_set:
                    continue
                visited_in_feeding.add(tid)
                feeding_chain.append(tid)
                t = task_map[tid]
                for d in t.get('dependencies', []):
                    if d not in cc_set:
                        queue.append(d)

            if feeding_chain:
                fb_size = size_buffer(feeding_chain, task_map)
                feeding_buffers.append({
                    'merge_point': cc_task_id,
                    'merge_point_name': cc_task['name'],
                    'feeding_tasks': feeding_chain,
                    'buffer_size': fb_size
                })

    return feeding_buffers


def analyze_project(data):
    require_fields(data, ['tasks'])
    tasks = data['tasks']
    if not tasks:
        return {'error': 'No tasks provided'}, 'Error: no tasks'

    for t in tasks:
        require_fields(t, ['id', 'name', 'duration_aggressive', 'duration_safe'], context=f"task '{t.get('id', '?')}'")
        t.setdefault('dependencies', [])
        t.setdefault('resource', None)

    task_map = build_task_map(tasks)

    # Step 1: Critical path by aggressive duration
    cp_ids, cp_duration, es_memo, ef_cp = find_critical_path(tasks, task_map)

    # Step 2: Resolve resource contention
    scheduled_start, resource_schedule = resolve_resource_contention(tasks, task_map, es_memo, cp_ids)

    # Step 3: Critical chain = longest path after resource resolution
    cc_ids, cc_end = find_critical_chain(tasks, task_map, scheduled_start)

    # Step 4: Size project buffer
    project_buffer = size_buffer(cc_ids, task_map)
    total_duration = cc_end + project_buffer

    # Step 5: Feeding buffers
    feeding_buffers = find_feeding_chains(tasks, task_map, cc_ids)

    # Step 6: Build schedule
    schedule = []
    for t in tasks:
        tid = t['id']
        ss = scheduled_start[tid]
        dur = t['duration_aggressive']
        schedule.append({
            'id': tid,
            'name': t['name'],
            'resource': t.get('resource'),
            'start': ss,
            'end': ss + dur,
            'on_critical_chain': tid in set(cc_ids)
        })
    schedule.sort(key=lambda x: (x['start'], x['id']))

    # Resource utilization summary
    resource_util = {}
    for resource, windows in resource_schedule.items():
        total_busy = sum(e - s for s, e, _ in windows)
        resource_util[resource] = {
            'tasks': len(windows),
            'busy_periods': total_busy,
            'span': cc_end
        }

    result = {
        'critical_chain': {
            'task_ids': cc_ids,
            'task_names': [task_map[tid]['name'] for tid in cc_ids],
            'chain_duration': cc_end,
            'project_buffer': project_buffer,
            'total_project_duration': round(total_duration, 2)
        },
        'critical_path_before_resource_resolution': {
            'task_ids': cp_ids,
            'duration': cp_duration
        },
        'feeding_buffers': feeding_buffers,
        'schedule': schedule,
        'resource_utilization': resource_util
    }

    summary_lines = [
        f"Critical Chain: {' → '.join(task_map[tid]['name'] for tid in cc_ids)}",
        f"Chain Duration: {cc_end} periods",
        f"Project Buffer: {project_buffer} periods (50% rule)",
        f"Total Project Duration: {round(total_duration, 2)} periods",
    ]
    if feeding_buffers:
        summary_lines.append(f"\nFeeding Buffers ({len(feeding_buffers)}):")
        for fb in feeding_buffers:
            names = [task_map[tid]['name'] for tid in fb['feeding_tasks']]
            summary_lines.append(f"  Into '{fb['merge_point_name']}': {fb['buffer_size']} periods [{', '.join(names)}]")

    return result, '\n'.join(summary_lines)


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    result, summary = analyze_project(data)
    format_output(result, summary)


if __name__ == '__main__':
    main()
