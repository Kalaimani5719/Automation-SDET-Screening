"""
compare_headers.py
==================
Compare the header rows of two CSV files without relying on any CSV
parsing library.

Usage:
    python compare_headers.py <expected_csv> <actual_csv>

Exit codes:
    0  — headers are identical
    1  — headers differ (or a usage/file error occurred)
"""

import sys
import os


# ---------------------------------------------------------------------------
# Core logic (pure functions — easy to unit-test independently)
# ---------------------------------------------------------------------------

def read_header(filepath: str) -> list[str]:
    """
    Open *filepath*, read the first line, strip the newline, split on
    commas, and trim whitespace from every field.

    Raises:
        FileNotFoundError  — path does not exist
        ValueError         — file is empty or header contains no valid fields
    """
    with open(filepath, encoding="utf-8", newline="") as fh:
        first_line = fh.readline()

    # readline() returns "" only at true EOF (empty file)
    if not first_line:
        raise ValueError(f"File is empty: {filepath}")

    # Strip universal line endings before splitting
    first_line = first_line.rstrip("\r\n")

    headers = [h.strip() for h in first_line.split(",")]

    # Reject a row that is entirely blank/whitespace tokens
    valid = [h for h in headers if h]
    if not valid:
        raise ValueError(f"Header row has no valid fields in: {filepath}")

    return headers


def compare_headers(expected: list[str], actual: list[str]) -> dict:
    """
    Return a dict with four keys:

    only_in_expected : list[str]   — headers present only in *expected*
    only_in_actual   : list[str]   — headers present only in *actual*
    common           : list[str]   — headers present in both (order from expected)
    same_order       : bool        — True when common headers appear in the same
                                     relative order in both lists
    """
    expected_set = set(expected)
    actual_set = set(actual)

    only_in_expected = [h for h in expected if h not in actual_set]
    only_in_actual = [h for h in actual if h not in expected_set]
    common = [h for h in expected if h in actual_set]

    # Relative order: extract common headers from each list preserving
    # their original positions, then check whether the two sequences match.
    common_in_expected_order = [h for h in expected if h in actual_set]
    common_in_actual_order = [h for h in actual if h in expected_set]
    same_order = common_in_expected_order == common_in_actual_order

    return {
        "only_in_expected": only_in_expected,
        "only_in_actual": only_in_actual,
        "common": common,
        "same_order": same_order,
    }


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def _bullet_list(items: list[str]) -> str:
    return "\n".join(f"  {item}" for item in items) if items else "  (none)"


def print_report(
    expected_path: str,
    actual_path: str,
    result: dict,
) -> None:
    """Print a human-readable comparison report to stdout."""
    exp_name = os.path.basename(expected_path)
    act_name = os.path.basename(actual_path)

    print(f"\nOnly in {exp_name}:")
    print(_bullet_list(result["only_in_expected"]))

    print(f"\nOnly in {act_name}:")
    print(_bullet_list(result["only_in_actual"]))

    print("\nCommon headers:")
    print(_bullet_list(result["common"]))

    print("\nCommon headers in same relative order:")
    print(f"  {'true' if result['same_order'] else 'false'}")
    print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]

    # --- Coding Task 3: error handling ---

    # 1. Missing argument(s)
    if len(args) < 2:
        print(
            "Error: two CSV file paths are required.\n"
            "Usage: python compare_headers.py <expected_csv> <actual_csv>",
            file=sys.stderr,
        )
        return 1

    expected_path, actual_path = args[0], args[1]

    # 2. File does not exist
    for path in (expected_path, actual_path):
        if not os.path.exists(path):
            print(f"Error: file not found: {path}", file=sys.stderr)
            return 1

    # 3 & 4. Empty file / header row with no valid fields
    try:
        expected_headers = read_header(expected_path)
        actual_headers = read_header(actual_path)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    result = compare_headers(expected_headers, actual_headers)
    print_report(expected_path, actual_path, result)

    # Exit 0 when headers are identical, 1 when they differ
    headers_identical = (
        not result["only_in_expected"]
        and not result["only_in_actual"]
        and result["same_order"]
    )
    return 0 if headers_identical else 1


if __name__ == "__main__":
    sys.exit(main())
