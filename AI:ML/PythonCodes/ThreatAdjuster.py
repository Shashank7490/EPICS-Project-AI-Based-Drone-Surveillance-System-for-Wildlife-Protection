# filename: resize_yolov8_dataset.py
# Adjust YOLOv8 splits to: train=420, valid=90, test=90
# Works for datasets with either:
#  - root/images/{train,val|valid,test} and root/labels/{train,val|valid,test}
#  - or root/{train,val|valid,test}/{images,labels} (auto-normalized)
#
# Usage:
#   1) Set DATASET_DIR to your dataset root path.
#   2) Run: python resize_yolov8_dataset.py
#
# Notes:
#  - Random selection is reproducible via RANDOM_SEED.
#  - Only image-label pairs with matching stems are included.
#  - If a split has fewer pairs than target (e.g., test=85 < 90), it will top-up
#    by moving pairs from valid, and if valid becomes short, from train.
#  - No cross-split duplicates after completion.

import os
import shutil
import random
from pathlib import Path

# ---------- CONFIG ----------
DATASET_DIR = Path("/Users/shashankk/Downloads/ForesFireDataset")  # e.g., "/Users/you/Downloads/ForesFireDataset"
TARGETS = {"train": 770, "valid": 161, "test": 81}
RANDOM_SEED = 42
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")
# ----------------------------

def exists_dir(p: Path) -> bool:
    return p.exists() and p.is_dir()

def list_subdirs(p: Path):
    return sorted([d.name for d in p.iterdir() if d.is_dir()]) if exists_dir(p) else []

def _collect_pairs(images_dir: Path, labels_dir: Path):
    imgs = []
    for ext in IMAGE_EXTS:
        imgs.extend(images_dir.glob(f"*{ext}"))
    stem_to_img = {i.stem: i for i in imgs}
    pairs = []
    for stem, img_path in stem_to_img.items():
        lbl = labels_dir / f"{stem}.txt"
        if lbl.exists():
            pairs.append((img_path, lbl))
    return pairs

def _count_pairs(images_dir: Path, labels_dir: Path) -> int:
    return len(_collect_pairs(images_dir, labels_dir))

def _downsample_to(images_dir: Path, labels_dir: Path, target_count: int):
    pairs = _collect_pairs(images_dir, labels_dir)
    current = len(pairs)
    if current <= target_count:
        return
    random.seed(RANDOM_SEED)
    keep = set(random.sample(pairs, target_count))
    drop = [p for p in pairs if p not in keep]
    for img_path, lbl_path in drop:
        if img_path.exists():
            img_path.unlink()
        if lbl_path.exists():
            lbl_path.unlink()

def _move_n_pairs(src_img_dir: Path, src_lbl_dir: Path, dst_img_dir: Path, dst_lbl_dir: Path, n: int):
    pairs = _collect_pairs(src_img_dir, src_lbl_dir)
    if len(pairs) < n:
        raise ValueError(f"Not enough pairs to move: need {n}, have {len(pairs)} in {src_img_dir}")
    random.seed(RANDOM_SEED)
    chosen = random.sample(pairs, n)
    dst_img_dir.mkdir(parents=True, exist_ok=True)
    dst_lbl_dir.mkdir(parents=True, exist_ok=True)
    for img_path, lbl_path in chosen:
        shutil.move(str(img_path), dst_img_dir / img_path.name)
        shutil.move(str(lbl_path), dst_lbl_dir / lbl_path.name)

def _ensure_exact(images_dir: Path, labels_dir: Path, target_count: int):
    current = _count_pairs(images_dir, labels_dir)
    if current > target_count:
        _downsample_to(images_dir, labels_dir, target_count)
    elif current < target_count:
        raise ValueError(f"Split at {images_dir} has {current} < target {target_count}; needs top-up.")

def _normalize_layout(base: Path):
    """
    Detects and normalizes dataset layout to:
        images/{train,valid,test}, labels/{train,valid,test}
    Returns (images_root, labels_root).
    """
    images_root = base / "images"
    labels_root = base / "labels"
    if exists_dir(images_root) and exists_dir(labels_root):
        return images_root, labels_root

    # Alternate layout: base/{train|valid|val|test}/{images,labels} or flat files
    split_candidates = ["train", "valid", "val", "test"]
    found_split_dirs = [base / s for s in split_candidates if exists_dir(base / s)]
    if not found_split_dirs:
        raise FileNotFoundError("Could not find images/labels or per-split directories under dataset root.")

    norm_images = base / "_normalized_images"
    norm_labels = base / "_normalized_labels"
    norm_images.mkdir(exist_ok=True)
    norm_labels.mkdir(exist_ok=True)

    for s in split_candidates:
        src_split = base / s
        if not exists_dir(src_split):
            continue
        # Map 'val' -> 'valid'
        dst_split_name = "valid" if s == "val" else s
        dst_img_dir = norm_images / dst_split_name
        dst_lbl_dir = norm_labels / dst_split_name
        dst_img_dir.mkdir(parents=True, exist_ok=True)
        dst_lbl_dir.mkdir(parents=True, exist_ok=True)

        # Prefer subdirs named images/ and labels/
        src_img_dir = src_split / "images"
        src_lbl_dir = src_split / "labels"

        if exists_dir(src_img_dir):
            for p in src_img_dir.iterdir():
                if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
                    shutil.copy2(p, dst_img_dir / p.name)
        else:
            # flat files as images
            for p in src_split.iterdir():
                if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
                    shutil.copy2(p, dst_img_dir / p.name)

        if exists_dir(src_lbl_dir):
            for p in src_lbl_dir.iterdir():
                if p.is_file() and p.suffix.lower() == ".txt":
                    shutil.copy2(p, dst_lbl_dir / p.name)
        else:
            # flat files as labels
            for p in src_split.iterdir():
                if p.is_file() and p.suffix.lower() == ".txt":
                    shutil.copy2(p, dst_lbl_dir / p.name)

    return norm_images, norm_labels

def _finalize(images_root: Path, labels_root: Path, base_dir: Path):
    final_images = base_dir / "images"
    final_labels = base_dir / "labels"

    def _replace_dir(src: Path, dst: Path):
        dst.mkdir(parents=True, exist_ok=True)
        for p in list(dst.iterdir()):
            if p.is_file():
                p.unlink()
            else:
                shutil.rmtree(p)
        for sub in src.iterdir():
            if sub.is_dir():
                shutil.copytree(sub, dst / sub.name)
            else:
                shutil.copy2(sub, dst / sub.name)

    _replace_dir(images_root, final_images)
    _replace_dir(labels_root, final_labels)

def main():
    # 1) Normalize dataset layout to images/labels roots
    images_root, labels_root = _normalize_layout(DATASET_DIR)

    # 2) Ensure train and valid downsample to targets (if above)
    _downsample_to(images_root / "train", labels_root / "train", TARGETS["train"])
    _downsample_to(images_root / "valid", labels_root / "valid", TARGETS["valid"])

    # 3) Adjust test to exact target; if short, top up from valid, then train
    test_img = images_root / "test"
    test_lbl = labels_root / "test"
    valid_img = images_root / "valid"
    valid_lbl = labels_root / "valid"
    train_img = images_root / "train"
    train_lbl = labels_root / "train"

    # If test has fewer than target, move from valid; if valid becomes short, move from train
    current_test = _count_pairs(test_img, test_lbl)
    if current_test < TARGETS["test"]:
        need = TARGETS["test"] - current_test
        valid_count = _count_pairs(valid_img, valid_lbl)
        move_from_valid = min(need, valid_count - max(0, valid_count - TARGETS["valid"]))  # move up to what's safe
        if move_from_valid > 0:
            _move_n_pairs(valid_img, valid_lbl, test_img, test_lbl, move_from_valid)
            need -= move_from_valid

        if need > 0:
            train_count = _count_pairs(train_img, train_lbl)
            if train_count < need:
                raise ValueError(f"Not enough pairs to top up test: need {need}, train has {train_count}.")
            _move_n_pairs(train_img, train_lbl, test_img, test_lbl, need)

    # 4) Now enforce exact counts for all splits
    _ensure_exact(train_img, train_lbl, TARGETS["train"])
    _ensure_exact(valid_img, valid_lbl, TARGETS["valid"])
    _ensure_exact(test_img, test_lbl, TARGETS["test"])

    # 5) Finalize to dataset/images and dataset/labels
    _finalize(images_root, labels_root, DATASET_DIR)

    # Print final counts
    print("Final counts:")
    for split in ("train", "valid", "test"):
        img_dir = DATASET_DIR / "images" / split
        lbl_dir = DATASET_DIR / "labels" / split
        print(f" - {split}: {_count_pairs(img_dir, lbl_dir)} pairs")

if __name__ == "__main__":
    main()
