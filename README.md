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

- CSV header comparison validation
- SQL data comparison scenarios
- API automation testing using Playwright
- Pytest-based test execution and reporting

The implementation focuses on:

- Clean test structure
- Reusable automation logic
- Proper error handling
- Maintainable test cases
- Clear documentation

The CSV comparison tests are written using standard Python assertions, allowing them to run both as a standalone script and through Pytest for reporting and automation.

---

# Prerequisites

Before running the project, ensure the following are installed:

- Python 3.10 or above
- MySQL (or any compatible SQL database)
- Required Python packages
- Playwright browsers

---

# Setup Instructions

## 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Install Playwright Browsers

```bash
playwright install
```

---

# Database Setup

Execute the `answers.sql` file in your SQL database.

The SQL script will:

- Create the `products_yesterday` table
- Create the `products_today` table
- Insert sample product data
- Execute SQL queries for all required scenarios

---

# SQL Solution Details

The complete SQL implementation is available in:

```text
answers.sql
```

## Task 1 – Price Changes

**Approach: INNER JOIN**

- Compares products available in both yesterday's and today's tables.
- Identifies products whose prices have changed.

---

## Task 2 – New Products

**Approach: LEFT JOIN + IS NULL**

- Finds products that exist only in today's table.
- Identifies newly added products.

---

## Task 3 – Missing Products

**Approach: LEFT JOIN + IS NULL**

- Compares yesterday's products with today's products.
- Identifies products that existed yesterday but are missing today.

---

## Task 4 – Status Changes

**Approach: INNER JOIN**

- Compares product status between both tables.
- Identifies products whose status has changed.

---

# Task 5 - SQL Explanation

### Why did I use `INNER JOIN`, `LEFT JOIN`, or `NOT EXISTS`?

I used **INNER JOIN** for comparing prices and product statuses because I only needed products that exist in both yesterday's and today's tables. This made it easy to compare the previous and current values.

For identifying new and missing products, I used **LEFT JOIN** with `IS NULL`. This approach clearly identifies records that are present in one table but not in the other. `NOT EXISTS` is another valid option that can be used to achieve the same result.

---

### What would change if `product_id` was not unique?

If `product_id` was not unique, the joins could return duplicate or incorrect results because one product could match multiple records in the other table. To avoid this, I would first ensure each product has a unique record by using additional columns such as a timestamp or version number, or by removing duplicates using techniques like `ROW_NUMBER()` or `GROUP BY` before comparing the data.

---

### What issue could happen if `price` or `status` can be `NULL`?

If `price` or `status` contains `NULL` values, normal comparison operators like `=` and `<>` may not work as expected because `NULL` represents an unknown value in SQL. This can cause actual changes to be missed during comparison. To handle this correctly, I would use `IS NULL`, `IS NOT NULL`, or database-specific functions such as `IS DISTINCT FROM` (where supported) to compare values accurately.

---

# CSV Header Comparison Tool

## Execute Header Comparison

Run:

```bash
python compare_headers.py expected_orders.csv actual_orders.csv
```

The tool compares:

- Headers present only in the expected CSV
- Headers present only in the actual CSV
- Common headers between both files
- Whether the common headers appear in the same relative order

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

Run the tests directly using Python:

```bash
python test_compare_headers.py
```

Or execute them using Pytest:

```bash
python -m pytest test_compare_headers.py -v
```

Generate an HTML report:

```bash
python -m pytest test_compare_headers.py -v --html=reports/report.html --self-contained-html
```

---

## Expected Result

```text
============================= test session starts =============================
collected 9 items

test_compare_headers.py .........

============================== 9 passed =======================================
```

The HTML report will be generated under:

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

- Five API validation test cases
- One Playwright API automation test

The Playwright API test validates:

- HTTP response status code is `200`
- Response status is `"PAID"`
- Response payload contents

---

## API Configuration

The API base URL is currently a placeholder.

Before execution:

1. Open `test_orders_api.py`.
2. Update the base URL with the target environment URL.
3. Execute the tests.

---

# Test Coverage Summary

## CSV Validation

The CSV comparison tests cover the following scenarios:

- Identical headers between two CSV files
- Missing headers in the actual CSV
- Header whitespace trimming
- Windows (CRLF) line ending support
- Header order comparison
- Empty CSV file validation
- Blank or invalid header row validation
- Missing command-line arguments
- Non-existent file handling

A total of **9 unit tests** are implemented using standard Python assertions. The tests can be executed directly as a Python script or with Pytest for reporting and integration into CI/CD pipelines.

---

## API Validation

Covered scenarios:

- API response validation
- HTTP status code verification
- Response body validation
- Order status verification

---

# Assumptions

- CSV files use comma (`,`) as the delimiter.
- Only the first row (header row) is compared.
- Leading and trailing whitespace in header names is ignored.
- Windows (`CRLF`) and Unix (`LF`) line endings are supported.
- Empty CSV files raise an appropriate validation error.
- Header rows containing only blank values are treated as invalid.
- The comparison checks the relative order of common headers.
- API base URL must be updated before execution.

---

# AI Usage Statement

I used the following AI tools during this exercise:

- ChatGPT (OpenAI)
- GitHub Copilot (Claude Sonnet 4.6)

AI assistance was used for:

- Generating and reviewing SQL queries
- Assisting with the Python CSV comparison implementation
- Suggesting additional error-handling scenarios
- Improving documentation and README structure

All AI-generated suggestions were:

- Reviewed manually
- Modified where required
- Tested locally
- Verified before submission

---

# Candidate Acknowledgement

I confirm that:

- I have disclosed my AI usage in `AI_TRANSCRIPT.md`.
- I reviewed and understood all AI-assisted content.
- I can explain, modify, debug, and extend the submitted solution without AI assistance.
- The final submission reflects my own understanding, implementation, and decisions.

---

# Author

**Kalaimani M**  
Automation Engineer / SDET
