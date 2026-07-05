from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List


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


@dataclass
class Scheduler:
    owner: Owner

    def retrieve_tasks(self) -> List[Task]:
        """Collect all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def build_daily_schedule(self, available_minutes: int = 120) -> List[Task]:
        """Build a simple priority-based daily schedule within the time budget."""
        pending_tasks = [task for task in self.retrieve_tasks() if not task.completed]
        ordered_tasks = sorted(
            pending_tasks,
            key=lambda task: self._priority_score(task.priority),
            reverse=True,
        )

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
            key=lambda task: task.scheduled_time or "23:59",
        )

    def filter_tasks(self, pet_name: str | None = None, completed: bool | None = None) -> List[Task]:
        """Filter tasks by pet name and completion state."""
        tasks = self.retrieve_tasks()
        if pet_name is not None:
            tasks = [task for task in tasks if any(pet.name == pet_name for pet in self.owner.pets if task in pet.tasks)]
        if completed is not None:
            tasks = [task for task in tasks if task.completed is completed]
        return tasks

    def detect_conflicts(self) -> List[str]:
        """Return a simple list of warning messages for tasks sharing the same time."""
        conflicts: List[str] = []
        tasks = [task for task in self.retrieve_tasks() if task.scheduled_time]
        seen = {}
        for task in tasks:
            key = task.scheduled_time
            seen.setdefault(key, []).append(task)
        for time_value, matching_tasks in seen.items():
            if len(matching_tasks) > 1:
                names = ", ".join(task.title for task in matching_tasks)
                conflicts.append(f"Conflict at {time_value}: {names}")
        return conflicts

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
            key=lambda task: self._priority_score(task.priority),
            reverse=True,
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
