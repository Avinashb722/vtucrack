from PIL import Image
import os

def generate_production_favicons(source_path):
    if not os.path.exists(source_path):
        print(f"Error: Source image not found at {source_path}")
        return

    # Basic configuration
    sizes = {
        "favicon-16x16.png": (16, 16),
        "favicon-32x32.png": (32, 32),
        "favicon-48x48.png": (48, 48),
        "favicon-96x96.png": (96, 96),
        "favicon-192x192.png": (192, 192),
        "favicon-512x512.png": (512, 512),
        "apple-touch-icon.png": (180, 180)
    }

    try:
        source = Image.open(source_path).convert("RGBA")
        print(f"Processing source: {source_path}...")

        # 1. Generate PNGs
        for filename, size in sizes.items():
            resized = source.resize(size, Image.Resampling.LANCZOS)
            resized.save(filename, "PNG")
            print(f"  Generated: {filename} ({size[0]}x{size[1]})")

        # 2. Generate multi-size favicon.ico
        ico_sizes = [(16, 16), (32, 32), (48, 48)]
        ico_images = []
        for size in ico_sizes:
            ico_images.append(source.resize(size, Image.Resampling.LANCZOS))
        
        ico_images[0].save(
            "favicon.ico", 
            format="ICO", 
            sizes=[(img.width, img.height) for img in ico_images]
        )
        print("  Generated: favicon.ico (multi-size)")

        print("\n✅ All production favicon files generated successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_production_favicons("favicon_master.png")
