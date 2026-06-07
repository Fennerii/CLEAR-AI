import cv2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

Recyclable_items = ['bottle', 'can', 'box']

def detection(frame):
    results = model(frame)
    detected_objects = []
    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            confidence = box.conf[0].item()
            label = model.names[class_id]
            if confidence > 0.5 and label in Recyclable_items:
                detected_objects.append(label)
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return frame, detected_objects

def main():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame, detected_objects = detection(frame)
        cv2.imshow("CLEAR-AI", frame)
        if detected_objects:
            print("Detected:", detected_objects)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()