import cv2
import numpy as np

def analysis_air_quality(image):
    """
    Estimate visible Haza from air image
    this is a visible heuristic method
    """

    image = cv2.resize(image, (640, 480))
    #convert bgr to other color spaces
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #contrast analysis
    contrast = float(np.std(gray))

    #color staturation
    saturation= float(np.mean(hsv[:, :, 1]))
    edges = cv2.Canny(gray, 50, 150)
    edge_density = float(np.mean(edges>0))
        # Normalised heuristic scores (0-100)
    contrast_score = np.clip(
        (contrast - 10) / 50 * 100, 0, 100
    )

    saturation_score = np.clip(
        saturation / 100 * 100, 0, 100
    )
    brightness = float(np.mean(gray))
    
    edge_score = np.clip(
        edge_density / 0.15 * 100, 0, 100
    )

    # Lower contrast, saturation and edge detail
    # may indicate greater visible haze.
    clarity_score = (
        0.45 * contrast_score +
        0.30 * saturation_score +
        0.25 * edge_score
    )

    haze_score = 100 - clarity_score

    # Broad visual categories, not AQI categories
    if haze_score < 25:
        category = "Clear Visual Conditions"
    elif haze_score < 45:
        category = "Slight Visual Haze"
    elif haze_score < 65:
        category = "Moderate Visual Haze"
    else:
        category = "High Visual Haze"

    return {
        "haze_score": round(float(haze_score), 2),
        "clarity_score": round(float(clarity_score), 2),
        "contrast": round(contrast, 2),
        "saturation": round(saturation, 2),
        "brightness": round(brightness, 2),
        "edge_density": round(edge_density, 4),
        "category": category
    }

