from pawpal_system import Owner, Pet, Task


def test_mark_complete_updates_task_status():
    task = Task(title="Medication", duration_minutes=10, priority="high")

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")

    pet.add_task(Task(title="Walk", duration_minutes=20, priority="medium"))

    assert pet.task_count() == 1
