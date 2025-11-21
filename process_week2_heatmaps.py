from PIL import Image
import os

def process_heatmap(image_path):
    """Clear black pixels, rotate 10° CCW, then add dark blue background back"""
    print(f"Processing: {image_path}")
    
    # Step 1: Load image and clear black pixels
    img = Image.open(image_path).convert("RGBA")
    pixels = img.getdata()

    new_pixels = []
    for r, g, b, a in pixels:
        # Clear pure black pixels (make them transparent)
        if r == 0 and g == 0 and b == 0:
            new_pixels.append((0, 0, 0, 0))
        # Also clear the specific dark blue you had before
        elif r == 0 and g == 0 and b == 131:
            new_pixels.append((0, 0, 0, 0))
        else:
            new_pixels.append((r, g, b, a))

    img.putdata(new_pixels)
    print(f"  ✓ Black pixels cleared")
    
    # Step 2: Rotate 10 degrees counter-clockwise with enlarged canvas
    original_size = img.size
    
    # Calculate the size needed to fit the rotated image without cropping
    # For a 10-degree rotation, we need smaller enlargement
    import math
    angle_rad = math.radians(10)
    cos_a = abs(math.cos(angle_rad))
    sin_a = abs(math.sin(angle_rad))
    
    new_width = int(original_size[0] * cos_a + original_size[1] * sin_a)
    new_height = int(original_size[0] * sin_a + original_size[1] * cos_a)
    
    # Create a larger canvas to hold the rotation without cropping
    enlarged_canvas = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
    
    # Paste the original image centered on the enlarged canvas
    paste_x = (new_width - original_size[0]) // 2
    paste_y = (new_height - original_size[1]) // 2
    enlarged_canvas.paste(img, (paste_x, paste_y), img)
    
    # Now rotate the enlarged canvas
    rotated_img = enlarged_canvas.rotate(10, expand=False, fillcolor=(0, 0, 0, 0))
    print(f"  ✓ Rotated 10° counter-clockwise (canvas enlarged to prevent cropping)")
    
    # Step 3: Add dark blue background back
    # Create a dark blue background with the new enlarged size
    blue_background = Image.new('RGB', (new_width, new_height), (0, 0, 131))
    
    # Composite the rotated image onto the dark blue background
    final_img = Image.alpha_composite(
        blue_background.convert('RGBA'),
        rotated_img
    )
    
    # Convert back to RGB (removing alpha channel)
    final_img = final_img.convert('RGB')
    print(f"  ✓ Dark blue background added (final size: {new_width}x{new_height})")
    
    # Save the final result
    final_img.save(image_path, "PNG")
    print(f"✅ Saved: {image_path}")

def main():
    base_dir = "static/heatmaps"
    
    # Week 2 heatmap files to process
    week2_heatmaps = [
        f"{base_dir}/week2_asma_heatmap.png",
        f"{base_dir}/week2_dapi_heatmap.png", 
        f"{base_dir}/week2_gfp_heatmap.png",
    ]
    
    print("🔄 Processing Week 2 heatmaps (clear black → rotate 10° CCW → add dark blue back)...")
    print("=" * 75)
    
    for heatmap_path in week2_heatmaps:
        if os.path.exists(heatmap_path):
            process_heatmap(heatmap_path)
        else:
            print(f"❌ File not found: {heatmap_path}")
    
    print("=" * 75)
    print("✅ All Week 2 heatmaps have been processed!")
    print("\nProcessing completed for:")
    print("- week2_asma_heatmap.png")
    print("- week2_dapi_heatmap.png") 
    print("- week2_gfp_heatmap.png")
    print("\nEach heatmap was: cleared of black → rotated 10° CCW → dark blue background restored")

if __name__ == "__main__":
    main()