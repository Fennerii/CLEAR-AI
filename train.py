from ultralytics import YOLO

model = YOLO("yolo26n.pt")

results = model.train(
    data="datasets/data.yaml",
    epochs=100,
    imgsz=640,
    batch=32,
    exist_ok=True,
    name="train_combined"
)

model.val()