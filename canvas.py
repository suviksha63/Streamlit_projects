import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import base64
import requests

# Set page layout
st.set_page_config(page_title="Drawing Canvas with Gemini", layout="centered")

st.title("🎨 Drawing Canvas with Save & Gemini API")

# Canvas settings
stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color: ", "#000000")
bg_color = st.sidebar.color_picker("Background color: ", "#ffffff")
drawing_mode = st.sidebar.selectbox("Drawing tool:", ("freedraw", "line", "rect", "circle", "transform"))

# Canvas
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0)",  # Transparent fill
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    update_streamlit=True,
    height=400,
    width=600,
    drawing_mode=drawing_mode,
    key="canvas"
)

# Save the image
if canvas_result.image_data is not None:
    img = Image.fromarray(canvas_result.image_data.astype('uint8'), mode="RGBA")

    # Show the image
    st.image(img, caption="Your Drawing", use_column_width=True)

    # Download button
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button("📥 Download Drawing", data=byte_im, file_name="drawing.png", mime="image/png")

    # Gemini API Integration
    st.subheader("🔗 Send to Gemini API")

    api_key = st.text_input("AIzaSyCfkKUOmAo_bmZo7izZdUn0iMwuB7Ogwgg", type="password")
    prompt = st.text_area("Enter prompt for Gemini:", "Describe this drawing...")

    if st.button("Send to Gemini"):
        if not api_key:
            st.error("AIzaSyCfkKUOmAo_bmZo7izZdUn0iMwuB7Ogwgg")
        else:
            # Convert image to base64
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()

            # Gemini API endpoint (example for Gemini Vision API)
            endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key=" + api_key

            headers = {
                "Content-Type": "application/json"
            }

            payload = {
                "contents": [{
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": img_base64
                            }
                        }
                    ]
                }]
            }

            response = requests.post(endpoint, headers=headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                output_text = result['candidates'][0]['content']['parts'][0]['text']
                st.success("✅ Gemini Response:")
                st.write(output_text)
            else:
                st.error(f"❌ Gemini API Error: {response.status_code}")
                st.json(response.json())
