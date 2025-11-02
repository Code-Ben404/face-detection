# save_class_names.py
import os, json, sys

train_dir = "train"
if not os.path.isdir(train_dir):
    print("Error: 'train' folder not found in current directory.")
    sys.exit(1)

classes = sorted([d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir,d))])
if not classes:
    print("No class subfolders found under 'train'.")
    sys.exit(1)

with open("class_names.json", "w") as f:
    json.dump(classes, f, indent=2)

print("Saved class_names.json with classes (index -> name):")
for i,c in enumerate(classes):
    print(f"  {i} -> {c}")
