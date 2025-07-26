import streamlit as st
import google.generativeai as genai

# Set Gemini API Key
genai.configure(api_key="AIzaSyB0lCJ0emIpVC8fQHgwa6miW7xwYJ3smfM")  # 🔒 Ideally, use secrets.toml

# Gemini prompt function
def get_movie_recommendations(genre, actor, plot):
    prompt = f"""
You are a movie recommendation assistant.

User Preferences:
- Genres: {genre}
- Actors: {actor}
- Plot Keywords: {plot}

Based on this, recommend 3 movies. For each movie, provide:
1. Movie Title
2. Short Description
3. Why this is recommended (personalized reason)
4. Poster image URL (if known or can be guessed)
Format your response as Markdown.
"""
    model = genai.GenerativeModel('gemini-2.0-flash')  # or 'gemini-1.5-flash' if available
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("🎬 Gemini AI Movie Recommender")

st.markdown("Enter your preferences to get AI-powered movie recommendations!")

genre_input = st.text_input("🎭 Favorite genres:")
actor_input = st.text_input("🎬 Favorite actors or actresses:")
plot_input = st.text_input("🧠 Plot themes or keywords:")

if st.button("Get Recommendations"):
    with st.spinner("🎥 Thinking..."):
        result = get_movie_recommendations(genre_input, actor_input, plot_input)
    st.markdown("### 🍿 Your Recommendations:")
    st.markdown(result)
