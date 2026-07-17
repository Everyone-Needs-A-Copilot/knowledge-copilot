#!/usr/bin/env python3
"""Apply Goldratt's Five Focusing Steps to identify and manage system constraints.

Analyzes system steps using utilization, WIP, and wait time to compute a
composite constraint score. Identifies the constraint and generates
exploit, subordinate, and elevate recommendations.

Composite score: utilization*0.4 + normalized_wip*0.3 + normalized_wait*0.3

Usage:
    python3 five_focusing_steps.py --file input.json
    echo '{...}' | python3 five_focusing_steps.py --stdin

Input JSON:
{
    "system_steps": [
        { "name": "Development", "utilization": 0.91, "wip": 12, "wait_time": 48 },
        { "name": "QA Review",   "utilization": 0.78, "wip": 6,  "wait_time": 16 },
        { "name": "Design",      "utilization": 0.65, "wip": 3,  "wait_time": 4  },
        { "name": "Deployment",  "utilization": 0.45, "wip": 1,  "wait_time": 2  }
    ]
}

Output: Per-step constraint scores, ranked list, identified constraint,
and recommendations for exploit, subordinate, and elevate actions.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, pct, rank_by, classify_zone


def normalize(value, min_val, max_val):
    """Normalize a value to 0-1 range. Returns 0 if all values are equal."""
    if max_val == min_val:
        return 0.0
    return (value - min_val) / (max_val - min_val)


def generate_exploit_recommendations(step_name, utilization, wip, wait_time):
    """Generate free exploitation moves for the identified constraint."""
    recs = []

    if utilization >= 0.90:
        recs.append(
            f"Protect {step_name} from interruptions — at {pct(utilization)} utilization, "
            "every context-switch is pure waste."
        )
    recs.append(
        f"Audit {step_name} for rework and defect handling. Work arriving broken "
        "consumes constraint capacity without producing throughput."
    )
    if wip >= 5:
        recs.append(
            f"Reduce batch size feeding into {step_name}. High WIP ({wip} items) "
            "increases queue variability and average wait."
        )
    recs.append(
        f"Move non-constraint work away from {step_name}. If anything can be done "
        "before or after without loss of quality, do it there."
    )
    recs.append(
        f"Ensure {step_name} is never idle waiting on upstream dependencies. "
        "Buffer one batch of ready work ahead of it at all times."
    )

    return recs


def generate_subordinate_recommendations(constraint_name, all_steps):
    """Generate subordination moves for non-constraint steps."""
    recs = []
    non_constraints = [s for s in all_steps if s['name'] != constraint_name]

    recs.append(
        f"Measure non-constraint steps ({', '.join(s['name'] for s in non_constraints)}) "
        f"on their ability to feed {constraint_name} steadily — not on their own utilization."
    )
    recs.append(
        f"Allow upstream steps to idle rather than build WIP ahead of {constraint_name}. "
        "Excess WIP ahead of the constraint creates queuing delays, not throughput."
    )
    recs.append(
        "Implement a drum-buffer-rope signal: release new work into the system only "
        f"when {constraint_name} has capacity to pull it."
    )
    recs.append(
        "Review incentives on non-constraint teams. If they are rewarded for "
        "utilization or individual output, they will over-produce and flood the constraint."
    )

    return recs


def generate_elevate_recommendations(step_name, utilization):
    """Generate investment-based elevation moves for the constraint."""
    recs = []

    recs.append(
        f"Only elevate {step_name} after exploit and subordinate steps are in place "
        "and the constraint persists. Elevation without exploitation wastes investment."
    )
    recs.append(
        f"Options to increase {step_name} capacity: add headcount, add tooling that "
        "reduces per-unit time, outsource overflow, or redesign the process to remove steps."
    )
    recs.append(
        f"After elevating, repeat Step 1 — the constraint will shift. "
        "Do not let inertia lock in the assumption that {step_name} is still the bottleneck."
    )
    if utilization >= 0.95:
        recs.append(
            f"At {pct(utilization)} utilization, {step_name} has no headroom for variability. "
            "Even modest demand spikes will cause exponential queue growth. Elevation is urgent."
        )

    return recs


def analyze_five_focusing_steps(data):
    require_fields(data, ['system_steps'])
    steps = data['system_steps']

    if not steps:
        print("Error: system_steps must contain at least one step", file=sys.stderr)
        sys.exit(1)

    for step in steps:
        require_fields(step, ['name', 'utilization', 'wip', 'wait_time'],
                       context=f"step '{step.get('name', '?')}'")

    # Compute normalization ranges
    wip_values = [s['wip'] for s in steps]
    wait_values = [s['wait_time'] for s in steps]
    wip_min, wip_max = min(wip_values), max(wip_values)
    wait_min, wait_max = min(wait_values), max(wait_values)

    scored = []
    for step in steps:
        util = float(step['utilization'])
        wip = step['wip']
        wait = step['wait_time']

        norm_wip = normalize(wip, wip_min, wip_max)
        norm_wait = normalize(wait, wait_min, wait_max)
        score = round(util * 0.4 + norm_wip * 0.3 + norm_wait * 0.3, 4)

        scored.append({
            'name': step['name'],
            'utilization': util,
            'utilization_pct': pct(util),
            'wip': wip,
            'wait_time_hours': wait,
            'normalized_wip': round(norm_wip, 4),
            'normalized_wait': round(norm_wait, 4),
            'constraint_score': score,
            'zone': classify_zone(util, 0.70, 0.90)
        })

    ranked = rank_by(scored, 'constraint_score')
    constraint = ranked[0]

    exploit_recs = generate_exploit_recommendations(
        constraint['name'], constraint['utilization'],
        constraint['wip'], constraint['wait_time_hours']
    )
    subordinate_recs = generate_subordinate_recommendations(constraint['name'], ranked)
    elevate_recs = generate_elevate_recommendations(
        constraint['name'], constraint['utilization']
    )

    result = {
        'identified_constraint': {
            'name': constraint['name'],
            'constraint_score': constraint['constraint_score'],
            'utilization': constraint['utilization_pct'],
            'wip': constraint['wip'],
            'wait_time_hours': constraint['wait_time_hours'],
            'zone': constraint['zone']
        },
        'all_steps_ranked': ranked,
        'five_focusing_steps': {
            'step_1_identify': {
                'constraint': constraint['name'],
                'basis': (
                    f"Highest composite score ({constraint['constraint_score']}) "
                    f"from utilization ({constraint['utilization_pct']}), "
                    f"WIP ({constraint['wip']}), and wait time ({constraint['wait_time_hours']}h)."
                )
            },
            'step_2_exploit': {
                'description': 'Maximize output from the constraint without spending money.',
                'recommendations': exploit_recs
            },
            'step_3_subordinate': {
                'description': 'Align all other steps to serve the constraint, not their own efficiency.',
                'recommendations': subordinate_recs
            },
            'step_4_elevate': {
                'description': 'Only after exploiting and subordinating: invest to increase constraint capacity.',
                'recommendations': elevate_recs
            },
            'step_5_repeat': {
                'description': (
                    f"After resolving {constraint['name']}, return to Step 1. "
                    "The constraint will shift. Do not assume the same bottleneck persists."
                )
            }
        }
    }

    summary_lines = [
        "Five Focusing Steps Analysis",
        "=" * 40,
        f"Identified Constraint: {constraint['name']}",
        f"  Score:       {constraint['constraint_score']}",
        f"  Utilization: {constraint['utilization_pct']}",
        f"  WIP:         {constraint['wip']} items",
        f"  Wait Time:   {constraint['wait_time_hours']}h",
        "",
        "All Steps (ranked by constraint score):",
    ]
    for s in ranked:
        indicator = " <-- CONSTRAINT" if s['rank'] == 1 else ""
        summary_lines.append(
            f"  #{s['rank']} {s['name']}: score={s['constraint_score']}, "
            f"util={s['utilization_pct']}, wip={s['wip']}{indicator}"
        )
    summary_lines.append("")
    summary_lines.append(f"Step 2 - Exploit ({len(exploit_recs)} recommendations):")
    for rec in exploit_recs:
        summary_lines.append(f"  - {rec}")
    summary_lines.append("")
    summary_lines.append(f"Step 3 - Subordinate ({len(subordinate_recs)} recommendations):")
    for rec in subordinate_recs:
        summary_lines.append(f"  - {rec}")

    return result, '\n'.join(summary_lines)


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    result, summary = analyze_five_focusing_steps(data)
    format_output(result, summary)


if __name__ == '__main__':
    main()
