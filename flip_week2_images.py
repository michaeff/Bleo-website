#!/usr/bin/env python3

from PIL import Image
import os

def flip_image_horizontally(image_path):
    """Flip an image horizontally and save it back"""
    print(f"Flipping: {image_path}")
    
    # Open the image
    img = Image.open(image_path)
    
    # Flip horizontally (left-right)
    flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
    
    # Save back to the same path
    flipped_img.save(image_path)
    print(f"✅ Saved: {image_path}")

def main():
    base_dir = "/Users/hayden/Desktop/WebsiteProject/static"
    
    # Week 2 images to flip
    week2_images = [
        # Thumbnail
        f"{base_dir}/thumbnails/week2.png",
        
        # CZI viewer channel images
        f"{base_dir}/processed/week2_channel1.png",
        f"{base_dir}/processed/week2_channel2.png", 
        f"{base_dir}/processed/week2_channel3.png",
        f"{base_dir}/processed/week2_channel4.png",
        
        # Heatmaps
        f"{base_dir}/heatmaps/week2_asma_heatmap.png",
        f"{base_dir}/heatmaps/week2_dapi_heatmap.png",
        f"{base_dir}/heatmaps/week2_gfp_heatmap.png",
    ]
    
    print("🔄 Flipping all Week 2 images horizontally...")
    print("=" * 50)
    
    for image_path in week2_images:
        if os.path.exists(image_path):
            flip_image_horizontally(image_path)
        else:
            print(f"❌ File not found: {image_path}")
    
    print("=" * 50)
    print("✅ All Week 2 images have been flipped horizontally!")
    print("\nImages affected:")
    print("- Thumbnail (main page)")
    print("- CZI viewer channels 1-4 (main page)")  
    print("- Heatmaps: ASMA, DAPI, GFP (main page)")

if __name__ == "__main__":
    main()
