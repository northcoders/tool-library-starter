// A small, provider-agnostic wrapper around an LLM API. Every task this
// week talks to the model through this module rather than a specific
// vendor SDK, so the mechanics (streaming, system prompts, structured
// output, embeddings) are the same regardless of which provider is behind
// it. Swap providers by changing the LLM_* environment variables -
// nothing in this module, or in any code that calls it, needs to change.
//
// Written against a generic OpenAI-compatible chat completions and
// embeddings REST shape, which a wide range of providers and gateways
// support.

const BASE_URL = process.env.LLM_API_BASE;
const API_KEY = process.env.LLM_API_KEY;
const MODEL = process.env.LLM_MODEL;
const EMBED_MODEL = process.env.LLM_EMBED_MODEL;

async function sendMessage({ system, messages, temperature = 0.7, topP = 1, maxTokens = 500, tools }) {
  const response = await fetch(`${BASE_URL}/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
    body: JSON.stringify({
      model: MODEL,
      temperature,
      top_p: topP,
      max_tokens: maxTokens,
      messages: [{ role: "system", content: system }, ...messages],
      ...(tools ? { tools } : {}),
    }),
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`LLM API error ${response.status}: ${body}`);
  }

  const data = await response.json();
  return data.choices[0].message;
}

async function* streamMessage({ system, messages, temperature = 0.7, topP = 1, maxTokens = 500 }) {
  const response = await fetch(`${BASE_URL}/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
    body: JSON.stringify({
      model: MODEL,
      temperature,
      top_p: topP,
      max_tokens: maxTokens,
      stream: true,
      messages: [{ role: "system", content: system }, ...messages],
    }),
  });

  if (!response.ok || !response.body) {
    const body = await response.text().catch(() => "");
    throw new Error(`LLM API error ${response.status}: ${body}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    const lines = buffer.split("\n");
    buffer = lines.pop();

    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed.startsWith("data:")) continue;
      const payload = trimmed.slice(5).trim();
      if (payload === "[DONE]") return;

      const chunk = JSON.parse(payload);
      const token = chunk.choices?.[0]?.delta?.content;
      if (token) yield token;
    }
  }
}

// Embeddings: by default these run locally, on your own machine, using a
// small open model (all-MiniLM-L6-v2, 384 dimensions) via
// @huggingface/transformers. That means no API key and no cost for Day 3,
// and it works the same no matter which chat provider you use (not every
// chat provider offers an embeddings endpoint). The model is downloaded once
// (~25MB) the first time embed() runs, then cached.
//
// Set EMBED_PROVIDER=api to call an OpenAI-compatible /embeddings endpoint
// instead (uses LLM_API_BASE, LLM_API_KEY and LLM_EMBED_MODEL).
const EMBED_PROVIDER = process.env.EMBED_PROVIDER || "local";
const LOCAL_EMBED_MODEL = "Xenova/all-MiniLM-L6-v2";

let localExtractor;

async function embedLocally(text) {
  if (!localExtractor) {
    const { pipeline } = await import("@huggingface/transformers");
    localExtractor = await pipeline("feature-extraction", LOCAL_EMBED_MODEL);
  }
  const output = await localExtractor(text, { pooling: "mean", normalize: true });
  return Array.from(output.data);
}

async function embedViaApi(text) {
  const response = await fetch(`${BASE_URL}/embeddings`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
    body: JSON.stringify({ model: EMBED_MODEL, input: text }),
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`LLM API error ${response.status}: ${body}`);
  }

  const data = await response.json();
  return data.data[0].embedding;
}

// Returns an array of numbers (a vector) representing the meaning of `text`.
async function embed(text) {
  return EMBED_PROVIDER === "api" ? embedViaApi(text) : embedLocally(text);
}

module.exports = { sendMessage, streamMessage, embed };
