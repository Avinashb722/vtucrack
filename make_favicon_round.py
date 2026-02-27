from PIL import Image, ImageDraw

def make_circle_with_padding(
    image_path,
    output_path,
    canvas_size=512,
    scale=1.15   # ⬅️ Increased size (was 0.75)
):
    # Open image
    img = Image.open(image_path).convert("RGBA")

    # Resize logo (slightly bigger)
    logo_size = int(canvas_size * scale)
    img = img.resize((logo_size, logo_size), Image.LANCZOS)

    # Create transparent canvas
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))

    # Center logo
    x = (canvas_size - logo_size) // 2
    y = (canvas_size - logo_size) // 2
    canvas.paste(img, (x, y), img)

    # Create circular mask (FULL CIRCLE)
    mask = Image.new("L", (canvas_size, canvas_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, canvas_size, canvas_size), fill=255)

    # Apply mask
    output = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    output.paste(canvas, (0, 0), mask=mask)

    # Save
    output.save(output_path, format="PNG")
    print(f"✅ Full circular favicon created: {output_path}")

if __name__ == "__main__":
    input_img = r"C:\Users\Hp\.gemini\antigravity\brain\d2751725-21c6-413c-8dc5-7a478b7b22ec\vtu_crack_favicon_solid_round_final_1772183162560.png"
    output_img = "favicon.png"
    make_circle_with_padding(input_img, output_img)