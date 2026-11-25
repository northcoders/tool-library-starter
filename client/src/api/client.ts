import type { ApiErrorBody } from "../types";

// Requests go to /api/... on the same origin; the Vite dev server forwards
// them to the FastAPI server (see vite.config.ts).
const BASE_URL = "";

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

const isApiErrorBody = (body: unknown): body is ApiErrorBody =>
  typeof body === "object" &&
  body !== null &&
  "detail" in body &&
  typeof body.detail === "string";

// Turns a failed response into an ApiError, using the server's "detail"
// message when there is one.
export const toApiError = async (response: Response): Promise<ApiError> => {
  let message = `Request failed with status ${response.status}`;
  try {
    const body: unknown = await response.json();
    if (isApiErrorBody(body)) message = body.detail;
  } catch {
    // Not JSON: keep the generic message.
  }
  return new ApiError(message, response.status);
};

export const apiGet = async <T>(path: string, signal?: AbortSignal): Promise<T> => {
  const response = await fetch(`${BASE_URL}${path}`, { signal });

  if (!response.ok) throw await toApiError(response);

  return (await response.json()) as T;
};

export const apiPost = async <T>(
  path: string,
  body: unknown,
  signal?: AbortSignal,
): Promise<T> => {
  const response = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal,
  });

  if (!response.ok) throw await toApiError(response);

  return (await response.json()) as T;
};
