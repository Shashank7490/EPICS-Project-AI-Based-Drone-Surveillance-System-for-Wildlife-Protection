import os

def check_pairs(dataset_path):
    splits = ["train", "val", "test"]
    total_images = 0
    total_labels = 0
    mismatches = []

    for split in splits:
        images_dir = os.path.join(dataset_path, split, "images")
        labels_dir = os.path.join(dataset_path, split, "labels")

        if not os.path.exists(images_dir) or not os.path.exists(labels_dir):
            continue

        image_files = [os.path.splitext(f)[0] for f in os.listdir(images_dir) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
        label_files = [os.path.splitext(f)[0] for f in os.listdir(labels_dir) if f.lower().endswith(".txt")]

        total_images += len(image_files)
        total_labels += len(label_files)

        # mismatched files
        for img in image_files:
            if img not in label_files:
                mismatches.append(f"❌ Missing label for {split}/images/{img}")

        for lbl in label_files:
            if lbl not in image_files:
                mismatches.append(f"❌ Missing image for {split}/labels/{lbl}")

    print(f"📊 Total Images: {total_images}, Total Labels: {total_labels}")
    if mismatches:
        print("\n⚠️ Mismatches found:")
        for m in mismatches:
            print(m)
    else:
        print("✅ All images and labels are properly paired!")

# Example usage
check_pairs("/Users/shashankk/Downloads/NewCheetah")