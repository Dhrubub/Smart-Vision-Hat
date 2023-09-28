import cv2
import json

# Load YOLO model
net = cv2.dnn.readNet('./yolov3.weights', './yolov3.cfg')

# Load class names from your config file
with open('config.json') as config_file:
    config = json.load(config_file)
    classNames = config["classes"]["classNames"]

# Open video capture
cap = cv2.VideoCapture(config["videoCapture"]["device"])
cap.set(cv2.CAP_PROP_FRAME_WIDTH, config["videoCapture"]["width"])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config["videoCapture"]["height"])

if cap.isOpened():
    while True:
        ret, frame = cap.read()
        
        # Prepare the frame for YOLO object detection
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)

        # Perform object detection
        detections = net.forward()

        # Loop through detected objects
        for detection in detections:
            for obj in detection:
                # Get bounding box coordinates
                x, y, width, height = obj[0:4]
                x = int(x * frame.shape[1])
                y = int(y * frame.shape[0])
                width = int(width * frame.shape[1])
                height = int(height * frame.shape[0])

                # Get class scores starting from index 5
                class_scores = obj[5:]

                # Find the class with the highest score
                class_id = class_scores.argmax()

                # Get the confidence score
                confidence = class_scores[class_id]

                # Check if the detection confidence is above a certain threshold (e.g., 0.5)
                if confidence > 0.5:
                    # Draw bounding box and label
                    color = (0, 255, 0)  # Green color
                    cv2.rectangle(frame, (x, y), (x + width, y + height), color, 2)
                    cv2.putText(frame, classNames[class_id], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Display the frame with detections
        cv2.imshow("Video", frame)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()


