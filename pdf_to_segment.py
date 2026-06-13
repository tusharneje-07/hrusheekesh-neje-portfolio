#!/usr/bin/env python3

import argparse
import json
import math
import sys
from pathlib import Path

from pdf2image import convert_from_path
from PIL import Image

# Prevent Pillow from rejecting very large PDF renders
Image.MAX_IMAGE_PIXELS = None

# ── Constants ────────────────────────────────────────────────────────────────

SEGMENT_WIDTH = 1920
SEGMENT_HEIGHT = 1080

DEFAULT_DPI = 300
DEFAULT_QUALITY = 100


# ─────────────────────────────────────────────────────────────────────────────

def pdf_to_segments(
    pdf_path: Path,
    output_dir: Path,
    dpi: int = DEFAULT_DPI,
    quality: int = DEFAULT_QUALITY,
) -> list[dict]:

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n  📄 Processing: {pdf_path.name}")
    print(f"     → Output dir : {output_dir}")

    pages = convert_from_path(
        str(pdf_path),
        dpi=dpi,
        thread_count=4,
        use_cropbox=True,
    )

    print(f"     → Pages rendered : {len(pages)}")

    segments: list[dict] = []
    segment_index = 1

    for page_num, page in enumerate(pages, start=1):

        print(
            f"     → Page {page_num}: "
            f"{page.width} × {page.height}"
        )

        scale = SEGMENT_WIDTH / page.width
        resized_height = math.ceil(page.height * scale)

        page = page.resize(
            (SEGMENT_WIDTH, resized_height),
            Image.Resampling.LANCZOS,
        )

        print(
            f"       Resized to: "
            f"{SEGMENT_WIDTH} × {resized_height}"
        )

        for y_start in range(0, page.height, SEGMENT_HEIGHT):

            y_end = min(
                y_start + SEGMENT_HEIGHT,
                page.height,
            )

            tile = page.crop(
                (
                    0,
                    y_start,
                    SEGMENT_WIDTH,
                    y_end,
                )
            )

            if tile.height < SEGMENT_HEIGHT:
                padded = Image.new(
                    "RGB",
                    (SEGMENT_WIDTH, SEGMENT_HEIGHT),
                    (255, 255, 255),
                )
                padded.paste(tile, (0, 0))
                tile = padded

            seg_name = f"seg_{segment_index:03d}.jpg"
            seg_path = output_dir / seg_name

            tile.save(
                seg_path,
                format="JPEG",
                quality=quality,
                optimize=True,
                progressive=True,
                dpi=(dpi, dpi),
            )

            segments.append(
                {
                    "index": segment_index,
                    "filename": seg_name,
                    "width": SEGMENT_WIDTH,
                    "height": SEGMENT_HEIGHT,
                    "is_last": False,
                }
            )

            segment_index += 1

    if segments:
        segments[-1]["is_last"] = True

    print(
        f"     → Segments : {len(segments)}"
    )

    print(
        f"     ✅ Done → {len(segments)} segments written"
    )

    return segments


# ─────────────────────────────────────────────────────────────────────────────

def update_manifest(
    manifest_path: Path,
    project_id: int,
    pdf_name: str,
    segments: list[dict],
) -> None:

    manifest_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = {}

    if manifest_path.exists():
        try:
            with open(
                manifest_path,
                "r",
                encoding="utf-8",
            ) as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(
                "  ⚠️ Existing manifest malformed. Recreating."
            )

    proj_key = f"portfolio_proj_{project_id}"

    data[proj_key] = {
        "project_id": project_id,
        "source_pdf": pdf_name,
        "image_dir": f"assets/images/{proj_key}",
        "total_segments": len(segments),
        "segment_width": SEGMENT_WIDTH,
        "segment_height": SEGMENT_HEIGHT,
        "segments": segments,
    }

    with open(
        manifest_path,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"     📝 Manifest updated → {manifest_path}"
    )


# ─────────────────────────────────────────────────────────────────────────────

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Convert PDFs into 1920x1080 JPEG segments."
        )
    )

    parser.add_argument(
        "--input-dir",
        default="./portfolio_design_pdfs",
        help="Directory containing PDFs",
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=DEFAULT_DPI,
    )

    parser.add_argument(
        "--quality",
        type=int,
        default=DEFAULT_QUALITY,
    )

    args = parser.parse_args()

    input_dir = Path(args.input_dir)

    manifest_path = Path(
        "assets/data/portfolio_img.json"
    )

    if not input_dir.exists():
        print(
            f"❌ Input directory not found: {input_dir}",
            file=sys.stderr,
        )
        sys.exit(1)

    pdf_files = sorted(
        input_dir.glob("*.pdf")
    )

    if not pdf_files:
        print(
            f"❌ No PDFs found in {input_dir}",
            file=sys.stderr,
        )
        sys.exit(1)

    print(
        f"\n🗂️ Found {len(pdf_files)} PDF(s) in '{input_dir}'"
    )

    for i, pdf in enumerate(pdf_files, start=1):
        size_mb = pdf.stat().st_size / 1048576
        print(
            f"   {i}. {pdf.name} ({size_mb:.1f} MB)"
        )

    for project_id, pdf_path in enumerate(
        pdf_files,
        start=1,
    ):

        output_dir = Path(
            f"assets/images/portfolio_proj_{project_id}"
        )

        segments = pdf_to_segments(
            pdf_path=pdf_path,
            output_dir=output_dir,
            dpi=args.dpi,
            quality=args.quality,
        )

        update_manifest(
            manifest_path=manifest_path,
            project_id=project_id,
            pdf_name=pdf_path.name,
            segments=segments,
        )

    print(
        f"\n🎉 All done! Manifest → {manifest_path}\n"
    )


if __name__ == "__main__":
    main()