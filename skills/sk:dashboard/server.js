// ShipKit Dashboard — zero-dependency Node.js server
const http = require("http");
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const PORT =
  parseInt(process.argv.find((_, i, a) => a[i - 1] === "--port") || process.env.PORT, 10) || 3333;

const HARD_GATES = new Set([12, 14, 16, 20, 22]);
const OPTIONALS = new Set([4, 5, 8, 18, 27]);

function stripMd(s) {
  return (s || "").replace(/\*\*/g, "").replace(/`/g, "").trim();
}

function discoverWorktrees() {
  try {
    const raw = execSync("git worktree list", { encoding: "utf8" });
    return raw
      .trim()
      .split("\n")
      .filter(Boolean)
      .map((line) => {
        const match = line.match(/^(.+?)\s+[0-9a-f]+\s+\[(.+?)\]$/);
        if (!match) return null;
        return { path: match[1].trim(), branch: match[2].trim() };
      })
      .filter(Boolean);
  } catch {
    return [{ path: process.cwd(), branch: "unknown" }];
  }
}

function parseWorkflowStatus(worktreePath) {
  const filePath = path.join(worktreePath, "tasks", "workflow-status.md");
  try {
    const lines = fs.readFileSync(filePath, "utf8").split("\n");

    let headerFound = false;
    let separatorSkipped = false;
    const steps = [];

    for (const line of lines) {
      if (!headerFound) {
        if (line.includes("| # |")) headerFound = true;
        continue;
      }
      if (!separatorSkipped) {
        separatorSkipped = true;
        continue;
      }
      const cells = line.split("|").slice(1, -1).map((c) => c.trim());
      if (cells.length < 3) continue;

      const number = parseInt(cells[0], 10);
      if (isNaN(number)) continue;

      const rawStep = stripMd(cells[1]);
      const cmdMatch = rawStep.match(/\((.+?)\)/);
      const command = cmdMatch ? cmdMatch[1].trim() : "";
      const name = rawStep.replace(/\s*\(.+?\)\s*/, "").trim();

      steps.push({
        number,
        name,
        command,
        status: stripMd(cells[2]),
        notes: stripMd(cells[3]),
        isHardGate: HARD_GATES.has(number),
        isOptional: OPTIONALS.has(number),
      });
    }
    return steps;
  } catch (err) {
    if (err.code === "ENOENT") return [];
    process.stderr.write(`Error parsing workflow-status.md: ${err.message}\n`);
    return [];
  }
}

function parseTodo(worktreePath) {
  const filePath = path.join(worktreePath, "tasks", "todo.md");
  try {
    const lines = fs.readFileSync(filePath, "utf8").split("\n");

    let taskName = "";
    let done = 0;
    let total = 0;

    for (const line of lines) {
      if (!taskName && line.startsWith("# TODO")) {
        const dashIdx = line.lastIndexOf("—");
        if (dashIdx !== -1) taskName = line.slice(dashIdx + 1).trim();
        else taskName = line.replace(/^#\s*TODO\s*/, "").trim();
      }
      if (/^\s*-\s*\[x\]/i.test(line)) { done++; total++; }
      else if (/^\s*-\s*\[\s\]/.test(line)) total++;
    }
    return { taskName, todosDone: done, todosTotal: total };
  } catch (err) {
    if (err.code === "ENOENT") return { taskName: "", todosDone: 0, todosTotal: 0 };
    process.stderr.write(`Error parsing todo.md: ${err.message}\n`);
    return { taskName: "", todosDone: 0, todosTotal: 0 };
  }
}

function buildStatus() {
  const worktrees = discoverWorktrees();
  return worktrees.map((wt) => {
    const steps = parseWorkflowStatus(wt.path);
    const todo = parseTodo(wt.path);

    let currentStep = 0;
    let totalDone = 0;
    let totalSkipped = 0;
    for (const s of steps) {
      if (s.status === ">> next <<") currentStep = s.number;
      if (s.status === "done") totalDone++;
      if (s.status === "skipped") totalSkipped++;
    }

    return {
      path: wt.path,
      branch: wt.branch,
      taskName: todo.taskName,
      todosDone: todo.todosDone,
      todosTotal: todo.todosTotal,
      currentStep,
      totalDone,
      totalSkipped,
      totalSteps: steps.length,
      steps,
    };
  });
}

const server = http.createServer((req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");

  if (req.method === "GET" && req.url === "/") {
    const htmlPath = path.join(__dirname, "dashboard.html");
    try {
      const html = fs.readFileSync(htmlPath, "utf8");
      res.writeHead(200, { "Content-Type": "text/html" });
      res.end(html);
    } catch {
      res.writeHead(404, { "Content-Type": "text/plain" });
      res.end("dashboard.html not found");
    }
    return;
  }

  if (req.method === "GET" && req.url === "/api/status") {
    try {
      const data = buildStatus();
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify(data));
    } catch (err) {
      process.stderr.write(`Error building status: ${err.message}\n`);
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "Internal server error" }));
    }
    return;
  }

  res.writeHead(404, { "Content-Type": "text/plain" });
  res.end("Not found");
});

server.listen(PORT, () => {
  console.log(`ShipKit Dashboard running at http://localhost:${PORT}`);
});
