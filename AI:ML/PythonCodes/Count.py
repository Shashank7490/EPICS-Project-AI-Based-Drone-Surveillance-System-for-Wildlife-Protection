import os

def count_yolo_files(dataset_path, split="train"):
    images_path = os.path.join(dataset_path, split, "images")
    labels_path = os.path.join(dataset_path, split, "labels")

    # Count images (.jpg and .png)
    image_files = [f for f in os.listdir(images_path) if f.endswith((".jpg", ".png"))]
    label_files = [f for f in os.listdir(labels_path) if f.endswith(".txt")]

    print(f"Dataset: {dataset_path}/{split}")
    print(f"Number of images: {len(image_files)}")
    print(f"Number of labels: {len(label_files)}")

    # Check if any labels are missing for images
    missing_labels = []
    for img in image_files:
        label_file = os.path.splitext(img)[0] + ".txt"
        if label_file not in label_files:
            missing_labels.append(img)

    if missing_labels:
        print(f"⚠️ Warning: {len(missing_labels)} images have no corresponding label files.")
    else:
        print("✅ All images have matching labels.")

# Example usage
dataset_path = "/Users/shashankk/Downloads/NewHumans"
count_yolo_files(dataset_path, "train")
count_yolo_files(dataset_path, "valid")
count_yolo_files(dataset_path, "test")
