# concepts/

Short explainers, written **from memory with no notes open**, then checked.

This directory exists to fix one specific diagnosed weakness: giving correct
answers I can't defend. Recognition is cheap — I can pick the right option from
four. Generation is the thing interviews and the job actually test.

## Rules

1. Write the whole thing before opening any reference.
2. Include a worked example with real numbers, not a definition.
3. End with "where this breaks" — the edge case, or the case where the usual
   advice is wrong.
4. Then check it. Mark corrections inline with `<!-- corrected: ... -->` rather
   than editing silently. The corrections are the interesting part.

Target length: one page. If it needs more, I don't understand it well enough yet.

## Queue

- [ ] Three-valued logic: why `NOT IN` with a NULL returns nothing
- [ ] Grain, and how to declare it
- [ ] Idempotent writes: overwrite-partition vs. MERGE
- [ ] Join fan-out and how to detect it before it ships
- [ ] SCD Type 2 versus Type 1
