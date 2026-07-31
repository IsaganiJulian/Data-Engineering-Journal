"""
SQL Correctness Lab 01 — environment setup.

Builds lab.duckdb with five small tables. The data is small on purpose:
every answer in this lab can be verified by hand. If you cannot compute the
expected result on paper first, you are not doing the exercise.

Run:  python setup.py
"""

import duckdb, os

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lab.duckdb")
if os.path.exists(DB):
    os.remove(DB)

con = duckdb.connect(DB)

# ---------------------------------------------------------------- customers
# Raw CRM extract. Note: this table is NOT one row per customer.
# customer 2 appears twice (a real update), customer 4 appears twice with the
# SAME updated_at (a tie — this is the trap), customer 5 has a NULL region.
con.execute("""
CREATE TABLE customer_raw (
    customer_id  INTEGER,
    name         VARCHAR,
    region       VARCHAR,
    updated_at   TIMESTAMP
);
INSERT INTO customer_raw VALUES
    (1, 'Alvarez Freight',  'WEST',  '2026-01-04 09:00:00'),
    (2, 'Boyd Logistics',   'EAST',  '2026-01-04 09:00:00'),
    (2, 'Boyd Logistics',   'SOUTH', '2026-03-11 14:30:00'),
    (3, 'Chen Supply Co',   'WEST',  '2026-02-20 11:15:00'),
    (4, 'Delacroix Parts',  'NORTH', '2026-02-01 08:00:00'),
    (4, 'Delacroix Parts',  'EAST',  '2026-02-01 08:00:00'),
    (5, 'Eastman Tooling',  NULL,    '2026-01-30 16:45:00');
""")

# ------------------------------------------------------------- blocked_ids
# Compliance hold list. One row has a NULL id — an upstream export bug that
# nobody upstream considers a bug.
con.execute("""
CREATE TABLE blocked_ids (customer_id INTEGER);
INSERT INTO blocked_ids VALUES (3), (NULL);
""")

# ------------------------------------------------------------------ orders
# One row per order. order_total is the authoritative order value.
con.execute("""
CREATE TABLE orders (
    order_id     INTEGER,
    customer_id  INTEGER,
    order_date   DATE,
    order_total  DECIMAL(10,2)
);
INSERT INTO orders VALUES
    (101, 1, '2026-04-02', 300.00),
    (102, 1, '2026-04-05', 150.00),
    (103, 2, '2026-04-05', 800.00),
    (104, 3, '2026-04-09', 250.00),
    (105, 4, '2026-04-11', 600.00),
    (106, 5, '2026-04-12', 100.00),
    (107, 2, '2026-04-18', 450.00),
    (108, 4, '2026-04-21', 200.00);
""")

# ------------------------------------------------------------- order_items
# One row per line item. Line amounts sum to the parent order_total.
# Order 105 has four lines — it is the biggest fan-out multiplier.
con.execute("""
CREATE TABLE order_items (
    item_id      INTEGER,
    order_id     INTEGER,
    category     VARCHAR,
    item_amount  DECIMAL(10,2)
);
INSERT INTO order_items VALUES
    (1,  101, 'TOOLS',    200.00),
    (2,  101, 'SAFETY',   100.00),
    (3,  102, 'TOOLS',    150.00),
    (4,  103, 'PARTS',    500.00),
    (5,  103, 'TOOLS',    300.00),
    (6,  104, 'SAFETY',   250.00),
    (7,  105, 'PARTS',    200.00),
    (8,  105, 'PARTS',    150.00),
    (9,  105, 'TOOLS',    150.00),
    (10, 105, 'SAFETY',   100.00),
    (11, 106, 'SAFETY',   100.00),
    (12, 107, 'PARTS',    450.00),
    (13, 108, 'TOOLS',    200.00);
""")

# ----------------------------------------------------------- daily_landing
# Two days of a vendor drop. Day 2 REDELIVERS two rows from day 1 (order 201,
# 202) plus one genuinely new row. This is what at-least-once looks like on
# a batch file feed.
con.execute("""
CREATE TABLE daily_landing (
    load_date    DATE,
    order_id     INTEGER,
    amount       DECIMAL(10,2)
);
INSERT INTO daily_landing VALUES
    ('2026-05-01', 201, 50.00),
    ('2026-05-01', 202, 75.00),
    ('2026-05-02', 201, 50.00),
    ('2026-05-02', 202, 75.00),
    ('2026-05-02', 203, 90.00);
""")

print("built:", DB)
for t in ["customer_raw", "blocked_ids", "orders", "order_items", "daily_landing"]:
    n = con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
    print(f"  {t:<15} {n} rows")
con.close()
