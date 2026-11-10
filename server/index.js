const express = require("express");
const cors = require("cors");
require("dotenv").config();

const toolsRouter = require("./routes/tools");
const membersRouter = require("./routes/members");
const loansRouter = require("./routes/loans");

const app = express();
app.use(cors());
app.use(express.json());

app.use("/api/tools", toolsRouter);
app.use("/api/members", membersRouter);
app.use("/api/loans", loansRouter);

// The week's running feature - POST /api/ask - is added here on Day 2,
// then extended in place through Day 5. It does not exist yet.

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Neighbourhood Tool Library API listening on port ${PORT}`);
});

module.exports = app;
