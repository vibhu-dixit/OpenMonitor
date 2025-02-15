from django.shortcuts import render

# Create your views here.

from ultralytics import YOLO
import cv2
import numpy as np
import os

def get_inference(frame):
    model = YOLO('yolov8x.pt')  # Using a more accurate model

    # Get video properties
    height, width, channels = frame.shape

        # Apply histogram equalization to each channel for better contrast
    b, g, r = cv2.split(frame)
    b_eq = cv2.equalizeHist(b)
    g_eq = cv2.equalizeHist(g)
    r_eq = cv2.equalizeHist(r)
    frame_eq = cv2.merge((b_eq, g_eq, r_eq))

    # Run YOLO model with a lower confidence threshold
    results = model(frame_eq, conf=0.6)[0]  # Lowering confidence threshold to 0.3

    person_detected = False

    # Process results
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        class_name = results.names[int(class_id)]

        # Only process 'person' detections
        if class_name == 'person':
            person_detected = True
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)
            cv2.putText(frame, f'{class_name} {score:.2f}', (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

            return frame
    return False
