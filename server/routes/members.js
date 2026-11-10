const express = require("express");
const members = require("../data/members");

const router = express.Router();

router.get("/", (req, res) => {
  res.json(members);
});

router.get("/:id", (req, res) => {
  const member = members.find((m) => m.id === Number(req.params.id));
  if (!member) return res.status(404).json({ error: "Member not found" });
  res.json(member);
});

module.exports = router;
