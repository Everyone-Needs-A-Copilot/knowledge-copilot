"""
Shared utilities for Theory of Constraints skills.

Provides input parsing, output formatting, validation helpers,
and zone classification used across all TOC scripts.

Usage in scripts:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
    from toc_common import parse_input, format_output, classify_zone
"""

import json
import sys


def parse_input(argv=None):
    """Parse input from --file, --stdin, or positional JSON argument.

    Returns parsed dict/list from JSON input.

    Usage:
        data = parse_input()           # auto-detect from sys.argv
        data = parse_input(sys.argv)   # explicit argv
    """
    if argv is None:
        argv = sys.argv[1:]

    if '--help' in argv or '-h' in argv:
        return None

    # --file path.json
    if '--file' in argv:
        idx = argv.index('--file')
        if idx + 1 >= len(argv):
            print("Error: --file requires a path argument", file=sys.stderr)
            sys.exit(1)
        filepath = argv[idx + 1]
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: file not found: {filepath}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON in {filepath}: {e}", file=sys.stderr)
            sys.exit(1)

    # --stdin
    if '--stdin' in argv:
        try:
            return json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON on stdin: {e}", file=sys.stderr)
            sys.exit(1)

    # Positional: first arg is JSON string
    if argv:
        try:
            return json.loads(argv[0])
        except json.JSONDecodeError:
            # Try treating it as a file path
            try:
                with open(argv[0], 'r') as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                print(f"Error: argument is neither valid JSON nor a readable file: {argv[0]}", file=sys.stderr)
                sys.exit(1)

    # Try stdin if it's not a terminal
    if not sys.stdin.isatty():
        try:
            return json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON on stdin: {e}", file=sys.stderr)
            sys.exit(1)

    return None


def format_output(result, summary=None):
    """Print JSON result to stdout with optional human-readable summary.

    Args:
        result: dict or list to serialize as JSON
        summary: optional string summary printed after JSON (to stderr so JSON stays clean on stdout)
    """
    print(json.dumps(result, indent=2))
    if summary:
        print(f"\n{summary}", file=sys.stderr)


def require_fields(data, fields, context="input"):
    """Validate that required fields exist in data dict.

    Args:
        data: dict to validate
        fields: list of required field names
        context: label for error messages

    Returns data if valid, exits with error if not.
    """
    if not isinstance(data, dict):
        print(f"Error: {context} must be a JSON object, got {type(data).__name__}", file=sys.stderr)
        sys.exit(1)

    missing = [f for f in fields if f not in data]
    if missing:
        print(f"Error: {context} missing required fields: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    return data


def classify_zone(value, green_threshold, red_threshold):
    """Classify a value into green/yellow/red zones.

    Args:
        value: numeric value to classify
        green_threshold: boundary between green and yellow
        red_threshold: boundary between yellow and red

    If green_threshold > red_threshold: green is ABOVE green_threshold (e.g., buffer remaining)
    If green_threshold < red_threshold: green is BELOW green_threshold (e.g., utilization)
    """
    if green_threshold > red_threshold:
        # Higher is better (e.g., buffer remaining: >66% green, <33% red)
        if value >= green_threshold:
            return "green"
        elif value <= red_threshold:
            return "red"
        else:
            return "yellow"
    else:
        # Lower is better (e.g., utilization: <70% green, >90% red)
        if value <= green_threshold:
            return "green"
        elif value >= red_threshold:
            return "red"
        else:
            return "yellow"


def currency(value):
    """Format a number as currency string."""
    if value < 0:
        return f"-${abs(value):,.2f}"
    return f"${value:,.2f}"


def pct(value):
    """Format a decimal as percentage string."""
    return f"{value * 100:.1f}%"


def rank_by(items, key, reverse=True):
    """Sort items by a key function, return with rank numbers.

    Args:
        items: list of dicts
        key: string key name or callable
        reverse: True for descending (default)

    Returns list of dicts with 'rank' field added.
    """
    if isinstance(key, str):
        key_name = key
        key = lambda x: x.get(key_name, 0)

    sorted_items = sorted(items, key=key, reverse=reverse)
    for i, item in enumerate(sorted_items):
        item['rank'] = i + 1
    return sorted_items
