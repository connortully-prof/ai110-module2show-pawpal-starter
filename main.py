from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner(name="Jordan")
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task(title="Morning walk", duration_minutes=30, priority="high"))
    dog.add_task(Task(title="Feeding", duration_minutes=10, priority="medium"))
    cat.add_task(Task(title="Litter cleanup", duration_minutes=15, priority="high"))
    cat.add_task(Task(title="Play session", duration_minutes=20, priority="low"))

    scheduler = Scheduler(owner=owner)
    schedule = scheduler.build_daily_schedule(available_minutes=60)

    print("Today's Schedule")
    print("=" * 20)
    for task in schedule:
        print(f"- {task.title} ({task.duration_minutes} min, {task.priority})")


if __name__ == "__main__":
    main()
