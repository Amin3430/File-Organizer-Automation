import os
import json
from utils import now_str

def load_config():
    cfg_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(cfg_path, "r", encoding="utf-8") as f:
        return json.load(f)

def heuristic_scan(folder, max_files=1000):
    """
    Scan folder for suspicious files.
    Returns a list of dicts: {"path": ..., "reason": ...}
    """
    cfg = load_config()
    suspicious = set(cfg.get("suspicious_exts", []))
    double_check = cfg.get("double_ext_suspicious", True)
    findings = []
    count = 0

    for root, dirs, files in os.walk(folder):
        for name in files:
            if count >= max_files:
                return findings
            count += 1
            path = os.path.join(root, name)
            ext = os.path.splitext(name)[1].lower()

            # Suspicious extension
            if ext in suspicious:
                findings.append({"path": path, "reason": f"Suspicious extension {ext}"})

            # Double extension check
            if double_check and name.count('.') >= 2:
                findings.append({"path": path, "reason": "Double extension (possible disguised file)"})

            # Large file heuristic
            try:
                size = os.path.getsize(path)
                if size > 100 * 1024 * 1024 and ext in suspicious:
                    findings.append({"path": path, "reason": f"Large suspicious file ({size} bytes)"})
            except Exception:
                continue

    return findings

# ---------- Test run ----------
if __name__ == "__main__":
    folder = input("Enter folder path to scan: ")
    results = heuristic_scan(folder)
    if results:
        print(f"Found {len(results)} suspicious files:")
        for item in results:
            print(f"{item['path']} -- {item['reason']}")
    else:
        print("No suspicious files found.")
