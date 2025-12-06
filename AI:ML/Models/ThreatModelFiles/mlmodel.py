from ultralytics import YOLO
import torch
from multiprocessing import freeze_support

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🚀 Training on {device.upper()}")

    model = YOLO("yolov8m.pt")  # upgraded model for better accuracy

    model.train(
        data="data.yaml",
        epochs=200,
        imgsz=512,
        batch=8,
        name="wildlife_yolov8_final_v2",
        project="runs/train",
        workers=8,
        device=device,
        patience=50,
        
        # Augmentation Boost
        mosaic=1.0,
        mixup=0.2,
        copy_paste=0.3,
        hsv_h=0.02,
        hsv_s=0.7,
        hsv_v=0.4,
        fliplr=0.5,
        perspective=0.0005,

        optimizer="AdamW",
        lr0=0.001,
        cos_lr=True,
        pretrained=True,

        save_period=10,
        deterministic=True,
    )

    print("📊 Validating best model...")
    metrics = model.val()

    print("📦 Exporting ONNX model...")
    model.export(format="onnx")

if __name__ == "__main__":
    freeze_support()
    main()