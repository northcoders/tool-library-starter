import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Requests to /api/* are forwarded to the Express server, so the React
// app can call fetch("/api/ask") without CORS or hard-coded ports.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": "http://localhost:3000",
    },
  },
});
