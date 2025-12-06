import os
import shutil
import random

def trim_and_split_yolo(dataset_path, output_path, total_images=600, ratios=(0.7, 0.15, 0.15), seed=42):
    random.seed(seed)

    # Collect all (image, label) pairs from train/val/test
    all_pairs = []
    for split in ["train", "val", "test"]:
        img_dir = os.path.join(dataset_path, split, "images")
        lbl_dir = os.path.join(dataset_path, split, "labels")
        if not os.path.exists(img_dir):
            continue
        for img_file in os.listdir(img_dir):
            if img_file.lower().endswith((".jpg", ".jpeg", ".png")):
                lbl_file = os.path.splitext(img_file)[0] + ".txt"
                lbl_path = os.path.join(lbl_dir, lbl_file)
                img_path = os.path.join(img_dir, img_file)
                if os.path.exists(lbl_path):  # only include if label exists
                    all_pairs.append((img_path, lbl_path))

    print(f"📊 Found {len(all_pairs)} total images with labels")

    # If dataset has fewer than required
    if len(all_pairs) < total_images:
        raise ValueError(f"Dataset only has {len(all_pairs)} images, but {total_images} requested")

    # Randomly select subset
    selected = random.sample(all_pairs, total_images)

    # Calculate split sizes
    n_train = int(total_images * ratios[0])
    n_val = int(total_images * ratios[1])
    n_test = total_images - n_train - n_val  # remaining

    train_set = selected[:n_train]
    val_set = selected[n_train:n_train+n_val]
    test_set = selected[n_train+n_val:]

    splits = {
        "train": train_set,
        "val": val_set,
        "test": test_set
    }

    # Create output directories
    for split in splits:
        os.makedirs(os.path.join(output_path, split, "images"), exist_ok=True)
        os.makedirs(os.path.join(output_path, split, "labels"), exist_ok=True)

    # Copy files
    for split, items in splits.items():
        for img_path, lbl_path in items:
            dst_img = os.path.join(output_path, split, "images", os.path.basename(img_path))
            dst_lbl = os.path.join(output_path, split, "labels", os.path.basename(lbl_path))
            shutil.copy(img_path, dst_img)
            shutil.copy(lbl_path, dst_lbl)
        print(f"✅ {split}: {len(items)} images")

    print(f"\n🎯 Trimmed dataset created at {output_path}")


# Example usage
dataset_path = "/Users/shashankk/Desktop/Data Science and AIML/EPICS/NewTiger"
output_path = "/Users/shashankk/Desktop/Data Science and AIML/EPICS/NewTiger2"

trim_and_split_yolo(dataset_path, output_path, total_images=600)