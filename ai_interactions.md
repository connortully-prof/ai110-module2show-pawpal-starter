# AI Interactions Log

## Agent Workflow

| Item | Details |
|------|---------|
| Files modified | [app.py](app.py), [pawpal_system.py](pawpal_system.py), [main.py](main.py), [tests/test_pawpal.py](tests/test_pawpal.py), [README.md](README.md), [ai_interactions.md](ai_interactions.md) |
| What I asked the agent to do | Add JSON persistence, priority-first scheduling, a next-available-slot capability, richer UI formatting, and documentation updates for PawPal+. |
| What the agent completed | Implemented Owner.save_to_json()/load_from_json(), added priority-based sorting and next-slot planning in the scheduler, improved the Streamlit UI formatting, and updated the README and tests. |
| Manual corrections | I verified the new scheduling behavior with pytest, adjusted the time-slot logic to match the expected 15-minute increments, and confirmed the app still launches correctly with Streamlit. |

## Prompt Comparison

| Aspect | Prompt A | Prompt B |
|--------|----------|----------|
| Model / tool used | GitHub Copilot | GitHub Copilot |
| Prompt / task | “Add priority-first scheduling and JSON persistence to PawPal+.” | “Improve the CLI and UI formatting and add a next-available-slot algorithm.” |
| What was useful | The response gave a strong object-oriented structure for serialization and scheduling. | The response was helpful for explaining how to present the plan more clearly in the terminal and UI. |
| What was flawed | It needed a follow-up pass to ensure the persistence layer handled dataclasses cleanly. | It did not fully account for how time-based slot logic should behave around existing tasks. |
| Final decision | I used the first approach as the base implementation and refined the slot logic manually to match the project’s test expectations. |
