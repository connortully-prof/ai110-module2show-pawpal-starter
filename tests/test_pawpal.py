from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_updates_task_status():
    task = Task(title="Medication", duration_minutes=10, priority="high")

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")

    pet.add_task(Task(title="Walk", duration_minutes=20, priority="medium"))

    assert pet.task_count() == 1


def test_sort_by_time_orders_tasks_by_scheduled_time():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    pet.add_task(Task(title="Walk", duration_minutes=20, priority="high", scheduled_time="09:30"))
    pet.add_task(Task(title="Feed", duration_minutes=10, priority="medium", scheduled_time="08:00"))

    scheduler = Scheduler(owner=owner)
    ordered = scheduler.sort_by_time()

    assert [task.title for task in ordered] == ["Feed", "Walk"]


def test_filter_tasks_by_status_and_pet_name():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    other_pet = Pet(name="Luna", species="cat")
    owner.add_pet(pet)
    owner.add_pet(other_pet)
    pet.add_task(Task(title="Feed", duration_minutes=10, priority="medium", scheduled_time="08:00"))
    other_pet.add_task(Task(title="Play", duration_minutes=15, priority="high", scheduled_time="10:00"))
    other_pet.tasks[0].mark_complete()

    scheduler = Scheduler(owner=owner)
    filtered = scheduler.filter_tasks(pet_name="Mochi", completed=False)

    assert [task.title for task in filtered] == ["Feed"]


def test_recurring_task_creates_next_occurrence_when_completed():
    pet = Pet(name="Mochi", species="dog")
    task = Task(title="Water plants", duration_minutes=5, priority="low", frequency="daily", scheduled_time="07:00")
    pet.add_task(task)

    next_task = task.mark_complete(pet=pet)

    assert task.completed is True
    assert next_task is not None
    assert next_task.frequency == "daily"
    assert next_task.completed is False
    assert pet.task_count() == 2


def test_detect_conflicts_returns_warning_for_matching_times():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    pet.add_task(Task(title="Walk", duration_minutes=20, priority="high", scheduled_time="09:00"))
    pet.add_task(Task(title="Feed", duration_minutes=10, priority="medium", scheduled_time="09:00"))

    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Walk" in conflicts[0] and "Feed" in conflicts[0]


def test_save_and_load_round_trip_persists_owner_and_tasks(tmp_path):
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    pet.add_task(Task(title="Walk", duration_minutes=20, priority="high", scheduled_time="09:00"))

    data_path = tmp_path / "data.json"
    owner.save_to_json(data_path)
    reloaded_owner = Owner.load_from_json(data_path)

    assert reloaded_owner.name == "Jordan"
    assert len(reloaded_owner.pets) == 1
    assert reloaded_owner.pets[0].tasks[0].title == "Walk"


def test_sort_by_priority_then_time_orders_high_priority_first():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    pet.add_task(Task(title="Walk", duration_minutes=20, priority="medium", scheduled_time="09:00"))
    pet.add_task(Task(title="Feed", duration_minutes=10, priority="high", scheduled_time="09:30"))
    pet.add_task(Task(title="Play", duration_minutes=15, priority="high", scheduled_time="08:00"))

    scheduler = Scheduler(owner=owner)
    ordered = scheduler.sort_by_priority_then_time()

    assert [task.title for task in ordered] == ["Play", "Feed", "Walk"]


def test_find_next_available_slot_returns_earliest_open_time():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    pet.add_task(Task(title="Walk", duration_minutes=20, priority="high", scheduled_time="09:00"))
    pet.add_task(Task(title="Feed", duration_minutes=10, priority="medium", scheduled_time="09:30"))

    scheduler = Scheduler(owner=owner)

    assert scheduler.find_next_available_slot(15, "08:00") == "08:00"
    assert scheduler.find_next_available_slot(20, "09:00") == "09:45"
