import os, shutil, time, logging, json
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "organizer.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ensure_folder(path):
    os.makedirs(path, exist_ok=True)

def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def read_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
