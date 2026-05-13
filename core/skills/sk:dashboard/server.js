// ShipKit Dashboard — zero-dependency Node.js server
const http = require("http");
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const PORT =
  parseInt(process.argv.find((_, i, a) => a[i - 1] === "--port") || process.env.PORT, 10) || 3333;

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
        const branchMatch = line.match(/^(.+?)\s+[0-9a-f]+\s+\[(.+?)\]$/);
        if (branchMatch) return { path: branchMatch[1].trim(), branch: branchMatch[2].trim() };
        const detachedMatch = line.match(/^(.+?)\s+[0-9a-f]+\s+\((.+?)\)$/);
        if (detachedMatch) return { path: detachedMatch[1].trim(), branch: detachedMatch[2].trim() };
        return null;
      })
      .filter(Boolean);
  } catch {
    return [{ path: process.cwd(), branch: "unknown" }];
  }
}

const STOP_HEADERS = new Set(["Verification", "Acceptance Criteria", "Risks", "Change Log", "Summary"]);

function parseTodo(worktreePath) {
  const filePath = path.join(worktreePath, "tasks", "todo.md");
  try {
    const lines = fs.readFileSync(filePath, "utf8").split("\n");

    let taskName = "";
    let done = 0;
    let total = 0;
    let section = "";
    let inMilestones = false;
    let pastMilestones = false;
    const todoItems = [];

    for (const line of lines) {
      if (!taskName && line.startsWith("# TODO")) {
        const dashIdx = line.indexOf("—");
        if (dashIdx !== -1) taskName = line.slice(dashIdx + 1).trim();
        else taskName = line.replace(/^#\s*TODO\s*/, "").trim();
      }

      if (line.startsWith("## ")) {
        const header = line.slice(3).trim();
        if (header.startsWith("Milestone")) {
          inMilestones = true;
          section = header;
        } else if (inMilestones && STOP_HEADERS.has(header)) {
          pastMilestones = true;
        }
      }

      if (/^\s*-\s*\[x\]/i.test(line)) {
        done++;
        total++;
        if (inMilestones && !pastMilestones) {
          todoItems.push({ text: stripMd(line.replace(/^\s*-\s*\[x\]\s*/i, "")), done: true, section });
        }
      } else if (/^\s*-\s*\[\s\]/.test(line)) {
        total++;
        if (inMilestones && !pastMilestones) {
          todoItems.push({ text: stripMd(line.replace(/^\s*-\s*\[\s\]\s*/, "")), done: false, section });
        }
      }
    }
    return { taskName, todosDone: done, todosTotal: total, todoItems };
  } catch (err) {
    if (err.code === "ENOENT") return { taskName: "", todosDone: 0, todosTotal: 0, todoItems: [] };
    process.stderr.write(`Error parsing todo.md: ${err.message}\n`);
    return { taskName: "", todosDone: 0, todosTotal: 0, todoItems: [] };
  }
}

function buildStatus() {
  const worktrees = discoverWorktrees();
  return worktrees.map((wt) => {
    const todo = parseTodo(wt.path);

    return {
      path: wt.path,
      branch: wt.branch,
      taskName: todo.taskName,
      todosDone: todo.todosDone,
      todosTotal: todo.todosTotal,
      todoItems: todo.todoItems,
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
