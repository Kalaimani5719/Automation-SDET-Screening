-- ============================================================
-- SETUP: Create and populate test tables
-- ============================================================

CREATE TABLE IF NOT EXISTS products_yesterday (
    product_id   INT          NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    price        DECIMAL(10,2),
    status       VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS products_today (
    product_id   INT          NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    price        DECIMAL(10,2),
    status       VARCHAR(20)
);

INSERT INTO products_yesterday (product_id, product_name, price, status) VALUES
  (1001, 'Coffee Mug',     12.50, 'ACTIVE'),
  (1002, 'Laptop Stand',   38.00, 'ACTIVE'),
  (1003, 'Wireless Mouse', 19.99, 'ACTIVE'),
  (1004, 'Old Keyboard',   29.99, 'DISCONTINUED'),
  (1005, 'Notebook',        4.50, 'ACTIVE'),
  (1008, 'Desk Lamp',      24.00, 'ACTIVE');

INSERT INTO products_today (product_id, product_name, price, status) VALUES
  (1001, 'Coffee Mug',     12.50, 'ACTIVE'),
  (1002, 'Laptop Stand',   35.00, 'ACTIVE'),
  (1003, 'Wireless Mouse', 21.99, 'ACTIVE'),
  (1005, 'Notebook',        4.50, 'INACTIVE'),
  (1006, 'Webcam',         59.00, 'ACTIVE'),
  (1007, 'USB Cable',       7.99, 'ACTIVE'),
  (1008, 'Desk Lamp',      24.00, 'ACTIVE');


-- ============================================================
-- Task 1: Products whose PRICE CHANGED from yesterday to today
-- ============================================================
-- INNER JOIN keeps only products that exist in both snapshots.
-- The WHERE clause filters to rows where the price differs.
-- NULL-safe comparison (price IS NULL parity handled explicitly).

SELECT
    t.product_id,
    t.product_name,
    y.price AS old_price,
    t.price AS new_price
FROM products_yesterday y
INNER JOIN products_today t
    ON y.product_id = t.product_id
WHERE
    -- Handle NULLs: treat NULL vs non-NULL as a change
    (y.price <> t.price)
    OR (y.price IS NULL AND t.price IS NOT NULL)
    OR (y.price IS NOT NULL AND t.price IS NULL);

/*
  Expected result:
  +------------+----------------+-----------+-----------+
  | product_id | product_name   | old_price | new_price |
  +------------+----------------+-----------+-----------+
  | 1002       | Laptop Stand   | 38.00     | 35.00     |
  | 1003       | Wireless Mouse | 19.99     | 21.99     |
  +------------+----------------+-----------+-----------+
*/


-- ============================================================
-- Task 2: NEW products (exist in today but NOT in yesterday)
-- ============================================================
-- LEFT JOIN from today back to yesterday; NULL on the right side
-- means the product_id was absent yesterday.

SELECT
    t.product_id,
    t.product_name,
    t.price,
    t.status
FROM products_today t
LEFT JOIN products_yesterday y
    ON t.product_id = y.product_id
WHERE y.product_id IS NULL;

/*
  Expected result:
  +------------+--------------+-------+--------+
  | product_id | product_name | price | status |
  +------------+--------------+-------+--------+
  | 1006       | Webcam       | 59.00 | ACTIVE |
  | 1007       | USB Cable    |  7.99 | ACTIVE |
  +------------+--------------+-------+--------+
*/


-- ============================================================
-- Task 3: MISSING products (existed yesterday, gone today)
-- ============================================================
-- LEFT JOIN from yesterday forward to today; NULL on the right
-- side means the product_id is no longer present today.

SELECT
    y.product_id,
    y.product_name,
    y.price,
    y.status
FROM products_yesterday y
LEFT JOIN products_today t
    ON y.product_id = t.product_id
WHERE t.product_id IS NULL;

/*
  Expected result:
  +------------+--------------+-------+--------------+
  | product_id | product_name | price | status       |
  +------------+--------------+-------+--------------+
  | 1004       | Old Keyboard | 29.99 | DISCONTINUED |
  +------------+--------------+-------+--------------+
*/


-- ============================================================
-- Task 4: Products whose STATUS CHANGED from yesterday to today
-- ============================================================
-- Same INNER JOIN pattern as Task 1; WHERE filters on status
-- mismatch with explicit NULL guards.

SELECT
    t.product_id,
    t.product_name,
    y.status AS old_status,
    t.status AS new_status
FROM products_yesterday y
INNER JOIN products_today t
    ON y.product_id = t.product_id
WHERE
    (y.status <> t.status)
    OR (y.status IS NULL AND t.status IS NOT NULL)
    OR (y.status IS NOT NULL AND t.status IS NULL);

/*
  Expected result:
  +------------+--------------+------------+------------+
  | product_id | product_name | old_status | new_status |
  +------------+--------------+------------+------------+
  | 1005       | Notebook     | ACTIVE     | INACTIVE   |
  +------------+--------------+------------+------------+
*/


-- ============================================================
-- Task 5 Explanation (inline comments — see README section below)
-- ============================================================

/*
  README SECTION — SQL Approach & Edge Cases
  ==========================================

  1. JOIN STRATEGY
  ----------------
  * Tasks 1 & 4 use INNER JOIN because we only care about products
    that appear in BOTH snapshots; if a product is new or missing
    it is out of scope for a "changed value" query.

  * Tasks 2 & 3 use LEFT JOIN (anti-join pattern) because we
    explicitly want the asymmetric set — rows present on one side
    and absent on the other. Returning the NULLs from the right
    side of the join and filtering WHERE right.id IS NULL is
    standard, readable, and well-optimised by every major engine.
    NOT EXISTS is an equivalent alternative; LEFT JOIN tends to be
    easier to extend (e.g. add more columns from either table).

  2. NON-UNIQUE product_id
  ------------------------
  If product_id is not unique within a snapshot, a join on it
  produces a Cartesian product of all matching rows.  For example,
  if 1002 appears twice in products_yesterday and twice in
  products_today the INNER JOIN yields 2×2 = 4 rows, inflating
  results and causing false positives in change detection.
  Defence options:
    a) Add a DISTINCT or GROUP BY to collapse duplicates before
       joining (use a CTE / subquery).
    b) Enforce a PRIMARY KEY or UNIQUE constraint on product_id.
    c) Use ROW_NUMBER() OVER (PARTITION BY product_id ...) to
       deterministically pick one row per id.

  3. NULL in price / status
  -------------------------
  Standard SQL comparison operators return UNKNOWN (not TRUE) when
  either operand is NULL, so:
      WHERE y.price <> t.price
  silently drops any row where either price is NULL, hiding real
  changes (e.g. price going from 19.99 → NULL or NULL → 5.00).

  Fix applied in Tasks 1 & 4: explicit OR arms handle all three
  NULL-change combinations:
      (y.col <> t.col)
      OR (y.col IS NULL AND t.col IS NOT NULL)
      OR (y.col IS NOT NULL AND t.col IS NULL)

  Alternatively, use the NULL-safe equality operator available in
  MySQL:   WHERE NOT (y.price <=> t.price)
  or in standard SQL:
           WHERE y.price IS DISTINCT FROM t.price
  Both treat NULL = NULL as equal and NULL ≠ non-NULL as different,
  removing the need for the three-part OR.
*/
