from pathlib import Path

import streamlit as st
import pawpal_system as pawpal_system_module
from pawpal_system import DailyPlanScheduler, Owner, Pet, Scheduler, Task

DATA_PATH = Path(__file__).with_name("data.json")
LOAD_OWNER_HELPER = getattr(pawpal_system_module, "load_owner_from_json", None)
SAVE_OWNER_HELPER = getattr(pawpal_system_module, "save_owner_to_json", None)

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.markdown(
    """
PawPal+ turns pet care tasks into a realistic daily plan with smart priority scheduling, conflict checks, and persistence between runs.
"""
)

if "owner" not in st.session_state:
    if hasattr(Owner, "load_from_json"):
        st.session_state.owner = Owner.load_from_json(DATA_PATH)
    elif LOAD_OWNER_HELPER is not None:
        st.session_state.owner = LOAD_OWNER_HELPER(DATA_PATH)
    else:
        st.session_state.owner = Owner(name="Owner")

if "current_pet_index" not in st.session_state:
    st.session_state.current_pet_index = 0

owner = st.session_state.owner


def persist_owner() -> None:
    if hasattr(owner, "save_to_json"):
        owner.save_to_json(DATA_PATH)
    elif SAVE_OWNER_HELPER is not None:
        SAVE_OWNER_HELPER(owner, DATA_PATH)


st.info(f"💾 Your profile is automatically saved to {DATA_PATH.name}.")

st.subheader("Owner details")
owner_name = st.text_input("Owner name", value=owner.name)
if st.button("Save owner"):
    owner.name = owner_name or "Owner"
    persist_owner()
    st.success(f"Owner updated to {owner.name}.")

st.divider()

st.subheader("Add a pet")
pet_name = st.text_input("Pet name", key="pet_name_input", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"], key="species_input")
if st.button("Add pet"):
    if pet_name.strip():
        pet = Pet(name=pet_name.strip(), species=species)
        owner.add_pet(pet)
        st.session_state.current_pet_index = len(owner.pets) - 1
        persist_owner()
        st.success(f"Added {pet.name} to {owner.name}'s profile.")
    else:
        st.warning("Please enter a pet name.")

if owner.pets:
    pet_names = [pet.name for pet in owner.pets]
    selected_pet_index = st.selectbox(
        "Select pet",
        options=list(range(len(owner.pets))),
        format_func=lambda index: pet_names[index],
        key="current_pet_index",
    )
    selected_pet = owner.pets[selected_pet_index]
else:
    selected_pet = None

st.divider()

st.subheader("Add or edit care tasks")
if selected_pet is None:
    st.info("Add a pet first to attach care tasks.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", key="task_title")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="task_duration")
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], key="task_priority")

    if st.button("Add task"):
        if task_title.strip():
            task = Task(title=task_title.strip(), duration_minutes=int(duration), priority=priority)
            selected_pet.add_task(task)
            persist_owner()
            st.success(f"Added {task.title} to {selected_pet.name}.")
        else:
            st.warning("Please enter a task title.")

    if selected_pet.tasks:
        tasks = selected_pet.tasks
        task_options = [f"{index + 1}. {task.title} ({task.duration_minutes} min, {task.priority})" for index, task in enumerate(tasks)]
        selected_task_index = st.selectbox(
            "Edit or remove a task",
            options=list(range(len(tasks))),
            format_func=lambda index: task_options[index],
            key="selected_task_index",
        )
        current_task = tasks[selected_task_index]

        with st.form("edit_task_form"):
            edit_title = st.text_input("Edit title", value=current_task.title, key="edit_title")
            edit_duration = st.number_input(
                "Edit duration (minutes)",
                min_value=1,
                max_value=240,
                value=current_task.duration_minutes,
                key="edit_duration",
            )
            edit_priority = st.selectbox(
                "Edit priority",
                ["low", "medium", "high"],
                index=["low", "medium", "high"].index(current_task.priority),
                key="edit_priority",
            )
            submitted = st.form_submit_button("Update task")
            if submitted:
                current_task.title = edit_title.strip() or current_task.title
                current_task.duration_minutes = int(edit_duration)
                current_task.priority = edit_priority
                persist_owner()
                st.success("Task updated.")

        if st.button("Remove selected task"):
            tasks.pop(selected_task_index)
            persist_owner()
            st.success("Task removed.")

        st.write("Current tasks")
        st.table(
            [
                {
                    "title": task.title,
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority,
                    "completed": "✅" if task.completed else "⏳",
                }
                for task in tasks
            ]
        )
    else:
        st.info("No tasks yet. Add one above to build a plan.")

st.divider()

st.subheader("Build schedule")
available_minutes = st.number_input(
    "Available minutes today",
    min_value=15,
    max_value=720,
    value=120,
    step=15,
)
if st.button("Generate schedule"):
    if selected_pet is None or not selected_pet.tasks:
        st.warning("Add a pet and at least one task before generating a schedule.")
    else:
        plan = DailyPlanScheduler(
            owner=owner,
            pet=selected_pet,
            tasks=selected_pet.tasks,
            available_minutes=int(available_minutes),
        ).build_plan()

        st.success(f"📅 Daily plan for {selected_pet.name} is ready.")
        st.write(f"Planned time: {plan.total_minutes} of {int(available_minutes)} minutes")

        scheduler = Scheduler(owner=owner)
        if hasattr(scheduler, "sort_by_priority_then_time"):
            sorted_tasks = scheduler.sort_by_priority_then_time()
        else:
            sorted_tasks = scheduler.sort_by_time()
        pending_tasks = scheduler.filter_tasks(pet_name=selected_pet.name, completed=False)
        conflicts = scheduler.detect_conflicts()
        if hasattr(scheduler, "find_next_available_slot"):
            next_slot = scheduler.find_next_available_slot(duration_minutes=20, start_time="08:00")
        else:
            next_slot = "08:00"

        st.caption("🧠 Scheduling uses priority first, then time, and highlights the next available slot for new tasks.")
        st.info(f"💡 Suggested next available slot for a 20-minute task: {next_slot}")

        if plan.items:
            st.write("### Included tasks")
            st.table(
                [
                    {
                        "title": item.title,
                        "duration_minutes": item.duration_minutes,
                        "priority": item.priority,
                    }
                    for item in plan.items
                ]
            )
        else:
            st.info("No tasks fit within the available time.")

        st.write("### Sorted tasks")
        st.table(
            [
                {
                    "title": task.title,
                    "time": task.scheduled_time or "unscheduled",
                    "priority": task.priority,
                }
                for task in sorted_tasks
            ]
        )

        st.write("### Pending tasks for this pet")
        st.table(
            [
                {
                    "title": task.title,
                    "time": task.scheduled_time or "unscheduled",
                    "priority": task.priority,
                }
                for task in pending_tasks
            ]
        )

        if conflicts:
            st.warning("### Conflicts detected")
            for conflict in conflicts:
                st.warning(f"- {conflict}")
        else:
            st.success("No scheduling conflicts detected.")

        st.write("### Why this plan was chosen")
        for reason in plan.reasons:
            st.write(f"- {reason}")

        if plan.skipped_tasks:
            st.write("### Skipped tasks")
            for task_name in plan.skipped_tasks:
                st.write(f"- {task_name}")
        else:
            st.write("### Skipped tasks")
            st.write("- None")
