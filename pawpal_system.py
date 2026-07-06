from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import List


def _parse_time_to_minutes(value: str | None) -> int:
    if not value:
        return 24 * 60
    try:
        hours_str, minutes_str = value.split(":", 1)
        hours = int(hours_str)
        minutes = int(minutes_str)
        return hours * 60 + minutes
    except ValueError:
        return 24 * 60


def _format_minutes_to_time(total_minutes: int) -> str:
    normalized = total_minutes % (24 * 60)
    hours = normalized // 60
    minutes = normalized % 60
    return f"{hours:02d}:{minutes:02d}"


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "once"
    completed: bool = False
    description: str | None = None
    scheduled_time: str | None = None
    due_date: date | None = None

    def mark_complete(self, pet: "Pet | None" = None) -> "Task | None":
        """Mark the task as completed and create a recurring follow-up when needed."""
        self.completed = True
        if self.frequency.lower() in {"daily", "weekly"} and pet is not None:
            next_due = date.today() + timedelta(days=1 if self.frequency.lower() == "daily" else 7)
            next_task = Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                scheduled_time=self.scheduled_time,
                due_date=next_due,
            )
            pet.add_task(next_task)
            return next_task
        return None

    def mark_incomplete(self) -> None:
        """Mark the task as pending again."""
        self.completed = False

    def to_summary(self) -> str:
        """Return a short human-readable summary of the task."""
        status = "done" if self.completed else "pending"
        return f"{self.title} ({self.duration_minutes} min, {self.priority}, {status})"

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "frequency": self.frequency,
            "completed": self.completed,
            "description": self.description,
            "scheduled_time": self.scheduled_time,
            "due_date": self.due_date.isoformat() if self.due_date else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        due_date = data.get("due_date")
        return cls(
            title=data.get("title", "Task"),
            duration_minutes=int(data.get("duration_minutes", 0)),
            priority=data.get("priority", "medium"),
            frequency=data.get("frequency", "once"),
            completed=bool(data.get("completed", False)),
            description=data.get("description"),
            scheduled_time=data.get("scheduled_time"),
            due_date=date.fromisoformat(due_date) if due_date else None,
        )


@dataclass
class Pet:
    name: str
    species: str
    age_months: int | None = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> Task:
        """Add a task to this pet."""
        self.tasks.append(task)
        return task

    def get_pending_tasks(self) -> List[Task]:
        """Return all pending tasks for this pet."""
        return [task for task in self.tasks if not task.completed]

    def task_count(self) -> int:
        """Return the number of tasks attached to this pet."""
        return len(self.tasks)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "species": self.species,
            "age_months": self.age_months,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Pet":
        pet = cls(
            name=data.get("name", "Pet"),
            species=data.get("species", "other"),
            age_months=data.get("age_months"),
        )
        pet.tasks = [Task.from_dict(task_data) for task_data in data.get("tasks", [])]
        return pet


@dataclass
class Owner:
    name: str
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> Pet:
        """Add a pet to the owner's profile."""
        self.pets.append(pet)
        return pet

    def get_all_tasks(self) -> List[Task]:
        """Return every task from every pet owned by this person."""
        return [task for pet in self.pets for task in pet.tasks]

    def get_pending_tasks(self) -> List[Task]:
        """Return all pending tasks across the owner's pets."""
        return [task for task in self.get_all_tasks() if not task.completed]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "preferences": self.preferences,
            "pets": [pet.to_dict() for pet in self.pets],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Owner":
        owner = cls(
            name=data.get("name", "Owner"),
            preferences=list(data.get("preferences", [])),
        )
        owner.pets = [Pet.from_dict(pet_data) for pet_data in data.get("pets", [])]
        return owner

    def save_to_json(self, path: str | Path) -> None:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, indent=2)

    @classmethod
    def load_from_json(cls, path: str | Path) -> "Owner":
        destination = Path(path)
        if not destination.exists():
            return cls(name="Owner")
        with destination.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return cls.from_dict(data)


def load_owner_from_json(path: str | Path) -> Owner:
    """Load an Owner from disk using a module-level helper for compatibility."""
    destination = Path(path)
    if not destination.exists():
        return Owner(name="Owner")
    with destination.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return Owner.from_dict(data)


def save_owner_to_json(owner: Owner, path: str | Path) -> None:
    """Save an Owner to disk using a module-level helper for compatibility."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        json.dump(owner.to_dict(), handle, indent=2)


@dataclass
class Scheduler:
    owner: Owner

    def retrieve_tasks(self) -> List[Task]:
        """Collect all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def build_daily_schedule(self, available_minutes: int = 120) -> List[Task]:
        """Build a priority-based daily schedule within the time budget."""
        pending_tasks = [task for task in self.retrieve_tasks() if not task.completed]
        ordered_tasks = self.sort_by_priority_then_time(pending_tasks)

        selected: List[Task] = []
        remaining_time = available_minutes
        for task in ordered_tasks:
            if task.duration_minutes <= remaining_time:
                selected.append(task)
                remaining_time -= task.duration_minutes
        return selected

    def sort_by_time(self) -> List[Task]:
        """Return all pending tasks sorted by their scheduled time."""
        pending_tasks = [task for task in self.retrieve_tasks() if not task.completed]
        return sorted(
            pending_tasks,
            key=lambda task: _parse_time_to_minutes(task.scheduled_time),
        )

    def sort_by_priority_then_time(self, tasks: List[Task] | None = None) -> List[Task]:
        """Return tasks sorted by priority first and then by scheduled time."""
        pending_tasks = tasks if tasks is not None else [task for task in self.retrieve_tasks() if not task.completed]
        return sorted(
            pending_tasks,
            key=lambda task: (-self._priority_score(task.priority), _parse_time_to_minutes(task.scheduled_time)),
        )

    def filter_tasks(self, pet_name: str | None = None, completed: bool | None = None) -> List[Task]:
        """Filter tasks by pet name and completion state."""
        tasks = self.retrieve_tasks()
        if pet_name is not None:
            tasks = [task for task in tasks if any(pet.name == pet_name and task in pet.tasks for pet in self.owner.pets)]
        if completed is not None:
            tasks = [task for task in tasks if task.completed is completed]
        return tasks

    def detect_conflicts(self) -> List[str]:
        """Return a simple list of warning messages for tasks sharing the same time."""
        conflicts: List[str] = []
        tasks = [task for task in self.retrieve_tasks() if task.scheduled_time]
        seen: dict[str, List[Task]] = {}
        for task in tasks:
            key = task.scheduled_time
            seen.setdefault(key, []).append(task)
        for time_value, matching_tasks in seen.items():
            if len(matching_tasks) > 1:
                names = ", ".join(task.title for task in matching_tasks)
                conflicts.append(f"Conflict at {time_value}: {names}")
        return conflicts

    def find_next_available_slot(self, duration_minutes: int, start_time: str | None = None) -> str:
        """Find the earliest available time slot that fits the requested duration."""
        start_value = start_time or "08:00"
        start_minutes = _parse_time_to_minutes(start_value)
        candidate_minutes = start_minutes

        while candidate_minutes <= 24 * 60:
            candidate_end = candidate_minutes + duration_minutes
            fits = True
            for task in self.retrieve_tasks():
                if not task.scheduled_time:
                    continue
                task_start = _parse_time_to_minutes(task.scheduled_time)
                task_end = task_start + task.duration_minutes
                if not (candidate_end <= task_start or candidate_minutes >= task_end):
                    fits = False
                    break
            if fits:
                return _format_minutes_to_time(candidate_minutes)
            candidate_minutes += 15

        return _format_minutes_to_time(candidate_minutes)

    @staticmethod
    def _priority_score(priority: str) -> int:
        """Map priority labels to a simple sorting score."""
        return {"low": 1, "medium": 2, "high": 3}.get(priority.lower(), 2)


@dataclass
class PlannedTask:
    title: str
    duration_minutes: int
    priority: str
    reason: str


@dataclass
class DailyPlan:
    owner: Owner
    pet: Pet
    items: List[PlannedTask]
    total_minutes: int
    skipped_tasks: List[str]
    reasons: List[str]


class DailyPlanScheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: List[Task], available_minutes: int):
        self.owner = owner
        self.pet = pet
        self.tasks = tasks
        self.available_minutes = available_minutes

    def build_plan(self) -> DailyPlan:
        """Create a simple plan for the Streamlit app using priority and time."""
        ordered_tasks = sorted(
            self.tasks,
            key=lambda task: (-self._priority_score(task.priority), _parse_time_to_minutes(task.scheduled_time)),
        )

        selected: List[PlannedTask] = []
        skipped: List[str] = []
        reasons: List[str] = []
        remaining_time = self.available_minutes

        for task in ordered_tasks:
            if task.duration_minutes <= remaining_time:
                remaining_time -= task.duration_minutes
                selected.append(
                    PlannedTask(
                        title=task.title,
                        duration_minutes=task.duration_minutes,
                        priority=task.priority,
                        reason=(
                            f"{task.title} was selected because it has a high priority "
                            f"and fit within the remaining time."
                        ),
                    )
                )
            else:
                skipped.append(task.title)
                reasons.append(
                    f"{task.title} was skipped because it did not fit within the remaining time."
                )

        reasons.extend([item.reason for item in selected])
        return DailyPlan(
            owner=self.owner,
            pet=self.pet,
            items=selected,
            total_minutes=self.available_minutes - remaining_time,
            skipped_tasks=skipped,
            reasons=reasons,
        )

    @staticmethod
    def _priority_score(priority: str) -> int:
        """Map priority labels to a simple sorting score."""
        return {"low": 1, "medium": 2, "high": 3}.get(priority.lower(), 2)
