#!/usr/bin/env python3
"""Size distribution buffers using TOC pull-based methodology.

Calculates buffer size from consumption rate, lead time, and variability.
Defines zone thresholds and classifies current level if provided.

Usage:
    python3 buffer_sizing.py --file sizing.json
    echo '{...}' | python3 buffer_sizing.py --stdin

Input JSON:
{
  "avg_daily_consumption": 10,
  "replenishment_lead_time_days": 5,
  "variability_factor": 1.5,
  "current_level": 35
}

variability_factor: 1.0 = low variability, 2.0 = high. Default 1.5.
current_level: optional. If provided, current zone is returned.

Output: buffer size, zone thresholds, current zone.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, classify_zone, pct


def size_buffer(data):
    require_fields(data, ['avg_daily_consumption', 'replenishment_lead_time_days'])

    avg_consumption = data['avg_daily_consumption']
    lead_time = data['replenishment_lead_time_days']
    variability_factor = data.get('variability_factor', 1.5)
    current_level = data.get('current_level', None)

    if avg_consumption <= 0:
        print("Error: avg_daily_consumption must be > 0", file=sys.stderr)
        sys.exit(1)
    if lead_time <= 0:
        print("Error: replenishment_lead_time_days must be > 0", file=sys.stderr)
        sys.exit(1)
    if not (1.0 <= variability_factor <= 3.0):
        print(f"Warning: variability_factor {variability_factor} is outside typical range 1.0-2.0", file=sys.stderr)

    # Buffer = consumption * lead_time * variability_factor
    buffer_size = avg_consumption * lead_time * variability_factor

    # Zone thresholds: green > 66%, yellow 33-66%, red < 33%
    green_threshold = buffer_size * 0.66
    yellow_threshold = buffer_size * 0.33

    # Days of supply at each threshold
    days_at_green = green_threshold / avg_consumption
    days_at_yellow = yellow_threshold / avg_consumption
    days_at_buffer = buffer_size / avg_consumption  # = lead_time * variability_factor

    result = {
        'buffer_size': round(buffer_size, 2),
        'inputs': {
            'avg_daily_consumption': avg_consumption,
            'replenishment_lead_time_days': lead_time,
            'variability_factor': variability_factor
        },
        'formula': 'buffer = consumption × lead_time × variability_factor',
        'zones': {
            'green_above': round(green_threshold, 2),
            'yellow_between': [round(yellow_threshold, 2), round(green_threshold, 2)],
            'red_below': round(yellow_threshold, 2)
        },
        'days_of_supply_at_thresholds': {
            'full_buffer': round(days_at_buffer, 1),
            'green_boundary': round(days_at_green, 1),
            'yellow_boundary': round(days_at_yellow, 1)
        },
        'current_status': None
    }

    summary_lines = [
        f"Buffer Size: {round(buffer_size, 2)} units",
        f"  = {avg_consumption} units/day × {lead_time} days × {variability_factor} variability",
        f"  = {round(days_at_buffer, 1)} days of supply",
        f"\nZone Thresholds:",
        f"  Green: above {round(green_threshold, 2)} units ({round(days_at_green, 1)} days supply)",
        f"  Yellow: {round(yellow_threshold, 2)} – {round(green_threshold, 2)} units",
        f"  Red: below {round(yellow_threshold, 2)} units ({round(days_at_yellow, 1)} days supply)",
    ]

    if current_level is not None:
        remaining_pct = current_level / buffer_size if buffer_size > 0 else 0
        # classify_zone: higher is better (buffer remaining)
        zone = classify_zone(remaining_pct, 0.66, 0.33)
        days_remaining = current_level / avg_consumption

        result['current_status'] = {
            'current_level': current_level,
            'remaining_pct': round(remaining_pct, 4),
            'days_of_supply': round(days_remaining, 1),
            'zone': zone,
            'units_to_replenish_to_full': round(max(0, buffer_size - current_level), 2)
        }

        summary_lines += [
            f"\nCurrent Level: {current_level} units",
            f"  Remaining: {pct(remaining_pct)} of buffer ({round(days_remaining, 1)} days supply)",
            f"  Zone: {zone.upper()}",
            f"  Units to refill: {round(max(0, buffer_size - current_level), 2)}"
        ]

    return result, '\n'.join(summary_lines)


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    result, summary = size_buffer(data)
    format_output(result, summary)


if __name__ == '__main__':
    main()
