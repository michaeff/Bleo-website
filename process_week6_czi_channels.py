#!/usr/bin/env python3

from PIL import Image
import os

def process_czi_channel(image_path):
    """Clear black pixels, rotate 35° CCW, then add black background back"""
    print(f"Processing CZI channel: {image_path}")
    
    # Step 1: Load image and clear black pixels
    img = Image.open(image_path).convert("RGBA")
    pixels = img.getdata()

    new_pixels = []
    for r, g, b, a in pixels:
        # Clear pure black pixels (make them transparent)
        if r == 0 and g == 0 and b == 0:
            new_pixels.append((0, 0, 0, 0))
        # Also clear the specific dark blue
        elif r == 0 and g == 0 and b == 131:
            new_pixels.append((0, 0, 0, 0))
        else:
            new_pixels.append((r, g, b, a))

    img.putdata(new_pixels)
    print(f"  ✓ Black pixels cleared")
    
    # Step 2: Rotate 35 degrees counter-clockwise with enlarged canvas
    original_size = img.size
    
    # Calculate the size needed to fit the rotated image without cropping
    # For a 35-degree rotation, we need larger enlargement
    import math
    angle_rad = math.radians(35)
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
    rotated_img = enlarged_canvas.rotate(35, expand=False, fillcolor=(0, 0, 0, 0))
    print(f"  ✓ Rotated 35° counter-clockwise (canvas enlarged to prevent cropping)")
    
    # Step 3: Add black background back
    # Create a black background with the new enlarged size
    black_background = Image.new('RGB', (new_width, new_height), (0, 0, 0))
    
    # Composite the rotated image onto the black background
    final_img = Image.alpha_composite(
        black_background.convert('RGBA'),
        rotated_img
    )
    
    # Convert back to RGB (removing alpha channel)
    final_img = final_img.convert('RGB')
    print(f"  ✓ Black background added (final size: {new_width}x{new_height})")
    
    # Save the final result
    final_img.save(image_path, "PNG")
    print(f"✅ Saved: {image_path}")

def main():
    base_dir = "static/processed"
    
    # Week 6 CZI channel files to process
    week6_channels = [
        f"{base_dir}/week6_channel1.png",
        f"{base_dir}/week6_channel2.png", 
        f"{base_dir}/week6_channel3.png",
        f"{base_dir}/week6_channel4.png",
    ]
    
    print("🔄 Processing Week 6 CZI channels (clear black → rotate 35° CCW → add black back)...")
    print("=" * 75)
    
    for channel_path in week6_channels:
        if os.path.exists(channel_path):
            process_czi_channel(channel_path)
        else:
            print(f"❌ File not found: {channel_path}")
    
    print("=" * 75)
    print("✅ All Week 6 CZI channels have been processed!")
    print("\nProcessing completed for:")
    print("- week6_channel1.png (DAPI)")
    print("- week6_channel2.png (GFP)") 
    print("- week6_channel3.png (ASMA)")
    print("- week6_channel4.png (Merged)")
    print("\nEach channel was: cleared of black → rotated 35° CCW → black background restored")

if __name__ == "__main__":
    main()
