"""
pixel_perfect_edit.py — Pixel-perfect date & salary editing on scanned demand letter PDFs.

Workflow:
1. Extract embedded JPEG image from each PDF page (via PyMuPDF)
2. Identify target text regions (dates, salaries) using coordinate-based approach
3. Paint over old text with background-matching rectangles
4. Render new text at same position with matched font
5. Reassemble into valid PDF
"""

import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
import io
import os
import json
import sys
import numpy as np
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class TextRegion:
    """A rectangular region of text to replace."""
    x1: int  # left
    y1: int  # top
    x2: int  # right
    y2: int  # bottom
    old_text: str
    new_text: str
    font_size: int = 14
    font_path: str = ""
    font_color: Tuple[int, int, int] = (0, 0, 0)
    bold: bool = False
    italic: bool = False
    alignment: str = "left"  # left, center, right


def sample_background_color(img: Image.Image, region: TextRegion, margin: int = 3) -> Tuple[int, int, int]:
    """Sample background color around a text region by averaging border pixels."""
    pixels = []
    w, h = img.size

    # Sample from edges of region (outside the text)
    for x in range(max(0, region.x1 - margin), min(w, region.x2 + margin)):
        for dy in [-margin, -margin + 1]:
            y = region.y1 + dy
            if 0 <= y < h:
                pixels.append(img.getpixel((x, y)))
        for dy in [margin, margin - 1]:
            y = region.y2 + dy
            if 0 <= y < h:
                pixels.append(img.getpixel((x, y)))

    for y in range(max(0, region.y1 - margin), min(h, region.y2 + margin)):
        for dx in [-margin, -margin + 1]:
            x = region.x1 + dx
            if 0 <= x < w:
                pixels.append(img.getpixel((x, y)))

    if not pixels:
        return (255, 255, 255)

    # Filter out very dark pixels (likely text bleed)
    light_pixels = [p for p in pixels if sum(p[:3]) > 400]
    if not light_pixels:
        light_pixels = pixels

    # Average
    r = int(np.mean([p[0] for p in light_pixels]))
    g = int(np.mean([p[1] for p in light_pixels]))
    b = int(np.mean([p[2] for p in light_pixels]))
    return (r, g, b)


def get_font(font_size: int, bold: bool = False, italic: bool = False) -> ImageFont.FreeTypeFont:
    """Get a matching font. Try system fonts first, fall back to default."""
    font_candidates = []

    if bold and italic:
        font_candidates = [
            "C:/Windows/Fonts/timesbi.ttf",
            "C:/Windows/Fonts/arialbi.ttf",
        ]
    elif bold:
        font_candidates = [
            "C:/Windows/Fonts/timesbd.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
        ]
    elif italic:
        font_candidates = [
            "C:/Windows/Fonts/timesi.ttf",
            "C:/Windows/Fonts/ariali.ttf",
        ]
    else:
        font_candidates = [
            "C:/Windows/Fonts/times.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
        ]

    for path in font_candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, font_size)

    # Fallback
    return ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)


def edit_image_region(img: Image.Image, region: TextRegion) -> Image.Image:
    """Edit a single text region in the image."""
    draw = ImageDraw.Draw(img)

    # 1. Sample background color
    bg_color = sample_background_color(img, region)

    # 2. Paint over old text with background color (with slight padding)
    pad = 2
    draw.rectangle(
        [region.x1 - pad, region.y1 - pad, region.x2 + pad, region.y2 + pad],
        fill=bg_color
    )

    # 3. Get matched font
    font = get_font(region.font_size, region.bold, region.italic)

    # 4. Calculate text position
    text_bbox = draw.textbbox((0, 0), region.new_text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]

    if region.alignment == "center":
        text_x = region.x1 + (region.x2 - region.x1 - text_w) // 2
    elif region.alignment == "right":
        text_x = region.x2 - text_w
    else:
        text_x = region.x1

    # Vertically center the text in the region
    region_h = region.y2 - region.y1
    text_y = region.y1 + (region_h - text_h) // 2

    # 5. Render new text
    draw.text((text_x, text_y), region.new_text, fill=region.font_color, font=font)

    return img


def rebuild_pdf_from_images(input_path: str, output_path: str, page_edits: Dict[int, List[TextRegion]]):
    """
    Extract each page as image, edit, and rebuild PDF.
    This avoids the complexity of in-place image replacement in PDF.
    """
    src_doc = fitz.open(input_path)
    out_doc = fitz.open()  # new empty PDF

    print(f"\nRebuilding: {os.path.basename(input_path)} ({len(src_doc)} pages)")

    for page_num in range(len(src_doc)):
        page = src_doc[page_num]

        # Extract the embedded image directly
        images = page.get_images()
        if not images:
            # Copy page as-is
            out_doc.insert_pdf(src_doc, from_page=page_num, to_page=page_num)
            continue

        xref = images[0][0]
        base_image = src_doc.extract_image(xref)
        img = Image.open(io.BytesIO(base_image["image"])).convert("RGB")

        # Apply edits if this page has any
        if page_num in page_edits:
            for region in page_edits[page_num]:
                print(f"  Page {page_num + 1}: '{region.old_text}' -> '{region.new_text}'")
                img = edit_image_region(img, region)

        # Convert back to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="JPEG", quality=95)
        img_bytes = img_bytes.getvalue()

        # Create new page with same dimensions
        rect = page.rect
        new_page = out_doc.new_page(width=rect.width, height=rect.height)
        new_page.insert_image(rect, stream=img_bytes)

    out_doc.save(output_path, garbage=4, deflate=True)
    out_doc.close()
    src_doc.close()
    print(f"  Saved: {output_path}")


# =============================================================================
# EDIT CONFIGURATIONS FOR EACH PDF
# =============================================================================

def get_al_rabeta_edits() -> Dict[int, List[TextRegion]]:
    """Al-Rabeta / Potential Region demand letter (768x1024, 1 page)."""
    return {
        0: [
            # "27 September 2022" -> "15 January 2027"
            TextRegion(
                x1=175, y1=142, x2=310, y2=158,
                old_text="27 September 2022",
                new_text="15 January 2027",
                font_size=14, font_color=(30, 30, 30)
            ),
            # "(Ref: KSM H00000118 Dated 17/09/2022)" -> updated date
            TextRegion(
                x1=210, y1=382, x2=325, y2=398,
                old_text="Dated 17/09/2022",
                new_text="Dated 15/01/2027",
                font_size=14, font_color=(30, 30, 30)
            ),
            # "1,500.00" -> "1,800.00"
            TextRegion(
                x1=338, y1=655, x2=405, y2=675,
                old_text="1,500.00",
                new_text="1,800.00",
                font_size=14, font_color=(30, 30, 30), bold=False
            ),
        ]
    }


def get_cck_farm_bl2_edits() -> Dict[int, List[TextRegion]]:
    """CCK Farm BL2 companion (768x1024, 1 page)."""
    return {
        0: [
            # "5 February 2023" -> "15 January 2027"
            TextRegion(
                x1=128, y1=270, x2=225, y2=290,
                old_text="5 February 2023",
                new_text="15 January 2027",
                font_size=15, font_color=(30, 30, 30)
            ),
            # "1,500.00" -> "1,800.00"
            TextRegion(
                x1=497, y1=898, x2=565, y2=917,
                old_text="1,500.00",
                new_text="1,800.00",
                font_size=15, font_color=(30, 30, 30), bold=False
            ),
        ]
    }


def get_exelite_edits() -> Dict[int, List[TextRegion]]:
    """Exelite Resources demand letter (768x1024, 1 page). This is a blank template — Date field is empty."""
    # This is a template with blank date/KDN fields, minimal edits needed
    return {}


if __name__ == "__main__":
    orig_dir = r"reports/sample_work_orders/originals"
    edit_dir = r"reports/sample_work_orders/edited"
    os.makedirs(edit_dir, exist_ok=True)

    # Focus on the 3 medium-resolution PDFs first
    edits = {
        "al_rabeta_potential_region_demand_letter.pdf": get_al_rabeta_edits(),
        "cck_farm_bl2_companion.pdf": get_cck_farm_bl2_edits(),
        "exelite_resources_demand_employment_letter.pdf": get_exelite_edits(),
    }

    for pdf_name, page_edits in edits.items():
        input_path = os.path.join(orig_dir, pdf_name)
        output_path = os.path.join(edit_dir, pdf_name)

        if not os.path.exists(input_path):
            print(f"Skipping {pdf_name}: not found")
            continue

        if not page_edits:
            # Just copy the file as-is
            import shutil
            shutil.copy2(input_path, output_path)
            print(f"Copied (no edits): {pdf_name}")
            continue

        rebuild_pdf_from_images(input_path, output_path, page_edits)

    print("\n=== Done! ===")
