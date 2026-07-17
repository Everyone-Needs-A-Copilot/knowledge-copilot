#!/usr/bin/env python3
"""Generate replenishment signals for a set of items using TOC buffer zones.

Calculates days of supply and zone for each item, generates action signals,
and sorts by urgency for daily operational review.

Usage:
    python3 replenishment_signal.py --file inventory.json
    echo '{...}' | python3 replenishment_signal.py --stdin

Input JSON:
{
  "items": [
    {
      "name": "Widget A",
      "buffer_target": 100,
      "current_level": 28,
      "avg_daily_consumption": 8
    },
    {
      "name": "Widget B",
      "buffer_target": 50,
      "current_level": 42,
      "avg_daily_consumption": 3
    }
  ]
}

Output: per-item signals (urgent/replenish/hold/reduce), sorted by urgency.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, classify_zone, pct


# Signal priority order (lower number = higher urgency)
SIGNAL_PRIORITY = {
    'urgent': 0,
    'replenish': 1,
    'hold': 2,
    'reduce': 3
}

SIGNAL_DESCRIPTIONS = {
    'urgent':   'EXPEDITE: Red zone with <3 days supply. Replenish immediately.',
    'replenish': 'ORDER: Yellow zone. Place standard replenishment order.',
    'hold':     'HOLD: Green zone. Buffer is healthy. No action required.',
    'reduce':   'REDUCE: Significantly above buffer target. Delay next replenishment.'
}


def determine_signal(remaining_pct, days_of_supply, current_level, buffer_target):
    """Determine replenishment signal based on zone and days of supply."""
    # Reduce: significantly above buffer target
    if current_level > buffer_target * 1.5:
        return 'reduce'

    # Classify zone: higher remaining is better (green > 66%, red < 33%)
    zone = classify_zone(remaining_pct, 0.66, 0.33)

    if zone == 'red':
        if days_of_supply < 3:
            return 'urgent'
        else:
            return 'replenish'  # red but not immediately critical
    elif zone == 'yellow':
        return 'replenish'
    else:
        return 'hold'


def analyze_replenishment(data):
    require_fields(data, ['items'])
    items = data['items']

    if not items:
        print("Error: items must not be empty", file=sys.stderr)
        sys.exit(1)

    results = []

    for item in items:
        require_fields(item, ['name', 'buffer_target', 'current_level', 'avg_daily_consumption'],
                       context=f"item '{item.get('name', '?')}'")

        name = item['name']
        buffer_target = item['buffer_target']
        current_level = item['current_level']
        avg_consumption = item['avg_daily_consumption']

        if buffer_target <= 0:
            print(f"Warning: '{name}' buffer_target must be > 0, skipping", file=sys.stderr)
            continue

        remaining_pct = current_level / buffer_target if buffer_target > 0 else 0
        days_of_supply = current_level / avg_consumption if avg_consumption > 0 else float('inf')

        zone = classify_zone(remaining_pct, 0.66, 0.33)
        signal = determine_signal(remaining_pct, days_of_supply, current_level, buffer_target)

        replenish_qty = max(0, buffer_target - current_level)
        pct_of_target = current_level / buffer_target

        results.append({
            'name': name,
            'signal': signal,
            'signal_description': SIGNAL_DESCRIPTIONS[signal],
            'zone': zone,
            'buffer_target': buffer_target,
            'current_level': current_level,
            'remaining_pct': round(remaining_pct, 4),
            'pct_of_target': round(pct_of_target, 4),
            'days_of_supply': round(days_of_supply, 1) if days_of_supply != float('inf') else None,
            'avg_daily_consumption': avg_consumption,
            'replenish_qty': round(replenish_qty, 2)
        })

    # Sort by urgency: urgent first, then replenish, then hold, then reduce
    # Within same signal: sort by days_of_supply ascending (most critical first)
    def sort_key(item):
        priority = SIGNAL_PRIORITY.get(item['signal'], 99)
        dos = item['days_of_supply'] if item['days_of_supply'] is not None else 9999
        return (priority, dos)

    results.sort(key=sort_key)

    # Summary counts
    signal_counts = {s: 0 for s in SIGNAL_PRIORITY}
    for r in results:
        signal_counts[r['signal']] = signal_counts.get(r['signal'], 0) + 1

    output = {
        'summary': {
            'total_items': len(results),
            'urgent': signal_counts.get('urgent', 0),
            'replenish': signal_counts.get('replenish', 0),
            'hold': signal_counts.get('hold', 0),
            'reduce': signal_counts.get('reduce', 0)
        },
        'items': results
    }

    summary_lines = [
        f"Replenishment Review: {len(results)} items",
        f"  URGENT:    {signal_counts.get('urgent', 0)} items",
        f"  REPLENISH: {signal_counts.get('replenish', 0)} items",
        f"  HOLD:      {signal_counts.get('hold', 0)} items",
        f"  REDUCE:    {signal_counts.get('reduce', 0)} items",
    ]

    urgent_items = [r for r in results if r['signal'] == 'urgent']
    if urgent_items:
        summary_lines.append(f"\nUrgent Items:")
        for item in urgent_items:
            dos_str = f"{item['days_of_supply']} days" if item['days_of_supply'] is not None else "N/A"
            summary_lines.append(
                f"  {item['name']}: {item['current_level']} / {item['buffer_target']} "
                f"({pct(item['remaining_pct'])}) — {dos_str} supply"
            )

    replenish_items = [r for r in results if r['signal'] == 'replenish']
    if replenish_items:
        summary_lines.append(f"\nReplenish Items:")
        for item in replenish_items:
            summary_lines.append(
                f"  {item['name']}: order {item['replenish_qty']} units "
                f"(currently {pct(item['remaining_pct'])} of buffer)"
            )

    return output, '\n'.join(summary_lines)


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    result, summary = analyze_replenishment(data)
    format_output(result, summary)


if __name__ == '__main__':
    main()
