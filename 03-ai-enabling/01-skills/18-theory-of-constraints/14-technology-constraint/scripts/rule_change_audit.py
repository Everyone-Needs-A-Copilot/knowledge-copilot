"""
Rule Change Audit — Technology Portfolio

Audits a portfolio of technology investments for the relationship between
rule-change completeness and value realization. Goldratt's hypothesis:
value realization is directly correlated with how many old rules were replaced
when the technology was introduced.

Usage:
    python3 scripts/rule_change_audit.py --file input.json
    python3 scripts/rule_change_audit.py '{"investments": [...]}'

Input JSON:
{
  "investments": [
    {
      "technology": "Salesforce CRM",
      "cost": 120000,
      "old_rules_count": 6,
      "rules_changed": 2,
      "value_expected": 300000,
      "value_realized": 80000
    },
    {
      "technology": "ERP System",
      "cost": 800000,
      "old_rules_count": 20,
      "rules_changed": 18,
      "value_expected": 1200000,
      "value_realized": 1100000
    }
  ]
}

Output: per-investment analysis, portfolio summary,
correlation between rule-change ratio and value realization,
recommendations for underperforming investments.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, currency, pct, rank_by


def calculate_investment_metrics(inv):
    """Calculate key metrics for a single investment."""
    cost = float(inv.get("cost", 0))
    old_rules_count = max(1, int(inv.get("old_rules_count", 1)))
    rules_changed = min(int(inv.get("rules_changed", 0)), old_rules_count)
    value_expected = float(inv.get("value_expected", 0))
    value_realized = float(inv.get("value_realized", 0))

    rule_change_ratio = rules_changed / old_rules_count
    value_realization_ratio = (value_realized / value_expected) if value_expected > 0 else 0
    value_gap = max(0, value_expected - value_realized)
    roi_expected = ((value_expected - cost) / cost) if cost > 0 else 0
    roi_realized = ((value_realized - cost) / cost) if cost > 0 else 0

    return {
        "technology": inv.get("technology", "Unknown"),
        "cost": cost,
        "cost_formatted": currency(cost),
        "old_rules_count": old_rules_count,
        "rules_changed": rules_changed,
        "rule_change_ratio": round(rule_change_ratio, 3),
        "rule_change_pct": pct(rule_change_ratio),
        "value_expected": value_expected,
        "value_expected_formatted": currency(value_expected),
        "value_realized": value_realized,
        "value_realized_formatted": currency(value_realized),
        "value_gap": value_gap,
        "value_gap_formatted": currency(value_gap),
        "value_realization_ratio": round(value_realization_ratio, 3),
        "value_realization_pct": pct(value_realization_ratio),
        "roi_expected": round(roi_expected, 3),
        "roi_realized": round(roi_realized, 3),
        "performance_label": _classify_performance(value_realization_ratio, rule_change_ratio),
    }


def _classify_performance(realization_ratio, rule_change_ratio):
    if realization_ratio >= 0.8 and rule_change_ratio >= 0.7:
        return "High performer — strong rule changes, strong value realization"
    elif realization_ratio >= 0.8 and rule_change_ratio < 0.7:
        return "Lucky high performer — good results despite incomplete rule changes (fragile)"
    elif realization_ratio < 0.4 and rule_change_ratio >= 0.7:
        return "Rule-changed but still underperforming — constraint may be elsewhere"
    elif realization_ratio < 0.4 and rule_change_ratio < 0.3:
        return "Classic failure pattern — technology implemented, rules unchanged"
    elif realization_ratio < 0.6:
        return "Underperforming — partial rule changes, partial value realization"
    else:
        return "Moderate performer — room for improvement in rule changes"


def pearson_correlation(xs, ys):
    """
    Compute Pearson correlation coefficient between two equal-length lists.
    Returns None if insufficient data or zero variance.
    """
    n = len(xs)
    if n < 2:
        return None
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    cov = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n))
    std_x = (sum((x - mean_x) ** 2 for x in xs) / n) ** 0.5
    std_y = (sum((y - mean_y) ** 2 for y in ys) / n) ** 0.5
    if std_x == 0 or std_y == 0:
        return None
    return round(cov / (n * std_x * std_y), 3)


def build_correlation_assessment(investments_metrics):
    """Assess correlation between rule_change_ratio and value_realization_ratio."""
    xs = [m["rule_change_ratio"] for m in investments_metrics]
    ys = [m["value_realization_ratio"] for m in investments_metrics]

    r = pearson_correlation(xs, ys)

    if r is None:
        return {
            "correlation": None,
            "interpretation": "Insufficient data for correlation analysis (need at least 2 investments)",
            "goldratt_hypothesis": "Not testable with current data",
        }

    if r >= 0.7:
        interpretation = (
            f"Strong positive correlation (r={r}): investments where more rules were changed "
            "delivered significantly more value. Goldratt's hypothesis is supported in this portfolio."
        )
    elif r >= 0.4:
        interpretation = (
            f"Moderate positive correlation (r={r}): some evidence that rule changes drive value, "
            "but other factors are also significant."
        )
    elif r >= 0.0:
        interpretation = (
            f"Weak positive correlation (r={r}): rule changes may help but the relationship "
            "is not strong in this portfolio. Look for other value drivers."
        )
    elif r >= -0.4:
        interpretation = (
            f"Weak negative correlation (r={r}): rule changes do not appear to drive value "
            "in this portfolio. The constraint may be elsewhere."
        )
    else:
        interpretation = (
            f"Negative correlation (r={r}): unusual result — investments with more rule changes "
            "are underperforming. The rule changes themselves may be counterproductive, "
            "or the technology may not be addressing real constraints."
        )

    return {
        "correlation": r,
        "interpretation": interpretation,
        "goldratt_hypothesis": (
            "Goldratt predicts: higher rule-change ratio → higher value realization. "
            f"Portfolio correlation: r={r}."
        ),
    }


def build_portfolio_summary(investments_metrics):
    total_cost = sum(m["cost"] for m in investments_metrics)
    total_expected = sum(m["value_expected"] for m in investments_metrics)
    total_realized = sum(m["value_realized"] for m in investments_metrics)
    total_gap = sum(m["value_gap"] for m in investments_metrics)
    portfolio_realization = total_realized / total_expected if total_expected > 0 else 0

    avg_rule_change = sum(m["rule_change_ratio"] for m in investments_metrics) / len(investments_metrics)
    avg_realization = sum(m["value_realization_ratio"] for m in investments_metrics) / len(investments_metrics)

    return {
        "total_investments": len(investments_metrics),
        "total_cost": total_cost,
        "total_cost_formatted": currency(total_cost),
        "total_value_expected": total_expected,
        "total_value_expected_formatted": currency(total_expected),
        "total_value_realized": total_realized,
        "total_value_realized_formatted": currency(total_realized),
        "total_value_gap": total_gap,
        "total_value_gap_formatted": currency(total_gap),
        "portfolio_realization_ratio": round(portfolio_realization, 3),
        "portfolio_realization_pct": pct(portfolio_realization),
        "avg_rule_change_ratio": round(avg_rule_change, 3),
        "avg_rule_change_pct": pct(avg_rule_change),
        "avg_value_realization_ratio": round(avg_realization, 3),
        "avg_value_realization_pct": pct(avg_realization),
    }


def build_recommendations(investments_metrics, correlation):
    recs = []

    # Identify worst performers by value gap
    by_gap = sorted(investments_metrics, key=lambda x: x["value_gap"], reverse=True)
    worst = [m for m in by_gap if m["value_realization_ratio"] < 0.5]

    if worst:
        names = ", ".join(m["technology"] for m in worst[:3])
        recs.append(
            f"Priority remediation targets: {names}. "
            "These investments have delivered less than 50% of expected value. "
            "Run tech_assessment.py for each to identify which old rules are still active."
        )

    # Identify classic failure pattern
    classic_failures = [
        m for m in investments_metrics
        if m["value_realization_ratio"] < 0.4 and m["rule_change_ratio"] < 0.3
    ]
    if classic_failures:
        names = ", ".join(m["technology"] for m in classic_failures)
        recs.append(
            f"Classic Goldratt failure pattern detected: {names}. "
            "Technology was implemented but old rules were not changed. "
            "These investments may still deliver value if rule changes are made now — "
            "it's not too late."
        )

    # Identify lucky high performers
    lucky = [
        m for m in investments_metrics
        if m["value_realization_ratio"] >= 0.8 and m["rule_change_ratio"] < 0.5
    ]
    if lucky:
        names = ", ".join(m["technology"] for m in lucky)
        recs.append(
            f"Fragile high performers: {names}. "
            "Good results achieved despite incomplete rule changes. "
            "This performance may not be sustainable or scalable. "
            "Identify and replace remaining old rules before the next constraint emerges."
        )

    if correlation and correlation["correlation"] is not None and correlation["correlation"] < 0.4:
        recs.append(
            "Portfolio correlation between rule changes and value realization is low. "
            "Technology may not be addressing the true binding constraint. "
            "Run a Current Reality Tree to verify whether these investments target the right limitation."
        )

    if not recs:
        recs.append(
            "Portfolio is performing well overall. Continue enforcing rule-change discipline "
            "for new technology investments. Conduct annual audits to verify old rules haven't crept back."
        )

    return recs


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    require_fields(data, ["investments"])
    investments = data["investments"]

    if not isinstance(investments, list) or len(investments) == 0:
        print("Error: investments must be a non-empty list", file=sys.stderr)
        sys.exit(1)

    metrics = [calculate_investment_metrics(inv) for inv in investments]
    metrics_ranked = rank_by(metrics, "value_gap", reverse=True)

    portfolio = build_portfolio_summary(metrics)
    correlation = build_correlation_assessment(metrics)
    recommendations = build_recommendations(metrics, correlation)

    result = {
        "portfolio_summary": portfolio,
        "correlation_assessment": correlation,
        "investments": metrics_ranked,
        "recommendations": recommendations,
    }

    summary_lines = [
        "=== Rule Change Audit — Technology Portfolio ===",
        f"Investments analyzed: {portfolio['total_investments']}",
        f"Total investment cost: {portfolio['total_cost_formatted']}",
        f"Total value expected:  {portfolio['total_value_expected_formatted']}",
        f"Total value realized:  {portfolio['total_value_realized_formatted']}",
        f"Total value gap:       {portfolio['total_value_gap_formatted']}",
        f"Portfolio realization: {portfolio['portfolio_realization_pct']}",
        "",
        f"Avg rule-change ratio:    {portfolio['avg_rule_change_pct']}",
        f"Avg value realization:    {portfolio['avg_value_realization_pct']}",
        "",
        f"Correlation (rule changes → value realization):",
        f"  {correlation['interpretation']}",
        "",
        "Investment breakdown (ranked by value gap, largest first):",
    ]
    for m in metrics_ranked:
        summary_lines.append(
            f"  #{m['rank']} {m['technology']}: "
            f"realized {m['value_realization_pct']} of expected value, "
            f"gap {m['value_gap_formatted']}, "
            f"rule changes {m['rule_change_pct']} — {m['performance_label']}"
        )
    summary_lines.append("")
    summary_lines.append("Recommendations:")
    for r in recommendations:
        summary_lines.append(f"  - {r}")

    format_output(result, "\n".join(summary_lines))


if __name__ == "__main__":
    main()
