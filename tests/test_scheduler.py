from pawpal_system import Owner, Pet, Task, DailyPlanScheduler


def test_scheduler_prioritizes_high_priority_tasks_within_time_limit():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    tasks = [
        Task(title="Morning walk", duration_minutes=30, priority="high"),
        Task(title="Feeding", duration_minutes=15, priority="low"),
        Task(title="Medication", duration_minutes=20, priority="high"),
    ]

    plan = DailyPlanScheduler(owner=owner, pet=pet, tasks=tasks, available_minutes=60).build_plan()

    assert [item.title for item in plan.items] == ["Morning walk", "Medication"]
    assert plan.total_minutes == 50
    assert plan.skipped_tasks == ["Feeding"]


def test_scheduler_skips_tasks_that_do_not_fit_remaining_time():
    owner = Owner(name="Alex")
    pet = Pet(name="Luna", species="cat")
    tasks = [
        Task(title="Grooming", duration_minutes=45, priority="medium"),
        Task(title="Play session", duration_minutes=20, priority="high"),
    ]

    plan = DailyPlanScheduler(owner=owner, pet=pet, tasks=tasks, available_minutes=40).build_plan()

    assert [item.title for item in plan.items] == ["Play session"]
    assert plan.skipped_tasks == ["Grooming"]


def test_plan_explains_reasons_for_selected_and_skipped_tasks():
    owner = Owner(name="Sam")
    pet = Pet(name="Biscuit", species="dog")
    tasks = [
        Task(title="Training", duration_minutes=20, priority="high"),
        Task(title="Brushing", duration_minutes=15, priority="low"),
    ]

    plan = DailyPlanScheduler(owner=owner, pet=pet, tasks=tasks, available_minutes=20).build_plan()

    assert any("fit within the remaining time" in item.reason for item in plan.items)
    assert any("did not fit" in reason for reason in plan.reasons)
