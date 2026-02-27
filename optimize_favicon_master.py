from PIL import Image, ImageChops

def trim_and_resize(image_path, output_path):
    # Open image
    img = Image.open(image_path).convert("RGBA")
    
    # 1. Autocrop (Remove unnecessary transparent margins)
    bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        img = img.crop(bbox)
        print(f"  Autocropped to: {bbox}")

    # 2. Make it a perfect square (padding with transparency if needed)
    width, height = img.size
    new_size = max(width, height)
    new_img = Image.new("RGBA", (new_size, new_size), (0, 0, 0, 0))
    new_img.paste(img, ((new_size - width) // 2, (new_size - height) // 2))
    
    # 3. Save as the new Master
    new_img.save(output_path, "PNG")
    print(f"  Master image optimized: {output_path}")

if __name__ == "__main__":
    trim_and_resize("favicon.png", "favicon_master.png")
