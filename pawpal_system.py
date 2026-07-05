from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "once"
    completed: bool = False
    description: str | None = None

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

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
