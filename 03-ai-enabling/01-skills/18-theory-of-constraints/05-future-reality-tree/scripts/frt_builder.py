#!/usr/bin/env python3
"""
frt_builder.py — Future Reality Tree structure validator and UDE coverage analyzer.

Takes injections, original UDEs, desirable effects, and cause-effect connections.
Calculates UDE coverage, identifies disconnected injections, validates structure.

Input (JSON):
  {
    "injections": [
      { "id": "I1", "description": "..." }
    ],
    "original_udes": [
      { "id": "U1", "description": "..." }
    ],
    "desirable_effects": [
      {
        "id": "DE1",
        "description": "...",
        "resolves_ude": "U1"    // UDE id this DE eliminates (optional)
      }
    ],
    "connections": [
      {
        "from_id": "I1",
        "to_id": "DE1",
        "rationale": "..."
      }
    ]
  }

Output (stdout): JSON analysis with coverage, resolved UDEs, warnings
Summary (stderr): human-readable overview
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, pct


HELP = """
Usage:
  python3 frt_builder.py '<json>'
  python3 frt_builder.py --file frt.json
  python3 frt_builder.py --stdin < frt.json

Required fields:
  injections[]        Proposed changes (id, description)
  original_udes[]     UDEs from the CRT (id, description)
  desirable_effects[] Expected positive outcomes (id, description, resolves_ude?)
  connections[]       Cause-effect links (from_id, to_id, rationale)

Output: UDE coverage analysis, disconnected injections, structural warnings.
"""


def _build_graph(connections):
    outgoing = {}
    incoming = {}
    for conn in connections:
        fid = conn['from_id']
        tid = conn['to_id']
        outgoing.setdefault(fid, []).append(tid)
        incoming.setdefault(tid, []).append(fid)
    return outgoing, incoming


def _collect_all_nodes(injections, desirable_effects, connections):
    nodes = set()
    for inj in injections:
        nodes.add(inj['id'])
    for de in desirable_effects:
        nodes.add(de['id'])
    for conn in connections:
        nodes.add(conn['from_id'])
        nodes.add(conn['to_id'])
    return nodes


def _find_reachable_from(start_ids, outgoing):
    """BFS/DFS from start_ids, return all reachable node ids."""
    visited = set()
    stack = list(start_ids)
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in outgoing.get(node, []):
            if neighbor not in visited:
                stack.append(neighbor)
    return visited


def _detect_cycles(all_nodes, outgoing):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in all_nodes}
    cycles = []
    path = []

    def dfs(node):
        color[node] = GRAY
        path.append(node)
        for neighbor in outgoing.get(node, []):
            if color[neighbor] == GRAY:
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])
            elif color[neighbor] == WHITE:
                dfs(neighbor)
        path.pop()
        color[node] = BLACK

    for node in all_nodes:
        if color[node] == WHITE:
            dfs(node)

    return cycles


def _validate_connections(connections):
    errors = []
    for i, conn in enumerate(connections):
        if 'from_id' not in conn:
            errors.append(f"connections[{i}] missing 'from_id'")
        if 'to_id' not in conn:
            errors.append(f"connections[{i}] missing 'to_id'")
        if 'rationale' not in conn or not str(conn.get('rationale', '')).strip():
            errors.append(f"connections[{i}] missing 'rationale'")
    return errors


def _validate_items(items, label, required_fields):
    errors = []
    for i, item in enumerate(items):
        for field in required_fields:
            if field not in item or not str(item.get(field, '')).strip():
                errors.append(f"{label}[{i}] missing '{field}'")
    return errors


def _compute_ude_coverage(original_udes, desirable_effects, reachable_from_injections):
    """
    A UDE is resolved if:
    - A desirable effect with resolves_ude == ude.id exists, AND
    - That desirable effect is reachable from at least one injection
    """
    de_by_id = {de['id']: de for de in desirable_effects}

    # Build: ude_id -> list of DE ids that claim to resolve it
    ude_resolvers = {}
    for de in desirable_effects:
        ude_id = de.get('resolves_ude')
        if ude_id:
            ude_resolvers.setdefault(ude_id, []).append(de['id'])

    resolved = []
    unresolved = []
    partially_resolved = []  # DE exists but is not reachable

    for ude in original_udes:
        uid = ude['id']
        resolving_des = ude_resolvers.get(uid, [])

        if not resolving_des:
            unresolved.append({
                "id": uid,
                "description": ude.get('description', ''),
                "reason": "No desirable effect claims to resolve this UDE",
            })
            continue

        # Check if at least one resolving DE is reachable from injections
        reachable_des = [de_id for de_id in resolving_des if de_id in reachable_from_injections]

        if reachable_des:
            resolved.append({
                "id": uid,
                "description": ude.get('description', ''),
                "resolved_by": reachable_des,
            })
        else:
            partially_resolved.append({
                "id": uid,
                "description": ude.get('description', ''),
                "reason": (
                    f"Desirable effect(s) {resolving_des} claim to resolve this UDE "
                    "but are not reachable from any injection via the connection graph"
                ),
            })

    return resolved, unresolved, partially_resolved


def analyze(data):
    require_fields(data, ['injections', 'original_udes', 'desirable_effects', 'connections'])

    injections = data['injections']
    original_udes = data['original_udes']
    desirable_effects = data['desirable_effects']
    connections = data['connections']

    for field, val in [('injections', injections), ('original_udes', original_udes),
                       ('desirable_effects', desirable_effects), ('connections', connections)]:
        if not isinstance(val, list):
            print(f"Error: '{field}' must be a list", file=sys.stderr)
            sys.exit(1)

    # Structural validation
    errors = (
        _validate_items(injections, 'injections', ['id', 'description']) +
        _validate_items(original_udes, 'original_udes', ['id', 'description']) +
        _validate_items(desirable_effects, 'desirable_effects', ['id', 'description']) +
        _validate_connections(connections)
    )

    # Build graph
    all_nodes = _collect_all_nodes(injections, desirable_effects, connections)
    outgoing, incoming = _build_graph(connections)

    # Cycle detection
    cycles = _detect_cycles(all_nodes, outgoing)

    # Reachability from injections
    injection_ids = set(inj['id'] for inj in injections)
    reachable_from_injections = _find_reachable_from(injection_ids, outgoing)

    # Disconnected injections (no outgoing connections)
    disconnected_injections = [
        inj for inj in injections
        if inj['id'] not in outgoing
    ]

    # Orphaned desirable effects (not reachable from injections)
    de_ids = set(de['id'] for de in desirable_effects)
    unreachable_des = [
        de for de in desirable_effects
        if de['id'] not in reachable_from_injections
    ]

    # UDE coverage
    resolved, unresolved, partially_resolved = _compute_ude_coverage(
        original_udes, desirable_effects, reachable_from_injections
    )

    total_udes = len(original_udes)
    coverage_count = len(resolved)
    coverage_pct = round(coverage_count / total_udes * 100, 1) if total_udes > 0 else 0

    coverage_quality = (
        "complete" if coverage_pct == 100 else
        "high" if coverage_pct >= 75 else
        "medium" if coverage_pct >= 50 else
        "low"
    )

    # Warnings
    warnings = list(errors)
    if cycles:
        for cycle in cycles:
            warnings.append(f"Cycle detected: {' -> '.join(cycle)}")
    if disconnected_injections:
        for inj in disconnected_injections:
            warnings.append(
                f"Injection '{inj['id']}' has no outgoing connections — "
                "it does not lead to any desirable effect"
            )
    if unreachable_des:
        for de in unreachable_des:
            warnings.append(
                f"Desirable effect '{de['id']}' is not reachable from any injection — "
                "add connections or remove this DE"
            )
    if partially_resolved:
        for pr in partially_resolved:
            warnings.append(
                f"UDE '{pr['id']}' has a resolution claim but the chain is broken: {pr['reason']}"
            )
    if coverage_pct < 100 and total_udes > 0:
        warnings.append(
            f"UDE coverage is {coverage_pct}% — "
            f"{len(unresolved) + len(partially_resolved)} UDE(s) unresolved. "
            "Return to the Evaporating Cloud to design additional injections."
        )

    result = {
        "summary": {
            "total_injections": len(injections),
            "total_original_udes": total_udes,
            "total_desirable_effects": len(desirable_effects),
            "total_connections": len(connections),
            "ude_coverage_pct": coverage_pct,
            "ude_coverage_quality": coverage_quality,
            "resolved_udes": coverage_count,
            "unresolved_udes": len(unresolved) + len(partially_resolved),
            "cycles_detected": len(cycles) > 0,
            "valid": len(errors) == 0 and len(cycles) == 0,
        },
        "ude_coverage": {
            "resolved": resolved,
            "unresolved": unresolved,
            "partially_resolved": partially_resolved,
        },
        "disconnected_injections": [
            {"id": inj['id'], "description": inj.get('description', '')}
            for inj in disconnected_injections
        ],
        "unreachable_desirable_effects": [
            {"id": de['id'], "description": de.get('description', '')}
            for de in unreachable_des
        ],
        "cycles": [
            {"path": cycle, "length": len(cycle) - 1}
            for cycle in cycles
        ],
        "warnings": warnings,
    }

    # Human summary
    lines = [
        "=== Future Reality Tree Analysis ===",
        f"Injections: {len(injections)}  |  UDEs to resolve: {total_udes}  |  DEs: {len(desirable_effects)}  |  Connections: {len(connections)}",
        f"UDE coverage: {coverage_count}/{total_udes} ({coverage_pct}%) — {coverage_quality}",
        f"Cycles: {'DETECTED — tree is invalid' if cycles else 'none'}",
    ]
    if resolved:
        lines.append(f"\nResolved UDEs ({len(resolved)}):")
        for r in resolved:
            lines.append(f"  + {r['id']}: {r['description'][:70]}")
    if unresolved or partially_resolved:
        lines.append(f"\nUnresolved UDEs ({len(unresolved) + len(partially_resolved)}):")
        for u in unresolved:
            lines.append(f"  - {u['id']}: {u['description'][:70]}")
            lines.append(f"    Reason: {u['reason']}")
        for p in partially_resolved:
            lines.append(f"  ~ {p['id']}: {p['description'][:70]}")
            lines.append(f"    Reason: {p['reason'][:100]}")
    if disconnected_injections:
        lines.append(f"\nDisconnected injections (need cause-effect connections):")
        for inj in disconnected_injections:
            lines.append(f"  ! {inj['id']}: {inj.get('description', '')[:70]}")
    if warnings:
        lines.append(f"\nWarnings: {len(warnings)}")

    format_output(result, "\n".join(lines))


if __name__ == '__main__':
    if '--help' in sys.argv or '-h' in sys.argv:
        print(HELP)
        sys.exit(0)

    data = parse_input()
    if data is None:
        print(HELP)
        sys.exit(0)

    analyze(data)
