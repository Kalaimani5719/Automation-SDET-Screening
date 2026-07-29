# Demo — QA Exercise

## 1. Language Used

- **Python 3.11+**
- Libraries: `playwright` (API testing), `pytest` (test runner)

---

## 2. How to Run the CSV Comparison Tool

### Setup
```bash
pip install playwright
```

### Run
```bash
cd tests/demo
python compare_headers.py expected_orders.csv actual_orders.csv
```

### Expected Output
```
Only in expected_orders.csv:
  amount
  created_at
  country

Only in actual_orders.csv:
  total_amount
  processed_at
  country_code

Common headers:
  order_id
  customer_id
  currency
  status

Common headers in same relative order:
  true
```

---

## 3. How to Run the Tests

### CSV Header Comparison Tests
```bash
cd tests/demo

# Plain Python runner
python test_compare_headers.py

# Or with pytest
pytest test_compare_headers.py -v
```

### API Tests
```bash
cd tests/demo

# Plain Python runner
python test_orders_api.py

# Or with pytest
pytest test_orders_api.py -v
```

---

## 4. SQL Answers

File: `tests/mysql.sql`

| Task | Approach | Key SQL |
|------|----------|---------|
| Task 1 — Price Changes | `INNER JOIN` on `product_id`, filter where `price` differs | `WHERE y.price <> t.price OR (NULL guards)` |
| Task 2 — New Products | `LEFT JOIN` anti-join from today → yesterday | `WHERE y.product_id IS NULL` |
| Task 3 — Missing Products | `LEFT JOIN` anti-join from yesterday → today | `WHERE t.product_id IS NULL` |
| Task 4 — Status Changes | `INNER JOIN` on `product_id`, filter where `status` differs | `WHERE y.status <> t.status OR (NULL guards)` |

**Task 5 — Explanations**

1. **JOIN strategy**: `INNER JOIN` for change detection (product must exist in both snapshots). `LEFT JOIN` anti-join for new/missing (asymmetric presence — rows absent on one side).

2. **Non-unique `product_id`**: A join on a non-unique key produces a Cartesian product of all matching rows, inflating results with false positives. Fix with a deduplication CTE, `DISTINCT`, or a `UNIQUE` constraint.

3. **NULL in `price`/`status`**: Standard `<>` returns `UNKNOWN` when either side is `NULL`, silently dropping real changes. Fix: use explicit `OR IS NULL` guards, MySQL's null-safe `<=>` operator, or standard SQL's `IS DISTINCT FROM`.

---

## 5. API Test Cases

Endpoint: `GET /api/orders/{order_id}`

| # | Test Name | Input | Expected Result | Why Useful |
|---|-----------|-------|-----------------|------------|
| 1 | Valid order returns 200 + body | `GET /api/orders/ORD-1001` | HTTP 200, JSON with all fields | Confirms happy path and response contract |
| 2 | Unknown order returns 404 | `GET /api/orders/ORD-9999` | HTTP 404 | Validates error handling for missing orders |
| 3 | Response body field types | `GET /api/orders/ORD-1001` | `amount` is float, `order_id` is string, `created_at` is ISO-8601 | Catches silent schema drift |
| 4 | Invalid order ID format → 400 | `GET /api/orders/INVALID##ID` | HTTP 400 | Ensures malformed input is rejected cleanly |
| 5 | Status is a known enum value | `GET /api/orders/ORD-1001` | `status` in `{PAID, PENDING, CANCELLED, REFUNDED}` | Guards against unexpected back-end changes |

**Automated test (Task 2):** Uses Playwright's `sync_api.APIRequestContext` — no browser required, no mocking. Replace `BASE_URL` in `test_orders_api.py` with the actual server before running.

---

## 6. Assumptions

- CSV files use comma (`,`) as delimiter and UTF-8 encoding.
- The first row of each CSV is always the header row.
- Header comparison is **case-sensitive** (`Status` ≠ `status`).
- SQL queries assume `product_id` is unique within each snapshot table. Non-unique handling is documented in Task 5.
- `NULL` values in `price`/`status` are handled explicitly with `OR IS NULL` guards in all comparison queries.
- API tests target a real server; `BASE_URL` in `test_orders_api.py` must be updated before running against a live environment.
- `created_at` timestamps follow ISO-8601 format (`YYYY-MM-DDTHH:MM:SSZ`).

---

## 7. AI Usage Statement

GitHub Copilot was used to assist with:
- Generating boilerplate code structure for the CSV comparison tool and test files.
- Suggesting SQL join patterns for change detection queries.
- Drafting Playwright API test syntax.

All generated code was reviewed, adjusted, and verified to match the exercise requirements. Logic, design decisions, and test case selection were made by the developer.

---

## Files in This Folder

| File | Description |
|------|-------------|
| `compare_headers.py` | CSV header comparison CLI tool |
| `test_compare_headers.py` | Unit tests for comparison logic (9 tests) |
| `expected_orders.csv` | Sample expected CSV file |
| `actual_orders.csv` | Sample actual CSV file |
| `test_orders_api.py` | Playwright API tests for `GET /api/orders/{order_id}` |
| `answers.sql` | SQL queries for Parts A (Tasks 1–5) |
