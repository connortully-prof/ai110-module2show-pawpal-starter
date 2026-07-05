# PawPal+ 

PawPal+ is a Streamlit-based pet care planning app that helps a busy pet owner organize daily tasks for their pets. The system combines a simple Python backend with an interactive user interface so owners can add pet details, define care tasks, and receive a practical daily schedule.

## Project Goal

The goal of PawPal+ is to make pet care more manageable by turning a list of tasks into a structured plan. The app considers task priority, duration, scheduled time, and available daily minutes, and it can also warn about scheduling conflicts and generate recurring follow-up tasks.

## Key Features

- Add and manage owner and pet information
- Create care tasks with a title, duration, priority, and optional scheduled time
- Generate a daily plan based on available time and task importance
- Sort tasks by time and filter them by pet or completion status
- Detect scheduling conflicts for tasks that share the same time slot
- Support recurring daily or weekly tasks through the backend logic
- Display the plan and scheduling insights in a clear Streamlit interface

## Project Structure

- [app.py](app.py) — Streamlit user interface
- [pawpal_system.py](pawpal_system.py) — backend classes and scheduling logic
- [main.py](main.py) — terminal demo script for the scheduler
- [tests/test_pawpal.py](tests/test_pawpal.py) — automated tests for core behaviors
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

## Example Output

```text
Today's Schedule
====================
- Morning walk (30 min, high)
- Litter cleanup (15 min, high)
- Feeding (10 min, medium)
```

## Smarter Scheduling

| Feature | Method | Description |
|---------|--------|-------------|
| Sorting by time | Scheduler.sort_by_time() | Orders pending tasks by their scheduled time |
| Filtering | Scheduler.filter_tasks() | Filters tasks by pet name and completion status |
| Conflict detection | Scheduler.detect_conflicts() | Warns when multiple tasks share the same time |
| Recurring tasks | Task.mark_complete() | Creates a new follow-up task for daily or weekly items |

## Testing

Run the test suite with:

```bash
.venv\Scripts\python -m pytest -q
```

The suite verifies:
- task completion behavior
- adding tasks to a pet
- time-based sorting
- filtering by pet and status
- recurring task creation
- conflict detection

Example test output:

```text
.........                                                                [100%]
9 passed in 0.06s
```

Confidence level: ⭐⭐⭐⭐☆

## Demo Walkthrough

1. Open the app in the browser and enter the owner's name.
2. Add one or more pets and then add care tasks for each pet.
3. Set the available minutes for the day and generate a schedule.
4. Review the sorted tasks, pending tasks, and any conflict warnings shown by the scheduler.
5. Edit or remove tasks and regenerate the plan to compare different outcomes.

## Reflection

This project demonstrates how a small object-oriented Python system can be connected to a user-facing interface and extended with practical scheduling behaviors. The implementation balances clarity and usefulness by using lightweight algorithms that are easy to understand and test.
