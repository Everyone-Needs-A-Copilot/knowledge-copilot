#!/usr/bin/env python3
"""
cloud_builder.py — Evaporating Cloud structure validator and assumption analyzer.

Validates the five-box EC structure, checks assumption coverage per arrow,
ranks assumptions by vulnerability, and identifies injection candidates.

Input (JSON):
  {
    "objective":  "...",
    "need_a":     "...",
    "need_b":     "...",
    "want_a":     "...",
    "want_b":     "...",
    "assumptions": [
      {
        "arrow":     "B-D",       // A-B | A-C | B-D | C-D' | D-D'
        "statement": "...",
        "type":      "policy"     // policy | belief | market | physics
      }
    ]
  }

Output (stdout): JSON cloud analysis
Summary (stderr): human-readable overview
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, rank_by


HELP = """
Usage:
  python3 cloud_builder.py '<json>'
  python3 cloud_builder.py --file cloud.json
  python3 cloud_builder.py --stdin < cloud.json

Required fields:
  objective     The shared goal both sides want to achieve (box A)
  need_a        First need — what must be true to achieve A (box B)
  need_b        Second need — what must also be true to achieve A (box C)
  want_a        What satisfies need_a — one side's position (box D)
  want_b        What satisfies need_b — conflicting position (box D')
  assumptions[] List of assumptions per arrow (arrow, statement, type)

Arrow labels: A-B, A-C, B-D, C-D', D-D'
Assumption types: policy, belief, market, physics

Output: validated cloud, completeness check, ranked assumptions, injection candidates.
"""

# Vulnerability score: higher = easier to invalidate
VULNERABILITY_SCORES = {
    "policy":  4,
    "belief":  3,
    "market":  2,
    "physics": 1,
}

VALID_ARROWS = {"A-B", "A-C", "B-D", "C-D'", "D-D'"}
VALID_TYPES = set(VULNERABILITY_SCORES.keys())

# Minimum assumptions expected per arrow for a thorough analysis
MIN_ASSUMPTIONS_PER_ARROW = 2


def _validate_five_boxes(data):
    """Check all five boxes are populated with non-trivial content."""
    boxes = {
        "objective": data.get("objective", ""),
        "need_a": data.get("need_a", ""),
        "need_b": data.get("need_b", ""),
        "want_a": data.get("want_a", ""),
        "want_b": data.get("want_b", ""),
    }
    errors = []
    for field, value in boxes.items():
        if not value or not str(value).strip():
            errors.append(f"Box '{field}' is missing or empty")
        elif len(str(value).strip()) < 8:
            errors.append(f"Box '{field}' is too brief — provide a complete statement")
    return errors, boxes


def _validate_assumptions(assumptions):
    """Validate individual assumption records."""
    errors = []
    warnings = []
    for i, assumption in enumerate(assumptions):
        if 'arrow' not in assumption:
            errors.append(f"assumptions[{i}] missing 'arrow'")
        elif assumption['arrow'] not in VALID_ARROWS:
            errors.append(
                f"assumptions[{i}] has invalid arrow '{assumption['arrow']}'; "
                f"must be one of: {', '.join(sorted(VALID_ARROWS))}"
            )
        if 'statement' not in assumption or not str(assumption.get('statement', '')).strip():
            errors.append(f"assumptions[{i}] missing 'statement'")
        if 'type' not in assumption:
            warnings.append(f"assumptions[{i}] missing 'type'; defaulting to 'belief'")
        elif assumption['type'] not in VALID_TYPES:
            errors.append(
                f"assumptions[{i}] invalid type '{assumption['type']}'; "
                f"must be one of: {', '.join(sorted(VALID_TYPES))}"
            )
    return errors, warnings


def _check_arrow_coverage(assumptions):
    """Check which arrows have sufficient assumption coverage."""
    coverage = {arrow: [] for arrow in VALID_ARROWS}
    for assumption in assumptions:
        arrow = assumption.get('arrow')
        if arrow in coverage:
            coverage[arrow].append(assumption)

    arrow_status = {}
    for arrow, arrow_assumptions in coverage.items():
        count = len(arrow_assumptions)
        arrow_status[arrow] = {
            "count": count,
            "sufficient": count >= MIN_ASSUMPTIONS_PER_ARROW,
            "assumptions": [a.get('statement', '') for a in arrow_assumptions],
        }

    missing_coverage = [
        arrow for arrow, status in arrow_status.items()
        if not status['sufficient']
    ]

    return arrow_status, missing_coverage


def _score_assumptions(assumptions):
    """Score each assumption by type vulnerability."""
    scored = []
    for assumption in assumptions:
        atype = assumption.get('type', 'belief')
        score = VULNERABILITY_SCORES.get(atype, VULNERABILITY_SCORES['belief'])
        scored.append({
            "arrow": assumption.get('arrow', ''),
            "statement": assumption.get('statement', ''),
            "type": atype,
            "vulnerability_score": score,
        })
    return rank_by(scored, 'vulnerability_score', reverse=True)


def _find_injection_candidates(scored_assumptions):
    """Top 3 most vulnerable assumptions are the best injection points."""
    return scored_assumptions[:3]


def _describe_arrow(arrow, boxes):
    """Return human-readable description of each arrow's logical meaning."""
    obj = boxes.get('objective', 'A')
    na = boxes.get('need_a', 'B')
    nb = boxes.get('need_b', 'C')
    wa = boxes.get('want_a', 'D')
    wb = boxes.get('want_b', "D'")

    descriptions = {
        "A-B": f"In order to [{obj}], we must satisfy [{na}]",
        "A-C": f"In order to [{obj}], we must satisfy [{nb}]",
        "B-D": f"In order to satisfy [{na}], we must have [{wa}]",
        "C-D'": f"In order to satisfy [{nb}], we must have [{wb}]",
        "D-D'": f"[{wa}] and [{wb}] cannot coexist simultaneously — this is the conflict",
    }
    return descriptions.get(arrow, arrow)


def analyze(data):
    require_fields(data, ['objective', 'need_a', 'need_b', 'want_a', 'want_b', 'assumptions'])

    assumptions = data.get('assumptions', [])
    if not isinstance(assumptions, list):
        print("Error: 'assumptions' must be a list", file=sys.stderr)
        sys.exit(1)

    # Validate five boxes
    box_errors, boxes = _validate_five_boxes(data)

    # Validate assumptions
    assumption_errors, assumption_warnings = _validate_assumptions(assumptions)

    all_errors = box_errors + assumption_errors
    valid = len(all_errors) == 0

    # Arrow coverage
    arrow_status, missing_coverage = _check_arrow_coverage(assumptions)

    # Score and rank assumptions
    scored_assumptions = _score_assumptions(assumptions)

    # Injection candidates
    injection_candidates = _find_injection_candidates(scored_assumptions)

    # Arrow descriptions
    arrow_descriptions = {
        arrow: _describe_arrow(arrow, boxes)
        for arrow in VALID_ARROWS
    }

    # Completeness check
    total_arrows = len(VALID_ARROWS)
    covered_arrows = total_arrows - len(missing_coverage)
    completeness_pct = round(covered_arrows / total_arrows * 100, 1)

    result = {
        "cloud": {
            "objective": data.get("objective"),
            "need_a": data.get("need_a"),
            "need_b": data.get("need_b"),
            "want_a": data.get("want_a"),
            "want_b": data.get("want_b"),
            "conflict": f"[{data.get('want_a')}] vs [{data.get('want_b')}]",
        },
        "validation": {
            "valid": valid,
            "errors": all_errors,
            "warnings": assumption_warnings,
        },
        "completeness": {
            "arrows_with_sufficient_coverage": covered_arrows,
            "total_arrows": total_arrows,
            "completeness_pct": completeness_pct,
            "arrows_needing_more_assumptions": missing_coverage,
            "note": (
                f"Each arrow should have at least {MIN_ASSUMPTIONS_PER_ARROW} assumptions. "
                f"Arrows with fewer: {', '.join(missing_coverage) if missing_coverage else 'none'}"
            ),
        },
        "arrow_coverage": {
            arrow: {
                "description": arrow_descriptions[arrow],
                "assumption_count": arrow_status[arrow]["count"],
                "sufficient": arrow_status[arrow]["sufficient"],
                "assumptions": arrow_status[arrow]["assumptions"],
            }
            for arrow in VALID_ARROWS
        },
        "assumptions_ranked": scored_assumptions,
        "injection_candidates": [
            {
                "rank": c["rank"],
                "arrow": c["arrow"],
                "assumption": c["statement"],
                "type": c["type"],
                "vulnerability_score": c["vulnerability_score"],
                "injection_prompt": (
                    f"What if this assumption were false? What new action would become possible "
                    f"that satisfies both [{data.get('need_a')}] and [{data.get('need_b')}] "
                    f"without requiring the conflict between [{data.get('want_a')}] and [{data.get('want_b')}]?"
                ),
            }
            for c in injection_candidates
        ],
    }

    # Human summary
    lines = [
        "=== Evaporating Cloud Analysis ===",
        f"Objective: {data.get('objective')}",
        f"Conflict:  [{data.get('want_a')}]  vs  [{data.get('want_b')}]",
        f"Structure valid: {'yes' if valid else 'NO — see errors'}",
        f"Assumption coverage: {covered_arrows}/{total_arrows} arrows have sufficient coverage ({completeness_pct}%)",
        f"Total assumptions: {len(assumptions)}",
    ]

    if all_errors:
        lines.append(f"\nErrors ({len(all_errors)}):")
        for e in all_errors:
            lines.append(f"  - {e}")

    if missing_coverage:
        lines.append(f"\nArrows needing more assumptions: {', '.join(missing_coverage)}")

    if injection_candidates:
        lines.append(f"\nTop injection candidates (most vulnerable assumptions):")
        for c in injection_candidates:
            lines.append(f"  [{c['rank']}] Arrow {c['arrow']} | {c['type']} | Score {c['vulnerability_score']}")
            lines.append(f"       \"{c['statement']}\"")

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
