import os

def count_images_labels(dataset_path):
    """
    Count total number of images and labels in YOLOv8 dataset (train/val/test).
    
    Args:
        dataset_path (str): Path to dataset containing train/val/test folders.
    """
    splits = ["train", "valid", "test"]
    total_images = 0
    total_labels = 0

    for split in splits:
        images_dir = os.path.join(dataset_path, split, "images")
        labels_dir = os.path.join(dataset_path, split, "labels")

        if not os.path.exists(images_dir) or not os.path.exists(labels_dir):
            continue

        image_files = [f for f in os.listdir(images_dir) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
        label_files = [f for f in os.listdir(labels_dir) if f.lower().endswith(".txt")]

        total_images += len(image_files)
        total_labels += len(label_files)

    print("📊 TOTAL across dataset:")
    print(f"   🖼️ Images: {total_images}")
    print(f"   📝 Labels: {total_labels}")


# Example usage
dataset_path = "/Users/shashankk/Downloads/NewHumans"
count_images_labels(dataset_path)