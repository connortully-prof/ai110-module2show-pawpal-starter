# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the agent to build the PawPal+ scheduling app end to end, including the backend scheduler, Streamlit UI, tests, and documentation updates.

**What did the agent do?**

The agent created the scheduler logic in scheduler.py, connected the app to the backend in app.py, added unit tests for priority-based scheduling, updated the UML diagram, and helped fix pytest import issues and Streamlit startup issues.

**What did you have to verify or fix manually?**

I verified the scheduler behavior by running pytest, confirmed the app should be launched with streamlit run rather than python app.py, and checked that the UML diagram matched the implemented code and app flow.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | GitHub Copilot agent | GitHub Copilot agent |
| **Prompt** | "Build the PawPal+ scheduler and connect it to the Streamlit app." | "Fix pytest import issues and make the Streamlit app run correctly." |
| **Response summary** | Produced a working scheduler, UI integration, and tests quickly. | Helped resolve environment-specific issues such as import path setup and correct Streamlit startup. |
| **What was useful** | Fast implementation and code generation. | Good debugging support for toolchain and runtime issues. |
| **Problems noticed** | Needed manual verification to ensure the UML and behavior matched the code. | Required a follow-up check to confirm the fix worked in the actual terminal environment. |
| **Decision** | I used the first approach for the main implementation because it was the most efficient and produced the correct app structure. |

**Which approach did you use in your final implementation and why?**

I used the implementation-focused approach for the main build because it created the scheduler, UI, and tests in a compact and reliable way. I then verified everything manually through pytest and by launching the app with Streamlit.
