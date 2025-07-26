import streamlit as st
import cv2
import numpy as np
from PIL import Image
import google.generativeai as genai
import io

# ---------------------
# CONFIGURE GEMINI API
# ---------------------
GEMINI_API_KEY = "AIzaSyDv_5NDF1yzEfuTHohxos3FmNj8SsNmMso"
genai.configure(api_key=GEMINI_API_KEY)

def apply_filter(image, filter_type):
    image = np.array(image.convert("RGB"))
    
    if filter_type == "Grayscale":
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return Image.fromarray(gray)

    elif filter_type == "Sepia":
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        sepia = cv2.transform(image, kernel)
        sepia = np.clip(sepia, 0, 255)
        return Image.fromarray(sepia.astype(np.uint8))

    elif filter_type == "Blur":
        blurred = cv2.GaussianBlur(image, (15, 15), 0)
        return Image.fromarray(blurred)

    elif filter_type == "Cartoon":
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(image, 9, 250, 250)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        return Image.fromarray(cartoon)

    return image

def describe_image_with_gemini(image_pil):
    buf = io.BytesIO()
    image_pil.save(buf, format='JPEG')
    byte_data = buf.getvalue()

    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content(
        [
            "Give a short caption for this image.",
            byte_data
        ]
    )
    return response.text

# ---------------------
# Streamlit UI
# ---------------------
st.set_page_config(page_title="Photo Filters App 🎨")
st.title("📸 Photo Filters App")
st.write("Upload an image and apply filters like Grayscale, Sepia, Blur, and Cartoon!")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    filter_choice = st.selectbox("Select a Filter", ["None", "Grayscale", "Sepia", "Blur", "Cartoon"])

    if filter_choice != "None":
        filtered_image = apply_filter(image, filter_choice)
        st.image(filtered_image, caption=f"{filter_choice} Image", use_column_width=True)

        if st.button("Get Gemini Caption"):
            with st.spinner("Thinking..."):
                caption = describe_image_with_gemini(filtered_image)
                st.success("Gemini says:")
                st.write(caption)
    else:
        st.info("Select a filter to apply.")
else:
    st.info("Please upload an image to get started.")
