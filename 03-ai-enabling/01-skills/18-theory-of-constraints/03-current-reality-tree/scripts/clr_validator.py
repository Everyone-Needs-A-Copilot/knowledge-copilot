#!/usr/bin/env python3
"""
clr_validator.py — Cause-Legitimacy Rules (CLR) structural validator for CRT connections.

Runs three structural checks on each connection in a CRT:
  1. Completeness — rationale is provided and non-empty
  2. Clarity     — cause and effect IDs are distinct and both stated
  3. Tautology   — cause description does not echo the effect description

Input (JSON): same tree format as crt_builder.py, with optional 'nodes' map for descriptions.
  {
    "udes": [ { "id": "U1", "description": "..." } ],
    "connections": [
      { "from_id": "N1", "to_id": "U1", "type": "causes", "rationale": "..." }
    ],
    "nodes": {
      "N1": "Description of node N1"
    }
  }

The 'nodes' map is optional but enables the tautology check.

Output (stdout): JSON with per-connection results and overall quality score
Summary (stderr): human-readable pass/fail overview
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields


HELP = """
Usage:
  python3 clr_validator.py '<json>'
  python3 clr_validator.py --file input.json
  python3 clr_validator.py --stdin < input.json

Required fields:
  udes[]          List of UDE objects (id, description)
  connections[]   List of connections (from_id, to_id, type, rationale)

Optional:
  nodes{}         Map of node_id -> description for tautology check

Output: per-connection CLR check results and structural quality score (0-100).
"""


def _build_description_map(udes, nodes_map):
    """Build a unified id->description lookup from UDEs and optional nodes map."""
    desc = {}
    for ude in udes:
        desc[ude['id']] = ude.get('description', '')
    if nodes_map and isinstance(nodes_map, dict):
        desc.update(nodes_map)
    return desc


def _check_completeness(conn):
    """Pass if rationale is present and non-empty."""
    rationale = conn.get('rationale', '')
    if not rationale or not str(rationale).strip():
        return False, "No rationale provided — the mechanism linking cause to effect is unstated"
    if len(str(rationale).strip()) < 10:
        return False, f"Rationale is too brief ('{rationale}') — explain the causal mechanism"
    return True, None


def _check_clarity(conn):
    """Pass if from_id and to_id are both present and non-empty."""
    from_id = conn.get('from_id', '')
    to_id = conn.get('to_id', '')
    if not from_id or not str(from_id).strip():
        return False, "Cause node (from_id) is missing or empty"
    if not to_id or not str(to_id).strip():
        return False, "Effect node (to_id) is missing or empty"
    return True, None


def _check_tautology(conn, desc_map):
    """Pass if cause and effect descriptions are meaningfully different."""
    from_id = conn.get('from_id', '')
    to_id = conn.get('to_id', '')

    from_desc = desc_map.get(from_id, '').lower().strip()
    to_desc = desc_map.get(to_id, '').lower().strip()

    if not from_desc or not to_desc:
        # Cannot check without descriptions — skip, treat as warning not failure
        return None, "Cannot check tautology — node descriptions not provided in 'nodes' map"

    # Exact match
    if from_desc == to_desc:
        return False, f"Cause and effect have identical descriptions — this is a tautology"

    # High word overlap (>70% of shorter description's words appear in longer)
    from_words = set(from_desc.split())
    to_words = set(to_desc.split())
    if len(from_words) == 0 or len(to_words) == 0:
        return True, None
    shorter = from_words if len(from_words) <= len(to_words) else to_words
    longer = to_words if len(from_words) <= len(to_words) else from_words
    overlap = len(shorter & longer) / len(shorter)
    if overlap > 0.80:
        return False, (
            f"Cause and effect descriptions have {round(overlap*100)}% word overlap — "
            "likely a tautology or restatement"
        )

    return True, None


def validate(data):
    require_fields(data, ['udes', 'connections'])

    udes = data['udes']
    connections = data['connections']
    nodes_map = data.get('nodes', {})

    if not isinstance(udes, list):
        print("Error: 'udes' must be a list", file=sys.stderr)
        sys.exit(1)
    if not isinstance(connections, list):
        print("Error: 'connections' must be a list", file=sys.stderr)
        sys.exit(1)

    desc_map = _build_description_map(udes, nodes_map)

    results = []
    total_checks = 0
    passed_checks = 0
    tautology_skipped = 0

    for i, conn in enumerate(connections):
        conn_id = f"{conn.get('from_id', '?')} -> {conn.get('to_id', '?')}"

        completeness_pass, completeness_msg = _check_completeness(conn)
        clarity_pass, clarity_msg = _check_clarity(conn)
        tautology_result, tautology_msg = _check_tautology(conn, desc_map)

        # tautology_result can be None (skipped), True (pass), False (fail)
        tautology_pass = tautology_result
        tautology_skipped_flag = tautology_result is None

        checks = {
            "completeness": {
                "pass": completeness_pass,
                "message": completeness_msg if not completeness_pass else "Rationale is present",
            },
            "clarity": {
                "pass": clarity_pass,
                "message": clarity_msg if not clarity_pass else "Cause and effect nodes are identified",
            },
            "tautology": {
                "pass": tautology_pass,
                "skipped": tautology_skipped_flag,
                "message": tautology_msg if tautology_msg else "Cause and effect are distinct",
            },
        }

        # Score this connection
        conn_total = 2  # completeness + clarity always count
        conn_passed = (1 if completeness_pass else 0) + (1 if clarity_pass else 0)

        if not tautology_skipped_flag:
            conn_total += 1
            conn_passed += (1 if tautology_pass else 0)
        else:
            tautology_skipped += 1

        total_checks += conn_total
        passed_checks += conn_passed

        conn_score = round(conn_passed / conn_total * 100, 1) if conn_total > 0 else 0
        conn_valid = completeness_pass and clarity_pass and (tautology_skipped_flag or tautology_pass)

        results.append({
            "connection": conn_id,
            "from_id": conn.get('from_id'),
            "to_id": conn.get('to_id'),
            "type": conn.get('type', 'causes'),
            "valid": conn_valid,
            "score": conn_score,
            "checks": checks,
        })

    overall_score = round(passed_checks / total_checks * 100, 1) if total_checks > 0 else 0
    passed_connections = sum(1 for r in results if r['valid'])
    failed_connections = [r for r in results if not r['valid']]

    quality_label = (
        "high" if overall_score >= 85 else
        "medium" if overall_score >= 60 else
        "low"
    )

    result = {
        "summary": {
            "total_connections": len(connections),
            "passed": passed_connections,
            "failed": len(connections) - passed_connections,
            "overall_score": overall_score,
            "quality": quality_label,
            "tautology_checks_skipped": tautology_skipped,
            "note": (
                "Add 'nodes' map with node descriptions to enable tautology checks"
                if tautology_skipped > 0 else None
            ),
        },
        "connections": results,
        "failures": [
            {
                "connection": r['connection'],
                "failed_checks": [
                    {"check": k, "message": v['message']}
                    for k, v in r['checks'].items()
                    if v.get('pass') is False
                ],
            }
            for r in results if not r['valid']
        ],
    }

    # Human summary
    lines = [
        "=== CLR Structural Validation ===",
        f"Connections checked: {len(connections)}",
        f"Passed: {passed_connections}  |  Failed: {len(connections) - passed_connections}",
        f"Overall structural quality score: {overall_score}/100 ({quality_label})",
    ]
    if tautology_skipped > 0:
        lines.append(f"Note: tautology check skipped for {tautology_skipped} connection(s) — add 'nodes' descriptions to enable")
    if failed_connections:
        lines.append(f"\nFailed connections:")
        for f in failed_connections:
            lines.append(f"  {f['connection']} (score: {f['score']}%)")
            for check_name, check_data in f['checks'].items():
                if check_data.get('pass') is False:
                    lines.append(f"    FAIL [{check_name}]: {check_data['message']}")
    else:
        lines.append("\nAll connections pass structural CLR checks.")

    format_output(result, "\n".join(lines))


if __name__ == '__main__':
    if '--help' in sys.argv or '-h' in sys.argv:
        print(HELP)
        sys.exit(0)

    data = parse_input()
    if data is None:
        print(HELP)
        sys.exit(0)

    validate(data)
