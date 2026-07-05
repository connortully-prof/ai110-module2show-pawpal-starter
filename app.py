import streamlit as st

from pawpal_system import DailyPlanScheduler, Owner, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
PawPal+ helps a busy pet owner turn a list of care tasks into a realistic daily plan.
The scheduler sorts tasks by importance, respects the available time, and explains why each task was included or skipped.
"""
)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

if "current_pet_index" not in st.session_state:
    st.session_state.current_pet_index = 0

owner = st.session_state.owner

st.subheader("Owner details")
owner_name = st.text_input("Owner name", value=owner.name)
if st.button("Save owner"):
    owner.name = owner_name or "Owner"
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
            task = Task(
                title=task_title.strip(),
                duration_minutes=int(duration),
                priority=priority,
            )
            selected_pet.add_task(task)
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
                st.success("Task updated.")

        if st.button("Remove selected task"):
            tasks.pop(selected_task_index)
            st.success("Task removed.")

        st.write("Current tasks")
        st.table(
            [
                {
                    "title": task.title,
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority,
                    "completed": task.completed,
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

        st.success(f"Daily plan for {selected_pet.name} is ready.")
        st.write(f"Planned time: {plan.total_minutes} of {int(available_minutes)} minutes")

        if plan.items:
            st.write("### Included tasks")
            for item in plan.items:
                st.write(f"- {item.title} ({item.duration_minutes} min, priority: {item.priority})")
        else:
            st.info("No tasks fit within the available time.")

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
