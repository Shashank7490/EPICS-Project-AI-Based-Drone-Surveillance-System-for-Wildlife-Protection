import os
import random
import shutil

# Source paths
source_images = "/Users/shashankk/Downloads/Humans/train/images"
source_labels = "/Users/shashankk/Downloads/Humans/train/labels"

output_path = "/Users/shashankk/Downloads/NewHumans"

train_count = 1099
test_count = 235
valid_count = 236

# Create output folder structure
for split in ["train", "test", "valid"]:
    os.makedirs(os.path.join(output_path, split, "images"), exist_ok=True)
    os.makedirs(os.path.join(output_path, split, "labels"), exist_ok=True)

# Read image-label pairs correctly
images = [f for f in os.listdir(source_images) if f.lower().endswith(".jpg")]
valid_pairs = []

for img in images:
    label = os.path.splitext(img)[0] + ".txt"
    if os.path.exists(os.path.join(source_labels, label)):
        valid_pairs.append(img)

print(f"Found {len(valid_pairs)} valid image-label pairs")

random.shuffle(valid_pairs)

# Split dataset
train_imgs = valid_pairs[:train_count]
test_imgs = valid_pairs[train_count:train_count + test_count]
valid_imgs = valid_pairs[train_count + test_count:train_count + test_count + valid_count]

def move_files(files, split):
    for img in files:
        label = os.path.splitext(img)[0] + ".txt"

        img_src = os.path.join(source_images, img)
        label_src = os.path.join(source_labels, label)

        img_dest = os.path.join(output_path, split, "images", img)
        label_dest = os.path.join(output_path, split, "labels", label)

        shutil.copy(img_src, img_dest)
        shutil.copy(label_src, label_dest)

# Copy datasets
move_files(train_imgs, "train")
move_files(test_imgs, "test")
move_files(valid_imgs, "valid")

print("Dataset successfully split!")
print(f"Train: {len(train_imgs)}, Test: {len(test_imgs)}, Valid: {len(valid_imgs)}")