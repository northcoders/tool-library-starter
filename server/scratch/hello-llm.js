// Checks your AI provider details in .env work.
// Run from the server/ folder with:  node scratch/hello-llm.js
require("dotenv").config();
const { sendMessage } = require("../llm");

async function main() {
  const reply = await sendMessage({
    system: "You are a helpful assistant. Reply in one short sentence.",
    messages: [{ role: "user", content: "Say hello to the Tool Library." }],
  });
  console.log(reply.content);
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
