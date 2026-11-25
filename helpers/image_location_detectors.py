"""
Functions that find a specific location in an image. 

input: BGR frame
output: location (x,y), value at that location
"""

import cv2
import numpy as np


# ----- Brightest spots ------------------------------------------------- #

def brightest_opencv(frame):
    """Brightest spot using an OpenCV function. Input: grayscale frame."""
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(frame)
    return max_loc, max_val


def brightest_numpy(frame):
    """Brightest spot using NumPy array operations. Input: grayscale frame."""
    flat_index = np.argmax(frame)                       # as if the image were one long row
    y, x = np.unravel_index(flat_index, frame.shape)    # back to (row, col) = (y, x)
    return (int(x), int(y)), int(frame[y, x])


def brightest_loop(frame):
    """Brightest spot using a double for-loop over the pixels. Input: grayscale frame."""
    height, width = frame.shape
    max_val = -1
    max_loc = (0, 0)
    for y in range(height):
        for x in range(width):
            if frame[y, x] > max_val:
                max_val = frame[y, x]
                max_loc = (x, y)
    return max_loc, int(max_val)



# ----- REDest spots ------------------------------------------------- #

def reddest_bgr(frame):
    """Reddest spot in BGR: redness = R - (G+B)/2. Input: BGR frame."""
    frame_int = frame.astype(np.int16)              # signed, so subtraction doesn't wrap around
    b, g, r = frame_int[:, :, 0], frame_int[:, :, 1], frame_int[:, :, 2]
    redness = r - (g + b) / 2
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(redness)
    return max_loc, max_val


def reddest_lab(frame_lab):
    """Reddest spot in L*a*b*: redness = a* channel. Input: Lab frame."""
    a = frame_lab[:, :, 1]                          # green (low) <-> red (high), 128 = neutral
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(a)
    return max_loc, max_val
