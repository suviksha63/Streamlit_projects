# streamlit_app.py
import streamlit as st
import google.generativeai as genai

# Set your Gemini API key here
genai.configure(api_key="AIzaSyBObx02Zye3bV281jTqDaFRYbfGPLgFIHo")

# Function to call Gemini for resume generation
def generate_resume(name, skills, experience, job_role):
    prompt = f"""
You are a professional resume writer. Create a clean, modern, and tailored resume for the user.

Details:
- Name: {name}
- Skills: {skills}
- Experience: {experience}
- Target Job Role: {job_role}

Include sections like Summary, Skills, Experience, and optionally Projects. Keep it concise and professional.
"""
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text


# Streamlit UI
st.title("📝 Resume Generator")

with st.form("resume_form"):
    name = st.text_input("Enter your name")
    skills = st.text_area("List your skills (comma-separated)")
    experience = st.text_area("Briefly describe your experience")
    job_role = st.text_input("Target Job Role")
    submitted = st.form_submit_button("Generate Resume")

if submitted:
    with st.spinner("Generating your resume..."):
        result = generate_resume(name, skills, experience, job_role)
        st.subheader("📄 Your Resume")
        st.code(result, language="markdown")
        st.download_button("Download Resume", result, file_name="resume.txt")
