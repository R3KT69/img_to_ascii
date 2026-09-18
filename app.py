import os

try:
    from PIL import Image
except ImportError:
    raise SystemExit("Pillow is required. Install it with: pip install pillow")

ASCII_CHARS = " .:-=+*#%@"


def resize_image(img, new_width=125):
    width, height = img.size
    aspect_ratio = height / width
    new_height = max(1, int(new_width * aspect_ratio * 0.3))
    return img.resize((new_width, new_height))


def pixels_to_ascii(pixels):
    return "".join(ASCII_CHARS[pixel * (len(ASCII_CHARS) - 1) // 256] for pixel in pixels)


def convert_to_ascii(image_path, new_width=125):
    image = Image.open(image_path).convert("L")
    image = resize_image(image, new_width)

    pixels = list(image.getdata())
    ascii_lines = [
        pixels_to_ascii(pixels[y * image.width : (y + 1) * image.width])
        for y in range(image.height)
    ]
    return "\n".join(ascii_lines)


if __name__ == "__main__":
    folder = os.path.dirname(os.path.abspath(__file__))
    image_files = sorted(
        name
        for name in os.listdir(folder)
        if name.lower().endswith((".png", ".jpg", ".jpeg"))
    )

    if not image_files:
        print("No PNG, JPG, or JPEG file was found in the same folder as this script.")
        print("Place your image there and run the script again.")
        input("Press Enter to exit...")
    else:
        image_name = image_files[0]
        image_path = os.path.join(folder, image_name)
        ascii_art = convert_to_ascii(image_path)

        print(f"Converting: {image_name}\n")
        print(ascii_art)

        output_path = os.path.join(folder, "ascii_output.txt")
        with open(output_path, "w", encoding="utf-8") as output_file:
            output_file.write(ascii_art)

        print(f"\nASCII art saved to: {output_path}")
