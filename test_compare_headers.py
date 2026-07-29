"""
test_compare_headers.py
=======================
Unit tests for the compare_headers module.
No external test framework required — plain assertions are used.
Run with:
    python test_compare_headers.py
Or with pytest (auto-discovered because functions are prefixed test_):
    pytest test_compare_headers.py -v
"""

import io
import os
import sys
import tempfile

# Make sure the sibling module is importable when running from any cwd
sys.path.insert(0, os.path.dirname(__file__))
from compare_headers import compare_headers, read_header, main


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _write_tmp(content: str, suffix: str = ".csv") -> str:
    """Write *content* to a temporary file and return its path."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
        fh.write(content)
    return path


# ---------------------------------------------------------------------------
# Test 1 — Identical headers
# ---------------------------------------------------------------------------

def test_identical_headers():
    """Two files with exactly the same headers should have no diffs and
    same_order == True."""
    result = compare_headers(
        ["order_id", "customer_id", "amount"],
        ["order_id", "customer_id", "amount"],
    )
    assert result["only_in_expected"] == [], "Expected no extra headers in expected"
    assert result["only_in_actual"] == [], "Expected no extra headers in actual"
    assert result["common"] == ["order_id", "customer_id", "amount"]
    assert result["same_order"] is True
    print("PASS  test_identical_headers")


# ---------------------------------------------------------------------------
# Test 2 — One header missing from actual
# ---------------------------------------------------------------------------

def test_missing_header_in_actual():
    """When actual is missing a header that expected has, it should appear
    in only_in_expected."""
    result = compare_headers(
        ["order_id", "customer_id", "amount", "status"],
        ["order_id", "customer_id", "status"],
    )
    assert result["only_in_expected"] == ["amount"]
    assert result["only_in_actual"] == []
    assert "amount" not in result["common"]
    print("PASS  test_missing_header_in_actual")


# ---------------------------------------------------------------------------
# Test 3 — Headers with extra surrounding whitespace
# ---------------------------------------------------------------------------

def test_whitespace_trimming():
    """read_header must strip leading/trailing spaces from every token."""
    path = _write_tmp("  order_id ,  customer_id ,  amount  \n1,C001,50.00\n")
    try:
        headers = read_header(path)
        assert headers == ["order_id", "customer_id", "amount"], (
            f"Unexpected headers after trimming: {headers}"
        )
    finally:
        os.unlink(path)
    print("PASS  test_whitespace_trimming")


# ---------------------------------------------------------------------------
# Test 4 — Windows line endings (CRLF)
# ---------------------------------------------------------------------------

def test_windows_line_endings():
    """Files with \\r\\n endings must be parsed correctly."""
    path = _write_tmp("order_id,customer_id,amount\r\n1,C001,50.00\r\n")
    try:
        headers = read_header(path)
        assert headers == ["order_id", "customer_id", "amount"], (
            f"CRLF not stripped correctly: {headers}"
        )
    finally:
        os.unlink(path)
    print("PASS  test_windows_line_endings")


# ---------------------------------------------------------------------------
# Test 5 — Common headers present but in a different order
# ---------------------------------------------------------------------------

def test_different_order():
    """same_order should be False when common headers appear in a different
    relative order between the two files."""
    result = compare_headers(
        ["order_id", "currency", "status"],
        ["status", "currency", "order_id"],
    )
    assert result["only_in_expected"] == []
    assert result["only_in_actual"] == []
    assert set(result["common"]) == {"order_id", "currency", "status"}
    assert result["same_order"] is False
    print("PASS  test_different_order")


# ---------------------------------------------------------------------------
# Test 6 — Empty file raises ValueError
# ---------------------------------------------------------------------------

def test_empty_file_raises():
    """read_header should raise ValueError for a completely empty file."""
    path = _write_tmp("")
    try:
        raised = False
        try:
            read_header(path)
        except ValueError:
            raised = True
        assert raised, "Expected ValueError for empty file"
    finally:
        os.unlink(path)
    print("PASS  test_empty_file_raises")


# ---------------------------------------------------------------------------
# Test 7 — Header row with no valid fields raises ValueError
# ---------------------------------------------------------------------------

def test_blank_header_row_raises():
    """A header row containing only commas/spaces should raise ValueError."""
    path = _write_tmp("  ,  ,  \n1,2,3\n")
    try:
        raised = False
        try:
            read_header(path)
        except ValueError:
            raised = True
        assert raised, "Expected ValueError for blank header row"
    finally:
        os.unlink(path)
    print("PASS  test_blank_header_row_raises")


# ---------------------------------------------------------------------------
# Test 8 — Missing file argument returns exit code 1
# ---------------------------------------------------------------------------

def test_missing_argument_returns_error():
    """main() with fewer than two arguments should return exit code 1."""
    exit_code = main([])
    assert exit_code == 1, f"Expected exit code 1, got {exit_code}"
    exit_code_one_arg = main(["only_one.csv"])
    assert exit_code_one_arg == 1
    print("PASS  test_missing_argument_returns_error")


# ---------------------------------------------------------------------------
# Test 9 — Non-existent file returns exit code 1
# ---------------------------------------------------------------------------

def test_nonexistent_file_returns_error():
    """main() with a path that does not exist should return exit code 1."""
    exit_code = main(["ghost_expected.csv", "ghost_actual.csv"])
    assert exit_code == 1, f"Expected exit code 1, got {exit_code}"
    print("PASS  test_nonexistent_file_returns_error")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        test_identical_headers,
        test_missing_header_in_actual,
        test_whitespace_trimming,
        test_windows_line_endings,
        test_different_order,
        test_empty_file_raises,
        test_blank_header_row_raises,
        test_missing_argument_returns_error,
        test_nonexistent_file_returns_error,
    ]

    failures = []
    for test in tests:
        try:
            test()
        except Exception as exc:
            failures.append((test.__name__, exc))
            print(f"FAIL  {test.__name__}: {exc}")

    print(f"\n{'=' * 40}")
    print(f"Results: {len(tests) - len(failures)}/{len(tests)} passed")
    if failures:
        sys.exit(1)
