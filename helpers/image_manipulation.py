"""
Functions that change or draw on an image.
"""

import cv2


# OpenCV conversion codes, from a BGR frame to the named format
COLOR_CONVERSIONS = {
    "gray": cv2.COLOR_BGR2GRAY,
    "hsv":  cv2.COLOR_BGR2HSV,
    "lab":  cv2.COLOR_BGR2LAB,
}


def convert_to(frame, color_format):
    """Convert a BGR frame to another colour format ("gray", "hsv" or "lab").
    Returns a new image; the input frame is not changed."""
    return cv2.cvtColor(frame, COLOR_CONVERSIONS[color_format])


def draw_box(frame, point, size=20, color=(255, 0, 0), thickness=2):
    """Draw a square box of side `size` centred on point (x, y). Draws in place."""
    x, y = point
    half = size // 2
    cv2.rectangle(frame, (x - half, y - half), (x + half, y + half), color, thickness)
    return frame
