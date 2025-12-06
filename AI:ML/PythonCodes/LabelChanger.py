import os

def force_class_id(dataset_path, new_id):
    """
    Overwrite ALL class IDs in YOLOv8 dataset labels with a single new ID.

    Args:
        dataset_path (str): Path to dataset (expects train/val/test/labels).
        new_id (int): The class ID to assign to every object.
    """
    total_changed = 0

    for split in ["train", "valid", "test"]:
        labels_dir = os.path.join(dataset_path, split, "labels")
        if not os.path.exists(labels_dir):
            continue

        for label_file in os.listdir(labels_dir):
            if not label_file.endswith(".txt"):
                continue

            file_path = os.path.join(labels_dir, label_file)
            new_lines = []

            with open(file_path, "r") as f:
                for line in f.readlines():
                    parts = line.strip().split()
                    if not parts:
                        continue
                    parts[0] = str(new_id)  # force overwrite ID
                    new_lines.append(" ".join(parts) + "\n")
                    total_changed += 1

            # overwrite file with new IDs
            with open(file_path, "w") as f:
                f.writelines(new_lines)

        print(f"✅ Updated labels in {labels_dir}")

    print(f"\n🎯 Done! Replaced class IDs with {new_id} for {total_changed} objects.")


# Example usage
dataset_path = "/Users/shashankk/Downloads/NewThreats/NewForestFire"

# Force ALL labels to class 0
force_class_id(dataset_path, new_id=4)