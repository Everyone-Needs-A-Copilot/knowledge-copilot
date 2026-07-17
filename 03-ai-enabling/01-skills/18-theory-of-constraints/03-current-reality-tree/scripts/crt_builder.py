#!/usr/bin/env python3
"""
crt_builder.py — Current Reality Tree structure validator and analyzer.

Takes a set of UDEs and cause-effect connections, validates tree integrity,
detects cycles, identifies root causes, and computes convergence ratio.

Input (JSON):
  {
    "udes": [
      { "id": "U1", "description": "..." }
    ],
    "connections": [
      {
        "from_id": "N1",
        "to_id": "U1",
        "type": "causes",       // "causes" | "and_causes"
        "rationale": "..."
      }
    ]
  }

Output (stdout): JSON analysis result
Summary (stderr): human-readable overview
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields


HELP = """
Usage:
  python3 crt_builder.py '<json>'
  python3 crt_builder.py --file input.json
  python3 crt_builder.py --stdin < input.json

Required fields:
  udes[]          List of UDE objects with 'id' and 'description'
  connections[]   List of connections with 'from_id', 'to_id', 'type', 'rationale'

Connection types:
  causes          Standard single-cause arrow
  and_causes      Arrow participates in an AND-connector group

Output: validated tree with root causes, convergence ratio, warnings.
"""


def _build_graph(connections):
    """Build adjacency structures from connections list."""
    # outgoing: from_id -> [to_id, ...]
    # incoming: to_id -> [from_id, ...]
    outgoing = {}
    incoming = {}
    for conn in connections:
        fid = conn['from_id']
        tid = conn['to_id']
        outgoing.setdefault(fid, []).append(tid)
        incoming.setdefault(tid, []).append(fid)
    return outgoing, incoming


def _collect_all_nodes(udes, connections):
    """Collect every node id mentioned anywhere in the tree."""
    nodes = set(u['id'] for u in udes)
    for conn in connections:
        nodes.add(conn['from_id'])
        nodes.add(conn['to_id'])
    return nodes


def _detect_cycles(all_nodes, outgoing):
    """DFS-based cycle detection. Returns list of cycles found (each a list of node ids)."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in all_nodes}
    cycles = []
    path = []

    def dfs(node):
        color[node] = GRAY
        path.append(node)
        for neighbor in outgoing.get(node, []):
            if color[neighbor] == GRAY:
                # Found cycle — extract the cycle portion of path
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


def _find_root_causes(all_nodes, incoming):
    """Nodes with no incoming connections are root causes."""
    return [n for n in all_nodes if n not in incoming]


def _find_ude_ids(udes):
    return set(u['id'] for u in udes)


def _check_ude_coverage(ude_ids, incoming, outgoing):
    """Check which UDEs are reachable from at least one root (have an incoming path or are roots themselves)."""
    # A UDE is 'explained' if it has at least one incoming connection
    explained = [uid for uid in ude_ids if uid in incoming]
    unexplained = [uid for uid in ude_ids if uid not in incoming]
    return explained, unexplained


def _find_and_connectors(connections):
    """Find all AND-connector groups: connections with type == 'and_causes' sharing the same to_id."""
    and_groups = {}
    for conn in connections:
        if conn.get('type') == 'and_causes':
            and_groups.setdefault(conn['to_id'], []).append(conn['from_id'])
    return and_groups


def _validate_connections(connections):
    """Check each connection has required fields."""
    errors = []
    required = ['from_id', 'to_id', 'type', 'rationale']
    valid_types = {'causes', 'and_causes'}
    for i, conn in enumerate(connections):
        missing = [f for f in required if f not in conn]
        if missing:
            errors.append(f"Connection[{i}] missing fields: {', '.join(missing)}")
        if 'type' in conn and conn['type'] not in valid_types:
            errors.append(f"Connection[{i}] invalid type '{conn['type']}'; must be 'causes' or 'and_causes'")
    return errors


def _validate_udes(udes):
    """Check each UDE has required fields."""
    errors = []
    for i, ude in enumerate(udes):
        if 'id' not in ude:
            errors.append(f"UDE[{i}] missing 'id'")
        if 'description' not in ude:
            errors.append(f"UDE[{i}] missing 'description'")
    return errors


def analyze(data):
    require_fields(data, ['udes', 'connections'])

    udes = data['udes']
    connections = data['connections']

    if not isinstance(udes, list):
        print("Error: 'udes' must be a list", file=sys.stderr)
        sys.exit(1)
    if not isinstance(connections, list):
        print("Error: 'connections' must be a list", file=sys.stderr)
        sys.exit(1)

    # Field validation
    ude_errors = _validate_udes(udes)
    conn_errors = _validate_connections(connections)
    validation_errors = ude_errors + conn_errors

    all_nodes = _collect_all_nodes(udes, connections)
    ude_ids = _find_ude_ids(udes)
    outgoing, incoming = _build_graph(connections)

    # Cycle detection
    cycles = _detect_cycles(all_nodes, outgoing)

    # Root causes
    root_causes = _find_root_causes(all_nodes, incoming)

    # UDE coverage
    explained_udes, unexplained_udes = _check_ude_coverage(ude_ids, incoming, outgoing)

    # AND-connectors
    and_groups = _find_and_connectors(connections)

    # Convergence ratio
    num_udes = len(udes)
    num_roots = len(root_causes)
    convergence_ratio = round(num_udes / num_roots, 2) if num_roots > 0 else None

    # Non-UDE root causes (intermediate nodes that happen to have no inputs)
    ude_root_causes = [r for r in root_causes if r in ude_ids]
    true_root_causes = [r for r in root_causes if r not in ude_ids]

    # Warnings
    warnings = list(validation_errors)
    if cycles:
        for cycle in cycles:
            warnings.append(f"Circular reference detected: {' -> '.join(cycle)}")
    if unexplained_udes:
        for uid in unexplained_udes:
            warnings.append(f"UDE '{uid}' has no incoming connections — it is unexplained or is itself a root cause")
    if ude_root_causes:
        warnings.append(
            f"UDEs appear as root causes (no causes identified): {', '.join(ude_root_causes)}. "
            "This may indicate incomplete analysis — ask 'what causes this UDE?'"
        )
    if convergence_ratio is not None and convergence_ratio < 2.0 and num_udes >= 3:
        warnings.append(
            f"Convergence ratio is {convergence_ratio} (low). "
            "Consider surfacing deeper root causes to improve explanatory power."
        )
    if num_udes < 5:
        warnings.append(
            f"Only {num_udes} UDE(s) listed. A robust CRT typically has 5–10 UDEs. "
            "Consider gathering more symptoms."
        )

    result = {
        "summary": {
            "total_nodes": len(all_nodes),
            "total_udes": num_udes,
            "total_connections": len(connections),
            "root_causes": true_root_causes,
            "root_cause_count": len(true_root_causes),
            "convergence_ratio": convergence_ratio,
            "convergence_quality": (
                "high" if convergence_ratio and convergence_ratio >= 3.0 else
                "medium" if convergence_ratio and convergence_ratio >= 2.0 else
                "low"
            ),
            "cycles_detected": len(cycles) > 0,
            "valid": len(validation_errors) == 0 and len(cycles) == 0,
        },
        "root_causes": [
            {
                "id": rc,
                "effects_caused": outgoing.get(rc, []),
                "effect_count": len(outgoing.get(rc, [])),
            }
            for rc in true_root_causes
        ],
        "ude_coverage": {
            "explained": explained_udes,
            "unexplained": unexplained_udes,
            "coverage_pct": round(len(explained_udes) / num_udes * 100, 1) if num_udes > 0 else 0,
        },
        "and_connectors": [
            {
                "effect_id": effect_id,
                "required_causes": causes,
                "note": "All listed causes must be present simultaneously to produce this effect",
            }
            for effect_id, causes in and_groups.items()
        ],
        "cycles": [
            {"path": cycle, "length": len(cycle) - 1}
            for cycle in cycles
        ],
        "connections_validated": len(connections),
        "warnings": warnings,
    }

    # Human summary
    lines = [
        "=== Current Reality Tree Analysis ===",
        f"Nodes: {len(all_nodes)}  |  UDEs: {num_udes}  |  Connections: {len(connections)}",
        f"Root causes: {len(true_root_causes)}  —  {', '.join(true_root_causes) if true_root_causes else 'none identified'}",
        f"Convergence ratio: {convergence_ratio} ({result['summary']['convergence_quality']})",
        f"Cycles: {'DETECTED — tree is invalid' if cycles else 'none'}",
        f"UDE coverage: {len(explained_udes)}/{num_udes} explained ({result['ude_coverage']['coverage_pct']}%)",
    ]
    if and_groups:
        lines.append(f"AND-connectors: {len(and_groups)} group(s) found")
    if warnings:
        lines.append(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            lines.append(f"  - {w}")
    else:
        lines.append("\nTree structure is valid.")

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
