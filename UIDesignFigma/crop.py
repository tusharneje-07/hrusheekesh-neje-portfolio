import os
import sys
from PIL import Image
import fitz  # PyMuPDF

# -----------------------------
# Usage:
# python script.py input.pdf output_folder
# -----------------------------

TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080
JPEG_QUALITY = 95


def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def crop_vertical_chunks(image, output_folder, base_name, start_index):
    """
    Splits a tall image into 1920x1080 chunks vertically.
    Saves as high-quality JPG.
    """
    width, height = image.size

    # Resize width to 1920 while maintaining aspect ratio
    if width != TARGET_WIDTH:
        new_height = int((TARGET_WIDTH / width) * height)
        image = image.resize((TARGET_WIDTH, new_height), Image.LANCZOS)
        width, height = image.size

    index = start_index
    y = 0

    while y < height:
        lower = min(y + TARGET_HEIGHT, height)

        # Crop chunk
        chunk = image.crop((0, y, TARGET_WIDTH, lower))

        # If last chunk height < 1080, pad with black background
        if chunk.size[1] < TARGET_HEIGHT:
            padded = Image.new("RGB", (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0))
            padded.paste(chunk, (0, 0))
            chunk = padded

        output_path = os.path.join(
            output_folder,
            f"{base_name}_{index:04d}.jpg"
        )

        chunk.save(
            output_path,
            "JPEG",
            quality=JPEG_QUALITY,
            optimize=True,
            subsampling=0
        )

        print(f"Saved: {output_path}")

        index += 1
        y += TARGET_HEIGHT

    return index


def pdf_to_images(pdf_path, output_folder):
    ensure_folder(output_folder)

    pdf = fitz.open(pdf_path)

    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    image_index = 1

    for page_number in range(len(pdf)):
        page = pdf.load_page(page_number)

        # Render page at high resolution
        zoom = 2.0
        matrix = fitz.Matrix(zoom, zoom)

        pix = page.get_pixmap(matrix=matrix, alpha=False)

        img = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        image_index = crop_vertical_chunks(
            img,
            output_folder,
            base_name,
            image_index
        )

    pdf.close()


def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <pdf_file> <output_folder>")
        sys.exit(1)

    pdf_file = sys.argv[1]
    output_folder = sys.argv[2]

    if not os.path.isfile(pdf_file):
        print(f"PDF file not found: {pdf_file}")
        sys.exit(1)

    pdf_to_images(pdf_file, output_folder)

    print("Done.")


if __name__ == "__main__":
    main()
