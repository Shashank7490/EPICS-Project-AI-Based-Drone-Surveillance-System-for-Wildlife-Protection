import os
import shutil

def filter_yolo_dataset(dataset_path, classes_to_remove, class_names):
    """
    Removes unwanted classes from a YOLOv8 dataset (train/val/test).
    
    Args:
        dataset_path (str): Root dataset path containing train/val/test.
        classes_to_remove (list): List of class names to remove.
        class_names (list): Full list of class names as in dataset.yaml.
    """

    # Map class names to IDs
    class_to_id = {name: idx for idx, name in enumerate(class_names)}
    remove_ids = {class_to_id[name] for name in classes_to_remove}

    # Process each split
    for split in ["train", "valid", "test"]:
        images_dir = os.path.join(dataset_path, split, "images")
        labels_dir = os.path.join(dataset_path, split, "labels")

        if not os.path.exists(images_dir):
            continue

        print(f"Processing {split} set...")

        for label_file in os.listdir(labels_dir):
            if not label_file.endswith(".txt"):
                continue

            label_path = os.path.join(labels_dir, label_file)
            img_file = os.path.splitext(label_file)[0] + ".jpg"
            img_path = os.path.join(images_dir, img_file)

            # Read label file
            with open(label_path, "r") as f:
                lines = f.readlines()

            # Keep only lines NOT in remove_ids
            new_lines = []
            for line in lines:
                parts = line.strip().split()
                if not parts:
                    continue
                cls_id = int(parts[0])
                if cls_id not in remove_ids:
                    new_lines.append(line)

            if not new_lines:
                # No valid labels left → remove image + label
                os.remove(label_path)
                if os.path.exists(img_path):
                    os.remove(img_path)
                print(f"Removed {img_file} (only unwanted classes).")
            else:
                # Save filtered labels
                with open(label_path, "w") as f:
                    f.writelines(new_lines)

        print(f"✅ Finished {split} set.")

# Example usage
dataset_path = "/Users/shashankk/Desktop/Data Science and AIML/EPICS/Animals"
all_classes = ["cheetah", "hyena", "lion", "tiger", "wolf"]  # your dataset.yaml order
remove_classes = ["hyena", "wolf"]

filter_yolo_dataset(dataset_path, remove_classes, all_classes)