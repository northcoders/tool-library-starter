const express = require("express");
const tools = require("../data/tools");

const router = express.Router();

router.get("/", (req, res) => {
  res.json(tools);
});

router.get("/:id", (req, res) => {
  const tool = tools.find((t) => t.id === Number(req.params.id));
  if (!tool) return res.status(404).json({ error: "Tool not found" });
  res.json(tool);
});

module.exports = router;
