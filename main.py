import cv2
import csv
import os
import time
import numpy as np
from helpers import image_location_detectors as det
from helpers import image_manipulation as manip

# ----- CONSTANTS ----- #
CAMERA_INDEX = 0  # laptop camera
BRIGHTEST_METHOD = "opencv"  # "opencv", "numpy" or "loop"



BRIGHTEST_FUNCTIONS = {
    "opencv": det.brightest_opencv,
    "numpy":  det.brightest_numpy,
    "loop":   det.brightest_loop,
}


# ----- GLOBALS ----- #
t_prev = 0  # time of the previous get_fps() call ; used in fps calculation

def get_fps():
    global t_prev
    
    t_now = time.perf_counter()
    
    # Get delta t
    dt = 1 if t_prev is None else t_now - t_prev
    
    t_prev = t_now
    
    return 1/dt

def pixel_hex(frame, point):
    # Colour of one pixel as an RGB hex string, e.g. "#FF0000" for pure red
    x, y = point
    b, g, r = frame[y, x]
    return f"#{r:02X}{g:02X}{b:02X}"

def process_frame(frame):
    
    # Convert to grayscale
    frame_gray = manip.convert_to(frame, "gray")
    
    # Convert to Lab
    frame_lab = manip.convert_to(frame, "lab")
    
    # Find brightest point
    bright_point, bright_value = BRIGHTEST_FUNCTIONS[BRIGHTEST_METHOD](frame_gray)
    
    # Find reddest points
    red_point_bgr, red_value_bgr = det.reddest_bgr(frame)
    red_point_lab, red_value_lab = det.reddest_lab(frame_lab)
    
    # Original pixel colours at those points (before the boxes are drawn)
    bright_rgb = pixel_hex(frame, bright_point)
    red_rgb_bgr = pixel_hex(frame, red_point_bgr)
    red_rgb_lab = pixel_hex(frame, red_point_lab)
    
    # Draw boxes: brightest = blue, reddest BGR = green, reddest Lab = yellow
    manip.draw_box(frame, bright_point)
    manip.draw_box(frame, red_point_bgr, color=(0, 255, 255))
    manip.draw_box(frame, red_point_lab, color=(255, 0, 255))
    
    # FPS
    fps = get_fps()
    text_fps = f"FPS: {fps:.1f}"
    cv2.putText(img = frame, 
                text = text_fps, 
                org = (10,30), 
                fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
                fontScale = 1, 
                color = (0, 0, 255),  # BGR: red
                thickness = 2)
    
    # One row of measurements for this frame
    measurement = [fps,
                   bright_point[0], bright_point[1], bright_value, bright_rgb,
                   red_point_bgr[0], red_point_bgr[1], red_value_bgr, red_rgb_bgr,
                   red_point_lab[0], red_point_lab[1], red_value_lab, red_rgb_lab]
    
    return frame, measurement

def save_data(filename, data):
    path = "results"
    os.makedirs(path, exist_ok=True)
    
    # One row per frame: frame number + the measurement from process_frame
    with open(os.path.join(path, filename), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["frame", "fps",
                         "bright_x", "bright_y", "bright_value", "bright_rgb",
                         "red_bgr_x", "red_bgr_y", "red_bgr_value", "red_bgr_rgb",
                         "red_lab_x", "red_lab_y", "red_lab_value", "red_lab_rgb"])
        for i, measurement in enumerate(data):
            writer.writerow([i] + measurement)


def main():
    
    # Start capture on camera X
    camera = cv2.VideoCapture(CAMERA_INDEX)
    
    # Check fps camera settings
    print(camera.get(cv2.CAP_PROP_FPS), camera.getBackendName())
    
    # Check image size
    print(camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Store previous frame if we want to compare frames
    prev_frame=0 
    
    # Store measurements, one row per frame
    measurements = []
    
    while True:
        # Get next frame
        ret, frame_bgr = camera.read() # ret[bool] If frame read; frame[np array]
        if not ret: continue
        
        ## Debug check: check the frames because FPS was to high
        # print(frame_bgr)
        # print(np.array_equal(frame_bgr, prev))
        # prev=frame_bgr
        
        # Process and show the new frame
        frame, measurement = process_frame(frame_bgr)
        cv2.imshow('frame',frame)
        measurements.append(measurement)
        
        # Check exit command
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # Clean exit
    camera.release()
    cv2.destroyAllWindows()
    
    # Save results
    save_data(f"02_brightest_reddest_spots_{BRIGHTEST_METHOD}.csv", measurements)


if __name__ == "__main__":
    main()
