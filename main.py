from pawpal_system import Owner, Pet, Task, Scheduler


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

    print("Today's Schedule")
    print("=" * 20)
    for task in schedule:
        print(f"- {task.title} ({task.duration_minutes} min, {task.priority})")

    print("\nSorted by time")
    for task in scheduler.sort_by_time():
        print(f"- {task.title} at {task.scheduled_time}")

    print("\nFiltered pending tasks for Mochi")
    for task in scheduler.filter_tasks(pet_name="Mochi", completed=False):
        print(f"- {task.title}")

    print("\nRecurring task demo")
    recurring.mark_complete(pet=dog)
    print(f"- Created next occurrence for {recurring.title}")

    print("\nConflicts")
    for warning in scheduler.detect_conflicts():
        print(f"- {warning}")


if __name__ == "__main__":
    main()
