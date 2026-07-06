from pawpal_system import Owner, Pet, Scheduler, Task


def _priority_icon(priority: str) -> str:
    return {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority.lower(), "⚪")


def main() -> None:
    owner = Owner(name="Jordan")
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", scheduled_time="09:30"))
    dog.add_task(Task(title="Feeding", duration_minutes=10, priority="medium", scheduled_time="08:00"))
    cat.add_task(Task(title="Litter cleanup", duration_minutes=15, priority="high", scheduled_time="10:00"))
    cat.add_task(Task(title="Play session", duration_minutes=20, priority="low", scheduled_time="09:00"))
    recurring = Task(title="Water plants", duration_minutes=5, priority="low", frequency="daily", scheduled_time="07:00")
    dog.add_task(recurring)
    dog.add_task(Task(title="Morning walk", duration_minutes=20, priority="high", scheduled_time="09:30"))

    scheduler = Scheduler(owner=owner)
    schedule = scheduler.build_daily_schedule(available_minutes=60)

    print("📅 Today's Schedule")
    print("=" * 24)
    for task in schedule:
        print(f"- {_priority_icon(task.priority)} {task.title} ({task.duration_minutes} min, {task.priority.upper()})")

    print("\n🕒 Sorted by priority and time")
    for task in scheduler.sort_by_priority_then_time():
        print(f"- {_priority_icon(task.priority)} {task.title} at {task.scheduled_time or 'unscheduled'}")

    print("\n🧼 Filtered pending tasks for Mochi")
    for task in scheduler.filter_tasks(pet_name="Mochi", completed=False):
        print(f"- {_priority_icon(task.priority)} {task.title}")

    print("\n🔁 Recurring task demo")
    recurring.mark_complete(pet=dog)
    print(f"- Created next occurrence for {recurring.title}")

    print("\n⚠️ Conflicts")
    for warning in scheduler.detect_conflicts():
        print(f"- {warning}")

    print("\n✨ Suggested next slot")
    print(f"- {scheduler.find_next_available_slot(20, '08:00')}")


if __name__ == "__main__":
    main()
