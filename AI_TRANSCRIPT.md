# AI_TRANSCRIPT.md

## Tools Used

* ChatGPT (OpenAI)
* GitHub Copilot (Claude Sonnet 4.6)

**Candidate:** Kalaimani M
**Date:** 29-July-2026

**Exercise:** SDET Candidate Screening – TCS / SIX GCC

---

## Summary

I used AI tools to help me understand the requirements, generate an initial solution, review the implementation, and improve the documentation.

All AI-generated suggestions were reviewed before use. I tested the code locally, made changes where required, and verified the outputs manually.

The final submission reflects my own understanding, and I can explain, modify, debug, and extend every part of the solution.

---

## Primary Prompt

Act as a Senior SDET with expertise in Python, SQL, API testing, Playwright, and test automation.

Help me complete an SDET screening assessment that includes:

* SQL queries using two product tables
* A Python CSV header comparison tool
* API test case design
* README and AI usage documentation

Generate clean, readable, and interview-ready solutions using Python best practices. Keep the implementation simple, maintainable, and suitable for a take-home exercise.

---

## AI Assistance Used

AI tools were used for:

* SQL query generation and review
* Python implementation for the CSV header comparison tool
* Error-handling suggestions
* Test case generation and improvements
* API test case design
* README and documentation review

---

## What I Accepted

* Overall project structure
* SQL query logic
* CSV comparison approach
* Python function structure
* Test case organization
* README structure

---

## What I Modified

* Improved the readability of the Python code.
* Added additional test cases for edge scenarios.
* Updated the console output to match the expected format.
* Added and refined docstrings where appropriate.
* Reviewed naming conventions and documentation before submission.

---

## What I Verified Manually

### SQL Validation

* Verified the output of all SQL queries using the provided data.
* Confirmed price changes, new products, missing products, and status changes.

### Python Validation

* Executed the CSV header comparison tool locally.
* Verified the output against the expected results.
* Confirmed error handling for:

  * Missing command-line arguments
  * Missing files
  * Empty CSV files
  * Invalid or blank header rows

### Test Validation

* Executed all Python test cases locally.
* Confirmed that all tests passed successfully.

---

## Key Design Decisions

### Separation of Concerns

Separated the CSV reading, comparison logic, and command-line interface to improve readability, testing, and maintainability.

### Standard Library Usage

Used Python's standard library for CSV processing to keep the solution lightweight and easy to run.

### Error Handling

Handled common user errors with clear messages instead of allowing the program to fail unexpectedly.

### SQL Strategy

* Used `INNER JOIN` to compare matching records.
* Used `LEFT JOIN` to identify new and missing records.
* Considered `NULL` values while comparing data.

---

## Candidate Statement

I confirm that:

* I reviewed all AI-generated content before submission.
* I tested and verified the solution manually.
* I understand the complete implementation.
* I can explain, modify, debug, and extend the submitted solution without AI assistance.
* The final submission reflects my own understanding and decisions.
