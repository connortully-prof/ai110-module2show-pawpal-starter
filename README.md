# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Example of the generated plan shown in the app:

```
Daily plan for Mochi is ready.
Planned time: 50 of 60 minutes

Included tasks
- Morning walk (30 min, priority: high)
- Medication (20 min, priority: high)

Why this plan was chosen
- Morning walk was selected because it has a high priority and fits within the remaining time.
- Medication was selected because it has a high priority and fits within the remaining time.

Skipped tasks
- Feeding
```

Terminal demo output from running main.py:

```
Today's Schedule
====================
- Morning walk (30 min, high)
- Litter cleanup (15 min, high)
- Feeding (10 min, medium)
```

## 🧪 Testing PawPal+

```bash
.venv\Scripts\python -m pytest -q
```

Sample test output:

```
5 passed in 0.06s
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting by time | Scheduler.sort_by_time() | Orders tasks by their scheduled time string so the day is easier to read |
| Filtering by pet/status | Scheduler.filter_tasks() | Filters tasks by pet name and completed/pending state |
| Conflict detection | Scheduler.detect_conflicts() | Warns when multiple tasks share the same scheduled time |
| Recurring tasks | Task.mark_complete() | Creates a next occurrence for daily or weekly tasks when the current one is completed |

## 📸 Demo Walkthrough

1. Enter the owner's name and the pet's name/species.
2. Add one or more care tasks with a duration and priority.
3. Adjust the available minutes for the day.
4. Click Generate schedule to see the selected tasks and the explanation for each choice.
5. Edit or remove tasks and regenerate the plan to compare different outcomes.

**Screenshot or video** *(optional)*: Add a screenshot of the Streamlit app once you run it locally.
