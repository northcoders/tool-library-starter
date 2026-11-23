# Eval Questions — Neighbourhood Tool Library Assistant

A fixed set of test questions, answered and recorded after every meaningful change to the `/api/ask` endpoint. Re-run the *same* questions each time rather than swapping them out, so the before/after comparison is real — this is the same instinct as writing a test before the code it tests, applied to output that isn't a simple assert.

This file is filled in for real in Day 2's sprint (Task 6). What follows is the shape to fill in, not pre-written content. Run the questions with `server/scratch/run_evals.py` (also written in Day 2 Task 6).

## Question set

<!-- 6 to 8 questions. Include at least:
     - three about the tool catalogue (tools.py can answer them);
     - one asking when a tool that's out on loan is due back (needs loans.py:
       Day 3's retrieval can't answer it, Day 4's tool call can);
     - one that's ambiguous;
     - one that's out of scope entirely (Day 3 uses it to test the no-match case).
     Write "Good answer looks like" BEFORE running anything. -->

1. **Q:**
   **Good answer looks like:**

2. **Q:**
   **Good answer looks like:**

3. **Q:**
   **Good answer looks like:**

4. **Q:**
   **Good answer looks like:**

5. **Q:**
   **Good answer looks like:**

6. **Q:**
   **Good answer looks like:**

7. **Q:** (optional)
   **Good answer looks like:**

8. **Q:** (optional)
   **Good answer looks like:**

## Run log

Every run starts with the same header line, so you always know which version of the code produced it:

`Run on <date> · commit <git rev-parse --short HEAD> · temperature <t>, top_p <p>`

Then, for each question: the answer, and a verdict of `good`, `vague`, `wrong` or `honest-unknown` (one line of reason for every `wrong`). From Day 3 on, also say whether it's **better, worse or the same** as the previous run, naming the fact that changed.

### Day 2 — baseline (ungrounded)

### Day 3 — grounded (RAG)

### Day 4 — tool-augmented

### Day 5 — hardened
