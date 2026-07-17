#!/usr/bin/env python3
"""
negative_branch.py — Negative branch detector and risk scorer for FRT injections.

Takes a proposed injection and a list of potential effects (positive or negative).
Scores each by likelihood * severity, groups by stakeholder, and suggests
trimming injections to prevent high-risk negative branches.

Input (JSON):
  {
    "injection": "...",
    "stakeholders": ["..."],
    "potential_effects": [
      {
        "description": "...",
        "likelihood":  3,    // 1 (very unlikely) to 5 (almost certain)
        "severity":    4,    // 1 (minor) to 5 (critical)
        "stakeholder": "...",
        "is_negative": true  // optional; if omitted, severity >= 3 && likelihood >= 2 is flagged
      }
    ]
  }

Output (stdout): JSON with ranked negative branches, risk score, trimming suggestions
Summary (stderr): human-readable analysis
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, rank_by


HELP = """
Usage:
  python3 negative_branch.py '<json>'
  python3 negative_branch.py --file nb.json
  python3 negative_branch.py --stdin < nb.json

Required fields:
  injection             The proposed change being analyzed
  stakeholders[]        List of stakeholders to consider
  potential_effects[]   Effects with description, likelihood (1-5), severity (1-5), stakeholder

Optional per effect:
  is_negative           Explicitly mark as negative (default: auto-detected from scores)

Output: ranked negative branches, risk scores, stakeholder impact grouping, trimming guidance.
"""

# Risk score = likelihood * severity
# Max = 25 (5 * 5)
RISK_THRESHOLD_HIGH = 12    # >= 12: high risk, trimming required
RISK_THRESHOLD_MEDIUM = 6   # 6-11: medium risk, trimming recommended


def _validate_effects(effects):
    errors = []
    for i, effect in enumerate(effects):
        if 'description' not in effect or not str(effect.get('description', '')).strip():
            errors.append(f"potential_effects[{i}] missing 'description'")
        for field in ['likelihood', 'severity']:
            val = effect.get(field)
            if val is None:
                errors.append(f"potential_effects[{i}] missing '{field}'")
            elif not isinstance(val, (int, float)) or not (1 <= val <= 5):
                errors.append(f"potential_effects[{i}] '{field}' must be a number between 1 and 5, got {val!r}")
        if 'stakeholder' not in effect or not str(effect.get('stakeholder', '')).strip():
            errors.append(f"potential_effects[{i}] missing 'stakeholder'")
    return errors


def _is_negative(effect):
    """Determine if an effect is a negative branch."""
    if 'is_negative' in effect:
        return bool(effect['is_negative'])
    # Auto-detect: an effect is likely negative if it's at least somewhat likely and at least moderate severity
    likelihood = effect.get('likelihood', 1)
    severity = effect.get('severity', 1)
    return likelihood >= 2 and severity >= 3


def _risk_label(score):
    if score >= RISK_THRESHOLD_HIGH:
        return "high"
    elif score >= RISK_THRESHOLD_MEDIUM:
        return "medium"
    else:
        return "low"


def _trimming_guidance(effect, injection):
    """Generate targeted trimming injection guidance."""
    likelihood = effect.get('likelihood', 1)
    severity = effect.get('severity', 1)
    stakeholder = effect.get('stakeholder', 'affected party')
    description = effect.get('description', '')

    if likelihood >= 4 and severity >= 4:
        guidance = (
            f"This is a critical negative branch (L{likelihood} x S{severity} = {likelihood*severity}). "
            f"A trimming injection is mandatory before proceeding. "
            f"Design a specific action that prevents [{description}] for [{stakeholder}] "
            f"while keeping the injection [{injection}] in place. "
            f"Consider: (a) phasing the injection so this effect is detected early, "
            f"(b) a compensating action that addresses {stakeholder}'s concern directly, "
            f"(c) redefining the injection's scope to exclude the condition that creates this branch."
        )
    elif likelihood >= 3 or severity >= 3:
        guidance = (
            f"This negative branch should be trimmed before full rollout. "
            f"For [{stakeholder}]: design an action that prevents or mitigates [{description}]. "
            f"Consider: monitoring, communication, or a parallel process that preserves "
            f"the benefit of [{injection}] while protecting {stakeholder}."
        )
    else:
        guidance = (
            f"Low-risk negative branch — monitor and have a contingency plan ready. "
            f"If [{description}] begins to materialize, intervene early with a targeted response "
            f"for [{stakeholder}] before it escalates."
        )
    return guidance


def analyze(data):
    require_fields(data, ['injection', 'stakeholders', 'potential_effects'])

    injection = data['injection']
    stakeholders = data.get('stakeholders', [])
    potential_effects = data.get('potential_effects', [])

    if not isinstance(stakeholders, list):
        print("Error: 'stakeholders' must be a list", file=sys.stderr)
        sys.exit(1)
    if not isinstance(potential_effects, list):
        print("Error: 'potential_effects' must be a list", file=sys.stderr)
        sys.exit(1)
    if not str(injection).strip():
        print("Error: 'injection' must be a non-empty string", file=sys.stderr)
        sys.exit(1)

    errors = _validate_effects(potential_effects)
    if errors:
        for e in errors:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Score all effects
    all_scored = []
    for effect in potential_effects:
        likelihood = effect['likelihood']
        severity = effect['severity']
        risk_score = likelihood * severity
        negative = _is_negative(effect)

        all_scored.append({
            "description": effect['description'],
            "stakeholder": effect['stakeholder'],
            "likelihood": likelihood,
            "severity": severity,
            "risk_score": risk_score,
            "risk_level": _risk_label(risk_score),
            "is_negative": negative,
            "trimming_required": negative and risk_score >= RISK_THRESHOLD_HIGH,
            "trimming_recommended": negative and RISK_THRESHOLD_MEDIUM <= risk_score < RISK_THRESHOLD_HIGH,
        })

    # Separate negative branches
    negative_branches = [e for e in all_scored if e['is_negative']]
    positive_effects = [e for e in all_scored if not e['is_negative']]

    # Rank negative branches by risk score (highest first)
    ranked_branches = rank_by(negative_branches, 'risk_score', reverse=True)

    # Add trimming guidance to ranked branches
    for branch in ranked_branches:
        branch['trimming_guidance'] = _trimming_guidance(branch, injection)

    # Group by stakeholder
    stakeholder_impact = {}
    for branch in ranked_branches:
        sh = branch['stakeholder']
        stakeholder_impact.setdefault(sh, []).append({
            "description": branch['description'],
            "risk_score": branch['risk_score'],
            "risk_level": branch['risk_level'],
        })

    # Sort stakeholders by max risk score
    stakeholder_summary = sorted(
        [
            {
                "stakeholder": sh,
                "branch_count": len(branches),
                "max_risk_score": max(b['risk_score'] for b in branches),
                "branches": branches,
            }
            for sh, branches in stakeholder_impact.items()
        ],
        key=lambda x: x['max_risk_score'],
        reverse=True
    )

    # Overall risk score: highest single negative branch score
    overall_risk_score = max((b['risk_score'] for b in ranked_branches), default=0)
    overall_risk_level = _risk_label(overall_risk_score)

    high_risk_count = sum(1 for b in ranked_branches if b['risk_level'] == 'high')
    medium_risk_count = sum(1 for b in ranked_branches if b['risk_level'] == 'medium')
    low_risk_count = sum(1 for b in ranked_branches if b['risk_level'] == 'low')
    trimming_required_count = sum(1 for b in ranked_branches if b['trimming_required'])

    result = {
        "injection": injection,
        "summary": {
            "total_effects_analyzed": len(all_scored),
            "negative_branches": len(ranked_branches),
            "positive_effects": len(positive_effects),
            "overall_risk_score": overall_risk_score,
            "overall_risk_level": overall_risk_level,
            "high_risk_branches": high_risk_count,
            "medium_risk_branches": medium_risk_count,
            "low_risk_branches": low_risk_count,
            "trimming_required": trimming_required_count,
            "safe_to_proceed": trimming_required_count == 0,
        },
        "negative_branches_ranked": ranked_branches,
        "stakeholder_impact": stakeholder_summary,
        "positive_effects": positive_effects,
    }

    # Human summary
    lines = [
        "=== Negative Branch Analysis ===",
        f"Injection: {injection}",
        f"Effects analyzed: {len(all_scored)}  |  Negative branches: {len(ranked_branches)}",
        f"Overall risk level: {overall_risk_level} (max score: {overall_risk_score}/25)",
        f"Trimming required: {trimming_required_count}  |  Recommended: {medium_risk_count}",
        f"Safe to proceed without trimming: {'YES' if trimming_required_count == 0 else 'NO'}",
    ]

    if ranked_branches:
        lines.append(f"\nNegative branches (ranked by risk):")
        for b in ranked_branches:
            flag = " [TRIM REQUIRED]" if b['trimming_required'] else (" [trim recommended]" if b['trimming_recommended'] else "")
            lines.append(f"  [{b['rank']}] Risk {b['risk_score']}/25 ({b['risk_level']}){flag}")
            lines.append(f"       Stakeholder: {b['stakeholder']}")
            lines.append(f"       Effect: {b['description'][:80]}")
            lines.append(f"       L={b['likelihood']} x S={b['severity']}")

    if stakeholder_summary:
        lines.append(f"\nStakeholders most affected:")
        for sh in stakeholder_summary[:3]:
            lines.append(f"  {sh['stakeholder']}: {sh['branch_count']} branch(es), max risk {sh['max_risk_score']}/25")

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
