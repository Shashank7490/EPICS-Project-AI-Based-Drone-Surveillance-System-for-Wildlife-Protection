from ultralytics import YOLO
model = YOLO("D:/PROJECTS/EPICS_mlMODEL/runs/train/wildlife_yolov8_final14/weights/best.pt")
model.export(format="onnx")