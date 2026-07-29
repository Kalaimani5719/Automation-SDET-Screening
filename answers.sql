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

