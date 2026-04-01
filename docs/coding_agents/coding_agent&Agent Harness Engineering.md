# Reference
## Courses
- 斯坦福大学 2025 年秋季课程 《The Modern Software Developer（CS146S）》
- 
## Open Source
- [learn-claude-code](https://github.com/shareAI-lab/learn-claude-code)
- [opened-claude-code](https://github.com/StarKnightt/Claude-Code)
- [opened-claude-code](https://github.com/michaelwfc/opened-claude-code/tree/main)

## Blogs

- [Zed 为什么不用自己造 Agent？OpenAI 架构师给出答案：Codex 重划 IDE × Coding Agent 的分工边界](https://www.infoq.cn/article/HFewc09HcZ1IaDyFj8D0)

- [My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey#step-5-engineer-the-harness)
这个词最早来自 Mitchell Hashimoto——HashiCorp 联合创始人、Terraform 的缔造者。他今年 2 月写了篇博客，把自己使用 AI 编程的进化拆成了六个阶段。第五个阶段叫 Engineer the Harness。


- [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- https://cobusgreyling.substack.com/p/the-rise-of-ai-harness-engineering
- https://birgitta.info/
- https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html





## Vedios
- [No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Horthy, HumanLayer](https://www.youtube.com/watch?v=rmvDxxNubIg)
- [Future-Proof Coding Agents – Bill Chen & Brian Fioca, OpenAI](https://www.youtube.com/watch?v=wVl6ZjELpBk)
- [OpenAI’s Michael Bolin on Codex, Harness Engineering, and the Real Future of Coding Agents](https://www.youtube.com/watch?v=6BAqgT3qe98)

## Podcasts

- [AI时代工程师的底牌是什么 | Michael Bolin | 前Meta E9 | 底层架构重构 | Meta Buck | 晋升教训 | Codex的诞生 | 工程师的核心价值](https://www.youtube.com/watch?v=w_XtnRX4mO0)
- [【人工智能】Agent Harness Engineering | Agent驾驭/管控工程 | 长时任务的缺陷 | 计算机的操作系统 | 通用型和垂直型 | 苦涩的教训 | 工程实践](https://www.youtube.com/watch?v=qua6FfJmydo&t=353s)




# Code Tools Comparison

## What These Tools *Are*

| Tool               | What it *fundamentally is*                                                                                                                                                              |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Claude Code**    | AI coding agent that *operates as an agent* in your terminal/IDE — it reads your codebase, edits files, runs commands, runs tests, and automates entire coding workflows. ([Claude][1]) |
| **OpenAI Codex**   | LLM trained for code generation; powers code writing and agent tasks (can be used as cloud agent). ([OpenAI][2])                                                                        |
| **GitHub Copilot** | AI pair programmer integrated into IDEs with real-time suggestions and (in newer modes) *agent-like task execution*. ([维基百科][3])                                                        |
| **Cursor**         | AI-enhanced **IDE (fork of VS Code)** with deep project understanding, multi-file refactors, and smart edits. ([维基百科][4])                                                               |

---

## Comparison Table (Claude Code vs Codex vs Copilot vs Cursor)

| **Aspect**                        | **Claude Code**                                                            | **OpenAI Codex**                                           | **GitHub Copilot**                                      | **Cursor**                                          |
| --------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------- |
| **Type**                          | *Agentic coding tool* (CLI + IDE + agent workflows)                        | *LLM code generator*                                       | *IDE code assistant / autocomplete*                     | *AI-enhanced coding IDE*                            |
| **Main Focus**                    | Full workflow automation: read, modify, test, commit, PR                   | Code generation from prompts, multi-task agent tasks       | Inline completion & suggestions                         | Real-time intelligent coding inside editor          |
| **Context Awareness**             | Reads full repo, dependencies, project context automatically ([Claude][1]) | Limited by model prompt/context                            | Integrated with IDE file but not full project semantics | Indexes project for refactor & rewrites ([维基百科][4]) |
| **Multi-File/Repo Changes**       | Yes — can plan & apply multi-file changes ([Claude API Docs][5])           | Yes (via API workflows but less seamless) ([OpenAI][2])    | Yes (via Copilot Chat / agent mode) ([维基百科][3])         | Yes — based on editor + AI logic ([维基百科][4])        |
| **Execution of Commands/Tests**   | Yes — can run tests, execute shell commands ([Claude API Docs][5])         | Not natively — needs custom tool integration ([OpenAI][2]) | Limited; mostly code suggestion, not automation         | Not a task executor (editor-centric)                |
| **Autonomy Level**                | *High* — agent can work until task completion ([Reddit][6])                | *Medium* — depends on integration                          | *Low*–*Medium* (recent agent modes) ([维基百科][3])         | *Low* (interactive)                                 |
| **IDE Integration**               | Terminal / VS Code / JetBrains ([Claude][1])                               | Via API or extensions                                      | Deep IDE integration (VS Code, JetBrains) ([维基百科][3])   | Built-in editor (fork of VS Code) ([维基百科][4])       |
| **Autonomous Workflows (Agents)** | Yes — CLI native agent workflows                                           | Possible with custom orchestration                         | Emerging via Copilot agent modes ([维基百科][3])            | No                                                  |
| **User Control (approval)**       | Explicit approval before file changes ([Claude API Docs][5])               | Depends on implementation                                  | Copilot *suggests*, user accepts                        | Real-time control                                   |
| **Best Use Case**                 | Large tasks (refactor, bug fix, PR automation)                             | Building custom code tools                                 | Interactive coding support                              | Live developer editing + context                    |
| **Typical UX**                    | Terminal or editor commands                                                | API responses                                              | In-IDE suggestions / chat                               | Editor UI with AI enhancements                      |

---

## Key Differences Explained

### **Claude Code — Agentic Workflow**

* Acts like a *coding agent* — not just text generation.
* Reads whole codebase, understands dependencies, can run commands and tests. ([Claude API Docs][5])
* Works where you work: terminal, IDE, Slack, etc. ([Claude][1])
* Designed for *large, multi-file tasks* and autonomous code changes.

**Summary:** *Code automation agent* — beyond simple suggestions.

---

### **OpenAI Codex — Foundational Model**

* Large language model specialized in generating code. ([OpenAI][2])
* Can be embedded in your own tools (CLIs, editors, agents).
* Not a standalone “product”; more like a *building block*.

**Summary:** *LLM engine* for code, not a full coding product.

---

### **GitHub Copilot — Pair Programmer**

* Works inside IDEs (VS Code, JetBrains) giving live suggestions. ([维基百科][3])
* Can generate small code snippets or larger blocks as you type.
* Newer “agent/assist” modes try to automate tasks inside IDE.

**Summary:** *Interactive suggestions inside editor.*

---

### **Cursor — AI Editor**

* Advanced AI editor (fork of VS Code) that deeply understands context. ([维基百科][4])
* Great for *multi-file refactoring* and *project-wide context*.

**Summary:** *AI-powered coding environment* focused on realtime editing.

---

##  Rough Categorization

| Category                    | Examples               |
| --------------------------- | ---------------------- |
| **LLM core model**          | OpenAI Codex           |
| **In-IDE coding assistant** | GitHub Copilot, Cursor |
| **Agentic coding agent**    | Claude Code            |

---

##  When to Use What

* **Daily development + inline help →** GitHub Copilot
* **Deep project edits + refactors →** Cursor or Claude Code
* **Automated workflows (end-to-end code tasks) →** Claude Code
* **Custom coding tools backend →** OpenAI Codex (as component)

---

###  Summary

* **Claude Code** isn’t just an IDE plugin — it’s an *agentic coding assistant* that can read a project, plan, edit, run tests, and produce commits autonomously. ([Claude API Docs][5])
* **OpenAI Codex** is the *model* that powers many code generation workflows. ([OpenAI][2])
* **GitHub Copilot** is your *AI pair programmer* inside IDEs. ([维基百科][3])
* **Cursor** is an *AI-enhanced editor* with deeper codebase semantics. ([维基百科][4])

---

If you want, I can also build a **feature roadmap matrix** showing when to choose each tool based on task complexity (e.g., bug fix vs full feature implementation).





