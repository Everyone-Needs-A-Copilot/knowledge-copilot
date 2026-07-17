#!/usr/bin/env python3
"""Build and validate a Prerequisite Tree (PRT) from obstacles and intermediate objectives.

Takes a target and a list of obstacles (each with an intermediate objective and
dependency list), performs topological sort, groups into phases, identifies the
critical path, and detects circular dependencies.

Usage:
    python3 prt_builder.py --file input.json
    python3 prt_builder.py --stdin
    python3 prt_builder.py '{"target": "...", "obstacles": [...]}'

Input JSON:
{
    "target": "Launch enterprise tier with SSO, admin controls, and dedicated onboarding",
    "obstacles": [
        {
            "id": "O1",
            "description": "We have no SSO integration",
            "intermediate_objective": "SSO authenticates users via SAML 2.0 against at least one enterprise identity provider",
            "dependencies": []
        },
        {
            "id": "O2",
            "description": "Enterprise pricing has not been validated with real prospects",
            "intermediate_objective": "3 target enterprise prospects confirm willingness to pay at the proposed price point",
            "dependencies": []
        },
        {
            "id": "O3",
            "description": "We have no admin UI for managing team members",
            "intermediate_objective": "Admins can invite, remove, and assign roles to team members via a self-serve UI",
            "dependencies": ["O1"]
        },
        {
            "id": "O4",
            "description": "The sales team has no enterprise pitch materials",
            "intermediate_objective": "Sales deck, ROI calculator, and case study template are ready and signed off",
            "dependencies": ["O2"]
        },
        {
            "id": "O5",
            "description": "We have no dedicated enterprise onboarding process",
            "intermediate_objective": "Enterprise onboarding playbook exists and has been piloted with one customer",
            "dependencies": ["O3", "O4"]
        }
    ]
}

Output: Phased sequence, parallel tracks, critical path, circular dependency warnings.
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields


def detect_cycles(graph, all_ids):
    """Detect circular dependencies using DFS with three-color marking.

    Returns list of cycles found, each as a list of node IDs.
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in all_ids}
    parent = {node: None for node in all_ids}
    cycles = []

    def dfs(node, path):
        color[node] = GRAY
        path.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in color:
                continue
            if color[neighbor] == GRAY:
                # Found a cycle — extract it
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])
            elif color[neighbor] == WHITE:
                parent[neighbor] = node
                dfs(neighbor, path[:])
        color[node] = BLACK

    for node in all_ids:
        if color[node] == WHITE:
            dfs(node, [])

    return cycles


def topological_sort(graph, all_ids):
    """Kahn's algorithm for topological sort.

    Returns (sorted_list, remaining_nodes_if_cycle).
    remaining_nodes will be non-empty if there is a cycle.
    """
    # Build in-degree count
    in_degree = {node: 0 for node in all_ids}
    for node in all_ids:
        for dep in graph.get(node, []):
            if dep in in_degree:
                in_degree[node] += 1

    # Start with nodes that have no dependencies
    queue = [node for node in all_ids if in_degree[node] == 0]
    sorted_order = []

    while queue:
        # Sort for deterministic output
        queue.sort()
        node = queue.pop(0)
        sorted_order.append(node)
        # Reduce in-degree for nodes that depend on this one
        for candidate in all_ids:
            if node in graph.get(candidate, []):
                in_degree[candidate] -= 1
                if in_degree[candidate] == 0:
                    queue.append(candidate)

    remaining = [n for n in all_ids if n not in sorted_order]
    return sorted_order, remaining


def assign_phases(obstacles_by_id):
    """Assign phase numbers using BFS-style level assignment.

    Phase 1 = no dependencies. Phase N = all dependencies in phases < N.
    Returns dict of {obstacle_id: phase_number}.
    """
    phase = {}
    resolved = set()

    # Nodes with no dependencies get phase 1
    changed = True
    current_phase = 1

    while changed:
        changed = False
        for oid, obs in obstacles_by_id.items():
            if oid in phase:
                continue
            deps = obs.get('dependencies', [])
            if all(d in resolved for d in deps):
                phase[oid] = current_phase
                changed = True

        # Add this phase's nodes to resolved, move to next phase
        newly_resolved = [oid for oid, p in phase.items() if p == current_phase and oid not in resolved]
        if newly_resolved:
            resolved.update(newly_resolved)
            current_phase += 1

    return phase


def find_critical_path(obstacles_by_id, phase_map):
    """Find the longest dependency chain by number of nodes.

    Returns the critical path as a list of obstacle IDs.
    """
    all_ids = list(obstacles_by_id.keys())

    # Memoized longest path ending at each node
    memo = {}

    def longest_path_to(node):
        if node in memo:
            return memo[node]
        deps = obstacles_by_id[node].get('dependencies', [])
        if not deps:
            memo[node] = [node]
            return [node]
        best = []
        for dep in deps:
            candidate = longest_path_to(dep)
            if len(candidate) > len(best):
                best = candidate
        result = best + [node]
        memo[node] = result
        return result

    critical = []
    for node in all_ids:
        path = longest_path_to(node)
        if len(path) > len(critical):
            critical = path

    return critical


def find_parallel_tracks(obstacles_by_id, phase_map):
    """Identify groups of obstacles in the same phase that share no dependencies.

    Returns dict of {phase: [[track_a_ids], [track_b_ids], ...]}.
    Obstacles that could be done in parallel are grouped together.
    """
    from collections import defaultdict
    phases = defaultdict(list)
    for oid, p in phase_map.items():
        phases[p].append(oid)

    parallel = {}
    for phase_num, ids in phases.items():
        if len(ids) <= 1:
            parallel[phase_num] = [ids]
            continue

        # Simple grouping: obstacles with overlapping dependency sets may be sequential;
        # obstacles with entirely disjoint dependency ancestry are parallel tracks.
        # We use union-find to group obstacles that share a common ancestor within this phase.
        def ancestors(oid, visited=None):
            if visited is None:
                visited = set()
            if oid in visited:
                return visited
            visited.add(oid)
            for dep in obstacles_by_id[oid].get('dependencies', []):
                ancestors(dep, visited)
            return visited

        ancestor_sets = {oid: ancestors(oid) for oid in ids}

        # Group by shared ancestors
        groups = []
        assigned = set()
        for oid in sorted(ids):
            if oid in assigned:
                continue
            group = [oid]
            assigned.add(oid)
            for other in sorted(ids):
                if other in assigned:
                    continue
                # Share ancestors (excluding selves) means they may be sequential
                shared = ancestor_sets[oid] & ancestor_sets[other] - {oid, other}
                if shared:
                    group.append(other)
                    assigned.add(other)
            groups.append(sorted(group))

        parallel[phase_num] = groups

    return {str(k): v for k, v in sorted(parallel.items())}


def validate_dependencies(obstacles, all_ids):
    """Check for references to non-existent obstacle IDs.

    Returns list of error strings.
    """
    errors = []
    id_set = set(all_ids)
    for obs in obstacles:
        for dep in obs.get('dependencies', []):
            if dep not in id_set:
                errors.append(
                    f"Obstacle '{obs['id']}' references unknown dependency '{dep}'"
                )
    return errors


def build_prt(data):
    require_fields(data, ['target', 'obstacles'])

    target = data['target']
    obstacles = data['obstacles']

    if not isinstance(obstacles, list) or len(obstacles) == 0:
        print("Error: 'obstacles' must be a non-empty list", file=sys.stderr)
        sys.exit(1)

    # Validate each obstacle
    for obs in obstacles:
        require_fields(obs, ['id', 'description', 'intermediate_objective'], context=f"obstacle '{obs.get('id', '?')}'")
        if 'dependencies' not in obs:
            obs['dependencies'] = []

    all_ids = [obs['id'] for obs in obstacles]
    obstacles_by_id = {obs['id']: obs for obs in obstacles}

    # Build dependency graph: node -> list of nodes it depends on
    dep_graph = {obs['id']: obs.get('dependencies', []) for obs in obstacles}

    # Validate dependency references
    ref_errors = validate_dependencies(obstacles, all_ids)

    # Detect cycles
    cycle_warnings = []
    cycles = detect_cycles(dep_graph, all_ids)
    if cycles:
        for cycle in cycles:
            cycle_warnings.append(f"Circular dependency detected: {' → '.join(cycle)}")

    # Topological sort to detect any remaining cycle issues
    sorted_ids, stuck_ids = topological_sort(dep_graph, all_ids)

    if stuck_ids and not cycle_warnings:
        cycle_warnings.append(f"Could not resolve order for obstacles: {', '.join(stuck_ids)} — check for cycles")

    # Assign phases (only if no unresolvable cycles)
    phase_map = {}
    if not stuck_ids:
        phase_map = assign_phases(obstacles_by_id)
    else:
        # Partial phase map for resolvable nodes
        resolvable = {oid: obstacles_by_id[oid] for oid in sorted_ids}
        phase_map = assign_phases(resolvable)

    # Group obstacles by phase
    from collections import defaultdict
    phases_grouped = defaultdict(list)
    for oid in sorted_ids:
        p = phase_map.get(oid, 0)
        phases_grouped[p].append(oid)

    # Build phase output
    phases_output = []
    for phase_num in sorted(phases_grouped.keys()):
        ids_in_phase = phases_grouped[phase_num]
        phase_obstacles = []
        for oid in ids_in_phase:
            obs = obstacles_by_id[oid]
            phase_obstacles.append({
                'id': oid,
                'description': obs['description'],
                'intermediate_objective': obs['intermediate_objective'],
                'dependencies': obs.get('dependencies', [])
            })
        phases_output.append({
            'phase': phase_num,
            'obstacle_count': len(ids_in_phase),
            'obstacles': phase_obstacles
        })

    # Critical path
    critical_path_ids = []
    critical_path_details = []
    if not stuck_ids:
        critical_path_ids = find_critical_path(obstacles_by_id, phase_map)
        critical_path_details = [
            {
                'id': oid,
                'intermediate_objective': obstacles_by_id[oid]['intermediate_objective']
            }
            for oid in critical_path_ids
        ]

    # Parallel tracks per phase
    parallel_tracks = {}
    if not stuck_ids:
        parallel_tracks = find_parallel_tracks(obstacles_by_id, phase_map)

    # Summary stats
    total_phases = len(phases_output)
    total_obstacles = len(obstacles)
    parallelizable_count = sum(
        len(ids_in_phase) - 1
        for ids_in_phase in phases_grouped.values()
        if len(ids_in_phase) > 1
    )

    result = {
        'target': target,
        'summary': {
            'total_obstacles': total_obstacles,
            'total_phases': total_phases,
            'critical_path_length': len(critical_path_ids),
            'parallelizable_obstacles': parallelizable_count,
            'has_circular_dependencies': len(cycle_warnings) > 0,
            'validation_errors': ref_errors
        },
        'phases': phases_output,
        'critical_path': critical_path_details,
        'parallel_tracks': parallel_tracks,
        'warnings': cycle_warnings + ref_errors
    }

    # Human summary
    lines = [
        f"Target: {target}",
        f"Obstacles: {total_obstacles} | Phases: {total_phases} | Critical path: {len(critical_path_ids)} steps",
        "",
        "Phase sequence:"
    ]
    for phase in phases_output:
        lines.append(f"  Phase {phase['phase']} ({phase['obstacle_count']} obstacle(s)):")
        for obs in phase['obstacles']:
            dep_str = f"  [deps: {', '.join(obs['dependencies'])}]" if obs['dependencies'] else ""
            lines.append(f"    [{obs['id']}] {obs['intermediate_objective']}{dep_str}")

    if critical_path_ids:
        lines.append(f"\nCritical path ({len(critical_path_ids)} steps): {' → '.join(critical_path_ids)}")

    if parallelizable_count:
        lines.append(f"Parallelizable work: {parallelizable_count} obstacle(s) can run concurrently within their phases")

    if cycle_warnings:
        lines.append("\nWARNINGS:")
        for w in cycle_warnings:
            lines.append(f"  ! {w}")

    return result, '\n'.join(lines)


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    result, summary = build_prt(data)
    format_output(result, summary)


if __name__ == '__main__':
    main()
