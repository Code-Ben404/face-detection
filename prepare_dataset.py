# prepare_dataset.py
"""
Usage:
  python prepare_dataset.py --src path/to/extracted_archive --dest path/to/FACE_DETECTION --split 0.8

If src contains 'train' and 'test' folders already, they'll be copied into dest.
If src contains class subfolders (e.g., angry/, happy/, ...), those will be split into train/test.
"""
import os
import shutil
import argparse
import random
import json

def ensure_dir(p):
    if not os.path.exists(p):
        os.makedirs(p)

def copy_tree(src, dst):
    ensure_dir(dst)
    # copy all files and subfolders
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

def split_class_folder(class_src, train_dest, test_dest, train_frac=0.8, seed=42):
    ensure_dir(train_dest)
    ensure_dir(test_dest)
    files = [f for f in os.listdir(class_src) if os.path.isfile(os.path.join(class_src, f))]
    random.Random(seed).shuffle(files)
    split_idx = int(len(files) * train_frac)
    train_files = files[:split_idx]
    test_files = files[split_idx:]
    for f in train_files:
        shutil.copy2(os.path.join(class_src, f), os.path.join(train_dest, f))
    for f in test_files:
        shutil.copy2(os.path.join(class_src, f), os.path.join(test_dest, f))
    return len(train_files), len(test_files)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", required=True, help="Path to extracted archive folder")
    parser.add_argument("--dest", required=True, help="Destination project folder (FACE_DETECTION)")
    parser.add_argument("--split", type=float, default=0.8, help="Train fraction (default 0.8)")
    parser.add_argument("--move_instead_of_copy", action="store_true", help="If set, move files instead of copying")
    args = parser.parse_args()

    src = os.path.abspath(args.src)
    dest = os.path.abspath(args.dest)
    train_dir = os.path.join(dest, "train")
    test_dir = os.path.join(dest, "test")

    ensure_dir(dest)

    # Case A: source already contains train/ and test/
    if os.path.isdir(os.path.join(src, "train")) and os.path.isdir(os.path.join(src, "test")):
        print("Detected train/ and test/ in source. Copying them to destination...")
        copy_tree(os.path.join(src, "train"), train_dir)
        copy_tree(os.path.join(src, "test"), test_dir)
    else:
        # Either src contains class subfolders, or there is a single folder containing classes
        # Find candidate class folders under src
        class_folders = [d for d in os.listdir(src) if os.path.isdir(os.path.join(src, d))]
        if len(class_folders) == 0:
            # maybe archive had a single top-level folder
            items = [d for d in os.listdir(src) if os.path.isdir(os.path.join(src, d))]
            if len(items) == 1:
                inner = os.path.join(src, items[0])
                class_folders = [d for d in os.listdir(inner) if os.path.isdir(os.path.join(inner, d))]
                src = inner
        if len(class_folders) == 0:
            raise RuntimeError("No class subfolders detected in source. Please inspect the extracted archive.")

        print("Detected class folders:", sorted(class_folders))
        # create train/test and split per class
        for cls in class_folders:
            cls_src = os.path.join(src, cls)
            cls_train_dest = os.path.join(train_dir, cls)
            cls_test_dest = os.path.join(test_dir, cls)
            tcount, vcount = split_class_folder(cls_src, cls_train_dest, cls_test_dest, train_frac=args.split)
            print(f"Class '{cls}': copied {tcount} train / {vcount} test")

    # After copying, produce class_names.json in alphabetical order (this is what Keras uses)
    classes = sorted([d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))])
    class_names_path = os.path.join(dest, "class_names.json")
    with open(class_names_path, "w") as f:
        json.dump(classes, f, indent=2)
    print("\nSaved class_names.json with the following ordered class names (folder -> label index):")
    for idx, c in enumerate(classes):
        print(f"  {idx} -> {c}")
    print("\nDone. Train and test folders are ready.")
    print("Train folder:", train_dir)
    print("Test folder:", test_dir)
    print("class_names.json:", class_names_path)

if __name__ == "__main__":
    main()
