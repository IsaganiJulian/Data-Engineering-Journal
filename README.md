# data-engineering-journal

A working log of my transition from data science into data engineering.

I'm a data science graduate rebuilding my fundamentals with the specific goal of
writing pipelines that stay correct when nobody is watching them. This repo is
the evidence, not the summary — it contains the problems I got wrong, the
reasoning that fixed them, and the projects where I applied it.

Started 31 July 2026.

---

## How this is organized

| Directory | What's in it |
|---|---|
| `log/` | One dated entry per working session. What I attempted, what broke, what I changed, what I still can't explain. |
| `drills/` | Focused exercises on one concept. Small, disposable, heavily commented. |
| `concepts/` | Short explainers written from memory, no notes. If I can't write it, I don't know it. |
| `projects/` | Complete builds with a stated problem, a design decision log, and tests. |

## Current focus

Working through fundamentals in priority order, based on a baseline diagnostic
taken 31 July ([results](log/2026-07-31-baseline.md)):

- [ ] **SQL as a correctness discipline** — NULL semantics, deterministic deduplication, join fan-out
- [ ] **Grain** — declaring what one row represents before writing any DDL
- [ ] **Idempotency** — making a rerun leave the same state as a first run
- [ ] Dimensional modeling — star schemas, SCD Type 2
- [ ] Data quality — assertions that fail loudly at ingestion boundaries
- [ ] *Deferred:* orchestration (Airflow), distributed compute (Spark), streaming

Deferrals are deliberate. Orchestration schedules pipelines that are already
correct; I want to be able to reason about correctness before I automate it.

## Log index

| Date | Session | Focus |
|---|---|---|
| 2026-07-31 | [Baseline diagnostic](log/2026-07-31-baseline.md) | Establishing what I actually know |

## A note on what's here

Entries include things I got wrong and haven't yet fixed. That's intentional.
A log that only records successes isn't a log, it's a brochure — and it can't
show the thing I'd most want a hiring manager to see, which is how I work a
problem I don't immediately understand.
