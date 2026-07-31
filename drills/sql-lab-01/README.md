# SQL Correctness Lab 01 — Saturday morning

**Time:** ~2.5 hours. **Prereq:** `pip install duckdb`, then `python setup.py`.

Open a session with `duckdb lab.duckdb` (CLI) or from Python.

## The one rule

**Before you run any query, write down the number you expect.** Every table here
is small enough to compute on paper. If your prediction and the result disagree,
that disagreement is the entire lesson — do not move on until you can explain it.

Keep your predictions in `answers.md` next to your final queries. That file is
the portfolio artifact, not the queries.

---

## Ex 1 — The exclusion that excludes everything

`blocked_ids` is a compliance hold list. You want all orders from customers who
are *not* on it.

```sql
SELECT count(*) FROM orders
WHERE customer_id NOT IN (SELECT customer_id FROM blocked_ids);
```

**Predict the count. Then run it.**

Now rewrite it with `NOT EXISTS` and run again. The two answers differ by
everything.

- Explain the difference in terms of three-valued logic. Why `UNKNOWN` and not `FALSE`?
- Write a third version using `LEFT JOIN ... WHERE b.customer_id IS NULL`. Which of the three would you put in production, and why?
- **The real question:** this query returned zero rows and threw no error. What would have caught it in a pipeline before a human noticed?

## Ex 2 — Deduplication with a tie

`customer_raw` is not one row per customer. Build a clean dimension with exactly
one current row per `customer_id`.

Start with the pattern most people reach for:

```sql
SELECT r.*
FROM customer_raw r
JOIN (SELECT customer_id, max(updated_at) AS m FROM customer_raw GROUP BY 1) x
  ON r.customer_id = x.customer_id AND r.updated_at = x.m;
```

**Predict the row count. Then run it.**

- Which customer breaks it, and why?
- Rewrite with `ROW_NUMBER()`. Does the naive version fix the problem, or hide it?
- Make it *deterministic*: two people running your query must get the identical row every time. What second `ORDER BY` key achieves that, and what does it cost you if the tie is a genuine data conflict rather than noise?

## Ex 3 — Fan-out

`orders.order_total` is the authoritative order value. `order_items` holds the
line detail. Finance asks for total revenue.

```sql
SELECT sum(o.order_total)
FROM orders o
JOIN order_items i USING (order_id);
```

**Predict the total. Then run it.** Then run `SELECT sum(order_total) FROM orders`.

- Explain the inflation factor. Which order contributes the most error, and why that one?
- Now produce revenue **by category** — which requires the join. Get a correct answer, and prove it's correct by reconciling against a total you trust.
- State the rule you'd give a junior teammate in one sentence, starting with "Before you aggregate across a join, ..."

## Ex 4 — Declare the grain

For the clean customer dimension you built in Ex 2, write its grain as a single
sentence in `answers.md`, in this form:

> One row per `<what>` per `<what>`.

Then do the same for `orders`, `order_items`, and a hypothetical table joining
orders to their items.

- For each, name the column set that enforces the grain.
- Which of the four grains is ambiguous as stated, and what question would you have to ask a stakeholder to resolve it?

## Ex 5 — Write the test, not just the query

A grain is a claim. Claims get tested.

Write a query that **returns zero rows when the grain holds and one or more rows
when it is violated**, for your clean customer dimension.

```sql
-- fill this in
SELECT customer_id, count(*) AS n
FROM <your_clean_dim>
GROUP BY 1
HAVING ...;
```

- Run it against `customer_raw` (should fail loudly) and your clean dim (should pass silently).
- Write a second test asserting that `region` is never NULL. Run it. It fails — customer 5. **Do not fix the data.** Instead, answer: is a NULL region a bug in your pipeline, a bug upstream, or a legitimate business state? How does your answer change what you build?
- This shape — a query that returns rows only on failure — is what dbt tests, Great Expectations, and every in-house framework compile down to. You now know the primitive.

## Ex 6 — Redelivery

`daily_landing` holds two days of a vendor file drop. Day 2 redelivered two rows
from day 1.

```sql
SELECT sum(amount) FROM daily_landing;
```

**Predict it. Then run it.** The true value is 215.00.

- Write a query returning the correct total, treating `order_id` as the business key.
- Now the harder half: you control the *load*. Describe in `answers.md` how you would change the ingest so this table never contains duplicates in the first place. Name the two standard approaches and the condition under which each is the right one.
- What must be true of `order_id` for either approach to work? What do you do if that isn't true?

---

## Before you close the laptop

In `answers.md`, write three sentences:

1. The thing I was most confident about and got wrong.
2. The concept I could now explain to someone else without notes.
3. The thing I still can't explain, stated as a specific question.

Item 3 is what we open with next session. Bring it sharp.
