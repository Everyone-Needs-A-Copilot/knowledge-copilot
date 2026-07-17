#!/usr/bin/env python3
"""Apply Little's Law to calculate optimal WIP for a target lead time.

Uses L = lambda * W to find the WIP level that achieves a desired lead time,
or diagnoses why current lead time exceeds the target.

Usage:
    python3 wip_calculator.py --file wip.json
    echo '{...}' | python3 wip_calculator.py --stdin

Input JSON:
{
  "throughput_rate": 5,
  "target_lead_time": 3,
  "current_wip": 25
}

throughput_rate: items completed per period (the drum rate)
target_lead_time: desired average lead time in periods
current_wip: optional — current items in flight

Output: optimal WIP, current vs target, lead time at current WIP, reduction needed.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, classify_zone, pct


def calculate_wip(data):
    require_fields(data, ['throughput_rate', 'target_lead_time'])

    throughput_rate = data['throughput_rate']
    target_lead_time = data['target_lead_time']
    current_wip = data.get('current_wip', None)

    if throughput_rate <= 0:
        print("Error: throughput_rate must be > 0", file=sys.stderr)
        sys.exit(1)
    if target_lead_time <= 0:
        print("Error: target_lead_time must be > 0", file=sys.stderr)
        sys.exit(1)

    # Little's Law: L = lambda * W
    # Optimal WIP = throughput_rate * target_lead_time
    optimal_wip = throughput_rate * target_lead_time

    result = {
        'littles_law': {
            'formula': 'L = lambda × W  (WIP = throughput_rate × lead_time)',
            'throughput_rate': throughput_rate,
            'target_lead_time': target_lead_time
        },
        'optimal_wip': round(optimal_wip, 1),
        'current_analysis': None
    }

    summary_lines = [
        f"Throughput Rate (lambda): {throughput_rate} items/period",
        f"Target Lead Time (W): {target_lead_time} periods",
        f"Optimal WIP (L): {round(optimal_wip, 1)} items",
    ]

    if current_wip is not None:
        # Current lead time implied by Little's Law
        current_lead_time = current_wip / throughput_rate
        lead_time_ratio = current_lead_time / target_lead_time

        # How much WIP needs to change
        wip_delta = current_wip - optimal_wip
        wip_reduction_pct = wip_delta / current_wip if current_wip > 0 else 0

        # Assessment
        if current_lead_time <= target_lead_time * 1.1:
            status = 'on_target'
            note = "WIP is at or near optimal. Lead time target is achievable."
        elif current_lead_time <= target_lead_time * 2.0:
            status = 'above_target'
            note = f"Lead time is {round(lead_time_ratio, 1)}× the target. Reduce WIP by {round(wip_delta, 1)} items to hit target."
        else:
            status = 'significantly_above_target'
            note = f"Lead time is {round(lead_time_ratio, 1)}× the target. Significant WIP reduction required ({round(wip_delta, 1)} items = {pct(wip_reduction_pct)} reduction)."

        result['current_analysis'] = {
            'current_wip': current_wip,
            'current_implied_lead_time': round(current_lead_time, 2),
            'target_lead_time': target_lead_time,
            'lead_time_ratio': round(lead_time_ratio, 3),
            'wip_to_reduce': round(max(0, wip_delta), 1),
            'wip_reduction_pct': round(wip_reduction_pct, 4),
            'status': status,
            'note': note
        }

        summary_lines += [
            f"\nCurrent WIP: {current_wip} items",
            f"Current Implied Lead Time: {round(current_lead_time, 2)} periods ({round(lead_time_ratio, 1)}× target)",
            f"WIP Reduction Needed: {round(max(0, wip_delta), 1)} items ({pct(max(0, wip_reduction_pct))})",
            f"Status: {status}",
            f"\n{note}"
        ]
    else:
        summary_lines.append(
            f"\nTo hit a lead time of {target_lead_time} periods at a throughput of {throughput_rate}/period, "
            f"keep WIP at or below {round(optimal_wip, 1)} items."
        )

    return result, '\n'.join(summary_lines)


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    result, summary = calculate_wip(data)
    format_output(result, summary)


if __name__ == '__main__':
    main()
