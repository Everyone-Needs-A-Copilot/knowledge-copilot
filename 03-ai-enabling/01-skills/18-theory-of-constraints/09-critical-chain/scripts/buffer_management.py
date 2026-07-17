#!/usr/bin/env python3
"""Classify project buffer health using CCPM buffer management rules.

Compares buffer consumption against chain completion to determine zone
(green/yellow/red) and recommend action.

Usage:
    python3 buffer_management.py --file status.json
    echo '{...}' | python3 buffer_management.py --stdin

Input JSON:
{
  "buffer_size": 10,
  "buffer_consumed": 4,
  "chain_completion_pct": 0.5
}

Optional: include "previous_readings" for trend analysis:
{
  "buffer_size": 10,
  "buffer_consumed": 4,
  "chain_completion_pct": 0.5,
  "previous_readings": [
    {"buffer_consumed": 1, "chain_completion_pct": 0.2},
    {"buffer_consumed": 2, "chain_completion_pct": 0.35}
  ]
}

Output: zone classification, trend, recommended action.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, classify_zone, pct


# Zone thresholds: how far ahead of completion % the consumption % is
# Green: consumed_pct <= completion_pct  (buffer is ahead of schedule)
# Yellow: consumed_pct is 0-30 percentage points ahead of completion_pct
# Red: consumed_pct is >30 percentage points ahead of completion_pct
YELLOW_DELTA = 0.20   # consumed exceeds completion by 20pp → yellow
RED_DELTA    = 0.40   # consumed exceeds completion by 40pp → red


ACTIONS = {
    'green': (
        "No action required. Buffer is healthy. Continue executing the plan. "
        "If tasks finish early, immediately start the next task — don't wait."
    ),
    'yellow': (
        "Develop contingency plans now. Identify which remaining tasks are most likely "
        "to cause further buffer erosion. Do not activate contingencies yet, but have "
        "them ready. Increase status check frequency."
    ),
    'red': (
        "Execute contingency plans immediately. Escalate to project sponsor. "
        "Consider scope reduction, resource addition, or parallel execution of "
        "remaining tasks where possible. Replan remaining work with updated estimates."
    )
}


def classify_buffer(buffer_consumed_pct, chain_completion_pct):
    """
    Classify zone by comparing consumption to completion.
    The standard CCPM buffer chart: plot completion (x) vs consumption (y).
    Green zone: y < x (consuming slower than progressing).
    Yellow zone: y between x and x + YELLOW_DELTA.
    Red zone: y > x + RED_DELTA.
    """
    delta = buffer_consumed_pct - chain_completion_pct
    if delta <= YELLOW_DELTA:
        return 'green', delta
    elif delta <= RED_DELTA:
        return 'yellow', delta
    else:
        return 'red', delta


def assess_trend(current_reading, previous_readings):
    """
    Determine if buffer health is improving, stable, or degrading.
    Trend is based on the delta (consumed - completion) over time.
    """
    if not previous_readings or len(previous_readings) < 2:
        return 'insufficient_data'

    def delta(r):
        return r['buffer_consumed_pct'] - r['chain_completion_pct']

    recent = [delta(r) for r in previous_readings[-3:]]
    current_delta = delta(current_reading)
    all_deltas = recent + [current_delta]

    # Compare first half vs second half
    mid = len(all_deltas) // 2
    first_half_avg = sum(all_deltas[:mid]) / mid if mid > 0 else current_delta
    second_half_avg = sum(all_deltas[mid:]) / len(all_deltas[mid:])

    diff = second_half_avg - first_half_avg
    if diff > 0.05:
        return 'degrading'
    elif diff < -0.05:
        return 'improving'
    else:
        return 'stable'


def analyze_buffer(data):
    require_fields(data, ['buffer_size', 'buffer_consumed', 'chain_completion_pct'])

    buffer_size = data['buffer_size']
    buffer_consumed = data['buffer_consumed']
    chain_completion_pct = data['chain_completion_pct']

    if buffer_size <= 0:
        import sys
        print("Error: buffer_size must be > 0", file=sys.stderr)
        sys.exit(1)

    buffer_consumed_pct = buffer_consumed / buffer_size
    buffer_remaining = buffer_size - buffer_consumed
    buffer_remaining_pct = buffer_remaining / buffer_size

    zone, delta = classify_buffer(buffer_consumed_pct, chain_completion_pct)

    # Trend analysis from previous readings if provided
    previous_raw = data.get('previous_readings', [])
    previous_normalized = []
    for r in previous_raw:
        if 'buffer_consumed' in r and 'chain_completion_pct' in r:
            previous_normalized.append({
                'buffer_consumed_pct': r['buffer_consumed'] / buffer_size,
                'chain_completion_pct': r['chain_completion_pct']
            })

    current_reading = {
        'buffer_consumed_pct': buffer_consumed_pct,
        'chain_completion_pct': chain_completion_pct
    }
    trend = assess_trend(current_reading, previous_normalized)

    # Penetration velocity: how fast buffer is being consumed relative to progress
    if chain_completion_pct > 0:
        penetration_velocity = buffer_consumed_pct / chain_completion_pct
    else:
        penetration_velocity = None

    result = {
        'zone': zone,
        'buffer_size': buffer_size,
        'buffer_consumed': buffer_consumed,
        'buffer_consumed_pct': round(buffer_consumed_pct, 4),
        'buffer_remaining': round(buffer_remaining, 2),
        'buffer_remaining_pct': round(buffer_remaining_pct, 4),
        'chain_completion_pct': chain_completion_pct,
        'consumption_vs_completion_delta': round(delta, 4),
        'penetration_velocity': round(penetration_velocity, 3) if penetration_velocity is not None else None,
        'trend': trend,
        'action': ACTIONS[zone],
        'thresholds': {
            'yellow_starts_at_delta': YELLOW_DELTA,
            'red_starts_at_delta': RED_DELTA
        }
    }

    summary_lines = [
        f"Zone: {zone.upper()}",
        f"Buffer Consumed: {pct(buffer_consumed_pct)} of {buffer_size} ({buffer_consumed} units)",
        f"Buffer Remaining: {pct(buffer_remaining_pct)} ({round(buffer_remaining, 2)} units)",
        f"Chain Completion: {pct(chain_completion_pct)}",
        f"Consumption Delta: {'+' if delta > 0 else ''}{pct(delta)} ahead of completion",
        f"Trend: {trend}",
        f"\nAction: {ACTIONS[zone]}"
    ]

    return result, '\n'.join(summary_lines)


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    result, summary = analyze_buffer(data)
    format_output(result, summary)


if __name__ == '__main__':
    main()
