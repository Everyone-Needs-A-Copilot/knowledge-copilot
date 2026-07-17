#!/usr/bin/env python3
"""Model the throughput impact of adding headcount.

Calculates fully loaded cost, breakeven timing, and year-1 ROI
to determine if a hire increases system throughput enough to justify
the operating expense increase.

Usage:
    python3 hiring_model.py --file input.json

Input JSON:
{
    "role": "Customer Success Manager",
    "annual_salary": 85000,
    "benefits_pct": 0.25,
    "overhead_pct": 0.10,
    "expected_monthly_throughput_increase": 12000,
    "ramp_months": 3,
    "current_constraint": "customer onboarding capacity"
}
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, currency, pct


def model_hire(data):
    require_fields(data, ['role', 'annual_salary', 'expected_monthly_throughput_increase'])

    role = data['role']
    salary = data['annual_salary']
    benefits_pct = data.get('benefits_pct', 0.25)
    overhead_pct = data.get('overhead_pct', 0.10)
    delta_t = data['expected_monthly_throughput_increase']
    ramp = data.get('ramp_months', 3)
    constraint = data.get('current_constraint', 'unspecified')

    # Fully loaded cost
    benefits = salary * benefits_pct
    overhead = salary * overhead_pct
    fully_loaded_annual = salary + benefits + overhead
    fully_loaded_monthly = fully_loaded_annual / 12

    # 12-month model
    months = []
    cumulative_t = 0
    cumulative_cost = 0

    for month in range(1, 13):
        if month <= ramp:
            month_t = delta_t * (month / ramp)
        else:
            month_t = delta_t

        cumulative_t += month_t
        cumulative_cost += fully_loaded_monthly

        months.append({
            'month': month,
            'throughput_gain': round(month_t, 2),
            'cumulative_throughput': round(cumulative_t, 2),
            'cumulative_cost': round(cumulative_cost, 2),
            'net_position': round(cumulative_t - cumulative_cost, 2)
        })

    # Find breakeven month
    breakeven = None
    for m in months:
        if m['net_position'] >= 0:
            breakeven = m['month']
            break

    year_1_throughput = cumulative_t
    year_1_cost = cumulative_cost
    year_1_net = year_1_throughput - year_1_cost
    year_1_roi = year_1_net / year_1_cost if year_1_cost > 0 else 0

    # Recommendation logic
    if breakeven and breakeven <= 6:
        recommendation = 'hire'
        rationale = f'Breaks even by month {breakeven}. Strong throughput ROI.'
    elif breakeven and breakeven <= 9:
        recommendation = 'hire_with_conditions'
        rationale = f'Breaks even by month {breakeven}. Hire if constraint is validated and ramp assumptions are realistic.'
    elif breakeven and breakeven <= 12:
        recommendation = 'evaluate'
        rationale = f'Breaks even by month {breakeven}. Marginal — consider if the constraint can be exploited first without hiring.'
    else:
        recommendation = 'defer'
        rationale = 'Does not break even within 12 months. Exploit and subordinate before elevating with headcount.'

    # Check if this hire addresses the constraint
    constraint_note = None
    if constraint == 'unspecified':
        constraint_note = 'WARNING: No constraint identified. Hiring without knowing the constraint risks adding OE without increasing T. Use constraint-identification skill first.'

    output = {
        'role': role,
        'cost_analysis': {
            'annual_salary': salary,
            'benefits': round(benefits, 2),
            'overhead': round(overhead, 2),
            'fully_loaded_annual': round(fully_loaded_annual, 2),
            'fully_loaded_monthly': round(fully_loaded_monthly, 2)
        },
        'throughput_analysis': {
            'expected_monthly_increase': delta_t,
            'ramp_months': ramp,
            'year_1_total_throughput': round(year_1_throughput, 2),
            'year_1_total_cost': round(year_1_cost, 2),
            'year_1_net_impact': round(year_1_net, 2),
            'year_1_roi': round(year_1_roi, 4)
        },
        'breakeven_month': breakeven,
        'monthly_detail': months,
        'recommendation': recommendation,
        'rationale': rationale,
        'constraint_addressed': constraint,
        'constraint_warning': constraint_note,
        'toc_checklist': {
            'is_this_the_constraint': 'Have you identified the system constraint? Hiring at a non-constraint adds cost without throughput.',
            'exploited_first': 'Have you maximized output from the constraint without spending money?',
            'subordinated': 'Is everything else already aligned to support the constraint?',
            'elevation_justified': 'Only after exploit and subordinate fail should you elevate (spend money).'
        }
    }

    summary_lines = [
        f"Hiring Analysis: {role}",
        f"  Fully loaded cost: {currency(fully_loaded_monthly)}/mo ({currency(fully_loaded_annual)}/yr)",
        f"  Expected throughput increase: {currency(delta_t)}/mo (after {ramp}mo ramp)",
        f"  Breakeven: {'month ' + str(breakeven) if breakeven else 'not within 12 months'}",
        f"  Year-1 net impact: {currency(year_1_net)}",
        f"  Year-1 ROI: {pct(year_1_roi)}",
        f"  Recommendation: {recommendation.upper()}",
        f"  Constraint: {constraint}"
    ]
    if constraint_note:
        summary_lines.append(f"\n  {constraint_note}")

    return output, '\n'.join(summary_lines)


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    result, summary = model_hire(data)
    format_output(result, summary)


if __name__ == '__main__':
    main()
