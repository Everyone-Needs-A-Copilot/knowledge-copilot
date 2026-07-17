"""
Mafia Offer Scorer

Evaluates whether a proposed offer qualifies as a "Mafia Offer" — one so
compelling that customers who have the target problem cannot refuse it, yet
remains profitable and defensible for the offering company.

Usage:
    python3 scripts/mafia_offer.py --file input.json
    python3 scripts/mafia_offer.py '{"offer_description": "...", ...}'

Input JSON:
{
  "offer_description": "We implement your CRM in 60 days or you don't pay.",
  "customer_pains": [
    {"pain": "Implementation takes 6-12 months", "severity": 9, "addressed_by_offer": true},
    {"pain": "High upfront cost before seeing value", "severity": 8, "addressed_by_offer": true},
    {"pain": "Poor adoption after go-live", "severity": 7, "addressed_by_offer": false}
  ],
  "competitor_offers": [
    {
      "competitor": "Acme CRM",
      "offer": "Standard implementation, timeline varies",
      "weakness": "No timeline guarantee, customer bears all risk"
    }
  ]
}

Output: unrefusable score 0-100, defensibility score 0-100,
gap analysis, competitive positioning.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, pct, rank_by

HIGH_SEVERITY_THRESHOLD = 7   # pains at or above this level are "significant"
UNREFUSABLE_WEIGHT_COVERAGE = 0.5   # 50% weight for % of top pains addressed
UNREFUSABLE_WEIGHT_SEVERITY = 0.5   # 50% weight for average severity addressed


def score_unrefusable(pains):
    """
    Score 0-100 on "unrefusable" dimension.

    Two sub-scores:
    - Coverage: what % of HIGH_SEVERITY_THRESHOLD+ pains are addressed (0-100)
    - Severity: average severity of addressed pains, normalized to 0-100

    Weighted average of both.
    """
    if not pains:
        return 0, [], []

    top_pains = [p for p in pains if p.get("severity", 0) >= HIGH_SEVERITY_THRESHOLD]
    addressed_top = [p for p in top_pains if p.get("addressed_by_offer", False)]
    all_addressed = [p for p in pains if p.get("addressed_by_offer", False)]
    unaddressed_top = [p for p in top_pains if not p.get("addressed_by_offer", False)]

    # Coverage sub-score
    if top_pains:
        coverage_score = (len(addressed_top) / len(top_pains)) * 100
    else:
        # No high-severity pains defined — score on all pains
        addressed_all = [p for p in pains if p.get("addressed_by_offer", False)]
        coverage_score = (len(addressed_all) / len(pains)) * 100 if pains else 0

    # Severity sub-score — average severity of addressed pains / 10 * 100
    if all_addressed:
        avg_severity = sum(p.get("severity", 5) for p in all_addressed) / len(all_addressed)
        severity_score = (avg_severity / 10) * 100
    else:
        severity_score = 0

    final = (
        coverage_score * UNREFUSABLE_WEIGHT_COVERAGE
        + severity_score * UNREFUSABLE_WEIGHT_SEVERITY
    )

    return round(final, 1), addressed_top, unaddressed_top


def score_defensibility(competitor_offers):
    """
    Score 0-100 on defensibility.

    Based on: how many distinct competitor weaknesses are being exploited
    by the offer. Each unique weakness exploited contributes to the score.

    Score formula: min(100, (weaknesses_count / max(1, competitors_count)) * 100)
    i.e., if every competitor has at least one weakness the offer exploits, score = 100.
    """
    if not competitor_offers:
        return 0, []

    weaknesses = [
        c.get("weakness", "").strip()
        for c in competitor_offers
        if c.get("weakness", "").strip()
    ]
    competitors_count = len(competitor_offers)
    weaknesses_exploited = len([w for w in weaknesses if w])

    score = min(100, (weaknesses_exploited / competitors_count) * 100)
    return round(score, 1), weaknesses


def classify_unrefusable(score):
    if score >= 75:
        return "Strong Mafia Offer"
    elif score >= 50:
        return "Moderate — needs improvement"
    elif score >= 25:
        return "Weak — significant gaps"
    else:
        return "Not a Mafia Offer — customer has little reason to switch"


def classify_defensibility(score):
    if score >= 75:
        return "Highly defensible — competitors cannot easily match"
    elif score >= 50:
        return "Moderately defensible — some differentiation"
    elif score >= 25:
        return "Low defensibility — competitors can copy quickly"
    else:
        return "Not defensible — offer is undifferentiated"


def build_gap_analysis(pains):
    """Identify high-severity pains not addressed by the offer."""
    gaps = []
    for p in pains:
        if not p.get("addressed_by_offer", False) and p.get("severity", 0) >= HIGH_SEVERITY_THRESHOLD:
            gaps.append({
                "pain": p.get("pain", ""),
                "severity": p.get("severity", 0),
                "impact": "High — this pain is significant and unaddressed by the offer",
            })
    return sorted(gaps, key=lambda x: x["severity"], reverse=True)


def build_competitive_positioning(competitor_offers, weaknesses_exploited):
    """Summarize competitive positioning."""
    if not competitor_offers:
        return {"note": "No competitor offers provided — cannot assess positioning"}

    positions = []
    for c in competitor_offers:
        positions.append({
            "competitor": c.get("competitor", "Unknown"),
            "their_offer": c.get("offer", ""),
            "their_weakness": c.get("weakness", ""),
            "exploited_by_your_offer": bool(c.get("weakness", "").strip()),
        })
    return {
        "competitors_analyzed": len(competitor_offers),
        "weaknesses_exploited": len([p for p in positions if p["exploited_by_your_offer"]]),
        "positions": positions,
    }


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    require_fields(data, ["offer_description", "customer_pains", "competitor_offers"])

    offer_description = data["offer_description"]
    pains = data["customer_pains"]
    competitor_offers = data["competitor_offers"]

    if not isinstance(pains, list):
        print("Error: customer_pains must be a list", file=sys.stderr)
        sys.exit(1)
    if not isinstance(competitor_offers, list):
        print("Error: competitor_offers must be a list", file=sys.stderr)
        sys.exit(1)

    unrefusable_score, addressed_top, unaddressed_top = score_unrefusable(pains)
    defensibility_score, weaknesses = score_defensibility(competitor_offers)
    gap_analysis = build_gap_analysis(pains)
    competitive_positioning = build_competitive_positioning(competitor_offers, weaknesses)

    unrefusable_label = classify_unrefusable(unrefusable_score)
    defensibility_label = classify_defensibility(defensibility_score)

    # Profitability is not modeled here — flagged for separate analysis
    profitability_note = (
        "Profitability is NOT assessed by this script. "
        "A Mafia Offer is only viable if your constraint removal makes delivery economical. "
        "Run throughput_analysis.py to validate margin assumptions before committing to the offer."
    )

    # Overall verdict
    if unrefusable_score >= 75 and defensibility_score >= 50:
        verdict = "STRONG MAFIA OFFER — pursue this offer design"
    elif unrefusable_score >= 50 and defensibility_score >= 25:
        verdict = "PROMISING — close gaps before committing"
    elif unrefusable_score < 50:
        verdict = "WEAK OFFER — address high-severity unaddressed pains first"
    else:
        verdict = "DEFENSIBILITY CONCERN — competitors will copy this quickly"

    recommendations = []
    if gap_analysis:
        top_gap = gap_analysis[0]
        recommendations.append(
            f"Critical gap: '{top_gap['pain']}' (severity {top_gap['severity']}) is unaddressed. "
            "This is the most likely reason customers will hesitate."
        )
    if unrefusable_score < 50:
        recommendations.append(
            "Increase offer strength by addressing more high-severity customer pains, "
            "or by making the risk-transfer mechanism more explicit (e.g., performance guarantee)."
        )
    if defensibility_score < 50:
        recommendations.append(
            "Improve defensibility by exploiting more competitor weaknesses, "
            "or by building delivery capabilities that competitors cannot easily replicate."
        )
    if not recommendations:
        recommendations.append(
            "Offer is strong. Validate delivery capability and profitability before launch."
        )

    result = {
        "offer_description": offer_description,
        "scores": {
            "unrefusable": unrefusable_score,
            "unrefusable_label": unrefusable_label,
            "defensibility": defensibility_score,
            "defensibility_label": defensibility_label,
            "profitability": None,
            "profitability_note": profitability_note,
        },
        "verdict": verdict,
        "pain_analysis": {
            "total_pains": len(pains),
            "high_severity_pains": len([p for p in pains if p.get("severity", 0) >= HIGH_SEVERITY_THRESHOLD]),
            "high_severity_addressed": len(addressed_top),
            "high_severity_unaddressed": len(unaddressed_top),
        },
        "gap_analysis": gap_analysis,
        "competitive_positioning": competitive_positioning,
        "recommendations": recommendations,
    }

    summary_lines = [
        "=== Mafia Offer Assessment ===",
        f"Offer: {offer_description}",
        "",
        f"Unrefusable score:   {unrefusable_score}/100 — {unrefusable_label}",
        f"Defensibility score: {defensibility_score}/100 — {defensibility_label}",
        f"Profitability score: NOT ASSESSED (see profitability_note)",
        "",
        f"Verdict: {verdict}",
        "",
        f"Customer pains analyzed: {len(pains)}",
        f"High-severity pains (>={HIGH_SEVERITY_THRESHOLD}): {len([p for p in pains if p.get('severity', 0) >= HIGH_SEVERITY_THRESHOLD])}",
        f"High-severity addressed: {len(addressed_top)}",
        f"High-severity NOT addressed: {len(unaddressed_top)}",
    ]
    if gap_analysis:
        summary_lines.append("")
        summary_lines.append("Critical gaps (unaddressed high-severity pains):")
        for g in gap_analysis:
            summary_lines.append(f"  - [{g['severity']}/10] {g['pain']}")
    summary_lines.append("")
    summary_lines.append("Recommendations:")
    for r in recommendations:
        summary_lines.append(f"  - {r}")

    format_output(result, "\n".join(summary_lines))


if __name__ == "__main__":
    main()
