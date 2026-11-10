
import streamlit as st
import cv2
import numpy as np
from PIL import Image
from air_quality import analysis_air_quality as analyse_air_quality
st.set_page_config(
    page_title="AI Air Quality Camera",
    layout="wide"
)

st.title(" AI Camera Air Quality Intelligence")

st.write(
    "Capture an image and analyse visible atmospheric haze."
)

st.warning(
    "This is an experimental visual clarity estimate. "
    "It does not measure AQI, PM2.5 or toxic gases."
)

# Capture image from camera
uploaded_image = st.camera_input("Take a picture")

if uploaded_image is not None:

    # Read image
    pil_image = Image.open(uploaded_image).convert("RGB")
    rgb_image = np.array(pil_image)

    # Convert RGB to OpenCV BGR
    image = cv2.cvtColor(
        rgb_image, cv2.COLOR_RGB2BGR
    )

    # Analyse image
    result = analyse_air_quality(image)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Captured Image")
        st.image(rgb_image, use_container_width=True)

    with col2:
        st.subheader("Visual Air Analysis")

        st.metric(
            "Visual Haze Score",
            f"{result['haze_score']}/100"
        )

        st.metric(
            "Visual Clarity Score",
            f"{result['clarity_score']}/100"
        )

        st.progress(
            result["haze_score"] / 100
        )

        st.info(result["category"])

    st.subheader("Image Processing Metrics")

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "Contrast",
        result["contrast"]
    )

    metric2.metric(
        "Saturation",
        result["saturation"]
    )

    metric3.metric(
        "Brightness",
        result["brightness"]
    )

    metric4.metric(
        "Edge Density",
        result["edge_density"]
    )

    
