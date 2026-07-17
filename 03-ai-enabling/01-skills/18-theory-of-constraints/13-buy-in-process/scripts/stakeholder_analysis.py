"""
Stakeholder Analysis

Maps stakeholders to quadrants (champion / supporter / blocker / bystander)
based on power and support levels. Calculates net support score weighted by
power. Recommends priority actions.

Usage:
    python3 scripts/stakeholder_analysis.py --file input.json
    python3 scripts/stakeholder_analysis.py '{"stakeholders": [...]}'

Input JSON:
{
  "stakeholders": [
    {"name": "Alice", "role": "CEO", "power": 5, "support": 4},
    {"name": "Bob", "role": "Plant Manager", "power": 3, "support": -2},
    {"name": "Carol", "role": "Analyst", "power": 1, "support": 3},
    {"name": "Dave", "role": "Union Rep", "power": 4, "support": -4}
  ]
}

Power: 1-5 (1=low influence, 5=high influence)
Support: -5 to +5 (negative=against, 0=neutral, positive=for)

Quadrants:
  Champion:  high power (>=3) AND positive support (>0)
  Supporter: low power (<3)  AND positive support (>0)
  Blocker:   high power (>=3) AND negative support (<0)
  Bystander: low power (<3)  AND negative/neutral support (<=0)

Output: quadrant mapping, net support score, priority actions.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, rank_by

POWER_THRESHOLD = 3       # >= this = high power
SUPPORT_POSITIVE = 0      # > this = supportive
SUPPORT_STRONG_POSITIVE = 3   # >= this = strong supporter
SUPPORT_STRONG_NEGATIVE = -3  # <= this = strong opponent


def classify_quadrant(power, support):
    """Classify stakeholder into quadrant based on power and support."""
    high_power = power >= POWER_THRESHOLD
    positive = support > SUPPORT_POSITIVE

    if high_power and positive:
        return "champion"
    elif not high_power and positive:
        return "supporter"
    elif high_power and not positive:
        return "blocker"
    else:
        return "bystander"


QUADRANT_DESCRIPTIONS = {
    "champion": {
        "label": "Champion",
        "description": "High power, supportive — your most valuable allies",
        "strategy": (
            "Leverage actively. Keep engaged and informed. "
            "Use their credibility to influence blockers and bystanders. "
            "Ask them to personally sponsor the change in high-stakes forums."
        ),
        "priority": 1,
    },
    "blocker": {
        "label": "Blocker",
        "description": "High power, opposed — your most dangerous risk",
        "strategy": (
            "Priority focus. Understand their specific resistance layer (use resistance_mapper.py). "
            "Engage privately before group settings. "
            "Convert to neutral before attempting to make them champions. "
            "Do not proceed over them without a plan — they will find ways to derail."
        ),
        "priority": 2,
    },
    "supporter": {
        "label": "Supporter",
        "description": "Low power, supportive — amplify their voice",
        "strategy": (
            "Nurture and amplify. Give them channels to express support publicly. "
            "They won't block you but they can build social proof and peer influence. "
            "Consider whether any supporters can grow their influence (power) over time."
        ),
        "priority": 3,
    },
    "bystander": {
        "label": "Bystander",
        "description": "Low power, neutral or opposed — monitor, don't ignore",
        "strategy": (
            "Do not assume harmless. Bystanders can become blockers if circumstances change. "
            "Low-cost engagement to understand concerns. "
            "If neutral, a short conversation may move them to supporter. "
            "If opposed but low power, monitor for shifts in their influence."
        ),
        "priority": 4,
    },
}


def calculate_net_support(stakeholders):
    """
    Net support score = sum(power * support) / sum(power)
    Range: -5 to +5 (weighted average of support, weighted by power)
    """
    total_weight = sum(s.get("power", 1) for s in stakeholders)
    if total_weight == 0:
        return 0
    weighted_sum = sum(
        s.get("power", 1) * s.get("support", 0)
        for s in stakeholders
    )
    return round(weighted_sum / total_weight, 2)


def classify_net_support(score):
    if score >= 2:
        return "Strong net support — change is likely to succeed with execution"
    elif score >= 0.5:
        return "Moderate net support — proceed but address blockers"
    elif score >= -0.5:
        return "Near-neutral — outcome uncertain, focus on converting blockers"
    elif score >= -2:
        return "Net opposition — change will face significant resistance"
    else:
        return "Strong net opposition — change is unlikely to succeed without major realignment"


def build_priority_actions(quadrant_groups, net_support):
    """Generate specific priority actions based on the stakeholder landscape."""
    actions = []

    blockers = quadrant_groups.get("blocker", [])
    champions = quadrant_groups.get("champion", [])
    supporters = quadrant_groups.get("supporter", [])
    bystanders = quadrant_groups.get("bystander", [])

    if blockers:
        strong_blockers = [b for b in blockers if b.get("support", 0) <= SUPPORT_STRONG_NEGATIVE]
        if strong_blockers:
            names = ", ".join(b["name"] for b in strong_blockers)
            actions.append({
                "priority": 1,
                "action": f"Immediate 1:1 with strong blockers: {names}",
                "rationale": (
                    "Strong opposition from high-power stakeholders will derail the change. "
                    "Understand their resistance layer before any group sessions."
                ),
            })
        moderate_blockers = [b for b in blockers if b.get("support", 0) > SUPPORT_STRONG_NEGATIVE]
        if moderate_blockers:
            names = ", ".join(b["name"] for b in moderate_blockers)
            actions.append({
                "priority": 2,
                "action": f"Address moderate blockers before group presentations: {names}",
                "rationale": (
                    "Moderate blockers may be persuadable. Private engagement is more effective "
                    "than confrontation in group settings."
                ),
            })

    if champions:
        names = ", ".join(c["name"] for c in champions)
        actions.append({
            "priority": 3,
            "action": f"Brief champions before key decision meetings: {names}",
            "rationale": (
                "Champions with advance preparation can address objections in real time "
                "and lend credibility that external advocates cannot."
            ),
        })

    if supporters:
        actions.append({
            "priority": 4,
            "action": f"Create visible channels for {len(supporters)} supporter(s) to express support",
            "rationale": (
                "Supporters build social proof. Their peer influence can shift bystanders "
                "and soften blocker resistance over time."
            ),
        })

    if net_support < 0.5:
        actions.append({
            "priority": 5,
            "action": "Do not proceed to group decision forum until net support score is positive",
            "rationale": (
                f"Current net support score ({net_support}) indicates the change will not pass. "
                "Moving forward risks hardening opposition."
            ),
        })

    if not actions:
        actions.append({
            "priority": 1,
            "action": "Maintain engagement — landscape is favorable but can shift",
            "rationale": "Net support is positive. Focus on execution and monitor for shifts.",
        })

    return sorted(actions, key=lambda x: x["priority"])


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    require_fields(data, ["stakeholders"])

    stakeholders = data["stakeholders"]
    if not isinstance(stakeholders, list) or len(stakeholders) == 0:
        print("Error: stakeholders must be a non-empty list", file=sys.stderr)
        sys.exit(1)

    # Validate and classify each stakeholder
    classified = []
    warnings = []
    for s in stakeholders:
        name = s.get("name", "Unknown")
        power = s.get("power", 3)
        support = s.get("support", 0)

        # Clamp to valid ranges
        power = max(1, min(5, int(power)))
        support = max(-5, min(5, float(support)))

        quadrant = classify_quadrant(power, support)
        meta = QUADRANT_DESCRIPTIONS[quadrant]

        classified.append({
            "name": name,
            "role": s.get("role", ""),
            "power": power,
            "support": support,
            "quadrant": quadrant,
            "quadrant_label": meta["label"],
            "quadrant_description": meta["description"],
            "strategy": meta["strategy"],
        })

    # Group by quadrant
    quadrant_groups = {"champion": [], "supporter": [], "blocker": [], "bystander": []}
    for s in classified:
        quadrant_groups[s["quadrant"]].append(s)

    net_support = calculate_net_support(stakeholders)
    net_support_label = classify_net_support(net_support)
    priority_actions = build_priority_actions(quadrant_groups, net_support)

    # Summary counts
    counts = {q: len(v) for q, v in quadrant_groups.items()}

    result = {
        "summary": {
            "total_stakeholders": len(classified),
            "net_support_score": net_support,
            "net_support_score_range": "-5 (full opposition) to +5 (full support), weighted by power",
            "net_support_label": net_support_label,
            "quadrant_counts": counts,
        },
        "stakeholders_by_quadrant": {
            "champions": quadrant_groups["champion"],
            "blockers": quadrant_groups["blocker"],
            "supporters": quadrant_groups["supporter"],
            "bystanders": quadrant_groups["bystander"],
        },
        "all_stakeholders": sorted(classified, key=lambda x: (
            QUADRANT_DESCRIPTIONS[x["quadrant"]]["priority"],
            -x["power"],
        )),
        "priority_actions": priority_actions,
        "warnings": warnings,
    }

    summary_lines = [
        "=== Stakeholder Analysis ===",
        f"Total stakeholders: {len(classified)}",
        f"Net support score: {net_support:+.2f} — {net_support_label}",
        "",
        f"Champions: {counts['champion']}  |  Blockers: {counts['blocker']}  |  "
        f"Supporters: {counts['supporter']}  |  Bystanders: {counts['bystander']}",
        "",
    ]
    if quadrant_groups["blocker"]:
        summary_lines.append("BLOCKERS (high power, opposed):")
        for b in sorted(quadrant_groups["blocker"], key=lambda x: x["support"]):
            summary_lines.append(
                f"  - {b['name']} ({b['role']}) power={b['power']} support={b['support']:+.0f}"
            )
        summary_lines.append("")
    if quadrant_groups["champion"]:
        summary_lines.append("CHAMPIONS (high power, supportive):")
        for c in sorted(quadrant_groups["champion"], key=lambda x: -x["support"]):
            summary_lines.append(
                f"  - {c['name']} ({c['role']}) power={c['power']} support={c['support']:+.0f}"
            )
        summary_lines.append("")
    summary_lines.append("Priority Actions:")
    for action in priority_actions:
        summary_lines.append(f"  #{action['priority']}: {action['action']}")

    format_output(result, "\n".join(summary_lines))


if __name__ == "__main__":
    main()
