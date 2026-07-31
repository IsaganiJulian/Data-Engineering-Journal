# projects/

Complete builds. A drill practices one concept; a project has a stated problem,
real design decisions, and tests.

Every project directory contains:

- `README.md` — the problem, the design, the tradeoffs I made and rejected
- `DECISIONS.md` — a running log of choices, each with the alternative I didn't pick
- `tests/` — assertions that fail when the data is wrong, not just when the code is
- runnable source

`DECISIONS.md` is the one hiring managers read. Anyone can produce working code;
what's scarce is being able to say why it's shaped the way it is.

## Queue

- [ ] **01 — Idempotent local pipeline.** A messy daily vendor drop, ingested,
      modeled and tested, that produces identical output no matter how many
      times it is rerun. Python + DuckDB, no cloud, no orchestrator.
