import os
import random
import shutil

def trim_dataset(dataset_path, target_count, output_path):
    """
    Trims a YOLOv8 dataset (images + labels) to a target count.
    
    Args:
        dataset_path (str): Path to dataset (with 'images' and 'labels' subfolders).
        target_count (int): Number of samples to keep.
        output_path (str): Where to save trimmed dataset.
    """

    images_path = os.path.join(dataset_path, "images")
    labels_path = os.path.join(dataset_path, "labels")

    # Get all image files (assuming .jpg/.png)  
    all_images = [f for f in os.listdir(images_path) if f.endswith((".jpg", ".png"))]
    random.shuffle(all_images)

    # Trim to target count
    selected_images = all_images[:target_count]

    # Make output dirs
    os.makedirs(os.path.join(output_path, "images"), exist_ok=True)
    os.makedirs(os.path.join(output_path, "labels"), exist_ok=True)

    for img_file in selected_images:
        label_file = os.path.splitext(img_file)[0] + ".txt"

        # Copy image
        shutil.copy(os.path.join(images_path, img_file),
                    os.path.join(output_path, "images", img_file))

        # Copy corresponding label if it exists
        label_src = os.path.join(labels_path, label_file)
        if os.path.exists(label_src):
            shutil.copy(label_src,
                        os.path.join(output_path, "labels", label_file))

    print(f"Trimmed dataset saved to {output_path} with {len(selected_images)} images.")
    

# Example usage
dataset_path = "/Users/shashankk/Downloads/ForestFire/valid"
output_path = "/Users/shashankk/Downloads/NewForestFire/val"
target_count = 161 # set based on smallest dataset
trim_dataset(dataset_path, target_count, output_path)