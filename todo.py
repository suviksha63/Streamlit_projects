import streamlit as st
import datetime

# Page setup
st.set_page_config(page_title="📝 To‑Do Manager", layout="centered")
st.title("✅ To‑Do Task Manager with Deadlines & Progress")

# Initialize task list in session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Function to calculate progress
def calculate_progress():
    total = len(st.session_state.tasks)
    done = sum([1 for task in st.session_state.tasks if task["completed"]])
    return int((done / total) * 100) if total > 0 else 0

# Add new task
with st.form("Add Task"):
    col1, col2 = st.columns([3, 2])
    with col1:
        title = st.text_input("Task Title")
    with col2:
        deadline = st.date_input("Deadline", min_value=datetime.date.today())

    submitted = st.form_submit_button("Add Task")
    if submitted and title.strip():
        st.session_state.tasks.append({
            "title": title.strip(),
            "deadline": deadline,
            "completed": False
        })
        st.success(f"Task '{title.strip()}' added!")

# Show tasks
if st.session_state.tasks:
    st.subheader("📋 Your Tasks")

    for i, task in enumerate(st.session_state.tasks):
        cols = st.columns([0.05, 0.5, 0.3, 0.15])
        with cols[0]:
            st.session_state.tasks[i]["completed"] = st.checkbox("", value=task["completed"], key=f"cb_{i}")
        with cols[1]:
            st.markdown(f"**{task['title']}**")
        with cols[2]:
            st.markdown(f"🗓️ `{task['deadline'].strftime('%Y-%m-%d')}`")
        with cols[3]:
            if st.button("❌ Delete", key=f"del_{i}"):
                st.session_state.tasks.pop(i)
                st.experimental_rerun()

    # Progress bar
    st.subheader("📈 Progress")
    progress = calculate_progress()
    st.progress(progress / 100)
    st.write(f"**{progress}% completed**")

else:
    st.info("No tasks added yet.")

# Placeholder: Connect to external API (e.g., Google Sheets, Firebase)
with st.expander("🔐 Connect to API (Optional)"):
    st.text_input("AIzaSyCfkKUOmAo_bmZo7izZdUn0iMwuB7Ogwgg", type="password", key="api_key")
    st.write("→ Integrate with Google Sheets, Firebase, or other services if needed.")
