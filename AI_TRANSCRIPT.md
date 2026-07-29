# AI Transcript — QA Exercise

## 1. AI Tool Used

- **Tool:** GitHub Copilot (Chat)
- **Model:** Claude Sonnet 4.6
- **IDE:** Visual Studio Code

---

## 2. Prompts Entered & AI Responses Relied On

---

### Part A — SQL Exercise

**Prompt:**
> You are given two tables representing yesterday's and today's product data.
> Write SQL queries for:
> - Task 1: Price Changes
> - Task 2: New Products
> - Task 3: Missing Products
> - Task 4: Status Changes
> - Task 5: Short explanation on JOIN choices, non-unique product_id, and NULL handling

**AI Response Accepted:**
- Generated `CREATE TABLE` and `INSERT` setup statements for both tables
- Task 1: `INNER JOIN` with `WHERE y.price <> t.price` plus explicit `OR IS NULL` guards
- Task 2: `LEFT JOIN` anti-join from `products_today` → `products_yesterday`, filter `WHERE y.product_id IS NULL`
- Task 3: `LEFT JOIN` anti-join reversed, filter `WHERE t.product_id IS NULL`
- Task 4: `INNER JOIN` with `WHERE y.status <> t.status` plus `OR IS NULL` guards
- Task 5: Inline `/* ... */` comment block explaining INNER vs LEFT JOIN rationale, Cartesian product risk for non-unique keys, and NULL-safe comparison alternatives (`<=>`, `IS DISTINCT FROM`)

**Follow-up Prompt:**
> I want expected result with header in doc string

**AI Response Accepted:**
- Added formatted `/* ... */` comment blocks after each query showing results as ASCII tables with column headers and row data

---

### Part B — CSV Header Comparison Tool

**Prompt:**
> Create a small command-line Python tool that compares headers of two CSV files.
> - Accept two CSV file paths as input
> - Read only the first row from each file
> - Split and trim headers
> - Print: only in expected, only in actual, common headers, same relative order
> - Add at least 3 tests
> - Handle errors: missing args, file not found, empty file, blank header row

**AI Response Accepted:**
- `compare_headers.py` with `read_header()` and `compare_headers()` as pure functions
- `print_report()` formatting helper
- `main()` with all 4 error cases handled (missing args, file not found, empty file, blank headers)
- `test_compare_headers.py` with 9 tests covering identical headers, missing header, whitespace trimming, CRLF endings, different order, empty file, blank header row, missing args, non-existent file

**Follow-up Prompt:**
> Create inside the demo folder

**AI Response Accepted:**
- All files created under `tests/demo/`

**Follow-up Prompt:**
> I want to run in cmd so give terminal cmd

**AI Response Accepted:**
- Provided exact `cd` + `python` commands for running the tool and tests

---

### Part C — API Testing

**Prompt:**
> Write 5 test cases for GET /api/orders/{order_id} and one automated test that validates HTTP 200 and status = PAID. I want only Playwright API testing.

**AI Response Accepted:**
- 5 test cases documented in a comment table (valid order 200, unknown 404, field types, invalid ID 400, status enum check)
- 5 async Playwright tests using `async_playwright` and `APIRequestContext`

**Follow-up Prompt:**
> I want to validate this part only with Playwright request library, no need to mock, no need to run, just want the syntax — I will replace the URL later

**AI Response Accepted:**
- Single clean sync Playwright test using `sync_playwright` and `p.request.new_context(base_url=BASE_URL)`

**Follow-up Prompt:**
> Put base URL in global

**AI Response Accepted:**
- Moved `BASE_URL = "http://localhost:8000"` to module-level global constant

**Follow-up Prompt:**
> Add only relevant doc string

**AI Response Accepted:**
- Trimmed docstring to 3 lines: purpose + 2 bullet checks

**Follow-up Prompt:**
> Here remove Task 2 and add `test_orders_api_simple.py` content as Task 2 in this file

**AI Response Accepted:**
- Replaced async multi-test Task 2 block with the single clean sync test
- Removed `pytest`, `pytest-asyncio`, `async_playwright` imports; replaced with `sync_playwright`

**Follow-up Prompt:**
> Delete `test_orders_api_simple.py` file

**AI Response Accepted:**
- File deleted via PowerShell `Remove-Item`

---

### Part D — README

**Prompt:**
> Create a short README.md for the demo folder containing: language used, how to run the CSV tool, how to run tests, SQL answers, API test cases, assumptions, AI usage statement.

**AI Response Accepted:**
- Full `README.md` with all 7 sections, including a files table and SQL summary table

---

## 3. Generated Code or Suggestions Accepted

| File | Accepted |
|------|----------|
| `mysql.sql` | Full SQL (setup + 4 queries + Task 5 explanation block) |
| `compare_headers.py` | Full implementation |
| `test_compare_headers.py` | All 9 tests |
| `expected_orders.csv` | File content |
| `actual_orders.csv` | File content |
| `test_orders_api.py` | Final Task 1 comment table + Task 2 sync Playwright test |
| `README.md` | Full content |

---

## 4. Generated Code or Suggestions Rejected

| Suggestion | Reason Rejected |
|------------|-----------------|
| Async Playwright tests using `@pytest.mark.asyncio` for Task 2 | Too complex for a single validation test; replaced with sync Playwright API |
| Multiple alternative implementations (RestAssured pseudo-code, Postman pseudo-code, `requests` mock) appended as comments | Not needed — exercise asked for one approach; removed to keep file clean |
| Overly detailed docstring with Purpose / Endpoint / Input / Expected Result / Why Useful / Notes sections | Too verbose for a simple test function; trimmed to 3-line relevant docstring |
| `pytest-asyncio` as a dependency | Removed when switching to sync Playwright |

---

## 5. What Was Changed Manually

- **`BASE_URL`** value in `test_orders_api.py` updated from `"http://localhost:8000"` to `"www.example.com"` as a placeholder to match actual environment.
- **File locations** — initially AI placed files in `data/inputs/` and `scripts/Python/`; redirected to `tests/demo/` via follow-up prompt.
- **Scope trimming** — AI initially generated JavaScript and Java versions of the CSV tool; explicitly rejected and limited scope to Python only.
- **Test count** — AI generated 9 tests for the CSV tool; all were reviewed and kept as they covered the required scenarios from the exercise spec.
- Reviewed all SQL `NULL` guard logic manually to confirm correctness before accepting.
