"""
Viable Vision Revenue Model

Models sequential constraint removal and projects revenue trajectory toward
Goldratt's four-year target: revenue grows to equal current profit level
(interpreted as: throughput covers OE at a dramatically improved margin).

Usage:
    python3 scripts/revenue_model.py --file input.json
    python3 scripts/revenue_model.py '{"current_annual_revenue": 5000000, ...}'

Input JSON:
{
  "current_annual_revenue": 5000000,
  "current_annual_profit": 1000000,
  "constraints": [
    {
      "name": "Sales capacity",
      "type": "capacity",
      "estimated_revenue_unlock": 800000,
      "removal_difficulty": 3
    }
  ]
}

Output: constraint removal sequence, cumulative revenue trajectory,
years to target, feasibility assessment.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, currency, pct, rank_by

CONSTRAINT_TYPES = {"market", "capacity", "policy", "knowledge"}

# Policy and knowledge constraints are faster/cheaper to remove — apply a type bonus
TYPE_BONUS = {
    "policy": 1.4,
    "knowledge": 1.2,
    "capacity": 1.0,
    "market": 0.8,
}

YEARS = 4


def score_constraint(c):
    """Score a constraint by unlock-per-difficulty, adjusted for type speed."""
    difficulty = max(1, min(5, c.get("removal_difficulty", 3)))
    unlock = max(0, c.get("estimated_revenue_unlock", 0))
    ctype = c.get("type", "capacity").lower()
    bonus = TYPE_BONUS.get(ctype, 1.0)
    return (unlock / difficulty) * bonus


def distribute_over_years(constraints, years=YEARS):
    """
    Assign constraints to years based on removal_difficulty.
    Difficulty 1-2 → year 1, 3 → year 2, 4 → year 3, 5 → year 4.
    Multiple constraints in same year stack.
    """
    year_map = {1: [], 2: [], 3: [], 4: []}
    difficulty_to_year = {1: 1, 2: 1, 3: 2, 4: 3, 5: 4}
    for c in constraints:
        difficulty = max(1, min(5, c.get("removal_difficulty", 3)))
        year = difficulty_to_year[difficulty]
        year_map[year].append(c)
    return year_map


def build_trajectory(base_revenue, year_map, years=YEARS):
    """Build cumulative revenue trajectory year by year."""
    trajectory = []
    cumulative_revenue = base_revenue
    cumulative_unlock = 0

    for year in range(1, years + 1):
        year_constraints = year_map.get(year, [])
        year_unlock = sum(c.get("estimated_revenue_unlock", 0) for c in year_constraints)
        cumulative_unlock += year_unlock
        cumulative_revenue = base_revenue + cumulative_unlock

        trajectory.append({
            "year": year,
            "constraints_removed": [c["name"] for c in year_constraints],
            "revenue_unlocked_this_year": year_unlock,
            "cumulative_unlock": cumulative_unlock,
            "projected_revenue": cumulative_revenue,
            "projected_revenue_formatted": currency(cumulative_revenue),
        })

    return trajectory


def assess_feasibility(trajectory, target_revenue, current_revenue):
    """Determine whether target is met within 4 years and in which year."""
    for entry in trajectory:
        if entry["projected_revenue"] >= target_revenue:
            return {
                "achievable_within_4_years": True,
                "target_met_in_year": entry["year"],
                "revenue_at_target_year": entry["projected_revenue"],
                "revenue_at_target_year_formatted": currency(entry["projected_revenue"]),
            }

    final_revenue = trajectory[-1]["projected_revenue"] if trajectory else current_revenue
    gap = max(0, target_revenue - final_revenue)
    return {
        "achievable_within_4_years": False,
        "target_met_in_year": None,
        "revenue_at_year_4": final_revenue,
        "revenue_at_year_4_formatted": currency(final_revenue),
        "shortfall": gap,
        "shortfall_formatted": currency(gap),
        "shortfall_pct": round((gap / target_revenue) * 100, 1) if target_revenue > 0 else 0,
    }


def classify_constraints(constraints):
    """Validate and normalize constraint type fields."""
    normalized = []
    warnings = []
    for c in constraints:
        ctype = c.get("type", "capacity").lower()
        if ctype not in CONSTRAINT_TYPES:
            warnings.append(f"Unknown constraint type '{ctype}' for '{c.get('name', '?')}' — defaulting to 'capacity'")
            ctype = "capacity"
        normalized.append({**c, "type": ctype})
    return normalized, warnings


def build_removal_sequence(constraints):
    """Rank constraints by priority score and annotate."""
    scored = []
    for c in constraints:
        difficulty = max(1, min(5, c.get("removal_difficulty", 3)))
        unlock = max(0, c.get("estimated_revenue_unlock", 0))
        score = score_constraint(c)
        scored.append({
            "name": c.get("name", "Unnamed"),
            "type": c.get("type", "capacity"),
            "estimated_revenue_unlock": unlock,
            "estimated_revenue_unlock_formatted": currency(unlock),
            "removal_difficulty": difficulty,
            "priority_score": round(score, 2),
            "rationale": (
                f"Unlock {currency(unlock)} at difficulty {difficulty} "
                f"({c.get('type', 'capacity')} type) → score {score:.2f}"
            ),
        })
    return rank_by(scored, "priority_score", reverse=True)


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    require_fields(data, ["current_annual_revenue", "current_annual_profit", "constraints"])

    current_revenue = float(data["current_annual_revenue"])
    current_profit = float(data["current_annual_profit"])
    raw_constraints = data["constraints"]

    if not isinstance(raw_constraints, list) or len(raw_constraints) == 0:
        print("Error: constraints must be a non-empty list", file=sys.stderr)
        sys.exit(1)

    # Viable Vision target: revenue equals current profit
    # (i.e., you operate the business at near-zero OE relative to throughput,
    # or more precisely: your throughput improvement makes the margin profile
    # equivalent to running at current_profit as total revenue)
    # Practical interpretation: total revenue unlock needed = current_profit
    target_revenue = current_profit
    target_label = (
        f"Goldratt's Viable Vision target: {currency(target_revenue)} revenue unlock "
        f"(equal to current profit of {currency(current_profit)})"
    )

    constraints, warnings = classify_constraints(raw_constraints)
    removal_sequence = build_removal_sequence(constraints)

    # Distribute by difficulty into years using the ranked order
    year_map = distribute_over_years(removal_sequence)
    trajectory = build_trajectory(current_revenue, year_map)
    feasibility = assess_feasibility(trajectory, current_revenue + target_revenue, current_revenue)

    total_unlock = sum(c.get("estimated_revenue_unlock", 0) for c in constraints)
    unlock_coverage = (total_unlock / target_revenue) if target_revenue > 0 else 0

    result = {
        "summary": {
            "current_annual_revenue": current_revenue,
            "current_annual_revenue_formatted": currency(current_revenue),
            "current_annual_profit": current_profit,
            "current_annual_profit_formatted": currency(current_profit),
            "viable_vision_target_revenue": current_revenue + target_revenue,
            "viable_vision_target_revenue_formatted": currency(current_revenue + target_revenue),
            "target_label": target_label,
            "total_constraints": len(constraints),
            "total_estimated_unlock": total_unlock,
            "total_estimated_unlock_formatted": currency(total_unlock),
            "unlock_covers_target": pct(min(unlock_coverage, 1.0)),
        },
        "constraint_removal_sequence": removal_sequence,
        "revenue_trajectory": trajectory,
        "feasibility": feasibility,
        "warnings": warnings,
        "recommendations": _build_recommendations(feasibility, removal_sequence, unlock_coverage),
    }

    summary_lines = [
        "=== Viable Vision Revenue Model ===",
        f"Current revenue:  {currency(current_revenue)}",
        f"Current profit:   {currency(current_profit)}",
        f"VV target:        {currency(current_revenue + target_revenue)} (revenue = current profit level)",
        "",
        f"Constraints identified: {len(constraints)}",
        f"Total estimated unlock: {currency(total_unlock)} ({pct(min(unlock_coverage, 1.0))} of target)",
        "",
        "Removal sequence (ranked by priority):",
    ]
    for c in removal_sequence:
        summary_lines.append(
            f"  #{c['rank']} {c['name']} — unlock {c['estimated_revenue_unlock_formatted']}, "
            f"difficulty {c['removal_difficulty']}, score {c['priority_score']}"
        )
    summary_lines.append("")
    if feasibility["achievable_within_4_years"]:
        summary_lines.append(
            f"FEASIBLE: Target achievable in Year {feasibility['target_met_in_year']}"
        )
    else:
        summary_lines.append(
            f"NOT FEASIBLE within 4 years. "
            f"Shortfall: {feasibility.get('shortfall_formatted', 'N/A')} "
            f"({feasibility.get('shortfall_pct', 0)}% of target)"
        )

    format_output(result, "\n".join(summary_lines))


def _build_recommendations(feasibility, removal_sequence, unlock_coverage):
    recs = []
    if not feasibility["achievable_within_4_years"]:
        recs.append(
            "Target is not achievable with identified constraints alone. "
            "Look for additional constraints or re-estimate unlock potential."
        )
    if unlock_coverage < 0.5:
        recs.append(
            "Identified constraints cover less than 50% of the target unlock. "
            "There are likely significant constraints not yet identified — "
            "conduct a deeper Current Reality Tree analysis."
        )
    high_difficulty = [c for c in removal_sequence if c["removal_difficulty"] >= 4]
    if high_difficulty:
        names = ", ".join(c["name"] for c in high_difficulty)
        recs.append(
            f"High-difficulty constraints ({names}) carry execution risk. "
            "Validate removal assumptions before committing to the trajectory."
        )
    policy_constraints = [c for c in removal_sequence if c["type"] == "policy"]
    if policy_constraints:
        recs.append(
            f"Policy constraints ({', '.join(c['name'] for c in policy_constraints)}) "
            "should be removed first — they are fastest and typically unlock capacity elsewhere."
        )
    if not recs:
        recs.append(
            "Constraint portfolio looks well-structured. "
            "Validate estimated unlock figures against real market/capacity data."
        )
    return recs


if __name__ == "__main__":
    main()
