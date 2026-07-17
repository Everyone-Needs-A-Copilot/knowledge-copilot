#!/usr/bin/env python3
"""Build and validate a Transition Tree (TrT) for cause-effect action planning.

Takes a sequence of steps (each with current_reality, action, expected_effect,
rationale) and validates chain continuity, rationale completeness, and logical
structure. Flags gaps where expected_effect doesn't connect to the next
current_reality.

Usage:
    python3 trt_builder.py --file input.json
    python3 trt_builder.py --stdin
    python3 trt_builder.py '{"steps": [...]}'

Input JSON:
{
    "steps": [
        {
            "id": "S1",
            "current_reality": "We have no public pricing page; prospects must contact sales to learn pricing",
            "action": "Publish a transparent pricing page with three tiers and monthly/annual toggle",
            "expected_effect": "Prospects can self-serve pricing information without contacting sales",
            "rationale": "Support ticket analysis shows 34% of pre-sale contacts are pricing questions. Removing this friction reduces sales team load and accelerates prospect decision-making."
        },
        {
            "id": "S2",
            "current_reality": "Prospects can self-serve pricing information without contacting sales",
            "action": "Add a 14-day free trial CTA on the pricing page for the mid-tier plan",
            "expected_effect": "Prospects who understand pricing can begin a trial without sales involvement",
            "rationale": "Self-served prospects who can compare tiers are more likely to self-qualify. Adding a direct trial path captures this intent at the moment of highest purchase intent."
        }
    ]
}

Output: Validated chain, gap analysis, completeness score, flagged steps.
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields


# Minimum rationale length to be considered substantive (characters)
RATIONALE_MIN_LENGTH = 40

# Minimum word overlap ratio to consider a chain transition "connected"
CONTINUITY_THRESHOLD = 0.15


def normalize_text(text):
    """Lowercase and split text into a set of meaningful words.

    Strips common stop words so overlap reflects meaningful content.
    """
    stop_words = {
        'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
        'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
        'will', 'would', 'could', 'should', 'may', 'might', 'can',
        'this', 'that', 'these', 'those', 'we', 'our', 'their', 'its',
        'not', 'no', 'so', 'as', 'if', 'it', 'they', 'them', 'from'
    }
    words = text.lower().replace(',', ' ').replace('.', ' ').replace(';', ' ').split()
    return {w for w in words if w not in stop_words and len(w) > 2}


def continuity_score(effect_text, next_reality_text):
    """Compute a simple word-overlap ratio between two text fields.

    Returns float between 0.0 (no overlap) and 1.0 (identical content).
    This is a heuristic — the human analyst must interpret flagged gaps.
    """
    effect_words = normalize_text(effect_text)
    reality_words = normalize_text(next_reality_text)

    if not effect_words or not reality_words:
        return 0.0

    overlap = len(effect_words & reality_words)
    union = len(effect_words | reality_words)
    return overlap / union if union > 0 else 0.0


def score_rationale(rationale_text):
    """Score the strength of a rationale field.

    Returns 'strong', 'weak', or 'missing'.
    Criteria:
        - missing: empty or whitespace only
        - weak: present but very short (< RATIONALE_MIN_LENGTH chars)
        - strong: substantive (>= RATIONALE_MIN_LENGTH chars)
    """
    if not rationale_text or not rationale_text.strip():
        return 'missing'
    if len(rationale_text.strip()) < RATIONALE_MIN_LENGTH:
        return 'weak'
    return 'strong'


def validate_step_fields(step, index):
    """Validate that a step has all required fields and they are non-empty strings.

    Returns list of error strings.
    """
    errors = []
    required = ['id', 'current_reality', 'action', 'expected_effect', 'rationale']
    for field in required:
        if field not in step:
            errors.append(f"Step {index + 1}: missing required field '{field}'")
        elif not isinstance(step[field], str):
            errors.append(f"Step {index + 1} ({step.get('id', '?')}): field '{field}' must be a string")
        elif field != 'rationale' and not step[field].strip():
            errors.append(f"Step {index + 1} ({step.get('id', '?')}): field '{field}' must not be empty")
    return errors


def check_for_duplicate_ids(steps):
    """Return list of duplicate IDs found in the steps list."""
    seen = {}
    duplicates = []
    for step in steps:
        sid = step.get('id', '')
        if sid in seen:
            duplicates.append(sid)
        seen[sid] = True
    return duplicates


def analyze_chain(steps):
    """Analyze chain continuity across all consecutive step pairs.

    Returns list of gap analysis dicts, one per transition.
    """
    gaps = []
    for i in range(len(steps) - 1):
        current = steps[i]
        next_step = steps[i + 1]

        effect = current.get('expected_effect', '')
        next_reality = next_step.get('current_reality', '')

        score = continuity_score(effect, next_reality)
        is_gap = score < CONTINUITY_THRESHOLD

        # Check for exact or near-exact match (best case)
        is_strong = score >= 0.4

        gaps.append({
            'from_step': current.get('id', f'step_{i + 1}'),
            'to_step': next_step.get('id', f'step_{i + 2}'),
            'transition_index': i + 1,
            'overlap_score': round(score, 3),
            'continuity': 'strong' if is_strong else ('weak' if not is_gap else 'gap'),
            'flagged': is_gap,
            'from_expected_effect': effect,
            'to_current_reality': next_reality
        })

    return gaps


def build_trt(data):
    require_fields(data, ['steps'])

    steps = data['steps']

    if not isinstance(steps, list) or len(steps) == 0:
        print("Error: 'steps' must be a non-empty list", file=sys.stderr)
        sys.exit(1)

    # Validate all steps
    validation_errors = []
    for i, step in enumerate(steps):
        validation_errors.extend(validate_step_fields(step, i))

    # Check for duplicate IDs
    duplicate_ids = check_for_duplicate_ids(steps)
    if duplicate_ids:
        for dup in duplicate_ids:
            validation_errors.append(f"Duplicate step ID: '{dup}'")

    if validation_errors:
        # Report validation errors but continue analysis where possible
        print("Validation errors:", file=sys.stderr)
        for e in validation_errors:
            print(f"  ! {e}", file=sys.stderr)

    # Analyze each step
    step_analysis = []
    rationale_scores = {'strong': 0, 'weak': 0, 'missing': 0}

    for i, step in enumerate(steps):
        rat_score = score_rationale(step.get('rationale', ''))
        rationale_scores[rat_score] += 1

        step_analysis.append({
            'id': step.get('id', f'step_{i + 1}'),
            'position': i + 1,
            'current_reality': step.get('current_reality', ''),
            'action': step.get('action', ''),
            'expected_effect': step.get('expected_effect', ''),
            'rationale': step.get('rationale', ''),
            'rationale_score': rat_score,
            'flagged': rat_score in ('weak', 'missing')
        })

    # Analyze chain continuity
    gap_analysis = analyze_chain(steps)

    # Identify flagged steps (weak rationale or part of a gap)
    gap_step_ids = set()
    for gap in gap_analysis:
        if gap['flagged']:
            gap_step_ids.add(gap['from_step'])
            gap_step_ids.add(gap['to_step'])

    for step in step_analysis:
        if step['id'] in gap_step_ids:
            step['flagged'] = True

    # Completeness score: percentage of steps with strong rationale
    total_steps = len(steps)
    strong_count = rationale_scores['strong']
    completeness_score = round(strong_count / total_steps, 3) if total_steps > 0 else 0.0

    # Classify overall chain health
    gap_count = sum(1 for g in gap_analysis if g['flagged'])
    weak_rationale_count = rationale_scores['weak'] + rationale_scores['missing']
    flagged_step_ids = [s['id'] for s in step_analysis if s['flagged']]

    if gap_count == 0 and weak_rationale_count == 0:
        chain_health = 'healthy'
    elif gap_count == 0 and weak_rationale_count <= 1:
        chain_health = 'good'
    elif gap_count <= 1 and weak_rationale_count <= 2:
        chain_health = 'needs_review'
    else:
        chain_health = 'significant_gaps'

    result = {
        'summary': {
            'total_steps': total_steps,
            'completeness_score': completeness_score,
            'chain_health': chain_health,
            'gaps_found': gap_count,
            'weak_rationale_count': weak_rationale_count,
            'missing_rationale_count': rationale_scores['missing'],
            'flagged_steps': flagged_step_ids,
            'validation_errors': validation_errors
        },
        'steps': step_analysis,
        'gap_analysis': gap_analysis,
        'rationale_summary': {
            'strong': rationale_scores['strong'],
            'weak': rationale_scores['weak'],
            'missing': rationale_scores['missing']
        }
    }

    # Human summary
    health_labels = {
        'healthy': 'Healthy — chain is complete and well-reasoned',
        'good': 'Good — minor rationale gaps, no chain breaks',
        'needs_review': 'Needs review — some gaps or weak rationale detected',
        'significant_gaps': 'Significant gaps — chain has breaks that need attention'
    }

    lines = [
        f"Transition Tree: {total_steps} step(s)",
        f"Chain health: {health_labels[chain_health]}",
        f"Completeness score: {int(completeness_score * 100)}% of steps have strong rationale",
        ""
    ]

    if gap_count > 0:
        lines.append(f"Chain gaps detected ({gap_count}):")
        for gap in gap_analysis:
            if gap['flagged']:
                lines.append(f"  ! Gap between {gap['from_step']} → {gap['to_step']} (overlap: {gap['overlap_score']})")
                lines.append(f"    Effect:  \"{gap['from_expected_effect'][:80]}{'...' if len(gap['from_expected_effect']) > 80 else ''}\"")
                lines.append(f"    Reality: \"{gap['to_current_reality'][:80]}{'...' if len(gap['to_current_reality']) > 80 else ''}\"")
        lines.append("")

    if weak_rationale_count > 0:
        lines.append(f"Weak or missing rationale ({weak_rationale_count} step(s)):")
        for step in step_analysis:
            if step['rationale_score'] in ('weak', 'missing'):
                lines.append(f"  ! [{step['id']}] rationale is {step['rationale_score']}: \"{step['action'][:60]}{'...' if len(step['action']) > 60 else ''}\"")
        lines.append("")

    if validation_errors:
        lines.append(f"Validation errors ({len(validation_errors)}):")
        for e in validation_errors:
            lines.append(f"  ! {e}")
        lines.append("")

    if chain_health == 'healthy':
        lines.append("No issues found. Chain is complete and every step is well-reasoned.")

    return result, '\n'.join(lines)


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    result, summary = build_trt(data)
    format_output(result, summary)


if __name__ == '__main__':
    main()
