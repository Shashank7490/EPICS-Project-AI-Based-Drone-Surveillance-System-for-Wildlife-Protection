import os
import random
import shutil

# Paths
source_path = "dataset_all"  # folder containing all images & labels
output_path = "dataset_split"  # destination folder

train_count = 2800
test_count = 420
valid_count = 420

# Create output subfolders
for split in ["train", "test", "valid"]:
    os.makedirs(os.path.join(output_path, split, "images"), exist_ok=True)
    os.makedirs(os.path.join(output_path, split, "labels"), exist_ok=True)

# Fetch only images
image_exts = [".jpg", ".jpeg", ".png"]
images = [f for f in os.listdir(source_path) if os.path.splitext(f)[1].lower() in image_exts]

random.shuffle(images)

train_imgs = images[:train_count]
test_imgs = images[train_count : train_count + test_count]
valid_imgs = images[train_count + test_count : train_count + test_count + valid_count]

def move_files(file_list, split_name):
    for img in file_list:
        img_path = os.path.join(source_path, img)
        label_path = os.path.join(source_path, os.path.splitext(img)[0] + ".txt")

        # Copy image
        shutil.copy(img_path, os.path.join(output_path, split_name, "images", img))

        # Copy label if exists
        if os.path.exists(label_path):
            shutil.copy(label_path, os.path.join(output_path, split_name, "labels", os.path.basename(label_path)))

# Move files
move_files(train_imgs, "train")
move_files(test_imgs, "test")
move_files(valid_imgs, "valid")

print("Dataset successfully split!")
print(f"Train: {len(train_imgs)}, Test: {len(test_imgs)}, Valid: {len(valid_imgs)}")