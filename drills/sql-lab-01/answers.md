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