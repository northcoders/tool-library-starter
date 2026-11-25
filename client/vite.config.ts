import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// Requests to /api/* are forwarded to the FastAPI server, so the React
// app can call fetch("/api/ask") without CORS or hard-coded ports.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
