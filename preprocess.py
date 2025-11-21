# preprocess.py

import os
from czi_utils import process_czi, process_detailed_czi

ROOT                   = os.path.dirname(os.path.abspath(__file__))
STATIC                 = os.path.join(ROOT, 'static')

# Single‐layer (front page)
CZI_DIR                = os.path.join(STATIC, 'czi_images')
PROCESSED_DIR          = os.path.join(STATIC, 'processed')

# Multi‐Z (detail page)
DETAILED_CZI_DIR       = os.path.join(STATIC, 'czi_images_detailed')
PROCESSED_DETAILED_DIR = os.path.join(STATIC, 'processed_detailed')

# Make sure output dirs exist
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(PROCESSED_DETAILED_DIR, exist_ok=True)

# 1) Re‐process single‐layer CZI → processed/*.png
print("=== Reprocessing single‐layer CZI files ===")
for fn in sorted(os.listdir(CZI_DIR)):
    if not fn.lower().endswith('.czi'):
        continue
    src = os.path.join(CZI_DIR, fn)
    print(f"[PROCESSING] single‐layer: {fn}")
    process_czi(src, PROCESSED_DIR)

# 2) Re‐process detailed multi‐Z CZI → processed_detailed/<week>/...
print("\n=== Reprocessing multi‐Z CZI files ===")
for fn in sorted(os.listdir(DETAILED_CZI_DIR)):
    if not fn.lower().endswith('.czi'):
        continue
    src = os.path.join(DETAILED_CZI_DIR, fn)
    print(f"[PROCESSING] multi‐Z: {fn}")
    process_detailed_czi(src, PROCESSED_DETAILED_DIR)

print("\n✅ All done!")
