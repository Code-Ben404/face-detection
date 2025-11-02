# verify_folders.py
import os, json, sys

# project root = folder where this script lives
root = os.path.abspath(os.path.dirname(__file__))

class_names_path = os.path.join(root, "class_names.json")
if not os.path.exists(class_names_path):
    print(f"Error: class_names.json not found at {class_names_path}")
    sys.exit(1)

with open(class_names_path, "r") as f:
    classes = json.load(f)

print("Class names (index -> folder):")
for i, c in enumerate(classes):
    train_dir = os.path.join(root, "train", c)
    test_dir = os.path.join(root, "test", c)

    tcount = 0
    vcount = 0
    if os.path.isdir(train_dir):
        tcount = len([f for f in os.listdir(train_dir) if os.path.isfile(os.path.join(train_dir, f))])
    if os.path.isdir(test_dir):
        vcount = len([f for f in os.listdir(test_dir) if os.path.isfile(os.path.join(test_dir, f))])

    print(f"{i}: {c}  -- train: {tcount}, test: {vcount}")
