import os
import shutil

def merge_yolo_datasets(dataset1, dataset2, output_path):
    """
    Merge two YOLOv8 datasets (with same classes) into one.
    Keeps train/val/test splits intact if present in both.
    """

    splits = ["train", "val", "test"]

    for split in splits:
        for sub in ["images", "labels"]:
            os.makedirs(os.path.join(output_path, split, sub), exist_ok=True)

        for dataset in [dataset1, dataset2]:
            img_dir = os.path.join(dataset, split, "images")
            lbl_dir = os.path.join(dataset, split, "labels")

            if not os.path.exists(img_dir):
                continue  # skip if this dataset has no split

            for file in os.listdir(img_dir):
                src_img = os.path.join(img_dir, file)
                src_lbl = os.path.join(lbl_dir, os.path.splitext(file)[0] + ".txt")

                dst_img = os.path.join(output_path, split, "images", file)
                dst_lbl = os.path.join(output_path, split, "labels", os.path.splitext(file)[0] + ".txt")

                # Avoid overwriting duplicates
                if not os.path.exists(dst_img):
                    shutil.copy(src_img, dst_img)
                if os.path.exists(src_lbl) and not os.path.exists(dst_lbl):
                    shutil.copy(src_lbl, dst_lbl)

        print(f"✅ Merged {split} set")

    print(f"\n🎯 All datasets merged into: {output_path}")


# Example usage
dataset1 = "/Users/shashankk/Desktop/Data Science and AIML/EPICS/tiger"
dataset2 = "/Users/shashankk/Downloads/tiger"
output_path = "/Users/shashankk/Desktop/Data Science and AIML/EPICS/NewTiger"

merge_yolo_datasets(dataset1, dataset2, output_path)