import os
import random
import shutil

def split_yolo_dataset(dataset_path, output_path, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, seed=42):
    random.seed(seed)

    # Paths
    images_path = os.path.join(dataset_path, "images")
    labels_path = os.path.join(dataset_path, "labels")

    # Collect all image files
    image_files = [f for f in os.listdir(images_path) if f.endswith((".jpg", ".png"))]
    random.shuffle(image_files)

    total_images = len(image_files)
    train_end = int(total_images * train_ratio)
    val_end = train_end + int(total_images * val_ratio)

    splits = {
        "train": image_files[:train_end],
        "valid": image_files[train_end:val_end],
        "test":  image_files[val_end:]
    }

    for split, files in splits.items():
        print(f"{split}: {len(files)} images")

        split_img_dir = os.path.join(output_path, split, "images")
        split_lbl_dir = os.path.join(output_path, split, "labels")
        os.makedirs(split_img_dir, exist_ok=True)
        os.makedirs(split_lbl_dir, exist_ok=True)

        for img_file in files:
            # Copy image
            shutil.copy(os.path.join(images_path, img_file), os.path.join(split_img_dir, img_file))

            # Copy label
            label_file = os.path.splitext(img_file)[0] + ".txt"
            src_label = os.path.join(labels_path, label_file)
            if os.path.exists(src_label):
                shutil.copy(src_label, os.path.join(split_lbl_dir, label_file))
            else:
                print(f"⚠️ Warning: No label found for {img_file}")

# Example usage
dataset_path = "/Users/shashankk/Desktop/Data Science and AIML/EPICS/Jackal/train"  
output_path = "/Users/shashankk/Desktop/Data Science and AIML/EPICS/NewJackal"  

split_yolo_dataset(dataset_path, output_path)