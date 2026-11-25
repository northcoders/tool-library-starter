# Neighbourhood Tool Library — Starter App

The shared codebase for the AI/ML week. A small FastAPI app over three seeded datasets (tools, members, loan records), plus a minimal React + TypeScript client. It starts as an ordinary read-only API on Day 2 and gets one LLM endpoint added and extended every day through Day 5.

## Structure

```
tool-library-starter/
  server/
    main.py            FastAPI app: every route lives here
    llm.py             provider-agnostic LLM wrapper (see below)
    data/              seed data: tools, members, loans
    scratch/           small scripts you run by hand (hello_llm.py)
    tests/             pytest tests for the existing routes
    requirements.txt
  client/              minimal Vite + React + TypeScript app (proxies
                       /api to the server); the chat UI is built here
                       on Day 4
    src/api/client.ts  shared fetch helpers (apiGet, apiPost, ApiError)
    src/types.ts       types for the API's request and response bodies
  eval-questions.md    the week's running evaluation question set
  .env.example
```

## Setup

Server (Python 3.12 or newer):

```
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env          # fill in your LLM provider's details
uvicorn main:app --reload        # http://localhost:8000
```

Activate the virtual environment in every new terminal before running anything in `server/`.

```
pytest                           # runs the tests in tests/
python -m scratch.hello_llm      # checks your provider details work
```

Scripts in `scratch/` are run as modules from `server/` (`python -m scratch.<name>`, no `.py`), so they can import `llm` and `data`.

Client (Day 4):

```
cd client
npm install
npm run dev                      # http://localhost:5173
```

`npm run build`, `npx tsc --noEmit` and `npm run lint` should all pass.

## The `llm.py` wrapper

Every LLM call this week goes through `server/llm.py`, not a vendor SDK directly. It exposes three functions:

- `await send_message(system=..., messages=..., temperature=..., top_p=..., max_tokens=..., tools=...)` returns the model's reply message as a dict (`{"role", "content", "tool_calls"?}`).
- `stream_message(system=..., messages=..., ...)` is an async generator that yields the reply a few tokens at a time (`async for piece in stream_message(...)`).
- `embed(text)` returns a list of numbers (a vector) representing the meaning of `text`.

If the provider answers with an error, `send_message` and `stream_message` raise `LLMAPIError("LLM API error <status>: <body>")`. If it can't be reached at all, they raise `ConnectionError`. Neither has a time limit of its own.

Chat calls use a generic OpenAI-compatible REST shape, which a wide range of providers and gateways support. Point `.env`'s `LLM_API_BASE`, `LLM_API_KEY` and `LLM_MODEL` at whichever provider you're using; nothing else in this repo needs to change. `LLM_REASONING_EFFORT` is optional: some models spend tokens on hidden "thinking" before they answer, and `none` switches that off on providers that support it (this course's NVIDIA model does).

Embeddings run **locally by default** (`EMBED_PROVIDER=local`), using a small open model through `fastembed`. That needs no key and costs nothing. The model (~90MB) downloads the first time `embed()` runs and is cached in `~/.cache/fastembed`, so run it once before Day 3's session. Set `EMBED_PROVIDER=api` and `LLM_EMBED_MODEL` to use a provider's embeddings endpoint instead.

Instructors: confirm these three functions actually work against your chosen provider before Day 2 — swap the `.env` values, don't touch `llm.py` itself.

## What gets added, day by day

- **Day 2:** `POST /api/ask` — a single LLM endpoint, ungrounded. `eval-questions.md` gets its first entries and baseline run.
- **Day 3:** the same endpoint, now grounded in the tool catalogue via embeddings and similarity search (with no member names or emails in what gets embedded), plus a no-match threshold.
- **Day 4:** the same `POST /api/ask`, now streaming its answer as plain text into a React chat UI in `client/`, plus one function-calling tool (`lookup_tool`) in a single round trip.
- **Day 5:** hardening — no new endpoints, fixes and edge-case handling only.

## API conventions

- Responses are wrapped in a named key: `GET /api/tools` returns `{"tools": [...]}`, `GET /api/tools/3` returns `{"tool": {...}}`.
- Errors are `{"detail": "..."}` with a matching status code. An invalid request (for example `/api/tools/abc`) is a `400` with `{"detail": "Bad request"}`.
- The one exception, from Day 4: a successful `POST /api/ask` streams plain text rather than JSON.

## Seed data shape

`server/data/tools.py`: `id`, `name`, `category`, `description`, `loan_period_days`, `available`.
`server/data/members.py`: `id`, `name`, `email`, `joined_date`.
`server/data/loans.py`: `id`, `tool_id`, `member_id`, `borrowed_date`, `due_date`, `returned_date` (`None` while still out).
