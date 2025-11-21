from PIL import Image

img = Image.open("static/heatmaps/week6_dapi_heatmap.png").convert("RGBA")
pixels = img.getdata()

new_pixels = []
for r,g,b,a in pixels:
    if r == 0 and g == 0 and b == 131:
        new_pixels.append((0, 0, 0, 0))
    else:
        new_pixels.append((r, g, b, a))

img.putdata(new_pixels)
img.save("/Users/hayden/Desktop/week6_clear_black.png", "PNG")