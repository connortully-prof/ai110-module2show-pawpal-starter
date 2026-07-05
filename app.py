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

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "selected_task_index" not in st.session_state:
    st.session_state.selected_task_index = 0

st.subheader("Owner and pet details")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
available_minutes = st.number_input(
    "Available minutes today",
    min_value=15,
    max_value=720,
    value=120,
    step=15,
)

st.divider()

st.subheader("Add or edit care tasks")
col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", key="task_title")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="task_duration")
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], key="task_priority")

if st.button("Add task"):
    if task_title.strip():
        st.session_state.tasks.append(
            {
                "title": task_title.strip(),
                "duration_minutes": int(duration),
                "priority": priority,
            }
        )
        st.success(f"Added {task_title.strip()}.")
    else:
        st.warning("Please enter a task title.")

if st.session_state.tasks:
    task_options = [
        f"{index + 1}. {task['title']} ({task['duration_minutes']} min, {task['priority']})"
        for index, task in enumerate(st.session_state.tasks)
    ]
    selected_index = st.selectbox(
        "Edit an existing task",
        options=list(range(len(st.session_state.tasks))),
        format_func=lambda index: task_options[index],
        key="selected_task_index",
    )

    current_task = st.session_state.tasks[selected_index]
    with st.form("edit_task_form"):
        edit_title = st.text_input("Edit title", value=current_task["title"], key="edit_title")
        edit_duration = st.number_input(
            "Edit duration (minutes)",
            min_value=1,
            max_value=240,
            value=current_task["duration_minutes"],
            key="edit_duration",
        )
        edit_priority = st.selectbox(
            "Edit priority",
            ["low", "medium", "high"],
            index=["low", "medium", "high"].index(current_task["priority"]),
            key="edit_priority",
        )
        submitted = st.form_submit_button("Update task")
        if submitted:
            st.session_state.tasks[selected_index] = {
                "title": edit_title.strip() or current_task["title"],
                "duration_minutes": int(edit_duration),
                "priority": edit_priority,
            }
            st.success("Task updated.")

    if st.button("Remove selected task"):
        st.session_state.tasks.pop(selected_index)
        st.session_state.selected_task_index = max(0, min(selected_index, len(st.session_state.tasks) - 1))
        st.success("Task removed.")

    st.write("Current tasks")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above to build a plan.")

st.divider()

st.subheader("Build schedule")
if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        owner = Owner(name=owner_name or "Owner")
        pet = Pet(name=pet_name or "Pet", species=species)
        tasks = [
            Task(
                title=task["title"],
                duration_minutes=int(task["duration_minutes"]),
                priority=task["priority"],
            )
            for task in st.session_state.tasks
        ]

        plan = DailyPlanScheduler(
            owner=owner,
            pet=pet,
            tasks=tasks,
            available_minutes=int(available_minutes),
        ).build_plan()

        st.success(f"Daily plan for {pet.name} is ready.")
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
