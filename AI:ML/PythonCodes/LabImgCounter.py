import os

def count_images_labels(dataset_path):
    """
    Count number of images and labels in YOLOv8 dataset (train/val/test).
    
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
            print(f"⚠️ {split} split missing 'images' or 'labels' folder.")
            continue

        image_files = [f for f in os.listdir(images_dir) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
        label_files = [f for f in os.listdir(labels_dir) if f.lower().endswith(".txt")]

        total_images += len(image_files)
        total_labels += len(label_files)

        print(f"📂 {split.upper()} set:")
        print(f"   🖼️ Images: {len(image_files)}")
        print(f"   📝 Labels: {len(label_files)}")

        # Optional: Check mismatches
        missing_labels = [img for img in image_files if os.path.splitext(img)[0] + ".txt" not in label_files]
        if missing_labels:
            print(f"   ⚠️ {len(missing_labels)} images have no matching label files.")
        else:
            print(f"   ✅ All images have labels.")

    print("\n📊 TOTAL across dataset:")
    print(f"   🖼️ Images: {total_images}")
    print(f"   📝 Labels: {total_labels}")


# Example usage
dataset_path = "/Users/shashankk/Downloads/weaponDetection"
count_images_labels(dataset_path)