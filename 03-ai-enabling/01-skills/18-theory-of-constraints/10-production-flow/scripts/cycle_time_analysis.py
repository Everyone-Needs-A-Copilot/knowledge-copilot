#!/usr/bin/env python3
"""Analyze cycle times from completed item history.

Calculates mean, median, stdev, and percentiles (P50/P85/P95). Detects
trend (improving/stable/degrading) by comparing first-half vs second-half means.

Usage:
    python3 cycle_time_analysis.py --file items.json
    echo '{...}' | python3 cycle_time_analysis.py --stdin

Input JSON:
{
  "completed_items": [
    {"start_date": "2024-01-02", "end_date": "2024-01-05"},
    {"start_date": "2024-01-03", "end_date": "2024-01-09", "name": "Feature X"}
  ],
  "period_label": "days"
}

Dates must be ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS).
period_label: optional label for the unit of measurement (default "days").

Output: stats, percentiles, trend, SLA recommendations.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, classify_zone, pct

import statistics
from datetime import datetime


def parse_date(s):
    """Parse ISO date string, returning datetime."""
    for fmt in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%d'):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse date: {s}")


def percentile(sorted_data, p):
    """Calculate Nth percentile from sorted list using nearest-rank method."""
    if not sorted_data:
        return None
    n = len(sorted_data)
    rank = (p / 100) * n
    idx = max(0, min(int(rank) - 1, n - 1)) if rank >= 1 else 0
    # Linear interpolation between two nearest ranks
    lower_idx = max(0, int(rank) - 1)
    upper_idx = min(n - 1, lower_idx + 1)
    fraction = rank - int(rank)
    return sorted_data[lower_idx] + fraction * (sorted_data[upper_idx] - sorted_data[lower_idx])


def detect_trend(cycle_times):
    """Compare first-half vs second-half mean to detect trend direction."""
    if len(cycle_times) < 4:
        return 'insufficient_data', None, None

    mid = len(cycle_times) // 2
    first_half = cycle_times[:mid]
    second_half = cycle_times[mid:]

    first_mean = statistics.mean(first_half)
    second_mean = statistics.mean(second_half)

    if first_mean == 0:
        return 'stable', first_mean, second_mean

    change_pct = (second_mean - first_mean) / first_mean

    if change_pct < -0.10:
        trend = 'improving'
    elif change_pct > 0.10:
        trend = 'degrading'
    else:
        trend = 'stable'

    return trend, first_mean, second_mean


def analyze_cycle_times(data):
    require_fields(data, ['completed_items'])
    items = data['completed_items']
    period_label = data.get('period_label', 'days')

    if not items:
        print("Error: completed_items must not be empty", file=sys.stderr)
        sys.exit(1)

    cycle_times = []
    parse_errors = []

    for i, item in enumerate(items):
        require_fields(item, ['start_date', 'end_date'], context=f"item #{i+1}")
        try:
            start = parse_date(item['start_date'])
            end = parse_date(item['end_date'])
            ct = (end - start).total_seconds() / 86400  # convert to days
            if ct < 0:
                parse_errors.append(f"Item #{i+1}: end_date before start_date")
                continue
            cycle_times.append(ct)
        except ValueError as e:
            parse_errors.append(f"Item #{i+1}: {e}")

    if not cycle_times:
        print("Error: no valid cycle times could be calculated", file=sys.stderr)
        if parse_errors:
            for err in parse_errors:
                print(f"  {err}", file=sys.stderr)
        sys.exit(1)

    sorted_ct = sorted(cycle_times)
    n = len(sorted_ct)

    mean_ct = statistics.mean(cycle_times)
    median_ct = statistics.median(cycle_times)
    stdev_ct = statistics.stdev(cycle_times) if n > 1 else 0
    min_ct = min(cycle_times)
    max_ct = max(cycle_times)

    p50 = percentile(sorted_ct, 50)
    p85 = percentile(sorted_ct, 85)
    p95 = percentile(sorted_ct, 95)

    trend, first_half_mean, second_half_mean = detect_trend(cycle_times)

    # SLA recommendations: P85 is a common SLA target (85% of items delivered within this time)
    sla_recommendation = round(p85, 1)
    conservative_sla = round(p95, 1)

    # Coefficient of variation: stdev/mean, indicator of process predictability
    cv = stdev_ct / mean_ct if mean_ct > 0 else 0
    if cv < 0.3:
        predictability = 'high'
    elif cv < 0.6:
        predictability = 'moderate'
    else:
        predictability = 'low'

    result = {
        'sample_size': n,
        'period_label': period_label,
        'statistics': {
            'mean': round(mean_ct, 2),
            'median': round(median_ct, 2),
            'stdev': round(stdev_ct, 2),
            'min': round(min_ct, 2),
            'max': round(max_ct, 2),
            'coefficient_of_variation': round(cv, 3)
        },
        'percentiles': {
            'P50': round(p50, 2),
            'P85': round(p85, 2),
            'P95': round(p95, 2)
        },
        'trend': {
            'direction': trend,
            'first_half_mean': round(first_half_mean, 2) if first_half_mean is not None else None,
            'second_half_mean': round(second_half_mean, 2) if second_half_mean is not None else None,
            'change_pct': round((second_half_mean - first_half_mean) / first_half_mean, 4)
                if first_half_mean and first_half_mean != 0 else None
        },
        'predictability': predictability,
        'sla_recommendations': {
            'standard_sla': sla_recommendation,
            'conservative_sla': conservative_sla,
            'basis': 'P85 for standard (85% on-time), P95 for conservative (95% on-time)'
        },
        'parse_errors': parse_errors if parse_errors else None
    }

    summary_lines = [
        f"Sample: {n} items",
        f"Mean: {round(mean_ct, 2)} {period_label}  |  Median: {round(median_ct, 2)}  |  Stdev: {round(stdev_ct, 2)}",
        f"Range: {round(min_ct, 2)} – {round(max_ct, 2)} {period_label}",
        f"P50: {round(p50, 2)}  |  P85: {round(p85, 2)}  |  P95: {round(p95, 2)} {period_label}",
        f"Predictability: {predictability} (CV: {round(cv, 3)})",
        f"Trend: {trend}",
    ]
    if trend != 'insufficient_data' and first_half_mean is not None:
        direction = "improved" if trend == 'improving' else "degraded" if trend == 'degrading' else "stable"
        summary_lines.append(
            f"  First-half mean: {round(first_half_mean, 2)}  →  Second-half mean: {round(second_half_mean, 2)} ({direction})"
        )
    summary_lines.append(
        f"\nSLA Recommendation: {sla_recommendation} {period_label} (P85) or {conservative_sla} {period_label} (P95)"
    )

    return result, '\n'.join(summary_lines)


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    result, summary = analyze_cycle_times(data)
    format_output(result, summary)


if __name__ == '__main__':
    main()
