# from ultralytics import YOLO
# import cv2

# model = YOLO('yolov8s.pt')


# img = cv2.imread('test_beach_image.jpg')
# results = model(img)[0]

# results.save(filename = 'output3.jpg')

# plotted_img = results.plot()
# cv2.imwrite('output3.jpg',plotted_img)


# for result in results.boxes.data.tolist():
#     x1,y1,x2,y2,score,class_id = result
#     class_name = results.names[int(class_id)]
#     cv2.rectangle(img, (int(x1),int(y1)),(int(x2),int(y2)), (0,0,0),4)
#     cv2.putText(img, f'{class_name}{score:.2f}',(int(x1),int(y1)),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),3)
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.imwrite('output.jpg',img)

# cv2.destroyAllWindows()

# # cap = cv2.VideoCapture(0)
# # cap.set(3,1200)
# # cap.set(4,720)
# # while True:
# #     ret, frame = cap.read()
# #     if not ret:
# #         break
# #     results =model(frame)[0]

# #     for result in results.boxes.data.tolist():
# #         x1,y1,x2,y2,score,class_id = result
# #         class_name = results.names[int(class_id)]
# #         cv2.rectangle(img, (int(x1),int(y1)),(int(x2),int(y2)), (0,0,0),4)
# #         cv2.putText(img, f'{class_name}{score:.2f}',(int(x1),int(y1)),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),3)
# #     cv2.imshow('image',frame)
# #     cv2.waitKey(0)

# from ultralytics import YOLO
# import cv2
# import numpy as np

# # Load YOLO model
# model = YOLO('yolov8x.pt')  # Using a more accurate model

# # Read image
# img = cv2.imread('test_beach_image.jpg')
# height, width, _ = img.shape

# # Split the image into its respective Blue, Green, and Red channels
# b, g, r = cv2.split(img)

# # Apply histogram equalization to each channel
# b_eq = cv2.equalizeHist(b)
# g_eq = cv2.equalizeHist(g)
# r_eq = cv2.equalizeHist(r)

# # Merge the equalized channels back into a color image
# img_eq = cv2.merge((b_eq, g_eq, r_eq))

# # Define danger zone (top half of the image)
# danger_zone = np.array([[0, 0], [width, 0], [width, height // 2], [0, height // 2]])

# def is_inside_danger_zone(centroid, polygon):
#     return cv2.pointPolygonTest(polygon, centroid, False) >= 0

# # Run YOLO model with a lower confidence threshold
# results = model(img_eq, conf=0.6)[0]  # Lowering confidence threshold to 0.3

# # Process results
# for result in results.boxes.data.tolist():
#     x1, y1, x2, y2, score, class_id = result
#     class_name = results.names[int(class_id)]
    
#     # Only process 'person' detections
#     if class_name == 'person':
#         centroid = ((x1 + x2) // 2, (y1 + y2) // 2)
        
#         if is_inside_danger_zone(centroid, danger_zone):
#             cv2.rectangle(img_eq, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)
#             cv2.putText(img_eq, f'{class_name} {score:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

# # Show and save image
# cv2.imshow('image', img_eq)
# cv2.waitKey(0)
# cv2.imwrite('output_danger_zone.jpg', img_eq)
# cv2.destroyAllWindows()

from ultralytics import YOLO
import cv2
import numpy as np
import os

# Load YOLO model
model = YOLO('yolov8x.pt')  # Using a more accurate model

# Open the video file
cap = cv2.VideoCapture('sample_video.mp4')

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (width, height))

# Define danger zone (top half of the frame)
danger_zone = np.array([[0, 0], [width, 0], [width, height // 2], [0, height // 2]])

# Create directory to save frames with detections
os.makedirs('detected_frames', exist_ok=True)

def is_inside_danger_zone(centroid, polygon):
    return cv2.pointPolygonTest(polygon, centroid, False) >= 0

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

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
            centroid = ((x1 + x2) // 2, (y1 + y2) // 2)

            if is_inside_danger_zone(centroid, danger_zone):
                person_detected = True
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)
                cv2.putText(frame, f'{class_name} {score:.2f}', (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    # If a person is detected in the danger zone, save the frame as an image
    if person_detected:
        cv2.imwrite(f'detected_frames/frame_{frame_count:04d}.jpg', frame)

    # Write the frame to the output video
    out.write(frame)

    # Display the frame (optional)
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
