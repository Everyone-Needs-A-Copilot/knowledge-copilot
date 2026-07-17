#!/usr/bin/env python3
"""
assumption_analyzer.py — In-depth assumption vulnerability analyzer for Evaporating Cloud.

Takes assumptions with supporting evidence and examination status.
Scores each assumption's vulnerability for invalidation.
Ranks for targeted injection design.

Input (JSON):
  {
    "assumptions": [
      {
        "statement":        "...",
        "type":             "policy",   // policy | belief | market | physics
        "evidence_for":     "...",      // evidence supporting the assumption
        "evidence_against": "...",      // evidence that challenges it
        "examined":         false       // has this assumption been explicitly questioned before?
      }
    ]
  }

Output (stdout): JSON with ranked assumptions, vulnerability scores, injection candidates
Summary (stderr): human-readable analysis
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, rank_by


HELP = """
Usage:
  python3 assumption_analyzer.py '<json>'
  python3 assumption_analyzer.py --file assumptions.json
  python3 assumption_analyzer.py --stdin < assumptions.json

Required fields:
  assumptions[]   List of assumption objects

Per assumption:
  statement         (required) The assumption as a falsifiable claim
  type              (required) policy | belief | market | physics
  evidence_for      (optional) Evidence supporting the assumption
  evidence_against  (optional) Evidence challenging the assumption
  examined          (optional) Has this been questioned before? (boolean, default false)

Output: ranked assumptions by vulnerability, scores, top injection candidates.
"""

# Base vulnerability by type (higher = more vulnerable)
TYPE_BASE_SCORE = {
    "policy":  40,
    "belief":  30,
    "market":  20,
    "physics": 10,
}

VALID_TYPES = set(TYPE_BASE_SCORE.keys())


def _score_assumption(assumption):
    """
    Score vulnerability on a 0-100 scale using multiple factors:

    Base score by type:
      policy  = 40 pts  (internally controlled, can be changed)
      belief  = 30 pts  (mental model, can be challenged)
      market  = 20 pts  (external but can shift)
      physics = 10 pts  (genuine constraint, hardest to change)

    Modifiers:
      +20  unexamined (examined=False) — unquestioned assumptions are especially vulnerable
      +20  has counter-evidence (evidence_against is non-empty)
      +10  no supporting evidence (evidence_for is empty)
      -10  strong supporting evidence (evidence_for is detailed, >50 chars)
       +5  very short statement (<30 chars) — vague assumption, harder to defend
    """
    atype = assumption.get('type', 'belief')
    score = TYPE_BASE_SCORE.get(atype, TYPE_BASE_SCORE['belief'])

    examined = assumption.get('examined', False)
    evidence_for = str(assumption.get('evidence_for', '') or '').strip()
    evidence_against = str(assumption.get('evidence_against', '') or '').strip()
    statement = str(assumption.get('statement', '') or '').strip()

    if not examined:
        score += 20

    if evidence_against:
        score += 20

    if not evidence_for:
        score += 10
    elif len(evidence_for) > 50:
        score -= 10

    if len(statement) < 30:
        score += 5

    # Cap at 100
    return min(score, 100)


def _classify_vulnerability(score):
    if score >= 75:
        return "high"
    elif score >= 50:
        return "medium"
    else:
        return "low"


def _validate_assumptions(assumptions):
    errors = []
    warnings = []
    for i, a in enumerate(assumptions):
        if 'statement' not in a or not str(a.get('statement', '')).strip():
            errors.append(f"assumptions[{i}] missing 'statement'")
        if 'type' not in a:
            warnings.append(f"assumptions[{i}] missing 'type'; defaulting to 'belief'")
        elif a['type'] not in VALID_TYPES:
            errors.append(
                f"assumptions[{i}] invalid type '{a['type']}'; "
                f"must be one of: {', '.join(sorted(VALID_TYPES))}"
            )
        if 'examined' in a and not isinstance(a['examined'], bool):
            warnings.append(f"assumptions[{i}] 'examined' should be a boolean")
    return errors, warnings


def _injection_guidance(assumption):
    """Generate targeted injection guidance based on assumption type."""
    atype = assumption.get('type', 'belief')
    statement = assumption.get('statement', '')

    guidance = {
        "policy": (
            f"This is a policy assumption. Ask: who created this policy, when, and why? "
            f"Is the original reason still valid? Can the policy be changed, suspended, or scoped differently? "
            f"Design an injection that achieves the need without relying on this policy."
        ),
        "belief": (
            f"This is a belief or mental model. Ask: what would have to be true in the world for this belief "
            f"to be false? What data would change this belief? "
            f"Design an injection that tests or contradicts this belief with a small experiment."
        ),
        "market": (
            f"This is a market assumption. Ask: is this market condition permanent, or has it changed recently? "
            f"Are there segments, channels, or customer types for whom this condition does not apply? "
            f"Design an injection that operates in a segment where this condition does not hold."
        ),
        "physics": (
            f"This is a physical or logical constraint. These are hardest to invalidate. "
            f"Ask: is this truly a physical law, or does it feel physical because of habit? "
            f"Are there analogous industries or situations where this 'physical' constraint was overcome? "
            f"Design an injection that uses technology, process redesign, or reframing to work around it."
        ),
    }
    return guidance.get(atype, guidance['belief'])


def analyze(data):
    require_fields(data, ['assumptions'])

    assumptions = data.get('assumptions', [])
    if not isinstance(assumptions, list):
        print("Error: 'assumptions' must be a list", file=sys.stderr)
        sys.exit(1)

    if len(assumptions) == 0:
        print("Error: 'assumptions' list is empty — provide at least one assumption", file=sys.stderr)
        sys.exit(1)

    errors, warnings = _validate_assumptions(assumptions)
    if errors:
        for e in errors:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Score each assumption
    scored = []
    for assumption in assumptions:
        score = _score_assumption(assumption)
        scored.append({
            "statement": assumption.get('statement', ''),
            "type": assumption.get('type', 'belief'),
            "examined": assumption.get('examined', False),
            "evidence_for": assumption.get('evidence_for', '') or '',
            "evidence_against": assumption.get('evidence_against', '') or '',
            "vulnerability_score": score,
            "vulnerability": _classify_vulnerability(score),
            "injection_guidance": _injection_guidance(assumption),
        })

    ranked = rank_by(scored, 'vulnerability_score', reverse=True)

    # Top injection candidates: highest vulnerability
    top_candidates = ranked[:3]

    # Counts by vulnerability
    high_count = sum(1 for r in ranked if r['vulnerability'] == 'high')
    medium_count = sum(1 for r in ranked if r['vulnerability'] == 'medium')
    low_count = sum(1 for r in ranked if r['vulnerability'] == 'low')

    # Unexamined count
    unexamined_count = sum(1 for r in ranked if not r['examined'])

    result = {
        "summary": {
            "total_assumptions": len(ranked),
            "high_vulnerability": high_count,
            "medium_vulnerability": medium_count,
            "low_vulnerability": low_count,
            "unexamined": unexamined_count,
            "recommendation": (
                "Start injection design with the highest-vulnerability assumptions. "
                "Unexamined assumptions are especially likely to yield breakthroughs."
            ),
        },
        "assumptions_ranked": ranked,
        "top_injection_candidates": [
            {
                "rank": c["rank"],
                "statement": c["statement"],
                "type": c["type"],
                "vulnerability_score": c["vulnerability_score"],
                "vulnerability": c["vulnerability"],
                "examined": c["examined"],
                "evidence_against": c["evidence_against"],
                "guidance": c["injection_guidance"],
            }
            for c in top_candidates
        ],
        "warnings": warnings,
    }

    # Human summary
    lines = [
        "=== Assumption Vulnerability Analysis ===",
        f"Total assumptions: {len(ranked)}",
        f"High vulnerability: {high_count}  |  Medium: {medium_count}  |  Low: {low_count}",
        f"Unexamined: {unexamined_count} (unexamined = +20 vulnerability points)",
        "",
        "Top injection candidates:",
    ]
    for c in top_candidates:
        examined_flag = "unexamined" if not c['examined'] else "examined"
        lines.append(
            f"  [{c['rank']}] Score {c['vulnerability_score']}/100 | {c['type']} | {examined_flag}"
        )
        lines.append(f"       \"{c['statement']}\"")
        if c['evidence_against']:
            lines.append(f"       Counter-evidence: {c['evidence_against'][:80]}...")

    if warnings:
        lines.append(f"\nWarnings:")
        for w in warnings:
            lines.append(f"  - {w}")

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
