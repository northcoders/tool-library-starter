const express = require("express");
const loans = require("../data/loans");

const router = express.Router();

router.get("/", (req, res) => {
  res.json(loans);
});

router.get("/overdue", (req, res) => {
  const today = new Date().toISOString().slice(0, 10);
  const overdue = loans.filter((l) => l.returnedDate === null && l.dueDate < today);
  res.json(overdue);
});

module.exports = router;
