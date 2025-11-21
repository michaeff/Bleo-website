#!/usr/bin/env python3
import os
from PIL import Image

# === CONFIG ===
ANGLE_DEGREES = 35  # negative = CCW
PROCESSED_DIR = os.path.join('static', 'processed')

def rotate_processed_folder(folder, angle_deg):
    for fname in os.listdir(folder):
        if not fname.lower().endswith('.png'):
            continue
        if not fname.startswith('week6_'):
            continue

        path = os.path.join(folder, fname)
        with Image.open(path) as img:
            # ensure alpha channel if present, else fill background black
            if img.mode in ('RGBA', 'LA') or img.info.get("transparency", False):
                base = img.convert('RGBA')
                fill = (0, 0, 0, 0)
            else:
                base = img.convert('RGB')
                fill = (0, 0, 0)

            # rotate
            rotated = base.rotate(
                angle_deg,
                resample=Image.NEAREST,
                expand=True,
                fillcolor=fill
            )

            # overwrite original
            rotated.save(path)
            print(f"[OK] Rotated {path} → {rotated.size}")

if __name__ == "__main__":
    if os.path.isdir(PROCESSED_DIR):
        rotate_processed_folder(PROCESSED_DIR, ANGLE_DEGREES)
    else:
        print(f"[ERROR] Folder not found: {PROCESSED_DIR}")
