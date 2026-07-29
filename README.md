# SDET Take-Home Screening Exercise

**Candidate:** Kalaimani M
**Role:** Automation Engineer / SDET
**Language:** Python 3.10+
**Testing Framework:** Pytest

---

# Repository Structure

```text
sdet-take-home/
├── execution_screenshots/
├── reports/
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

# Project Overview

This project contains automation solutions for:

* CSV header comparison validation
* SQL data comparison scenarios
* API automation testing using Playwright
* Pytest-based test execution and reporting

The implementation focuses on:

* Clean test structure
* Reusable automation logic
* Proper error handling
* Maintainable test cases
* Clear documentation

---

# Prerequisites

Before running the project, ensure the following are installed:

* Python 3.10 or above
* MySQL or compatible SQL database
* Required Python packages
* Playwright browsers

---

# Setup Instructions

## 1. Install Python Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

---

## 2. Install Playwright Browsers

Install Playwright browser dependencies:

```bash
playwright install
```

---

# Database Setup

Execute the `answers.sql` file in your SQL database.

The SQL script will:

* Create the `products_yesterday` table
* Create the `products_today` table
* Insert sample product data
* Execute SQL queries for all required scenarios

---

# SQL Solution Details

The complete SQL implementation is available in:

```text
answers.sql
```

## Task 1 – Price Changes

**Approach: INNER JOIN**

* Compares products available in both yesterday and today's tables.
* Identifies products where the price has changed.

Example scenario:

A product exists in both tables, but the price value is different.

---

## Task 2 – New Products

**Approach: LEFT JOIN + IS NULL**

* Finds products that exist only in today's table.
* Identifies newly added products.

---

## Task 3 – Missing Products

**Approach: LEFT JOIN + IS NULL**

* Compares yesterday's products with today's products.
* Identifies products that existed yesterday but are missing today.

---

## Task 4 – Status Changes

**Approach: INNER JOIN**

* Compares product status between both tables.
* Identifies products where the status has changed.

---

## SQL Explanation

The SQL file also includes explanations for:

### Why INNER JOIN or LEFT JOIN?

* `INNER JOIN` is used when we need only matching records from both tables.
* `LEFT JOIN + IS NULL` is used to find records missing from another table.
* `NOT EXISTS` can also be used as an alternative approach.

---

### Handling Non-Unique Product IDs

If `product_id` is not unique, joins may create duplicate records.

Example:

* Yesterday table contains product_id `1002` twice.
* Today table contains product_id `1002` twice.

The join result can produce:

```
2 × 2 = 4 rows
```

To avoid incorrect results:

* Remove duplicates using `ROW_NUMBER()`
* Or aggregate records using `GROUP BY`

---

### Handling NULL Values

Normal SQL comparisons do not work correctly with NULL values.

Example:

```sql
NULL <> 100
```

does not return TRUE.

To handle NULL values:

PostgreSQL:

```sql
y.price IS DISTINCT FROM t.price
```

Standard SQL:

```sql
(
 y.price <> t.price
 OR y.price IS NULL
 OR t.price IS NULL
)
```

The same approach applies to status comparison.

---

# CSV Header Comparison Tool

## Execute Header Comparison

Run:

```bash
python compare_headers.py expected_orders.csv actual_orders.csv
```

The tool compares:

* Missing headers
* Common headers
* Header order validation

---

## Example Output

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

---

# Running Automated Tests

## CSV Header Comparison Tests

Execute:

```bash
python -m pytest test_compare_headers.py -v
```

With HTML report generation:

```bash
python -m pytest test_compare_headers.py -v --html=reports/report.html --self-contained-html
```

---

## Expected Result

```
9 tests passed successfully
```

The execution report will be generated under:

```text
reports/report.html
```

---

# API Automation Testing

## Endpoint

```text
GET /api/orders/{order_id}
```

---

## API Test Coverage

The API automation includes:

* Five API validation test cases
* One Playwright API automation test

The Playwright API test validates:

* HTTP response status code is `200`
* Response status value is `"PAID"`
* Response payload validation

---

## API Configuration

The API base URL is currently a placeholder.

Before execution:

1. Open `test_orders_api.py`
2. Update the base URL with the target environment URL
3. Execute the test

---

# Test Coverage Summary

## CSV Validation

Covered scenarios:

* Header comparison between expected and actual CSV files
* Missing column detection
* Common column identification
* Header order comparison
* Empty CSV handling
* Invalid header handling
* Whitespace trimming

---

## API Validation

Covered scenarios:

* API response validation
* HTTP status verification
* Response body validation
* Order status verification

---

# Assumptions

* CSV files use comma (`,`) as the delimiter.
* Only the first row (header row) is compared.
* Leading and trailing spaces in headers are ignored.
* Empty CSV files are handled with appropriate validation messages.
* Invalid header formats are handled safely.
* API base URL must be updated before execution.

---

# AI Usage Statement

I used the following AI tools during this exercise:

* ChatGPT (OpenAI)
* GitHub Copilot (Claude Sonnet 4.6)

AI assistance was used for:

* Generating and reviewing SQL queries.
* Assisting with Python CSV comparison implementation.
* Suggesting additional error handling scenarios.
* Improving documentation and README structure.

All AI-generated suggestions were:

* Reviewed manually
* Modified where required
* Tested locally
* Verified before submission

---

# Candidate Acknowledgement

I confirm that:

* I have disclosed my AI usage in `AI_TRANSCRIPT.md`.
* I reviewed and understood all AI-assisted content.
* I can explain, modify, debug, and extend the submitted solution without AI assistance.
* The final submission reflects my own understanding, implementation, and decisions.

---

# Author

**Kalaimani M**
Automation Engineer / SDET
