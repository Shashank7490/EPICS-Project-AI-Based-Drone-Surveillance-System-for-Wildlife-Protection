from ultralytics import YOLO
import torch
from multiprocessing import freeze_support

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"✅ Using {device.upper()}")

    # Load model
    model = YOLO("yolov8s.pt")

    # Train
    model.train(
        data="data.yaml",
        epochs=150,
        imgsz=256,
        batch=16,
        name="wildlife_yolov8_final",
        project="runs/train",
        workers=8,
        device=device,
        patience=20,
        optimizer="AdamW",
        lr0=0.001,
        augment=True,
        cos_lr=True,
        pretrained=True,
        save_period=5
    )

    # Validate
    metrics = model.val()

    # Export to ONNX
    model.export(format="onnx")

if __name__ == "__main__":
    freeze_support()  # Important for Windows
    main()