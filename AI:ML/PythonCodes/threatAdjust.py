# # filename: threatAdjust.py
# import os
# import shutil
# import random
# from pathlib import Path

# # ---------- CONFIG ----------
# # Set this to the folder that contains your dataset. Examples:
# # - .../dataset              (and inside: images/, labels/)
# # - .../datasets/yolov8_data (and inside: images/, labels/)
# DATASET_DIR = Path("/Users/shashankk/Downloads/ForesFireDataset")
# TARGET_TRAIN = 420
# TARGET_VALID = 90
# RANDOM_SEED = 42
# # ----------------------------

# IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")

# def exists_dir(p: Path) -> bool:
#     return p.exists() and p.is_dir()

# def list_subdirs(p: Path):
#     return sorted([d.name for d in p.iterdir() if d.is_dir()]) if exists_dir(p) else []

# def find_images_labels_root(base: Path):
#     """
#     Detect images/ and labels/ dirs under the dataset. Return paths.
#     Accepts structures like:
#       base/images/{train,val,test}, base/labels/{train,val,test}
#     or flat:
#       base/train/images, base/train/labels, etc. (we'll normalize).
#     """
#     images_root = base / "images"
#     labels_root = base / "labels"

#     if exists_dir(images_root) and exists_dir(labels_root):
#         return images_root, labels_root

#     # Try alternate common layout: base/{train,valid,val,test}/{images,labels}
#     split_candidates = ["train", "valid", "val", "test"]
#     split_roots = []
#     for s in split_candidates:
#         split_dir = base / s
#         if exists_dir(split_dir):
#             split_roots.append(split_dir)

#     if split_roots:
#         # Build normalized images_root/labels_root under a temp normalization
#         norm_images_root = base / "_normalized_images"
#         norm_labels_root = base / "_normalized_labels"
#         norm_images_root.mkdir(exist_ok=True)
#         norm_labels_root.mkdir(exist_ok=True)

#         # Move or copy from per-split dirs to normalized dirs
#         for s in split_candidates:
#             split_dir = base / s
#             if not exists_dir(split_dir):
#                 continue
#             # Possible subdirs:
#             img_dir = split_dir / "images"
#             lbl_dir = split_dir / "labels"
#             # Accept flat files inside split (no subdirs)
#             if exists_dir(img_dir):
#                 dest_img_dir = norm_images_root / ("valid" if s == "val" else s)
#                 dest_img_dir.mkdir(parents=True, exist_ok=True)
#                 for p in img_dir.iterdir():
#                     if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
#                         shutil.copy2(p, dest_img_dir / p.name)
#             else:
#                 # flat files as images
#                 dest_img_dir = norm_images_root / ("valid" if s == "val" else s)
#                 dest_img_dir.mkdir(parents=True, exist_ok=True)
#                 for p in split_dir.iterdir():
#                     if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
#                         shutil.copy2(p, dest_img_dir / p.name)

#             if exists_dir(lbl_dir):
#                 dest_lbl_dir = norm_labels_root / ("valid" if s == "val" else s)
#                 dest_lbl_dir.mkdir(parents=True, exist_ok=True)
#                 for p in lbl_dir.iterdir():
#                     if p.is_file() and p.suffix.lower() == ".txt":
#                         shutil.copy2(p, dest_lbl_dir / p.name)
#             else:
#                 # flat files as labels
#                 dest_lbl_dir = norm_labels_root / ("valid" if s == "val" else s)
#                 dest_lbl_dir.mkdir(parents=True, exist_ok=True)
#                 for p in split_dir.iterdir():
#                     if p.is_file() and p.suffix.lower() == ".txt":
#                         shutil.copy2(p, dest_lbl_dir / p.name)

#         return norm_images_root, norm_labels_root

#     # Not found
#     return None, None

# def find_split_name(base_dir: Path, candidates=("train", "valid", "val", "test")):
#     found = {}
#     for name in candidates:
#         p = base_dir / name
#         if exists_dir(p):
#             found[name] = name
#     if "valid" in found and "val" in found:
#         del found["val"]
#     elif "val" in found and "valid" not in found:
#         found["valid"] = found.pop("val")
#     return found

# def list_image_label_pairs(images_dir: Path, labels_dir: Path):
#     pairs = []
#     images = []
#     for ext in IMAGE_EXTS:
#         images.extend(images_dir.glob(f"*{ext}"))
#     image_stems = {img.stem: img for img in images}
#     for stem, img_path in image_stems.items():
#         label_path = labels_dir / f"{stem}.txt"
#         if label_path.exists():
#             pairs.append((img_path, label_path))
#     return pairs

# def report_missing(images_dir: Path, labels_dir: Path):
#     images = []
#     for ext in IMAGE_EXTS:
#         images.extend(images_dir.glob(f"*{ext}"))
#     image_stems = {img.stem for img in images}
#     label_files = list(labels_dir.glob("*.txt"))
#     label_stems = {lbl.stem for lbl in label_files}
#     missing_labels = sorted(image_stems - label_stems)
#     missing_images = sorted(label_stems - image_stems)
#     return missing_labels, missing_images

# def safe_clear_dir(dir_path: Path):
#     dir_path.mkdir(parents=True, exist_ok=True)
#     for p in dir_path.iterdir():
#         if p.is_file():
#             p.unlink()
#         elif p.is_dir():
#             shutil.rmtree(p)

# def copy_pairs(pairs, target_images_dir: Path, target_labels_dir: Path):
#     target_images_dir.mkdir(parents=True, exist_ok=True)
#     target_labels_dir.mkdir(parents=True, exist_ok=True)
#     for img_path, lbl_path in pairs:
#         shutil.copy2(img_path, target_images_dir / img_path.name)
#         shutil.copy2(lbl_path, target_labels_dir / lbl_path.name)

# def resize_split(split_name: str, target_count: int, images_root: Path, labels_root: Path):
#     images_dir = images_root / split_name
#     labels_dir = labels_root / split_name
#     if not exists_dir(images_dir) or not exists_dir(labels_dir):
#         raise FileNotFoundError(f"Missing split directories for {split_name}: {images_dir} or {labels_dir}")

#     missing_labels, missing_images = report_missing(images_dir, labels_dir)
#     if missing_labels:
#         print(f"[WARN] {split_name}: {len(missing_labels)} images without labels. Excluding.")
#     if missing_images:
#         print(f"[WARN] {split_name}: {len(missing_images)} labels without images. Excluding.")

#     pairs = list_image_label_pairs(images_dir, labels_dir)
#     current_count = len(pairs)
#     print(f"[INFO] {split_name}: {current_count} pairs available.")
#     if target_count > current_count:
#         raise ValueError(f"Target {target_count} > available {current_count} in '{split_name}'")

#     random.seed(RANDOM_SEED)
#     selected = random.sample(pairs, target_count)

#     tmp_images = images_root / f".tmp_{split_name}_images"
#     tmp_labels = labels_root / f".tmp_{split_name}_labels"
#     safe_clear_dir(tmp_images)
#     safe_clear_dir(tmp_labels)

#     copy_pairs(selected, tmp_images, tmp_labels)

#     safe_clear_dir(images_dir)
#     safe_clear_dir(labels_dir)

#     for p in tmp_images.iterdir():
#         shutil.move(str(p), images_dir / p.name)
#     for p in tmp_labels.iterdir():
#         shutil.move(str(p), labels_dir / p.name)

#     tmp_images.rmdir()
#     tmp_labels.rmdir()
#     print(f"[DONE] {split_name}: resized to {target_count} pairs.")

# def main():
#     print(f"[DEBUG] DATASET_DIR = {DATASET_DIR}")
#     images_root, labels_root = find_images_labels_root(DATASET_DIR)
#     if images_root is None or labels_root is None:
#         print("[ERROR] Could not detect images/ and labels/ folders under the dataset root.")
#         print("Tips:")
#         print("- Set DATASET_DIR to the directory that contains 'images/' and 'labels/'")
#         print("- Or to a directory that contains split folders like 'train/', 'val/' each having images/labels or flat files.")
#         print("Current directory listing:")
#         if exists_dir(DATASET_DIR):
#             for name in list_subdirs(DATASET_DIR):
#                 print(f"  - {name}/")
#         else:
#             print("  - Dataset dir does not exist.")
#         return

#     print(f"[DEBUG] images_root = {images_root}")
#     print(f"[DEBUG] labels_root = {labels_root}")
#     print(f"[DEBUG] images_root subdirs: {list_subdirs(images_root)}")
#     print(f"[DEBUG] labels_root subdirs: {list_subdirs(labels_root)}")

#     image_splits = find_split_name(images_root, candidates=("train", "valid", "val", "test"))
#     label_splits = find_split_name(labels_root, candidates=("train", "valid", "val", "test"))

#     print(f"[DEBUG] detected image_splits: {list(image_splits.keys())}")
#     print(f"[DEBUG] detected label_splits: {list(label_splits.keys())}")

#     for split in ("train", "valid", "test"):
#         if split not in image_splits or split not in label_splits:
#             raise FileNotFoundError(
#                 f"Missing split '{split}' in images or labels.\n"
#                 f"Images has: {list(image_splits.keys())}, Labels has: {list(label_splits.keys())}\n"
#                 f"If you use 'val', it will be normalized to 'valid' automatically."
#             )

#     resize_split("train", TARGET_TRAIN, images_root, labels_root)
#     resize_split("valid", TARGET_VALID, images_root, labels_root)
#     print("[INFO] Test split left unchanged.")

# if __name__ == "__main__":
#     main()

# filename: finalize_normalized_dataset.py
# from pathlib import Path
# import shutil

# DATASET_DIR = Path("/Users/shashankk/Downloads/ForesFireDataset")

# def replace_dir(src: Path, dst: Path):
#     dst.mkdir(parents=True, exist_ok=True)
#     # Clear destination
#     for p in dst.iterdir():
#         if p.is_file():
#             p.unlink()
#         else:
#             shutil.rmtree(p)
#     # Copy from src
#     for sub in src.iterdir():
#         if sub.is_dir():
#             shutil.copytree(sub, dst / sub.name)
#         else:
#             shutil.copy2(sub, dst / sub.name)

# def main():
#     norm_images = DATASET_DIR / "_normalized_images"
#     norm_labels = DATASET_DIR / "_normalized_labels"
#     final_images = DATASET_DIR / "images"
#     final_labels = DATASET_DIR / "labels"

#     if not norm_images.exists() or not norm_labels.exists():
#         raise FileNotFoundError("Normalized folders not found. Run threatAdjust.py first.")

#     replace_dir(norm_images, final_images)
#     replace_dir(norm_labels, final_labels)

#     print("[DONE] Finalized dataset to:")
#     print(f" - {final_images}")
#     print(f" - {final_labels}")
#     print("Splits inside should be train/ valid/ test/")

# if __name__ == "__main__":
#     main()


# filename: threatAdjust.py
# import os
# import shutil
# import random
# from pathlib import Path

# # ---------- CONFIG ----------
# DATASET_DIR = Path("/Users/shashankk/Downloads/ForesFireDataset")
# TARGETS = {
#     "train": 420,
#     "valid": 90,   # 'val' is normalized to 'valid'
#     "test": 90
# }
# RANDOM_SEED = 42
# # ----------------------------

# IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")

# def exists_dir(p: Path) -> bool:
#     return p.exists() and p.is_dir()

# def list_subdirs(p: Path):
#     return sorted([d.name for d in p.iterdir() if d.is_dir()]) if exists_dir(p) else []

# def find_images_labels_root(base: Path):
#     """
#     Detect images/ and labels/ dirs under the dataset. Return paths.
#     Accepts structures like:
#       base/images/{train,val,test}, base/labels/{train,val,test}
#     or flat:
#       base/train/images, base/train/labels, etc. (we'll normalize).
#     """
#     images_root = base / "images"
#     labels_root = base / "labels"

#     if exists_dir(images_root) and exists_dir(labels_root):
#         return images_root, labels_root

#     # Try alternate common layout: base/{train,valid,val,test}/{images,labels}
#     split_candidates = ["train", "valid", "val", "test"]
#     split_roots = []
#     for s in split_candidates:
#         split_dir = base / s
#         if exists_dir(split_dir):
#             split_roots.append(split_dir)

#     if split_roots:
#         norm_images_root = base / "_normalized_images"
#         norm_labels_root = base / "_normalized_labels"
#         norm_images_root.mkdir(exist_ok=True)
#         norm_labels_root.mkdir(exist_ok=True)

#         for s in split_candidates:
#             split_dir = base / s
#             if not exists_dir(split_dir):
#                 continue

#             # Images
#             img_dir = split_dir / "images"
#             dest_img_dir = norm_images_root / ("valid" if s == "val" else s)
#             dest_img_dir.mkdir(parents=True, exist_ok=True)
#             if exists_dir(img_dir):
#                 for p in img_dir.iterdir():
#                     if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
#                         shutil.copy2(p, dest_img_dir / p.name)
#             else:
#                 for p in split_dir.iterdir():
#                     if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
#                         shutil.copy2(p, dest_img_dir / p.name)

#             # Labels
#             lbl_dir = split_dir / "labels"
#             dest_lbl_dir = norm_labels_root / ("valid" if s == "val" else s)
#             dest_lbl_dir.mkdir(parents=True, exist_ok=True)
#             if exists_dir(lbl_dir):
#                 for p in lbl_dir.iterdir():
#                     if p.is_file() and p.suffix.lower() == ".txt":
#                         shutil.copy2(p, dest_lbl_dir / p.name)
#             else:
#                 for p in split_dir.iterdir():
#                     if p.is_file() and p.suffix.lower() == ".txt":
#                         shutil.copy2(p, dest_lbl_dir / p.name)

#         return norm_images_root, norm_labels_root

#     return None, None

# def find_split_name(base_dir: Path, candidates=("train", "valid", "val", "test")):
#     found = {}
#     for name in candidates:
#         p = base_dir / name
#         if exists_dir(p):
#             found[name] = name
#     if "valid" in found and "val" in found:
#         del found["val"]
#     elif "val" in found and "valid" not in found:
#         found["valid"] = found.pop("val")
#     return found

# def list_image_label_pairs(images_dir: Path, labels_dir: Path):
#     pairs = []
#     images = []
#     for ext in IMAGE_EXTS:
#         images.extend(images_dir.glob(f"*{ext}"))
#     image_stems = {img.stem: img for img in images}
#     for stem, img_path in image_stems.items():
#         label_path = labels_dir / f"{stem}.txt"
#         if label_path.exists():
#             pairs.append((img_path, label_path))
#     return pairs

# def report_missing(images_dir: Path, labels_dir: Path):
#     images = []
#     for ext in IMAGE_EXTS:
#         images.extend(images_dir.glob(f"*{ext}"))
#     image_stems = {img.stem for img in images}
#     label_files = list(labels_dir.glob("*.txt"))
#     label_stems = {lbl.stem for lbl in label_files}
#     missing_labels = sorted(image_stems - label_stems)
#     missing_images = sorted(label_stems - image_stems)
#     return missing_labels, missing_images

# def safe_clear_dir(dir_path: Path):
#     dir_path.mkdir(parents=True, exist_ok=True)
#     for p in list(dir_path.iterdir()):
#         if p.is_file():
#             p.unlink()
#         elif p.is_dir():
#             shutil.rmtree(p)

# def copy_pairs(pairs, target_images_dir: Path, target_labels_dir: Path):
#     target_images_dir.mkdir(parents=True, exist_ok=True)
#     target_labels_dir.mkdir(parents=True, exist_ok=True)
#     for img_path, lbl_path in pairs:
#         shutil.copy2(img_path, target_images_dir / img_path.name)
#         shutil.copy2(lbl_path, target_labels_dir / lbl_path.name)

# def resize_split(split_name: str, target_count: int, images_root: Path, labels_root: Path):
#     images_dir = images_root / split_name
#     labels_dir = labels_root / split_name
#     if not exists_dir(images_dir) or not exists_dir(labels_dir):
#         raise FileNotFoundError(f"Missing split directories for {split_name}: {images_dir} or {labels_dir}")

#     missing_labels, missing_images = report_missing(images_dir, labels_dir)
#     if missing_labels:
#         print(f"[WARN] {split_name}: {len(missing_labels)} images without labels. Excluding.")
#     if missing_images:
#         print(f"[WARN] {split_name}: {len(missing_images)} labels without images. Excluding.")

#     pairs = list_image_label_pairs(images_dir, labels_dir)
#     current_count = len(pairs)
#     print(f"[INFO] {split_name}: {current_count} pairs available.")
#     if target_count > current_count:
#         raise ValueError(f"Target {target_count} > available {current_count} in '{split_name}'")

#     random.seed(RANDOM_SEED)
#     selected = random.sample(pairs, target_count)

#     tmp_images = images_root / f".tmp_{split_name}_images"
#     tmp_labels = labels_root / f".tmp_{split_name}_labels"
#     safe_clear_dir(tmp_images)
#     safe_clear_dir(tmp_labels)

#     copy_pairs(selected, tmp_images, tmp_labels)

#     safe_clear_dir(images_dir)
#     safe_clear_dir(labels_dir)

#     for p in list(tmp_images.iterdir()):
#         shutil.move(str(p), images_dir / p.name)
#     for p in list(tmp_labels.iterdir()):
#         shutil.move(str(p), labels_dir / p.name)

#     tmp_images.rmdir()
#     tmp_labels.rmdir()
#     print(f"[DONE] {split_name}: resized to {target_count} pairs.")

# def finalize_normalized(images_root: Path, labels_root: Path, base_dir: Path):
#     final_images = base_dir / "images"
#     final_labels = base_dir / "labels"

#     def replace_dir(src: Path, dst: Path):
#         dst.mkdir(parents=True, exist_ok=True)
#         for p in list(dst.iterdir()):
#             if p.is_file():
#                 p.unlink()
#             else:
#                 shutil.rmtree(p)
#         for sub in src.iterdir():
#             if sub.is_dir():
#                 shutil.copytree(sub, dst / sub.name)
#             else:
#                 shutil.copy2(sub, dst / sub.name)

#     replace_dir(images_root, final_images)
#     replace_dir(labels_root, final_labels)
#     print("[DONE] Finalized dataset to:")
#     print(f" - {final_images}")
#     print(f" - {final_labels}")
#     print("Splits inside should be train/ valid/ test/")

# def main():
#     print(f"[DEBUG] DATASET_DIR = {DATASET_DIR}")
#     images_root, labels_root = find_images_labels_root(DATASET_DIR)
#     if images_root is None or labels_root is None:
#         print("[ERROR] Could not detect images/ and labels/ folders under the dataset root.")
#         return

#     print(f"[DEBUG] images_root = {images_root}")
#     print(f"[DEBUG] labels_root = {labels_root}")
#     print(f"[DEBUG] images_root subdirs: {list_subdirs(images_root)}")
#     print(f"[DEBUG] labels_root subdirs: {list_subdirs(labels_root)}")

#     image_splits = find_split_name(images_root, candidates=("train", "valid", "val", "test"))
#     label_splits = find_split_name(labels_root, candidates=("train", "valid", "val", "test"))

#     print(f"[DEBUG] detected image_splits: {list(image_splits.keys())}")
#     print(f"[DEBUG] detected label_splits: {list(label_splits.keys())}")

#     for split, count in TARGETS.items():
#         if split not in image_splits or split not in label_splits:
#             raise FileNotFoundError(
#                 f"Missing split '{split}' in images or labels.\n"
#                 f"Images has: {list(image_splits.keys())}, Labels has: {list(label_splits.keys())}\n"
#                 f"If you use 'val', it will be normalized to 'valid' automatically."
#             )

#     for split, count in TARGETS.items():
#         resize_split(split, count, images_root, labels_root)

#     finalize_normalized(images_root, labels_root, DATASET_DIR)

# if __name__ == "__main__":
#     main()

# filename: threatAdjust.py
import random
from pathlib import Path
import shutil

DATASET_DIR = Path("/Users/shashankk/Downloads/ForesFireDataset")
RANDOM_SEED = 42
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")

def exists_dir(p: Path) -> bool:
    return p.exists() and p.is_dir()

def list_pairs(images_dir: Path, labels_dir: Path):
    images = []
    for ext in IMAGE_EXTS:
        images.extend(images_dir.glob(f"*{ext}"))
    stems = {img.stem: img for img in images}
    pairs = []
    for stem, img_path in stems.items():
        lbl_path = labels_dir / f"{stem}.txt"
        if lbl_path.exists():
            pairs.append((img_path, lbl_path))
    return pairs

def ensure_counts(split: str, target_count: int, images_root: Path, labels_root: Path):
    """Downsample to target_count if over; error if under."""
    img_dir = images_root / split
    lbl_dir = labels_root / split
    assert exists_dir(img_dir) and exists_dir(lbl_dir), f"Missing {split} dirs"
    pairs = list_pairs(img_dir, lbl_dir)
    current = len(pairs)
    print(f"[INFO] {split}: {current} pairs available.")
    if current < target_count:
        raise ValueError(f"{split} has {current} < target {target_count}. Top up separately.")
    if current == target_count:
        print(f"[DONE] {split}: already at target {target_count}.")
        return
    # Downsample
    random.seed(RANDOM_SEED)
    selected = set(random.sample(pairs, target_count))
    # Remove extras
    to_remove = [p for p in pairs if p not in selected]
    for img_path, lbl_path in to_remove:
        if img_path.exists():
            img_path.unlink()
        if lbl_path.exists():
            lbl_path.unlink()
    print(f"[DONE] {split}: resized to {target_count} pairs.")

def move_pairs(src_split: str, dst_split: str, n: int, images_root: Path, labels_root: Path):
    """Move n pairs from src_split to dst_split."""
    src_img = images_root / src_split
    src_lbl = labels_root / src_split
    dst_img = images_root / dst_split
    dst_lbl = labels_root / dst_split
    assert exists_dir(src_img) and exists_dir(src_lbl)
    dst_img.mkdir(parents=True, exist_ok=True)
    dst_lbl.mkdir(parents=True, exist_ok=True)

    pairs = list_pairs(src_img, src_lbl)
    if len(pairs) < n:
        raise ValueError(f"Not enough pairs in {src_split} to move {n}. Has {len(pairs)}.")
    random.seed(RANDOM_SEED)
    chosen = random.sample(pairs, n)
    for img_path, lbl_path in chosen:
        shutil.move(str(img_path), dst_img / img_path.name)
        shutil.move(str(lbl_path), dst_lbl / lbl_path.name)
    print(f"[MOVE] {n} pairs moved {src_split} → {dst_split}.")

def main():
    images_root = DATASET_DIR / "images"
    labels_root = DATASET_DIR / "labels"
    for p in (images_root, labels_root):
        if not exists_dir(p):
            raise FileNotFoundError(f"Missing directory: {p}")

    # Ensure train=420, valid=90 (downsample if needed)
    ensure_counts("train", 420, images_root, labels_root)
    ensure_counts("valid", 90, images_root, labels_root)

    # Adjust test to 90
    test_pairs = list_pairs(images_root / "test", labels_root / "test")
    test_count = len(test_pairs)
    print(f"[INFO] test: {test_count} pairs available.")

    if test_count < 90:
        needed = 90 - test_count
        # Move from valid to test
        move_pairs("valid", "test", needed, images_root, labels_root)
    elif test_count > 90:
        ensure_counts("test", 90, images_root, labels_root)
    else:
        print("[DONE] test: already at target 90.")

    # After moving, re-ensure valid is 90 exactly (in case it dropped below)
    ensure_counts("valid", 90, images_root, labels_root)

    print("[FINAL] Targets achieved: train=420, valid=90, test=90")

if __name__ == "__main__":
    main()
