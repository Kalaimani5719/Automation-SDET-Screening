"""
test_orders_api.py
==================
Part C — Basic API Testing (Playwright API Testing)

Endpoint under test:
    GET /api/orders/{order_id}

Approach: Playwright's APIRequestContext for API testing (no browser needed).

Setup:
    pip install playwright

Run:
    python test_orders_api.py
    pytest test_orders_api.py -v
"""


# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

from playwright.sync_api import sync_playwright

# Global Configuration
BASE_URL = "www.example.com"  # Replace with the actual base URL of the API


# ===========================================================================
# API Task 1 — Test Case Design (5 test cases)
# ===========================================================================
#
# ┌─────┬──────────────────────────────────┬──────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────┐
# │  #  │ Test Name                        │ Input / Expected Result                  │ Why Useful                                                                   │
# ├─────┼──────────────────────────────────┼──────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
# │  1  │ Valid order returns 200 + body   │ GET /api/orders/ORD-1001                 │ Confirms the happy path: endpoint is reachable and the response contract     │
# │     │                                  │ → HTTP 200, JSON body with all fields    │ (all required fields, correct types) is met.                                 │
# ├─────┼──────────────────────────────────┼──────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
# │  2  │ Unknown order returns 404        │ GET /api/orders/ORD-9999                 │ Validates error handling: the server should return 404 (not 200 with empty   │
# │     │                                  │ → HTTP 404, error message in body        │ body, not 500) so clients can distinguish "not found" from server errors.    │
# ├─────┼──────────────────────────────────┼──────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
# │  3  │ Response body field types        │ GET /api/orders/ORD-1001                 │ Catches schema drift: a field renamed or its type changed (e.g. amount       │
# │     │                                  │ → amount is float, order_id is string,   │ returned as string "100.50" instead of number 100.50) breaks consumers       │
# │     │                                  │    created_at matches ISO-8601 format    │ silently without a type-level check.                                         │
# ├─────┼──────────────────────────────────┼──────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
# │  4  │ Invalid order_id format → 400    │ GET /api/orders/INVALID##ID              │ Boundary / negative test: the API should reject malformed IDs with a clear   │
# │     │                                  │ → HTTP 400, validation error message     │ 400 rather than an unhandled 500 or silently returning null data.            │
# ├─────┼──────────────────────────────────┼──────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
# │  5  │ Status field is a known value    │ GET /api/orders/ORD-1001                 │ Business-rule check: status must be one of the defined enum values           │
# │     │                                  │ → status in {PAID, PENDING, CANCELLED,   │ (PAID/PENDING/CANCELLED/REFUNDED). An unexpected value like "COMPLETE"       │
# │     │                                  │               REFUNDED}                  │ indicates a back-end change that could break downstream processing.          │
# └─────┴──────────────────────────────────┴──────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────┘


# ===========================================================================
# API Task 2 — Simple Playwright API Test
# ===========================================================================


def test_get_order_returns_200_and_status_paid():
    """
    Validate GET /api/orders/ORD-1001 returns HTTP 200 with status=PAID
    
    Checks:
    - HTTP status code is 200
    - Response status field equals "PAID"
    """
    with sync_playwright() as p:
        # Create API request context (no browser needed)
        api_context = p.request.new_context(base_url=BASE_URL)
        
        # Make GET request
        response = api_context.get("/api/orders/ORD-1001")
        
        # Assert HTTP 200
        assert response.status == 200, f"Expected status 200, got {response.status}"
        
        # Parse JSON and assert status field
        body = response.json()
        assert body["status"] == "PAID", f"Expected status='PAID', got '{body['status']}'"
        
        # Cleanup
        api_context.dispose()
        
        print("✓ Test PASSED: GET /api/orders/ORD-1001 returns 200 with status=PAID")


if __name__ == "__main__":
    test_get_order_returns_200_and_status_paid()


