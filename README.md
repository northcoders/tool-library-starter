# Neighbourhood Tool Library — Starter App

The shared codebase for the AI/ML week. A small Express API over three seeded datasets (tools, members, loan records), plus a minimal React client. It starts as an ordinary CRUD API on Day 2 and gets one LLM endpoint added and extended every day through Day 5.

## Structure

```
tool-library-starter/
  server/
    index.js          Express app entry point
    llm.js             provider-agnostic LLM wrapper (see below)
    data/               seed data: tools, members, loans
    routes/             existing CRUD routes (tools, members, loans)
  client/               minimal Vite + React app (proxies /api to the
                        server); the chat UI is built here on Day 4
  eval-questions.md      the week's running evaluation question set
  .env.example
```

## Setup

Server:

```
cd server
npm install
cp ../.env.example .env   # fill in your LLM provider's details
npm run dev
```

Client:

```
cd client
npm install
npm run dev
```

## The `llm.js` wrapper

Every LLM call this week goes through `server/llm.js`, not a vendor SDK directly. It exposes three functions:

- `sendMessage({ system, messages, temperature, topP, maxTokens, tools })` resolves to the model's reply message (`{ role, content, tool_calls? }`).
- `streamMessage({ system, messages, ... })` is an async generator that yields the reply a few tokens at a time.
- `embed(text)` resolves to an array of numbers (a vector) representing the meaning of `text`.

Chat calls use a generic OpenAI-compatible REST shape, which a wide range of providers and gateways support. Point `.env`'s `LLM_API_BASE`, `LLM_API_KEY` and `LLM_MODEL` at whichever provider you're using; nothing else in this repo needs to change.

Embeddings run **locally by default** (`EMBED_PROVIDER=local`), using a small open model through `@huggingface/transformers`. That needs no key and costs nothing. The model (~25MB) downloads the first time `embed()` runs, so run it once before Day 3's session. Set `EMBED_PROVIDER=api` and `LLM_EMBED_MODEL` to use a provider's embeddings endpoint instead.

Instructors: confirm these three functions actually work against your chosen provider before Day 2 — swap the `.env` values, don't touch `llm.js` itself.

## What gets added, day by day

- **Day 2:** `POST /api/ask` — a single LLM endpoint, ungrounded. `eval-questions.md` gets its first entries and baseline run.
- **Day 3:** the same endpoint, now grounded in the tool catalogue via embeddings and similarity search (with no member names or emails in what gets embedded), plus a no-match threshold.
- **Day 4:** the same `POST /api/ask`, now streaming its answer as plain text into a React chat UI in `client/`, plus one function-calling tool (`lookupTool`) in a single round trip.
- **Day 5:** hardening — no new endpoints, fixes and edge-case handling only.

## Seed data shape

`server/data/tools.js` — id, name, category, description, loanPeriodDays, available.
`server/data/members.js` — id, name, email, joinedDate.
`server/data/loans.js` — id, toolId, memberId, borrowedDate, dueDate, returnedDate (`null` while still out).
