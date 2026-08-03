# Answers
- Your prediction
- Reasoning
- The actual result


## Exercise 1: The exclusion that excludes everything
**Prediction**
My prediction was that the query using NOT IN will return 0 rows, while the NOT EXIST query will return all 7 rows. 

**Reasoning**
My reasoning for this is because the blocked_id table only shows two rows with the values of 3 and none. The NOT EXIST query will return 7 rows becasue the blocked customer_id will match the amount of customer_id found in the order table.

**Results**The actual result was 0 rows for NOT IN and 7 Rows for NOT EXISTS.


**Questions:**

1. Explain the difference in terms of three-valued logic. Why `UNKNOWN` and not `FALSE`?
- When comparing anything to NULL in SQL, the result is UNKNOWN and not FALSE. The NOT IN query expands to 3 and NULL, and for every row customer_id NULL evaluates to UNKNOWN. When you AND anything with UNKNOWN, the result is UNKNOWN. WHERE clause only passes TRUE rows and UNKNOWN rows get rejected like FALSE rows, resulting in zero rows passing the filter. UNKNOWN is neither TRUE or FALSE, so it then gets filtered out.

2. Write a third version using `LEFT JOIN ... WHERE b.customer_id IS NULL`. Which of the three would you put in production, and why?
   - I would use NOT EXIST becuase it excludes orders where a block exists, this option is typically faster and can short circuit as soon as it finds a match. The LEFT JOIN whorks but it has to scan the entire table, resulting in a slower query search. NOT IN is broken and is not compatible with the NULL semantics.

3. This query returned zero rows and threw no error. What would have caught it in a pipeline before a human noticed?
   -  This assertion: assert row_count > 0, f"ALERT: Query returned {row_count} rows. Expected > 0. Check for NULL in blocked_ids."
   
   I would include a row count assertion in the test to ensure that the query does not return zero rows. If we know what rows should be expected, then we can create an assertion that ensures the unexpected value will flag an error in the pipeline. Production needs a check that fails loudly when the number is wrong.

   ## Exercise 2: Deduplciation with a tie
   **Prediction**   
   My prediction is that the MAX dedup will return 6 rows.

   **Reasoning**
   My reasoning is that the rows returned will result in 6 rows, because cusotmer 4 has two rows with the same updated timestamp. The MAX finds the timestamp and since both rows match on the JOIN, they will both come back.

   **Answer**
   The answer was 5 rows.


1. Which customer breaks it, and why?
- Customer 4 breaks the pipeline because there are two rows with the same time stamps. The MAX finds the timestamp and since both rows match on the join, they will both be reuruned and come back. 

2. Rewrite with `ROW_NUMBER()`. Does the naive version fix the problem, or hide it?
- The naive version hides the problem. The value should be 5, instead the naive version returns 6. When using ROW_NUMBER, it partions by the customer_id and the updated_at time based on DESC.

3.  Make it *deterministic*: two people running your query must get the identical row every time. What second `ORDER BY` key achieves that, and what does it cost you if the tie is a genuine data conflict rather than noise? 
- We would need to order the row by region to differentiate both rows. East will always come before North alphabetically, so the EAST option will always return instead if that is the case. The downstream analysis will always show the East customer, meaning we would lose data on the North. If the tie is a real data conflict we could:
    - flag it as ambiguious data that needs review.
    - Keep both rows as separate versions.
    - Ask the business which is the true most recent version. 

## Exercise 3: Fan out
**Prediction**
- My predction is that the total revenue is 2,850

**Reasoning**
-  I addded the order_total revenue as is from the Orders table.

**Answer**
-  The answer was 2,850.

1) Explain the inflation factor. Which order contributes the most error, and why that one?
- Order 105 has 4 line items in order_items. When you join orders to order_items and sum order_total, order 105's $600 gets counted 4 times (once per line item row) instead of 1 time. That's 3 extra counts × $600 = $1,800 of the $2,900 inflation. The fix is to sum item_amount, which is already at the line-item grain and doesn't duplicate.

2) Now produce revenue **by category** — which requires the join. Get a correct answer, and prove it's correct by reconciling against a total you trust.
- The results were:
  PARTS: 1300.00
  SAFETY: 550.00
  TOOLS: 1000.00
 I then ran a query to find the sum of revenue for the categories and it resulted in the same number for the total revenue, meaning the results for the categories were correct. 

  3) State the rule you'd give a junior teammate in one sentence, starting with "Before you aggregate across a join, ..."
  - Before you aggregate accross a join, aggregate the detail table to its grain first, then join to the fact table and aggregate there. Never sum a fact table column after joining to detail or else you will count multiple times. 

## Exercise 4: Declare the grain
**Prediction**
customer_raw: one row per customer per updated_at
orders: one row per order
order_items: one row per line item?
orders + order_items joined: one row per order per line item?

1) For each, name the column set that enforces the grain.
customer_raw: one row per customer per updated_at
- customer_id
- updated_at
orders: one row per order
- order_id
order_items: one row per line item
- item_id
orders + order_items joined: one row per order per line item
- order_id
- item_id

2) - Which of the four grains is ambiguous as stated, and what question would you have to ask a stakeholder to resolve it?
- customer_raw is ambiguous. The grain says "one row per customer per updated_at", but customer 4 has two rows with the same customer_id AND the same updated_at (2026-02-01 08:00:00). This violates the grain.

- Question for stakeholder: "When a customer has multiple updates at the exact same timestamp, should we keep both rows, or keep only one? If only one, which?"

## Exercise 5: Write the test, not just the query
**Query**
SELECT customer_id, count(*) AS n
FROM <your_clean_dim>
GROUP BY 1
HAVING count(*) > 1;

**Prediction**
- My prediction is