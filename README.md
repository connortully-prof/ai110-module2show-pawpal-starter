# PawPal+

PawPal+ is a Streamlit-based pet care planning app that helps a busy owner turn care tasks into a realistic daily schedule. The system combines a Python backend with an interactive UI so users can add pets and tasks, review scheduling recommendations, and keep their information between runs.

## Project Goal

The app makes pet care easier by organizing tasks around priority, available time, scheduled windows, and potential conflicts. It goes beyond the basic requirement by supporting priority-first scheduling, next-slot planning, and JSON persistence.

## Key Features

- Add and manage owner and pet information
- Create care tasks with a title, duration, priority, and optional scheduled time
- Generate a daily plan based on available time and task importance
- Sort tasks by priority first, then by time
- Find the next available slot for a new task
- Detect scheduling conflicts for tasks that share the same time slot
- Support recurring daily or weekly tasks through the backend logic
- Save pets and tasks between runs using data.json
- Display the plan and scheduling insights with emoji-based formatting in the UI and CLI

## Project Structure

- [app.py](app.py) — Streamlit user interface
- [pawpal_system.py](pawpal_system.py) — backend classes and scheduling logic
- [main.py](main.py) — terminal demo script for the scheduler
- [tests/test_pawpal.py](tests/test_pawpal.py) — automated tests for core behaviors
- [data.json](data.json) — persisted owner, pet, and task data
- [diagrams/uml_final.mmd](diagrams/uml_final.mmd) — final Mermaid UML diagram

## Getting Started

### Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Run the Streamlit App

```bash
streamlit run app.py
```

### Run the Terminal Demo

```bash
python main.py
```

## Persistence Workflow

PawPal+ stores owner, pet, and task data in [data.json](data.json). The workflow is:

1. Start the app and load the existing profile from data.json.
2. Add or edit pets and tasks in the UI.
3. Every save action writes the updated owner object back to data.json.
4. On the next launch, the app reloads the saved data automatically.

The persistence logic is implemented in [pawpal_system.py](pawpal_system.py) through the Owner.save_to_json() and Owner.load_from_json() methods.

## Example CLI Output

```text
📅 Today's Schedule
========================
- 🔴 Morning walk (30 min, HIGH)
- 🟡 Feeding (10 min, MEDIUM)
- 🟢 Water plants (5 min, LOW)

🕒 Sorted by priority and time
- 🔴 Morning walk at 09:30
- 🟡 Feeding at 08:00
- 🟢 Water plants at 07:00

✨ Suggested next slot
- 08:00
```

## Smarter Scheduling

| Feature | Method | Description |
|---------|--------|-------------|
| Priority-first ordering | Scheduler.sort_by_priority_then_time() | Orders tasks by priority first, then by scheduled time |
| Next available slot | Scheduler.find_next_available_slot() | Finds the earliest open time window for a new task |
| Filtering | Scheduler.filter_tasks() | Filters tasks by pet name and completion status |
| Conflict detection | Scheduler.detect_conflicts() | Warns when multiple tasks share the same time |
| Recurring tasks | Task.mark_complete() | Creates a new follow-up task for daily or weekly items |

## Formatting Features

The UI and CLI now use lightweight formatting enhancements to make the results easier to scan:

- Emojis for status and task categories in the Streamlit interface
- Clear task badges for priority levels in the terminal demo
- A simple, structured summary of scheduled items and conflicts

These visual cues come from the formatting logic in [app.py](app.py) and [main.py](main.py) rather than a heavy dependency.

## Testing

Run the test suite with:

```bash
.venv\Scripts\python -m pytest -q
```

The suite verifies:
- task completion behavior
- adding tasks to a pet
- time-based sorting
- priority-first scheduling
- next-available-slot planning
- persistence through JSON round-tripping
- filtering by pet and status
- recurring task creation
- conflict detection

Example test output:

```text
...........                                                              [100%]
12 passed in 0.40s
```

Confidence level: ⭐⭐⭐⭐☆

## Demo Walkthrough

1. Open the app in the browser and enter the owner's name.
2. Add one or more pets and then add care tasks for each pet.
3. Set the available minutes for the day and generate a schedule.
4. Review the sorted tasks, pending tasks, conflict warnings, and the suggested next slot.
5. Edit or remove tasks and regenerate the plan to compare different outcomes.

## Reflection

This project demonstrates how a small object-oriented Python system can be connected to a user-facing interface and extended with practical scheduling behaviors. The implementation balances clarity and usefulness by using lightweight algorithms that are easy to understand, test, and save across runs.
