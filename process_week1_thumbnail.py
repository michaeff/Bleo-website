#!/usr/bin/env python3
"""
Script to process Week 1 thumbnail image:
1. Remove all black pixels from the image
2. Scale the non-black content up by a factor of 1.2
3. Add the black background back at the same size and location
"""

import cv2
import numpy as np
from PIL import Image
import os

def process_week1_thumbnail():
    # Input and output paths
    input_path = "static/thumbnails/week1.png"
    output_path = "static/thumbnails/week1_processed.png"
    backup_path = "static/thumbnails/week1_original_backup.png"
    
    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} not found!")
        return False
    
    # Create backup of original
    if not os.path.exists(backup_path):
        import shutil
        shutil.copy2(input_path, backup_path)
        print(f"Created backup: {backup_path}")
    
    # Load the image
    print(f"Loading image: {input_path}")
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    
    if img is None:
        print("Error: Could not load image!")
        return False
    
    print(f"Original image shape: {img.shape}")
    
    # Convert BGR to RGB if needed (OpenCV loads as BGR)
    if len(img.shape) == 3 and img.shape[2] == 3:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    elif len(img.shape) == 3 and img.shape[2] == 4:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    else:
        img_rgb = img
    
    # Store original dimensions
    original_height, original_width = img_rgb.shape[:2]
    
    # Step 1: Create mask for non-black pixels
    # Define black threshold (allow for slight variations)
    black_threshold = 30  # Pixels with RGB values below this are considered black
    
    if len(img_rgb.shape) == 3:
        # For RGB/RGBA images
        if img_rgb.shape[2] == 4:  # RGBA
            # Consider a pixel black if RGB values are low (ignore alpha)
            non_black_mask = np.any(img_rgb[:, :, :3] > black_threshold, axis=2)
        else:  # RGB
            non_black_mask = np.any(img_rgb > black_threshold, axis=2)
    else:
        # For grayscale images
        non_black_mask = img_rgb > black_threshold
    
    print(f"Non-black pixels found: {np.sum(non_black_mask)}")
    
    # Step 2: Extract the non-black content
    # Find bounding box of non-black content
    non_black_coords = np.where(non_black_mask)
    if len(non_black_coords[0]) == 0:
        print("Error: No non-black pixels found!")
        return False
    
    min_y, max_y = np.min(non_black_coords[0]), np.max(non_black_coords[0])
    min_x, max_x = np.min(non_black_coords[1]), np.max(non_black_coords[1])
    
    print(f"Content bounding box: ({min_x}, {min_y}) to ({max_x}, {max_y})")
    
    # Extract the content region
    content_region = img_rgb[min_y:max_y+1, min_x:max_x+1].copy()
    
    # Step 3: Scale up the content by 1.2x
    scale_factor = 1.2
    new_content_height = int(content_region.shape[0] * scale_factor)
    new_content_width = int(content_region.shape[1] * scale_factor)
    
    print(f"Scaling content from {content_region.shape[:2]} to ({new_content_height}, {new_content_width})")
    
    # Use PIL for high-quality scaling
    if len(content_region.shape) == 3:
        pil_content = Image.fromarray(content_region)
    else:
        pil_content = Image.fromarray(content_region, mode='L')
    
    scaled_content = pil_content.resize((new_content_width, new_content_height), Image.Resampling.LANCZOS)
    scaled_content_array = np.array(scaled_content)
    
    # Step 4: Create new image with black background at original size
    if len(img_rgb.shape) == 3:
        if img_rgb.shape[2] == 4:  # RGBA
            result_img = np.zeros((original_height, original_width, 4), dtype=np.uint8)
            result_img[:, :, 3] = 255  # Set alpha to opaque
        else:  # RGB
            result_img = np.zeros((original_height, original_width, 3), dtype=np.uint8)
    else:
        result_img = np.zeros((original_height, original_width), dtype=np.uint8)
    
    # Calculate center position for scaled content
    content_center_y = (min_y + max_y) // 2
    content_center_x = (min_x + max_x) // 2
    
    # Calculate new position (centered on original content center)
    new_start_y = content_center_y - new_content_height // 2
    new_start_x = content_center_x - new_content_width // 2
    
    # Ensure we don't go outside image bounds
    new_start_y = max(0, min(new_start_y, original_height - new_content_height))
    new_start_x = max(0, min(new_start_x, original_width - new_content_width))
    
    new_end_y = new_start_y + new_content_height
    new_end_x = new_start_x + new_content_width
    
    # Handle case where scaled content is larger than original image
    content_start_y = 0
    content_start_x = 0
    content_end_y = new_content_height
    content_end_x = new_content_width
    
    if new_end_y > original_height:
        content_end_y = new_content_height - (new_end_y - original_height)
        new_end_y = original_height
    
    if new_end_x > original_width:
        content_end_x = new_content_width - (new_end_x - original_width)
        new_end_x = original_width
    
    if new_start_y < 0:
        content_start_y = -new_start_y
        new_start_y = 0
    
    if new_start_x < 0:
        content_start_x = -new_start_x
        new_start_x = 0
    
    print(f"Placing scaled content at: ({new_start_x}, {new_start_y}) to ({new_end_x}, {new_end_y})")
    
    # Place the scaled content
    if len(result_img.shape) == 3:
        result_img[new_start_y:new_end_y, new_start_x:new_end_x] = scaled_content_array[
            content_start_y:content_end_y, content_start_x:content_end_x
        ]
    else:
        result_img[new_start_y:new_end_y, new_start_x:new_end_x] = scaled_content_array[
            content_start_y:content_end_y, content_start_x:content_end_x
        ]
    
    # Step 5: Save the result
    # Convert back to PIL for saving
    if len(result_img.shape) == 3:
        if result_img.shape[2] == 4:
            result_pil = Image.fromarray(result_img, mode='RGBA')
        else:
            result_pil = Image.fromarray(result_img, mode='RGB')
    else:
        result_pil = Image.fromarray(result_img, mode='L')
    
    result_pil.save(output_path, 'PNG')
    print(f"Processed image saved to: {output_path}")
    
    # Replace original with processed version
    if os.path.exists(output_path):
        import shutil
        shutil.move(output_path, input_path)
        print(f"Replaced original file: {input_path}")
        print("Process completed successfully!")
        return True
    
    return False

if __name__ == "__main__":
    print("Processing Week 1 thumbnail image...")
    print("=" * 50)
    
    success = process_week1_thumbnail()
    
    print("=" * 50)
    if success:
        print("✅ Week 1 thumbnail processing completed successfully!")
        print("📁 Original backed up as: static/thumbnails/week1_original_backup.png")
    else:
        print("❌ Week 1 thumbnail processing failed!")
