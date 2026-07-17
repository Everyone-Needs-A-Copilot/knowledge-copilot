#!/usr/bin/env python3
"""Classify and rank constraints by type and business impact.

Accepts a list of identified constraints with type, evidence, and impact scores.
Classifies by Goldratt's constraint types, ranks by impact, and prominently flags
policy constraints — the most common and most overlooked type in knowledge work.

Usage:
    python3 constraint_assessment.py --file input.json
    echo '{...}' | python3 constraint_assessment.py --stdin

Input JSON:
{
    "constraints": [
        {
            "description": "All production deploys require VP approval",
            "type": "policy",
            "evidence": "Average 3-day delay between code-complete and production",
            "impact_score": 9
        },
        {
            "description": "Single QA engineer for 8 developers",
            "type": "physical",
            "evidence": "QA queue averages 14 items, 5-day average wait",
            "impact_score": 8
        }
    ]
}

Valid types: physical, policy, market, knowledge, time

Output: Ranked constraint list, type classification summary, policy constraint
prominence flag, and a warning if no policy constraints are identified.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, rank_by

VALID_TYPES = {'physical', 'policy', 'market', 'knowledge', 'time'}

TYPE_DESCRIPTIONS = {
    'physical': 'Physical resource with limited capacity (person, machine, tool, space).',
    'policy': 'Rule, habit, metric, or decision process that limits throughput artificially.',
    'market': 'Insufficient demand — the market will not absorb more output.',
    'knowledge': 'Missing expertise, skill, or information required to proceed.',
    'time': 'Deadline or duration that limits options regardless of other resources.'
}

TYPE_EXPLOIT_HINTS = {
    'physical': (
        'Protect from non-constraint work. Eliminate rework and defects feeding into it. '
        'Cross-train one other person as backup.'
    ),
    'policy': (
        'Challenge whether the policy still serves its original purpose. '
        'Most policy constraints were sensible rules that outlived their context. '
        'Ask: "What would have to be true for us to remove this policy safely?"'
    ),
    'market': (
        'Improving internal capacity will not help. Focus on marketing, sales, or '
        'product-market fit. This is a demand problem, not a flow problem.'
    ),
    'knowledge': (
        'Document what the knowledge-holder knows. Pair them with others. '
        'Invest in training or hire someone who already has the knowledge.'
    ),
    'time': (
        'Identify which time constraint is externally fixed vs internally assumed. '
        'Many time constraints are policy constraints in disguise.'
    )
}

POLICY_WARNING = (
    "Policy constraints are the most common in knowledge work — are you sure none exist? "
    "Look for: approval gates, handoff requirements, batch-size rules, metric-driven "
    "behaviors, and 'the way we've always done it' decisions."
)


def classify_constraint(constraint, rank):
    """Enrich a constraint dict with classification metadata."""
    ctype = constraint.get('type', '').lower().strip()

    if ctype not in VALID_TYPES:
        print(
            f"Warning: constraint '{constraint.get('description', '?')}' has unknown type "
            f"'{ctype}'. Valid types: {', '.join(sorted(VALID_TYPES))}",
            file=sys.stderr
        )
        ctype = 'physical'  # default fallback

    return {
        'rank': rank,
        'description': constraint['description'],
        'type': ctype,
        'type_description': TYPE_DESCRIPTIONS[ctype],
        'evidence': constraint['evidence'],
        'impact_score': constraint['impact_score'],
        'exploit_hint': TYPE_EXPLOIT_HINTS[ctype],
        'is_policy': ctype == 'policy'
    }


def build_type_summary(classified):
    """Count constraints by type and compute average impact per type."""
    by_type = {}
    for c in classified:
        t = c['type']
        if t not in by_type:
            by_type[t] = {'count': 0, 'total_impact': 0, 'items': []}
        by_type[t]['count'] += 1
        by_type[t]['total_impact'] += c['impact_score']
        by_type[t]['items'].append(c['description'])

    summary = []
    for t, data in sorted(by_type.items()):
        avg = data['total_impact'] / data['count']
        summary.append({
            'type': t,
            'count': data['count'],
            'average_impact': round(avg, 1),
            'descriptions': data['items']
        })

    return summary


def assess_constraints(data):
    require_fields(data, ['constraints'])
    constraints = data['constraints']

    if not constraints:
        print("Error: constraints list must not be empty", file=sys.stderr)
        sys.exit(1)

    for c in constraints:
        require_fields(
            c, ['description', 'type', 'evidence', 'impact_score'],
            context=f"constraint '{c.get('description', '?')}'"
        )

    # Rank by impact_score descending
    ranked_raw = rank_by(
        [dict(c) for c in constraints],
        'impact_score'
    )

    classified = [classify_constraint(c, c['rank']) for c in ranked_raw]

    policy_constraints = [c for c in classified if c['type'] == 'policy']
    policy_count = len(policy_constraints)
    type_summary = build_type_summary(classified)

    no_policy_warning = None
    if policy_count == 0:
        no_policy_warning = POLICY_WARNING

    # Priority constraint
    top = classified[0] if classified else None

    result = {
        'priority_constraint': top,
        'all_constraints_ranked': classified,
        'classification_summary': {
            'total_constraints': len(classified),
            'by_type': type_summary,
            'policy_constraint_count': policy_count,
            'policy_prominence': (
                'HIGH — policy constraints dominate. These are your highest-leverage targets.'
                if policy_count >= len(classified) / 2
                else 'LOW — few policy constraints identified. Consider whether policies are being overlooked.'
                if policy_count == 0
                else f'PRESENT — {policy_count} policy constraint(s) identified alongside other types.'
            )
        },
        'warnings': {
            'no_policy_constraints': no_policy_warning
        }
    }

    summary_lines = [
        "Constraint Assessment",
        "=" * 40,
        f"Total Constraints Analyzed: {len(classified)}",
        f"Policy Constraints Found:   {policy_count}",
    ]
    if no_policy_warning:
        summary_lines.append("")
        summary_lines.append(f"WARNING: {no_policy_warning}")

    summary_lines.append("")
    summary_lines.append("Ranked by Impact Score:")
    for c in classified:
        policy_marker = " *" if c['type'] == 'policy' else ""
        summary_lines.append(
            f"  #{c['rank']} [{c['type'].upper()}{policy_marker}] (impact {c['impact_score']}/10) "
            f"{c['description']}"
        )
        summary_lines.append(f"     Evidence: {c['evidence']}")

    summary_lines.append("")
    summary_lines.append("Type Distribution:")
    for t in type_summary:
        summary_lines.append(
            f"  {t['type']}: {t['count']} constraint(s), avg impact {t['average_impact']}"
        )

    if policy_constraints:
        summary_lines.append("")
        summary_lines.append("Policy Constraints (most overlooked, highest leverage):")
        for c in policy_constraints:
            summary_lines.append(f"  - {c['description']}")
            summary_lines.append(f"    Hint: {c['exploit_hint']}")

    return result, '\n'.join(summary_lines)


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    result, summary = assess_constraints(data)
    format_output(result, summary)


if __name__ == '__main__':
    main()
