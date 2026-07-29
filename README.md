# SDET Take-Home Screening Exercise

**Candidate:** Kalaimani M
**Role:** Automation Engineer / SDET
**Language:** Python 3.11+
**Testing Framework:** Pytest

---

# Repository Structure

```text
sdet-take-home/
├── execution_screenshots
├── reports
├── README.md
├── AI_TRANSCRIPT.md
├── requirements.txt
├── answers.sql
├── expected_orders.csv
├── actual_orders.csv
├── compare_headers.py
├── test_compare_headers.py
└── test_orders_api.py
```

---

# Prerequisites

* Python 3.10 or above
* SQL database (MySQL or compatible)

---

# Setup

## 1. Install Dependencies

```bash
pip install -r requirements.txt
playwright install
python -m pip install playwright
```

## 2. Database Setup

Run the `answers.sql` script in your SQL database.

The script will:

* Create the `products_yesterday` table.
* Create the `products_today` table.
* Insert the sample data.
* Execute the SQL queries for all required tasks.

## 3. Run the CSV Header Comparison Tool

```bash
python compare_headers.py expected_orders.csv actual_orders.csv
```

### Example Output

```text
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

## 4. Run the Unit Tests

```bash
python -m pytest test_compare_headers.py -v
```

**Expected Result**

All 9 tests should pass successfully.

---

# SQL Solution

The complete SQL solution is available in **answers.sql**.

### Task 1 – Price Changes

Uses **INNER JOIN** to identify products whose prices have changed between yesterday and today.

### Task 2 – New Products

Uses **LEFT JOIN** with `IS NULL` to identify products that exist only in today's table.

### Task 3 – Missing Products

Uses **LEFT JOIN** in the opposite direction to identify products that existed yesterday but are missing today.

### Task 4 – Status Changes

Uses **INNER JOIN** to identify products whose status has changed.

### Task 5 – Explanation

The SQL file also includes explanations for:

* Why `INNER JOIN` and `LEFT JOIN` were used.
* How non-unique `product_id` values affect joins.
* How `NULL` values are handled during comparisons.

---

# API Test Cases

**Endpoint**

```text
GET /api/orders/{order_id}
```

The API solution includes:

* Five API test cases.
* One Playwright API automation test that validates:

  * HTTP Status Code = **200**
  * Response status = **"PAID"**

The base URL is a placeholder and should be updated before running the test.

---

# Assumptions

* CSV files use a comma (`,`) as the delimiter.
* Only the first row (header) of each CSV file is compared.
* Leading and trailing whitespace in header values is ignored.
* Empty CSV files and invalid header rows are handled with appropriate error messages.
* The API base URL should be updated to match the target environment before execution.

---

# AI Usage Statement

I used the following AI tools during this exercise:

* ChatGPT (OpenAI)
* GitHub Copilot (Claude Sonnet 4.6)

AI was used to:

* Generate and review SQL queries.
* Assist with the Python CSV header comparison tool.
* Suggest error handling and test cases.
* Help improve the README and documentation.

All AI-generated content was reviewed, modified where necessary, tested locally, and verified before submission.

---

# Candidate Acknowledgement

I confirm that:

* I have disclosed my AI usage in **AI_TRANSCRIPT.md**.
* I reviewed all AI-generated content before submission.
* I understand the complete solution.
* I can explain, modify, debug, and extend the submitted solution without AI assistance.
* The final submission reflects my own understanding and decisions.
