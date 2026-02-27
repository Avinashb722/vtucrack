from PIL import Image

def maximize_logo(image_path, output_path):
    # Open the image
    img = Image.open(image_path).convert("RGBA")
    
    # Get the bounding box of non-transparent pixels
    # alpha = img.getchannel('A') # Extract alpha channel
    # bbox = alpha.getbbox() # Get bounding box of non-zero alpha
    
    # More robust way: check for any channel being non-zero
    bbox = img.getbbox()
    
    if not bbox:
        print("Error: Image is empty!")
        return

    print(f"  Content bounding box: {bbox}")
    
    # Crop to the content
    img_cropped = img.crop(bbox)
    
    # Get new dimensions
    w, h = img_cropped.size
    print(f"  Cropped size: {w}x{h}")
    
    # Make it a perfect square without adding padding
    # We want the content to be the square. 
    # If the content is already circular, we just want the circle to touch the edges.
    
    # Calculate the largest square size
    if w > h:
        new_size = w
        offset_y = (w - h) // 2
        offset_x = 0
    else:
        new_size = h
        offset_x = (h - w) // 2
        offset_y = 0
        
    final_img = Image.new("RGBA", (new_size, new_size), (0, 0, 0, 0))
    final_img.paste(img_cropped, (offset_x, offset_y))
    
    # Resize to a standard large size (e.g., 1024x1024) for the NEW Master
    final_img = final_img.resize((1024, 1024), Image.Resampling.LANCZOS)
    
    final_img.save(output_path)
    print(f"  Maximized Master saved to: {output_path}")

if __name__ == "__main__":
    maximize_logo("favicon.png", "favicon_master_max.png")
