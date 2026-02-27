from PIL import Image, ImageChops, ImageEnhance

def generate_production_favicons_v3(source_path):
    # Open the master image
    img = Image.open(source_path).convert("RGBA")
    
    # 1. Aggressive Autocrop to ensure content touches the very edges
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    
    # Ensure it's square
    w, h = img.size
    side = max(w, h)
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    square.paste(img, ((side - w) // 2, (side - h) // 2))
    
    # Define sizes
    sizes = {
        "favicon-16x16.png": 16,
        "favicon-32x32.png": 32,
        "favicon-48x48.png": 48,
        "favicon-96x96.png": 96,
        "favicon-192x192.png": 192,
        "favicon-512x512.png": 512,
        "apple-touch-icon.png": 180
    }

    print(f"Generating optimized icons from {source_path}...")

    for filename, size in sizes.items():
        # High-quality resize
        resized = square.resize((size, size), Image.Resampling.LANCZOS)
        
        # 2. Sharpening only for small sizes to prevent blur in tabs
        if size <= 48:
            enhancer = ImageEnhance.Sharpness(resized)
            resized = enhancer.enhance(1.5) # Slight boost to sharpness
            
        resized.save(filename, "PNG", optimize=True)
        print(f"  Exported: {filename}")

    # 3. Create Multi-size ICO with sharpening
    ico_images = []
    for s in [16, 32, 48]:
        resized = square.resize((s, s), Image.Resampling.LANCZOS)
        enhancer = ImageEnhance.Sharpness(resized)
        ico_images.append(enhancer.enhance(1.5))
    
    ico_images[0].save("favicon.ico", format="ICO", sizes=[(s,s) for s in [16, 32, 48]])
    print("  Exported: favicon.ico")

if __name__ == "__main__":
    generate_production_favicons_v3("favicon.png")
