"""
Technology Assessment (Necessary But Not Sufficient)

Evaluates a single technology investment using Goldratt's four-question
framework. Scores the quality of the investment thesis and identifies
where unrealized value is hiding due to unchanged rules.

Usage:
    python3 scripts/tech_assessment.py --file input.json
    python3 scripts/tech_assessment.py '{"technology": "CRM", ...}'

Input JSON:
{
  "technology": "Salesforce CRM",
  "power": "Real-time pipeline visibility and deal activity tracking",
  "limitation_diminished": "Manual weekly roll-up of deal status from sales reps",
  "investment_cost": 120000,
  "old_rules": [
    {
      "rule": "Weekly pipeline review meetings with all sales managers",
      "still_active": true,
      "replacement_rule": null
    },
    {
      "rule": "Reps update forecast on Friday only",
      "still_active": true,
      "replacement_rule": null
    },
    {
      "rule": "Manager intervention only after deal goes quiet for 2 weeks",
      "still_active": false,
      "replacement_rule": "CRM flags deals with no activity for 5 days automatically"
    }
  ]
}

Output: power clarity score, limitation match flag, rule-change completeness,
old rules audit, unrealized value assessment, recommendations.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, currency, pct

# Scoring weights
POWER_CLARITY_SPECIFICITY_WORDS = [
    "real-time", "automated", "instant", "zero", "eliminate",
    "always", "any", "across all", "without", "regardless",
]

def score_power_clarity(power_statement):
    """
    Score 0-100: is the power statement specific enough to be actionable?

    Heuristics:
    - Length: very short statements are vague (< 20 chars = 0, > 80 chars = 50)
    - Specificity words: more specific words = higher score
    - Avoids vague phrases: "better", "faster", "improved" alone = low score
    """
    if not power_statement or len(power_statement.strip()) < 10:
        return 0, "Power statement is missing or too brief"

    score = 0
    notes = []

    # Length heuristic
    length = len(power_statement.strip())
    if length >= 80:
        score += 40
        notes.append("Sufficient length")
    elif length >= 40:
        score += 25
        notes.append("Moderate length — may be missing specifics")
    else:
        score += 10
        notes.append("Too brief — power statement needs more specificity")

    # Specificity word heuristic
    lower = power_statement.lower()
    matched = [w for w in POWER_CLARITY_SPECIFICITY_WORDS if w in lower]
    specificity_score = min(40, len(matched) * 15)
    score += specificity_score
    if matched:
        notes.append(f"Specificity indicators found: {matched}")

    # Vague phrase penalty
    vague_phrases = ["better", "faster", "improved", "more efficient", "easier"]
    vague_found = [p for p in vague_phrases if p in lower and len(lower.split()) < 8]
    if vague_found and not matched:
        score = max(0, score - 20)
        notes.append(f"Vague phrases without specific capability: {vague_found}")

    # Cap
    score = min(100, max(0, score))
    return score, "; ".join(notes)


def score_rule_change_completeness(old_rules):
    """
    Score 0-100: what % of old rules have a defined replacement?

    A rule is "changed" if still_active=False AND replacement_rule is defined.
    A rule is "partially changed" if still_active=False but no replacement.
    A rule is "unchanged" if still_active=True.
    """
    if not old_rules:
        return 0, [], [], []

    fully_changed = []
    partially_changed = []
    unchanged = []

    for r in old_rules:
        rule_text = r.get("rule", "")
        still_active = r.get("still_active", True)
        replacement = r.get("replacement_rule")

        if not still_active and replacement:
            fully_changed.append(rule_text)
        elif not still_active and not replacement:
            partially_changed.append(rule_text)
        else:
            unchanged.append(rule_text)

    total = len(old_rules)
    # Fully changed = 100% credit; partially changed = 50% credit
    score = ((len(fully_changed) * 1.0 + len(partially_changed) * 0.5) / total) * 100
    return round(score, 1), fully_changed, partially_changed, unchanged


def assess_unrealized_value(old_rules, investment_cost):
    """
    Estimate unrealized value based on unchanged rules.
    Simple heuristic: each unchanged rule represents a portion of unrealized investment value.
    """
    total_rules = len(old_rules)
    if total_rules == 0:
        return {
            "unchanged_rule_count": 0,
            "unrealized_value_estimate": 0,
            "unrealized_value_formatted": currency(0),
            "note": "No old rules provided — cannot assess unrealized value",
        }

    unchanged = [r for r in old_rules if r.get("still_active", True)]
    unchanged_count = len(unchanged)
    unchanged_ratio = unchanged_count / total_rules

    # Unrealized value = proportion of investment cost attributed to unchanged rules
    # This is a rough heuristic — actual value realization depends on the constraint impact
    unrealized = investment_cost * unchanged_ratio

    return {
        "unchanged_rule_count": unchanged_count,
        "total_rule_count": total_rules,
        "unchanged_ratio": round(unchanged_ratio, 3),
        "unrealized_value_estimate": round(unrealized, 2),
        "unrealized_value_formatted": currency(unrealized),
        "note": (
            f"{unchanged_count} of {total_rules} old rules are still active. "
            f"Approximately {pct(unchanged_ratio)} of the technology's potential value "
            "may be unrealized because the rules it made obsolete haven't been replaced."
        ),
    }


def classify_overall(power_score, rule_score):
    """Classify overall investment quality."""
    avg = (power_score + rule_score) / 2
    if avg >= 75:
        return "Strong investment — technology and rule changes are aligned"
    elif avg >= 50:
        return "Moderate — value is being realized but significant gaps remain"
    elif avg >= 25:
        return "Underperforming — either unclear power or rule changes not happening"
    else:
        return "At risk — technology value is largely unrealized"


def build_recommendations(power_score, rule_score, unchanged_rules, partially_changed_rules):
    recs = []

    if power_score < 50:
        recs.append(
            "The power statement is too vague to drive rule change decisions. "
            "Rewrite it to name the specific new capability and what it makes possible for the first time."
        )

    if unchanged_rules:
        for rule in unchanged_rules[:3]:  # Top 3 unchanged
            recs.append(
                f"Old rule still active: '{rule}'. "
                "Ask: 'Why did we have this rule before this technology existed?' "
                "Then ask: 'What should replace it now that the old limitation is gone?'"
            )
        if len(unchanged_rules) > 3:
            recs.append(
                f"{len(unchanged_rules) - 3} more unchanged rules not shown. "
                "Address all unchanged rules to fully realize technology value."
            )

    if partially_changed_rules:
        recs.append(
            f"{len(partially_changed_rules)} rule(s) have been deactivated but have no replacement defined. "
            "A rule without a replacement creates a vacuum — people will revert to the old rule. "
            "Define explicit replacement rules for: "
            + "; ".join(f"'{r}'" for r in partially_changed_rules[:2])
        )

    if rule_score >= 80 and power_score >= 80:
        recs.append(
            "Investment looks well-structured. Validate that new rules are actually being followed "
            "in practice, not just documented on paper."
        )

    return recs


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    require_fields(data, ["technology", "power", "limitation_diminished", "old_rules", "investment_cost"])

    technology = data["technology"]
    power = data["power"]
    limitation = data["limitation_diminished"]
    old_rules = data["old_rules"]
    investment_cost = float(data["investment_cost"])

    if not isinstance(old_rules, list):
        print("Error: old_rules must be a list", file=sys.stderr)
        sys.exit(1)

    power_score, power_note = score_power_clarity(power)
    rule_score, fully_changed, partially_changed, unchanged = score_rule_change_completeness(old_rules)
    unrealized = assess_unrealized_value(old_rules, investment_cost)
    overall_label = classify_overall(power_score, rule_score)
    recommendations = build_recommendations(power_score, rule_score, unchanged, partially_changed)

    # Build old rules audit
    old_rules_audit = []
    for r in old_rules:
        still_active = r.get("still_active", True)
        replacement = r.get("replacement_rule")
        if not still_active and replacement:
            status = "changed"
        elif not still_active and not replacement:
            status = "deactivated_no_replacement"
        else:
            status = "still_active"

        old_rules_audit.append({
            "rule": r.get("rule", ""),
            "still_active": still_active,
            "replacement_rule": replacement,
            "status": status,
            "status_label": {
                "changed": "Changed — old rule replaced with new rule",
                "deactivated_no_replacement": "Deactivated but no replacement defined — value at risk",
                "still_active": "Still active — this rule is blocking value realization",
            }[status],
        })

    result = {
        "technology": technology,
        "investment_cost": investment_cost,
        "investment_cost_formatted": currency(investment_cost),
        "four_questions": {
            "q1_power": power,
            "q2_limitation_diminished": limitation,
            "q3_old_rules": [r.get("rule", "") for r in old_rules],
            "q4_new_rules": [
                r.get("replacement_rule", "") for r in old_rules
                if r.get("replacement_rule")
            ],
        },
        "scores": {
            "power_clarity": power_score,
            "power_clarity_note": power_note,
            "rule_change_completeness": rule_score,
            "rule_change_summary": {
                "total_rules": len(old_rules),
                "fully_changed": len(fully_changed),
                "partially_changed": len(partially_changed),
                "still_active": len(unchanged),
            },
            "overall_label": overall_label,
        },
        "unrealized_value": unrealized,
        "old_rules_audit": old_rules_audit,
        "recommendations": recommendations,
    }

    summary_lines = [
        f"=== Technology Assessment: {technology} ===",
        f"Investment: {currency(investment_cost)}",
        "",
        f"Power: {power}",
        f"Limitation diminished: {limitation}",
        "",
        f"Power clarity score:      {power_score}/100",
        f"Rule-change completeness: {rule_score}/100",
        f"Overall:                  {overall_label}",
        "",
        f"Old rules audit ({len(old_rules)} total):",
        f"  Fully changed:    {len(fully_changed)}",
        f"  Deactivated (no replacement): {len(partially_changed)}",
        f"  Still active:     {len(unchanged)}",
        "",
        f"Unrealized value estimate: {unrealized['unrealized_value_formatted']}",
        f"  {unrealized['note']}",
        "",
        "Recommendations:",
    ]
    for r in recommendations:
        summary_lines.append(f"  - {r}")

    format_output(result, "\n".join(summary_lines))


if __name__ == "__main__":
    main()
