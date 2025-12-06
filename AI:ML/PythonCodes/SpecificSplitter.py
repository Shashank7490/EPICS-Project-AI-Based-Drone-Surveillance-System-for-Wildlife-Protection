import os
import random
import shutil

def split_by_class(dataset_path, output_path, class_names, target_classes, ratios=(0.7, 0.15, 0.15), seed=42):
    random.seed(seed)

    images_dir = os.path.join(dataset_path, "images")
    labels_dir = os.path.join(dataset_path, "labels")

    for target_class in target_classes:
        class_id = class_names.index(target_class)

        # Collect all images that contain this class
        class_images = []
        for label_file in os.listdir(labels_dir):
            if not label_file.endswith(".txt"):
                continue
            label_path = os.path.join(labels_dir, label_file)

            with open(label_path, "r") as f:
                lines = f.readlines()

            keep = [line for line in lines if int(line.split()[0]) == class_id]
            if keep:
                class_images.append((label_file, keep))

        # Shuffle and split
        random.shuffle(class_images)
        n_total = len(class_images)
        n_train = int(n_total * ratios[0])
        n_val = int(n_total * ratios[1])
        n_test = n_total - n_train - n_val

        splits = {
            "train": class_images[:n_train],
            "valid": class_images[n_train:n_train + n_val],
            "test": class_images[n_train + n_val:]
        }

        # Create dirs
        for split in splits:
            os.makedirs(os.path.join(output_path, target_class, split, "images"), exist_ok=True)
            os.makedirs(os.path.join(output_path, target_class, split, "labels"), exist_ok=True)

        # Save data
        for split, items in splits.items():
            for label_file, lines in items:
                img_file = os.path.splitext(label_file)[0] + ".jpg"
                src_img = os.path.join(images_dir, img_file)
                dst_img = os.path.join(output_path, target_class, split, "images", img_file)

                if os.path.exists(src_img):
                    shutil.copy(src_img, dst_img)

                dst_label = os.path.join(output_path, target_class, split, "labels", label_file)
                with open(dst_label, "w") as f:
                    for line in lines:
                        parts = line.strip().split()
                        parts[0] = "0"  # reindex class to 0 for single-class dataset
                        f.write(" ".join(parts) + "\n")

        print(f"✅ {target_class}: {n_total} images → train {n_train}, valid {n_val}, test {n_test}")


# Example usage
dataset_path = "/Users/shashankk/Desktop/Data Science and AIML/EPICS/Animals/train"  # dataset with images/ + labels/
output_path = "/Users/shashankk/Desktop/Data Science and AIML/EPICS/NewAnimals"

all_classes = ["cheetah", "hyena", "lion", "tiger", "wolf"]  # same order as in dataset.yaml
target_classes = ["cheetah", "lion", "tiger"]  # animals you want

split_by_class(dataset_path, output_path, all_classes, target_classes)