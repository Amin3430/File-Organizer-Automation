import os
import shutil
import hashlib
import logging
import json
import tkinter as tk
from utils import now_str, ensure_folder

BASE = os.path.dirname(__file__)

# ---------- Stylish Button ----------
def create_styled_button(parent, text, bg, fg="white", active_bg=None, command=None):
    """
    Create a modern, flat, hoverable Tkinter button.
    """
    active_bg = active_bg or bg
    btn = tk.Button(
        parent,
        text=text,
        bg=bg,
        fg=fg,
        font=("Segoe UI", 11, "bold"),
        activebackground=active_bg,
        activeforeground=fg,
        bd=0,
        relief="flat",
        padx=12,
        pady=6,
        highlightthickness=0,
        cursor="hand2",
        command=command
    )

    # Hover effect
    btn.bind("<Enter>", lambda e: btn.config(bg=active_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn

# ---------- Load Config ----------
def load_config():
    cfg_path = os.path.join(BASE, "config.json")
    if not os.path.exists(cfg_path):
        logging.warning(f"Config not found at {cfg_path}")
        return {}
    with open(cfg_path, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------- MD5 Checksum ----------
def md5(path, block_size=65536):
    """
    Calculate MD5 checksum of a file.
    """
    h = hashlib.md5()
    try:
        with open(path, "rb", errors='ignore') as f:
            for blk in iter(lambda: f.read(block_size), b""):
                h.update(blk)
    except Exception as e:
        logging.error(f"Failed to compute MD5 for {path}: {e}")
        return None
    return h.hexdigest()

# ---------- File Organizer ----------
def categorize_and_move(src_folder, dest_root, dry_run=False):
    """
    Organize files from src_folder into categories under dest_root
    according to config.json mapping.
    """
    cfg = load_config()
    organize_map = cfg.get("organize_map", {})
    moved = []
    ensure_folder(dest_root)

    for root, dirs, files in os.walk(src_folder):
        # Skip destination folder itself
        if os.path.abspath(root).startswith(os.path.abspath(dest_root)):
            continue
        for name in files:
            src = os.path.join(root, name)
            ext = os.path.splitext(name)[1].lower()
            # Determine category
            target_dir = None
            for cat, exts in organize_map.items():
                if ext in [e.lower() for e in exts]:
                    target_dir = os.path.join(dest_root, cat)
                    break
            if not target_dir:
                target_dir = os.path.join(dest_root, "Others")
            ensure_folder(target_dir)
            dest = os.path.join(target_dir, name)
            if dry_run:
                moved.append((src, dest))
            else:
                try:
                    shutil.move(src, dest)
                    moved.append((src, dest))
                    logging.info(f"Moved {src} -> {dest}")
                except Exception as e:
                    logging.error(f"Failed to move {src}: {e}")
    return moved
