import streamlit as st
import google.generativeai as genai

# ---------------------
# CONFIGURE GEMINI API
# ---------------------
GEMINI_API_KEY = "AIzaSyDv_5NDF1yzEfuTHohxos3FmNj8SsNmMso"  # Replace this with your Gemini API key
genai.configure(api_key=GEMINI_API_KEY)

# ---------------------
# Function to Solve Math
# ---------------------
def solve_math_problem(question):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""
You are a math tutor. Solve the following problem step-by-step and explain clearly.

Problem: {question}
    
Provide all necessary steps and explanations in markdown format.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {e}"

# ---------------------
# Streamlit UI
# ---------------------
st.set_page_config(page_title="🧮 Math Problem Solver")
st.title("🧠 Math Problem Solver with Step-by-Step Explanation")
st.write("Enter a math problem below (e.g., `Solve x² + 5x + 6 = 0` or `Integrate x*sin(x)`):")

user_input = st.text_area("Enter your math problem:", height=150)

if st.button("Solve"):
    if user_input.strip():
        with st.spinner("Solving..."):
            solution = solve_math_problem(user_input)
        st.markdown("### ✅ Solution:")
        st.markdown(solution)
    else:
        st.warning("Please enter a math problem.")
