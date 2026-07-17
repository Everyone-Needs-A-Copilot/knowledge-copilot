#!/usr/bin/env python3
"""Deep-dive analysis on CLR 4: Cause Insufficiency.

Evaluates whether a stated cause is sufficient on its own to produce the stated
effect, or whether additional co-causes (connected by AND) are required.

This is the most commonly violated CLR in business reasoning. Most strategic
claims rest on a single cause that actually requires several co-causes to
produce the stated effect.

Usage:
    python3 sufficiency_check.py --file input.json
    echo '{...}' | python3 sufficiency_check.py --stdin

Input JSON:
{
    "cause": "We increase the marketing budget by 50%",
    "effect": "New customer acquisition doubles",
    "supporting_causes": [
        "The website conversion rate is sufficient to handle increased traffic",
        "The sales team has capacity to follow up on new leads"
    ]
}

The supporting_causes field is optional. When provided, the script evaluates
whether those causes are necessary co-causes or if the primary cause is
sufficient alone.

Output: Sufficiency verdict, potential missing co-causes, AND-connector
recommendation, and next steps.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields


# Domain pattern library: common co-cause categories for frequent effect types
# Maps effect signal words to categories of co-causes to consider
COCAUSE_PATTERNS = [
    {
        'signal_words': ['revenue', 'sales', 'customers', 'acquisition', 'growth', 'arr', 'mrr'],
        'category': 'Demand conversion',
        'co_cause_questions': [
            'Is there a channel or mechanism that converts the cause into demand?',
            'Is the sales/conversion process capable of handling increased volume?',
            'Is the product positioned and priced to capture the demand created?'
        ]
    },
    {
        'signal_words': ['deliver', 'throughput', 'output', 'faster', 'speed', 'velocity', 'cycle time'],
        'category': 'Delivery system capacity',
        'co_cause_questions': [
            'Does the downstream system have capacity to absorb increased flow?',
            'Are there approval gates or handoffs that will become the new bottleneck?',
            'Is quality maintained as throughput increases?'
        ]
    },
    {
        'signal_words': ['morale', 'engagement', 'retention', 'satisfaction', 'happy', 'motivated'],
        'category': 'Human system dynamics',
        'co_cause_questions': [
            'Are there other factors currently suppressing the effect that this cause does not address?',
            'Is the cause visible and meaningful to the people whose behavior would need to change?',
            'Are there systemic issues that would counteract the improvement?'
        ]
    },
    {
        'signal_words': ['quality', 'defects', 'bugs', 'errors', 'reliability', 'uptime'],
        'category': 'Quality system inputs',
        'co_cause_questions': [
            'Does the cause address the root source of defects, or only detection?',
            'Are there upstream inputs that produce defects regardless of this change?',
            'Do teams have the skills and tools to act on the improvement?'
        ]
    },
    {
        'signal_words': ['cost', 'expense', 'spend', 'budget', 'savings', 'reduce'],
        'category': 'Cost system dependencies',
        'co_cause_questions': [
            'Are there fixed costs that will not change regardless of this action?',
            'Are there behavioral responses (Jevons paradox, rebound effects) that could offset savings?',
            'Are there second-order costs created by the action that are not accounted for?'
        ]
    }
]

# Universal co-cause questions applied to every connection
UNIVERSAL_COCAUSE_QUESTIONS = [
    'Is the cause implemented correctly and completely? Partial implementation often produces no effect.',
    'Are there external conditions (market, environment, competition) that must also hold for the effect to occur?',
    'Is there a time delay between cause and effect that could mask the connection?',
    'Are there opposing forces that would cancel the effect of this cause?'
]


def detect_domain_patterns(effect_text):
    """Find relevant co-cause categories based on words in the effect statement."""
    effect_lower = effect_text.lower()
    matched = []

    for pattern in COCAUSE_PATTERNS:
        for word in pattern['signal_words']:
            if word in effect_lower:
                matched.append(pattern)
                break

    return matched


def assess_supporting_causes(cause, effect, supporting_causes):
    """Evaluate whether supporting causes are necessary or sufficient."""
    if not supporting_causes:
        return [], []

    necessary_candidates = []
    possibly_redundant = []

    for sc in supporting_causes:
        sc_lower = sc.lower()
        cause_lower = cause.lower()
        effect_lower = effect.lower()

        # Check if supporting cause is just restating the main cause
        cause_words = set(cause_lower.split())
        sc_words = set(sc_lower.split())
        overlap = len(cause_words & sc_words) / max(len(sc_words), 1)

        if overlap > 0.6:
            possibly_redundant.append({
                'supporting_cause': sc,
                'note': 'High overlap with primary cause — may be a restatement rather than an independent co-cause.'
            })
        else:
            necessary_candidates.append({
                'supporting_cause': sc,
                'assessment': (
                    'Appears to be a distinct contributing condition. '
                    'Verify: if this condition were absent, would the effect still occur from the primary cause alone?'
                )
            })

    return necessary_candidates, possibly_redundant


def check_sufficiency(data):
    require_fields(data, ['cause', 'effect'])

    cause = data['cause'].strip()
    effect = data['effect'].strip()
    supporting_causes = data.get('supporting_causes', [])

    if not cause:
        print("Error: cause must be a non-empty statement", file=sys.stderr)
        sys.exit(1)

    if not effect:
        print("Error: effect must be a non-empty statement", file=sys.stderr)
        sys.exit(1)

    # Detect domain patterns
    matched_patterns = detect_domain_patterns(effect)

    # Build domain-specific co-cause questions
    domain_questions = []
    for pattern in matched_patterns:
        domain_questions.append({
            'category': pattern['category'],
            'questions': pattern['co_cause_questions']
        })

    # Assess supporting causes if provided
    necessary_candidates, possibly_redundant = assess_supporting_causes(
        cause, effect, supporting_causes
    )

    # Determine sufficiency verdict
    # A cause is presumed insufficient if:
    # - No supporting causes are provided (likely oversimplified)
    # - Domain patterns suggest obvious co-causes
    # - The effect is complex (many words imply multiple conditions)
    has_supporting = len(supporting_causes) > 0
    has_domain_signals = len(matched_patterns) > 0
    effect_complexity = len(effect.split()) > 8

    if has_supporting and len(necessary_candidates) > 0:
        verdict = 'insufficient'
        verdict_rationale = (
            f"The stated cause requires {len(necessary_candidates)} identified co-cause(s) to produce the effect. "
            "Use AND-connectors in your thinking process tree to show all necessary conditions."
        )
    elif not has_supporting and (has_domain_signals or effect_complexity):
        verdict = 'likely_insufficient'
        verdict_rationale = (
            "The cause appears insufficient based on the complexity of the effect and domain patterns. "
            "Identify co-causes by working through the questions below before using this connection in a tree."
        )
    else:
        verdict = 'possibly_sufficient'
        verdict_rationale = (
            "No obvious co-causes detected structurally. However, CLR 4 cannot be fully verified without "
            "domain knowledge. Confirm by asking: 'If only this cause were true, and nothing else changed, "
            "would the effect necessarily occur?'"
        )

    # AND-connector recommendation
    if verdict in ('insufficient', 'likely_insufficient'):
        and_connector_rec = (
            "Use an AND-connector (ellipse) in your TOC tree to show that the primary cause AND "
            "the identified co-causes are ALL necessary to produce the effect. "
            "A connection without an AND-connector implies the single cause is sufficient."
        )
    else:
        and_connector_rec = (
            "A single arrow may be appropriate if domain review confirms no co-causes are required. "
            "Document your reasoning in the rationale field."
        )

    output = {
        'cause': cause,
        'effect': effect,
        'verdict': verdict,
        'verdict_rationale': verdict_rationale,
        'and_connector_recommendation': and_connector_rec,
        'supporting_causes_provided': len(supporting_causes),
        'necessary_co_causes': necessary_candidates,
        'possibly_redundant_supporting_causes': possibly_redundant,
        'domain_co_cause_questions': domain_questions,
        'universal_co_cause_questions': UNIVERSAL_COCAUSE_QUESTIONS,
        'next_steps': _build_next_steps(verdict, necessary_candidates, domain_questions)
    }

    summary_lines = [
        "Cause Insufficiency Check (CLR 4)",
        "=" * 40,
        f"Cause:   {cause}",
        f"Effect:  {effect}",
        "",
        f"Verdict: {verdict.upper()}",
        f"Rationale: {verdict_rationale}",
        "",
        f"AND-Connector: {and_connector_rec}",
    ]

    if necessary_candidates:
        summary_lines.append("")
        summary_lines.append("Identified Co-Causes (all are necessary for the effect):")
        for nc in necessary_candidates:
            summary_lines.append(f"  - {nc['supporting_cause']}")
            summary_lines.append(f"    {nc['assessment']}")

    if possibly_redundant:
        summary_lines.append("")
        summary_lines.append("Possibly Redundant Supporting Causes:")
        for pr in possibly_redundant:
            summary_lines.append(f"  - {pr['supporting_cause']}")
            summary_lines.append(f"    {pr['note']}")

    if domain_questions:
        summary_lines.append("")
        summary_lines.append("Domain Co-Cause Questions to Investigate:")
        for dq in domain_questions:
            summary_lines.append(f"  [{dq['category']}]")
            for q in dq['questions']:
                summary_lines.append(f"    ? {q}")

    summary_lines.append("")
    summary_lines.append("Universal Co-Cause Questions (apply to every connection):")
    for q in UNIVERSAL_COCAUSE_QUESTIONS:
        summary_lines.append(f"  ? {q}")

    return output, '\n'.join(summary_lines)


def _build_next_steps(verdict, necessary_candidates, domain_questions):
    steps = []

    if verdict == 'insufficient':
        steps.append(
            "Update your TOC tree to use AND-connectors showing all necessary co-causes."
        )
        steps.append(
            "Verify each co-cause is truly necessary by asking: "
            "'If this co-cause were absent, could the effect still occur from the other causes?'"
        )

    if verdict == 'likely_insufficient':
        steps.append(
            "Work through the domain co-cause questions to identify missing conditions."
        )
        steps.append(
            "Add identified co-causes to the input and re-run this check."
        )

    if domain_questions:
        steps.append(
            "Review domain co-cause questions above and document which conditions are truly necessary."
        )

    steps.append(
        "Run clr_full_audit.py on your complete tree after addressing cause insufficiency."
    )

    return steps


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    result, summary = check_sufficiency(data)
    format_output(result, summary)


if __name__ == '__main__':
    main()
