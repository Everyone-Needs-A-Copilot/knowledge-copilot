#!/usr/bin/env python3
"""Calculate Drum-Buffer-Rope parameters for a production/flow process.

Auto-identifies the constraint (lowest capacity step) if not marked,
computes drum rate, buffer size, rope release rate, and WIP limits.

Usage:
    python3 drum_buffer_rope.py --file process.json
    echo '{...}' | python3 drum_buffer_rope.py --stdin

Input JSON:
{
  "process_steps": [
    {
      "name": "Development",
      "capacity_per_period": 10
    },
    {
      "name": "Code Review",
      "capacity_per_period": 4,
      "is_constraint": true
    },
    {
      "name": "Testing",
      "capacity_per_period": 7
    }
  ],
  "variability_factor": 1.5,
  "demand_per_period": 8
}

variability_factor: 1.0 = no variability, 2.0 = high variability. Default 1.5.
demand_per_period: optional, used to calculate utilization vs demand.

Output: drum identification, buffer size, rope rate, max WIP, per-step utilization.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, classify_zone, pct


def analyze_dbr(data):
    require_fields(data, ['process_steps'])
    steps = data['process_steps']
    if not steps:
        import sys
        print("Error: process_steps must not be empty", file=sys.stderr)
        sys.exit(1)

    for s in steps:
        require_fields(s, ['name', 'capacity_per_period'], context=f"step '{s.get('name', '?')}'")

    variability_factor = data.get('variability_factor', 1.5)
    demand_per_period = data.get('demand_per_period', None)

    # Identify constraint: lowest capacity, or first explicitly marked
    explicit_constraints = [s for s in steps if s.get('is_constraint')]
    if explicit_constraints:
        constraint = explicit_constraints[0]
    else:
        constraint = min(steps, key=lambda s: s['capacity_per_period'])

    drum_rate = constraint['capacity_per_period']

    # Buffer size: time buffer = variability_factor * (average lead time to constraint)
    # Lead time to constraint = number of steps before it / drum_rate (simplified)
    constraint_idx = next(i for i, s in enumerate(steps) if s['name'] == constraint['name'])
    steps_before_constraint = constraint_idx  # 0-indexed count of steps before

    # Average processing time per step before constraint
    if steps_before_constraint > 0:
        upstream_steps = steps[:constraint_idx]
        avg_upstream_capacity = sum(s['capacity_per_period'] for s in upstream_steps) / len(upstream_steps)
        # Time to process one unit through upstream = steps / capacity (simplified)
        lead_time_to_constraint = steps_before_constraint / avg_upstream_capacity
    else:
        lead_time_to_constraint = 1.0 / drum_rate  # single processing step estimate

    buffer_size = round(variability_factor * lead_time_to_constraint, 2)

    # Rope rate = drum rate (release no faster than the drum can process)
    rope_rate = drum_rate

    # Max WIP via Little's Law: L = lambda * W
    # Throughput = drum_rate, lead_time = total steps / drum_rate (rough system lead time)
    system_lead_time = len(steps) / drum_rate
    max_wip = round(drum_rate * system_lead_time, 1)

    # Per-step utilization at drum rate
    step_results = []
    for s in steps:
        utilization = drum_rate / s['capacity_per_period']
        is_constraint = s['name'] == constraint['name']
        # For utilization: green < 80%, yellow 80-95%, red > 95%
        zone = classify_zone(utilization, 0.80, 0.95)
        step_results.append({
            'name': s['name'],
            'capacity_per_period': s['capacity_per_period'],
            'utilization_at_drum_rate': round(utilization, 4),
            'utilization_zone': zone,
            'is_constraint': is_constraint,
            'spare_capacity_pct': round(max(0, 1 - utilization), 4)
        })

    # Demand analysis
    demand_analysis = None
    if demand_per_period is not None:
        demand_vs_drum = demand_per_period / drum_rate
        if demand_per_period <= drum_rate:
            demand_status = 'feasible'
            demand_note = f"System can meet demand. Drum has {round((drum_rate - demand_per_period) / drum_rate * 100, 1)}% spare capacity."
        else:
            demand_status = 'exceeds_capacity'
            demand_note = f"Demand exceeds drum rate by {round(demand_per_period - drum_rate, 2)} units/period. Throughput will be capped at {drum_rate}."
        demand_analysis = {
            'demand_per_period': demand_per_period,
            'drum_rate': drum_rate,
            'demand_vs_drum_ratio': round(demand_vs_drum, 4),
            'status': demand_status,
            'note': demand_note
        }

    result = {
        'drum': {
            'step_name': constraint['name'],
            'rate': drum_rate,
            'identified_by': 'explicit' if explicit_constraints else 'auto (lowest capacity)'
        },
        'buffer': {
            'size': buffer_size,
            'variability_factor_used': variability_factor,
            'lead_time_to_constraint': round(lead_time_to_constraint, 3),
            'placement': f"Time buffer in front of '{constraint['name']}'"
        },
        'rope': {
            'release_rate': rope_rate,
            'description': 'Release new work at drum rate only — do not release faster'
        },
        'wip': {
            'max_wip': max_wip,
            'system_lead_time_estimate': round(system_lead_time, 2),
            'basis': "Little's Law: L = drum_rate × system_lead_time"
        },
        'process_steps': step_results,
        'demand_analysis': demand_analysis
    }

    summary_lines = [
        f"Drum (Constraint): {constraint['name']} @ {drum_rate} units/period",
        f"Buffer Size: {buffer_size} periods (variability factor: {variability_factor}×)",
        f"Rope Release Rate: {rope_rate} units/period (= drum rate)",
        f"Max WIP: {max_wip} items",
        f"\nStep Utilization at Drum Rate:",
    ]
    for s in step_results:
        marker = " ← DRUM" if s['is_constraint'] else ""
        summary_lines.append(
            f"  {s['name']}: {pct(s['utilization_at_drum_rate'])} [{s['utilization_zone']}]{marker}"
        )
    if demand_analysis:
        summary_lines.append(f"\nDemand: {demand_analysis['note']}")

    return result, '\n'.join(summary_lines)


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    result, summary = analyze_dbr(data)
    format_output(result, summary)


if __name__ == '__main__':
    main()
