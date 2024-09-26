import os
import shutil

def move_pyc_files(source_dir, destination_dir):
    for root, _, files in os.walk(source_dir):
        pycache_dir = os.path.join(root, "__pycache__")
        if os.path.exists(pycache_dir):
            for pyc_file in os.listdir(pycache_dir):
                if pyc_file.endswith(".pyc"):
                    source_file = os.path.join(pycache_dir, pyc_file)
                    dest_file = os.path.join(destination_dir, os.path.relpath(root, source_dir), pyc_file)
                    dest_file = dest_file.replace(".cpython-311","")
                    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                    shutil.move(source_file, dest_file)

if __name__ == "__main__":
    source_dir = r"/Users/saravanaganesh/Documents/elevator/ECE/ece-warehousemanagement-django/"
    destination_dir = r"/Users/saravanaganesh/Documents/elevator/ECE/ece-warehousemanagement-django/compiled"
    move_pyc_files(source_dir, destination_dir)
    print("Done!")