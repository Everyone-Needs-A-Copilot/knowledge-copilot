#!/usr/bin/env python3
"""Compare investment options through the Throughput Accounting lens.

Evaluates options by their impact on T, I, and OE — prioritizing
throughput increase over cost reduction (the opposite of cost accounting).

Usage:
    python3 investment_decision.py --file input.json

Input JSON:
{
    "options": [
        {
            "name": "Hire senior engineer",
            "cost": 180000,
            "delta_throughput_monthly": 15000,
            "delta_investment": 5000,
            "delta_operating_expense_monthly": 18000,
            "ramp_months": 3
        }
    ],
    "evaluation_horizon_months": 12
}
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, currency, pct, rank_by


def evaluate_investments(data):
    require_fields(data, ['options'])
    horizon = data.get('evaluation_horizon_months', 12)

    results = []
    for opt in data['options']:
        require_fields(opt, ['name', 'cost'], context=f"option '{opt.get('name', '?')}'")

        name = opt['name']
        cost = opt['cost']
        delta_t = opt.get('delta_throughput_monthly', 0)
        delta_i = opt.get('delta_investment', 0)
        delta_oe = opt.get('delta_operating_expense_monthly', 0)
        ramp = opt.get('ramp_months', 0)

        # Throughput gained over horizon (accounting for ramp)
        productive_months = max(0, horizon - ramp)
        ramp_t = sum(delta_t * (m / ramp) for m in range(1, ramp + 1)) if ramp > 0 else 0
        total_t_gain = ramp_t + (delta_t * productive_months)

        # Total cost over horizon
        total_oe_increase = delta_oe * horizon
        total_cost = cost + delta_i + total_oe_increase

        # Net impact
        net_impact = total_t_gain - total_cost

        # Payback: month where cumulative T gain exceeds cumulative cost
        payback_month = None
        cumulative_t = 0
        cumulative_cost = cost + delta_i
        for month in range(1, horizon + 1):
            if month <= ramp:
                cumulative_t += delta_t * (month / ramp) if ramp > 0 else delta_t
            else:
                cumulative_t += delta_t
            cumulative_cost += delta_oe
            if cumulative_t >= cumulative_cost and payback_month is None:
                payback_month = month

        roi = net_impact / total_cost if total_cost > 0 else None

        results.append({
            'name': name,
            'upfront_cost': cost,
            'delta_throughput_monthly': delta_t,
            'delta_oe_monthly': delta_oe,
            'total_throughput_gain': round(total_t_gain, 2),
            'total_cost': round(total_cost, 2),
            'net_impact': round(net_impact, 2),
            'roi': round(roi, 4) if roi is not None else None,
            'payback_month': payback_month,
            'recommendation': 'invest' if net_impact > 0 else 'defer'
        })

    # Rank by delta_throughput_monthly FIRST (Goldratt's priority), then by ROI
    results = rank_by(results, 'delta_throughput_monthly')

    output = {
        'options': results,
        'evaluation_horizon_months': horizon,
        'decision_framework': {
            'priority_1': 'Highest throughput increase (T has no ceiling)',
            'priority_2': 'Highest ROI (efficiency of capital)',
            'priority_3': 'Lowest OE increase (but never at expense of T)',
            'warning': 'Cost-cutting options that reduce T should be rejected even if they improve short-term profit.'
        }
    }

    summary_lines = [
        f"Investment Analysis ({horizon}-month horizon)",
        f"\nOptions ranked by throughput impact:"
    ]
    for r in results:
        payback_str = f"month {r['payback_month']}" if r['payback_month'] else "never"
        summary_lines.append(
            f"  #{r['rank']} {r['name']}: +{currency(r['delta_throughput_monthly'])}/mo T, "
            f"net {currency(r['net_impact'])}, payback: {payback_str} [{r['recommendation'].upper()}]"
        )

    return output, '\n'.join(summary_lines)


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    result, summary = evaluate_investments(data)
    format_output(result, summary)


if __name__ == '__main__':
    main()
