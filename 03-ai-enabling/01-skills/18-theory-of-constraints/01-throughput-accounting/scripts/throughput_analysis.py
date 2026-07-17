#!/usr/bin/env python3
"""Analyze revenue streams using Throughput Accounting (T, I, OE).

Takes revenue streams with variable costs and constraint usage,
computes throughput metrics, and ranks by throughput per constraint unit.

Usage:
    python3 throughput_analysis.py --file input.json
    echo '{"revenue_streams": [...], "operating_expenses": 5000}' | python3 throughput_analysis.py --stdin

Input JSON:
{
    "revenue_streams": [
        {
            "name": "Base Plan",
            "revenue": 9900,
            "variable_costs": 379,
            "constraint_units": 100,
            "units_sold": 100
        }
    ],
    "operating_expenses": 5000,
    "investment": 50000
}

Output: JSON with per-stream throughput analysis ranked by T/constraint_unit.
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, currency, pct, rank_by


def analyze_throughput(data):
    require_fields(data, ['revenue_streams', 'operating_expenses'])

    streams = data['revenue_streams']
    oe = data['operating_expenses']
    investment = data.get('investment', 0)

    results = []
    total_throughput = 0

    for stream in streams:
        require_fields(stream, ['name', 'revenue', 'variable_costs'], context=f"stream '{stream.get('name', '?')}'")

        revenue = stream['revenue']
        vc = stream['variable_costs']
        throughput = revenue - vc
        constraint_units = stream.get('constraint_units', 1)
        units_sold = stream.get('units_sold', 1)

        t_per_unit = throughput / units_sold if units_sold > 0 else 0
        t_per_constraint = throughput / constraint_units if constraint_units > 0 else 0

        total_throughput += throughput

        results.append({
            'name': stream['name'],
            'revenue': revenue,
            'variable_costs': vc,
            'throughput': throughput,
            'throughput_per_unit': round(t_per_unit, 2),
            'constraint_units': constraint_units,
            'throughput_per_constraint_unit': round(t_per_constraint, 2),
            'throughput_pct_of_revenue': round(throughput / revenue, 4) if revenue > 0 else 0
        })

    # Rank by throughput per constraint unit (highest first)
    results = rank_by(results, 'throughput_per_constraint_unit')

    net_profit = total_throughput - oe
    roi = (net_profit / investment) if investment > 0 else None
    productivity = (total_throughput / oe) if oe > 0 else None

    output = {
        'summary': {
            'total_throughput': round(total_throughput, 2),
            'operating_expenses': oe,
            'investment': investment,
            'net_profit': round(net_profit, 2),
            'roi': round(roi, 4) if roi is not None else None,
            'productivity_ratio': round(productivity, 4) if productivity is not None else None
        },
        'streams': results,
        'decision_guidance': {
            'highest_throughput_stream': results[0]['name'] if results else None,
            'prioritize': 'Increase throughput by focusing sales/capacity on highest T/CU streams',
            'warning': 'Do NOT use cost-per-unit to evaluate streams. A stream with high variable costs but high T/CU is more valuable than a low-cost stream with low T/CU.'
        }
    }

    summary_lines = [
        f"Total Throughput: {currency(total_throughput)}",
        f"Operating Expenses: {currency(oe)}",
        f"Net Profit (T - OE): {currency(net_profit)}",
    ]
    if roi is not None:
        summary_lines.append(f"ROI ((T-OE)/I): {pct(roi)}")
    summary_lines.append(f"\nStreams ranked by T/constraint unit:")
    for s in results:
        summary_lines.append(f"  #{s['rank']} {s['name']}: T={currency(s['throughput'])}, T/CU={currency(s['throughput_per_constraint_unit'])}")

    return output, '\n'.join(summary_lines)


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    result, summary = analyze_throughput(data)
    format_output(result, summary)


if __name__ == '__main__':
    main()
