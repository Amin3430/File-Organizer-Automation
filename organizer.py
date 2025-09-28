import os, shutil
from utils import ensure_folder

def categorize_and_move(src_folder, dest_folder):
    moved = []
    for file in os.listdir(src_folder):
        src_path = os.path.join(src_folder, file)
        if os.path.isfile(src_path):
            ext = os.path.splitext(file)[1].lower()
            folder_name = ext[1:].capitalize() if ext else "Others"
            dest_path = os.path.join(dest_folder, folder_name, file)
            ensure_folder(os.path.dirname(dest_path))
            shutil.move(src_path, dest_path)
            moved.append((src_path, dest_path))
    return moved
