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

1. Which customer breaks it, and why?
- Customer 4 breaks the pipeline because there are two rows with the same time stamps. The MAX finds the timestamp and since both rows match on the join, they will both be reuruned and come back. 

2. Rewrite with `ROW_NUMBER()`. Does the naive version fix the problem, or hide it?
- The naive version hides the problem. The value should be 5, instead the naive version returns 6. When using ROW_NUMBER, it partions by the customer_id and the updated_at time based on DESC.

3.  Make it *deterministic*: two people running your query must get the identical row every time. What second `ORDER BY` key achieves that, and what does it cost you if the tie is a genuine data conflict rather than noise? 
- We would need to order the row by region to differentiate both rows. East will always come before North alphabetically, so the EAST option will always return instead if that is the case. The downstream analysis will always show the East customer, meaning we would lose data on the North. If the tie is a real data conflict we could:
    - flag it as ambiguious data that needs review.
    - Keep both rows as separate versions.
    - Ask the business which is the true most recent version. 