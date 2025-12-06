import os

# Path to your dataset (root folder containing train/val/test)
dataset_path = "/Users/shashankk/Downloads/NewThreats/NewWeaponDetection"

# Collect all label files
label_files = []
for split in ["train", "valid", "test"]:
    label_dir = os.path.join(dataset_path, split, "labels")
    if os.path.exists(label_dir):
        for f in os.listdir(label_dir):
            if f.endswith(".txt"):
                label_files.append(os.path.join(label_dir, f))

# Track class IDs
class_ids = set()

# Read all label files
for file in label_files:
    with open(file, "r") as f:
        for line in f:
            parts = line.strip().split()
            if parts:  # skip empty lines
                class_id = int(parts[0])  # first value is class ID
                class_ids.add(class_id)

print("Unique class IDs found:", sorted(class_ids))
print("Total unique classes:", len(class_ids))