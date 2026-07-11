from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO("yolo26n.pt")

    results = model.train(
        data="datasets/data.yaml",
        epochs=100,
        imgsz=640,
        batch=32,
        exist_ok=True,
        name="train_combined",
        device=0,
        workers=0
    )

    model.val()
model.val()