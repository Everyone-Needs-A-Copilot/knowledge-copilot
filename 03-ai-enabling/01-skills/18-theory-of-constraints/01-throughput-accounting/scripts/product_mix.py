#!/usr/bin/env python3
"""Determine optimal product/service mix using Goldratt's greedy algorithm.

Ranks products by throughput per constraint unit and fills constraint
capacity from the top. This is the TOC answer to "what should we
build/sell/serve when we can't do everything?"

Usage:
    python3 product_mix.py --file input.json
    echo '...' | python3 product_mix.py --stdin

Input JSON:
{
    "products": [
        {
            "name": "Enterprise",
            "throughput_per_unit": 119,
            "constraint_units_per_unit": 2.5,
            "demand": 100
        }
    ],
    "constraint_capacity": 500,
    "constraint_name": "engineering hours/month"
}
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, currency, rank_by


def optimize_mix(data):
    require_fields(data, ['products', 'constraint_capacity'])

    products = data['products']
    capacity = data['constraint_capacity']
    constraint_name = data.get('constraint_name', 'constraint units')

    # Calculate T/CU for each product
    for p in products:
        require_fields(p, ['name', 'throughput_per_unit', 'constraint_units_per_unit', 'demand'],
                       context=f"product '{p.get('name', '?')}'")
        cu = p['constraint_units_per_unit']
        p['t_per_cu'] = p['throughput_per_unit'] / cu if cu > 0 else 0

    # Sort by T/CU descending (Goldratt's greedy algorithm)
    ranked = rank_by(products, 't_per_cu')

    remaining_capacity = capacity
    total_throughput = 0
    mix = []

    for p in ranked:
        max_units_by_demand = p['demand']
        max_units_by_capacity = remaining_capacity / p['constraint_units_per_unit'] if p['constraint_units_per_unit'] > 0 else float('inf')
        units_produced = min(max_units_by_demand, max_units_by_capacity)
        units_produced = max(0, int(units_produced))

        capacity_used = units_produced * p['constraint_units_per_unit']
        throughput = units_produced * p['throughput_per_unit']

        remaining_capacity -= capacity_used
        total_throughput += throughput

        status = 'full_demand'
        if units_produced == 0:
            status = 'rejected'
        elif units_produced < p['demand']:
            status = 'partial'

        mix.append({
            'rank': p['rank'],
            'name': p['name'],
            'throughput_per_unit': p['throughput_per_unit'],
            't_per_cu': round(p['t_per_cu'], 2),
            'demand': p['demand'],
            'units_produced': units_produced,
            'units_rejected': p['demand'] - units_produced,
            'capacity_used': round(capacity_used, 2),
            'throughput_contribution': round(throughput, 2),
            'status': status
        })

    output = {
        'optimal_mix': mix,
        'totals': {
            'total_throughput': round(total_throughput, 2),
            'capacity_used': round(capacity - remaining_capacity, 2),
            'capacity_remaining': round(remaining_capacity, 2),
            'capacity_utilization': round((capacity - remaining_capacity) / capacity, 4) if capacity > 0 else 0
        },
        'constraint': {
            'name': constraint_name,
            'total_capacity': capacity
        },
        'insight': 'Products are ranked by throughput per constraint unit, NOT by margin or revenue. A product that uses less of the constraint per dollar of throughput should always be prioritized.'
    }

    summary_lines = [
        f"Constraint: {constraint_name} (capacity: {capacity})",
        f"Total Throughput: {currency(total_throughput)}",
        f"Capacity Used: {round(capacity - remaining_capacity, 1)}/{capacity} ({round((capacity - remaining_capacity) / capacity * 100, 1)}%)",
        f"\nOptimal Mix:"
    ]
    for m in mix:
        summary_lines.append(f"  #{m['rank']} {m['name']}: {m['units_produced']}/{m['demand']} units [{m['status']}] T/CU={currency(m['t_per_cu'])}")

    return output, '\n'.join(summary_lines)


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    result, summary = optimize_mix(data)
    format_output(result, summary)


if __name__ == '__main__':
    main()
