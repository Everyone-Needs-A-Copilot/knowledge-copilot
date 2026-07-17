#!/usr/bin/env python3
"""Run all structural CLR (Categories of Legitimate Reservation) checks on cause-effect connections.

Validates each connection for clarity, entity existence, tautology, and causality.
Produces a quality score, per-connection results, and failure summary grouped by CLR type.

The eight CLRs:
  1. Clarity            - entities are unambiguous complete statements
  2. Entity Existence   - both entities are stated (not blank/placeholder)
  3. Causality Existence - rationale is provided for the connection
  4. Cause Insufficiency - (see sufficiency_check.py for deep dive)
  5. Additional Cause   - (requires domain context, flagged as advisory)
  6. Cause-Effect Reversal - (requires domain context, flagged as advisory)
  7. Predicted Effect    - (requires domain context, flagged as advisory)
  8. Tautology          - effect does not merely restate cause

Structural checks (automated): CLR 1, 2, 3, 8
Advisory checks (flagged for human review): CLR 4, 5, 6, 7

Usage:
    python3 clr_full_audit.py --file input.json
    echo '{...}' | python3 clr_full_audit.py --stdin

Input JSON:
{
    "connections": [
        {
            "id": "C01",
            "cause": "The deployment pipeline takes 4 hours to complete",
            "effect": "Engineers delay committing code until end of day",
            "rationale": "A 4-hour pipeline means feedback arrives outside working hours, so engineers batch commits to avoid interruption."
        }
    ]
}

Output: Quality score 0-100, per-connection CLR audit results,
grouped failures by CLR type, most common failure type, and overall assessment.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, rank_by


# Tokens that suggest incomplete or vague statements
VAGUE_TOKENS = {
    'things', 'stuff', 'issues', 'problems', 'something', 'everything',
    'various', 'some', 'many', 'etc', 'etc.', 'and so on'
}

# Very short entity is likely a topic, not a statement
MIN_ENTITY_WORDS = 4


def check_clarity(cause, effect):
    """CLR 1: Both entities must be clear, specific, declarative statements."""
    failures = []

    cause_words = cause.lower().split()
    effect_words = effect.lower().split()

    if len(cause_words) < MIN_ENTITY_WORDS:
        failures.append(
            f"Cause is too short ({len(cause_words)} words) — likely a topic, not a complete statement."
        )

    if len(effect_words) < MIN_ENTITY_WORDS:
        failures.append(
            f"Effect is too short ({len(effect_words)} words) — likely a topic, not a complete statement."
        )

    cause_vague = set(cause_words) & VAGUE_TOKENS
    if cause_vague:
        failures.append(
            f"Cause contains vague language: {', '.join(cause_vague)}. Make it specific."
        )

    effect_vague = set(effect_words) & VAGUE_TOKENS
    if effect_vague:
        failures.append(
            f"Effect contains vague language: {', '.join(effect_vague)}. Make it specific."
        )

    return failures


def check_entity_existence(cause, effect):
    """CLR 2: Both entities must be non-empty, stated conditions."""
    failures = []

    if not cause or not cause.strip():
        failures.append("Cause is empty. Both entities must be stated.")

    if not effect or not effect.strip():
        failures.append("Effect is empty. Both entities must be stated.")

    return failures


def check_causality_existence(rationale):
    """CLR 3: A rationale must be provided explaining the causal mechanism."""
    failures = []

    if not rationale or not rationale.strip():
        failures.append(
            "No rationale provided. A causal mechanism must be explained — "
            "correlation and temporal sequence alone do not establish causation."
        )
    elif len(rationale.strip().split()) < 5:
        failures.append(
            f"Rationale is very short ({len(rationale.strip().split())} words). "
            "Explain the mechanism by which the cause produces the effect."
        )

    return failures


def similarity_score(text_a, text_b):
    """Approximate word-overlap similarity between two strings (Jaccard-like).

    Returns 0.0 to 1.0. Used for tautology detection.
    Does not use external libraries — stdlib only.
    """
    stop_words = {
        'is', 'are', 'the', 'a', 'an', 'and', 'or', 'not', 'in', 'of',
        'to', 'for', 'with', 'that', 'this', 'it', 'we', 'our', 'their',
        'has', 'have', 'been', 'be', 'by', 'at', 'on', 'from', 'as',
        'so', 'which', 'when', 'than', 'more', 'less', 'very', 'too'
    }

    def meaningful_words(text):
        words = text.lower().split()
        return {w.strip('.,;:!?()') for w in words if w.strip('.,;:!?()') not in stop_words and len(w) > 2}

    words_a = meaningful_words(text_a)
    words_b = meaningful_words(text_b)

    if not words_a or not words_b:
        return 0.0

    intersection = words_a & words_b
    union = words_a | words_b

    return len(intersection) / len(union)


def check_tautology(cause, effect):
    """CLR 8: Effect must not merely restate the cause."""
    failures = []

    score = similarity_score(cause, effect)

    if score >= 0.65:
        failures.append(
            f"Possible tautology (similarity {score:.0%}): the effect appears to restate the cause. "
            "Check that the effect is a distinct condition produced by the cause, not a synonym for it."
        )
    elif score >= 0.50:
        failures.append(
            f"High similarity between cause and effect ({score:.0%}). "
            "Verify these are genuinely distinct states, not the same condition restated."
        )

    return failures


def audit_connection(conn):
    """Run all structural CLR checks on a single connection."""
    conn_id = conn.get('id', '?')
    cause = conn.get('cause', '')
    effect = conn.get('effect', '')
    rationale = conn.get('rationale', '')

    clr_results = {}
    all_failures = []

    # CLR 1: Clarity
    clarity_failures = check_clarity(cause, effect)
    clr_results['clr_1_clarity'] = {
        'passed': len(clarity_failures) == 0,
        'failures': clarity_failures
    }
    all_failures.extend([('CLR 1: Clarity', f) for f in clarity_failures])

    # CLR 2: Entity Existence
    entity_failures = check_entity_existence(cause, effect)
    clr_results['clr_2_entity_existence'] = {
        'passed': len(entity_failures) == 0,
        'failures': entity_failures
    }
    all_failures.extend([('CLR 2: Entity Existence', f) for f in entity_failures])

    # CLR 3: Causality Existence
    causality_failures = check_causality_existence(rationale)
    clr_results['clr_3_causality_existence'] = {
        'passed': len(causality_failures) == 0,
        'failures': causality_failures
    }
    all_failures.extend([('CLR 3: Causality Existence', f) for f in causality_failures])

    # CLR 8: Tautology (check before CLRs 4-7 since it is structural)
    tautology_failures = check_tautology(cause, effect)
    clr_results['clr_8_tautology'] = {
        'passed': len(tautology_failures) == 0,
        'failures': tautology_failures
    }
    all_failures.extend([('CLR 8: Tautology', f) for f in tautology_failures])

    # CLRs 4-7 require domain context — flag as advisory
    clr_results['clr_4_cause_insufficiency'] = {
        'passed': None,
        'advisory': (
            'Cannot be checked structurally. Use sufficiency_check.py for a dedicated analysis, '
            'or ask: "Is this cause alone sufficient to produce the effect, '
            'or do additional conditions need to be true?"'
        )
    }
    clr_results['clr_5_additional_cause'] = {
        'passed': None,
        'advisory': (
            'Cannot be checked structurally. Ask: "Could the effect occur through a completely '
            'different path, even if this cause were absent?"'
        )
    }
    clr_results['clr_6_cause_effect_reversal'] = {
        'passed': None,
        'advisory': (
            'Cannot be checked structurally. Ask: "Does A cause B, or does B cause A? '
            'Is there a feedback loop where both are true?"'
        )
    }
    clr_results['clr_7_predicted_effect'] = {
        'passed': None,
        'advisory': (
            'Cannot be checked structurally. Ask: "If this connection is real, what other '
            'secondary effects should we observe? Do we observe them?"'
        )
    }

    structural_checks = ['clr_1_clarity', 'clr_2_entity_existence', 'clr_3_causality_existence', 'clr_8_tautology']
    passed_count = sum(1 for k in structural_checks if clr_results[k]['passed'])
    connection_score = round((passed_count / len(structural_checks)) * 100)

    return {
        'id': conn_id,
        'cause': cause,
        'effect': effect,
        'structural_score': connection_score,
        'structural_checks_passed': passed_count,
        'structural_checks_total': len(structural_checks),
        'clr_results': clr_results,
        'all_structural_failures': [f for (_, f) in all_failures]
    }, all_failures


def run_full_audit(data):
    require_fields(data, ['connections'])
    connections = data['connections']

    if not connections:
        print("Error: connections list must not be empty", file=sys.stderr)
        sys.exit(1)

    for c in connections:
        require_fields(c, ['id', 'cause', 'effect', 'rationale'],
                       context=f"connection '{c.get('id', '?')}'")

    audited = []
    all_failures_by_clr = {}
    total_score = 0

    for conn in connections:
        result, failures = audit_connection(conn)
        audited.append(result)
        total_score += result['structural_score']

        for (clr_type, failure_msg) in failures:
            if clr_type not in all_failures_by_clr:
                all_failures_by_clr[clr_type] = []
            all_failures_by_clr[clr_type].append({
                'connection_id': result['id'],
                'failure': failure_msg
            })

    overall_score = round(total_score / len(audited)) if audited else 0

    # Most common failure type
    most_common_failure = None
    if all_failures_by_clr:
        most_common_failure = max(all_failures_by_clr.keys(), key=lambda k: len(all_failures_by_clr[k]))

    # Overall assessment
    if overall_score >= 90:
        assessment = "Strong — structural CLR checks largely pass. Review advisory CLRs 4-7 with domain knowledge."
    elif overall_score >= 70:
        assessment = "Acceptable — some structural issues. Address failures before treating this tree as reliable."
    elif overall_score >= 50:
        assessment = "Weak — significant structural problems. Major revision recommended before using this logic."
    else:
        assessment = "Poor — fundamental CLR violations throughout. Rebuild connections from clarity checks first."

    output = {
        'overall_score': overall_score,
        'total_connections': len(audited),
        'assessment': assessment,
        'most_common_failure_type': most_common_failure,
        'failures_by_clr_type': all_failures_by_clr,
        'connections': audited,
        'advisory_note': (
            'CLRs 4 (Cause Insufficiency), 5 (Additional Cause), 6 (Cause-Effect Reversal), '
            'and 7 (Predicted Effect) require domain knowledge and cannot be checked structurally. '
            'Review each connection against these CLRs manually using the definitions in SKILL.md.'
        )
    }

    # Summary for stderr
    summary_lines = [
        "CLR Full Audit",
        "=" * 40,
        f"Connections Audited: {len(audited)}",
        f"Overall Quality Score: {overall_score}/100",
        f"Assessment: {assessment}",
    ]
    if most_common_failure:
        failure_count = len(all_failures_by_clr[most_common_failure])
        summary_lines.append(f"Most Common Failure: {most_common_failure} ({failure_count} occurrence(s))")

    summary_lines.append("")
    summary_lines.append("Per-Connection Results:")
    for c in audited:
        status = "PASS" if c['structural_score'] == 100 else "FAIL"
        summary_lines.append(
            f"  [{status}] {c['id']}: {c['structural_score']}/100 structural "
            f"({c['structural_checks_passed']}/{c['structural_checks_total']} checks passed)"
        )
        for f in c['all_structural_failures']:
            summary_lines.append(f"         - {f}")

    if all_failures_by_clr:
        summary_lines.append("")
        summary_lines.append("Failures by CLR Type:")
        for clr_type, failures in sorted(all_failures_by_clr.items()):
            summary_lines.append(f"  {clr_type} ({len(failures)} failure(s)):")
            for f in failures:
                summary_lines.append(f"    [{f['connection_id']}] {f['failure']}")

    return output, '\n'.join(summary_lines)


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    result, summary = run_full_audit(data)
    format_output(result, summary)


if __name__ == '__main__':
    main()
