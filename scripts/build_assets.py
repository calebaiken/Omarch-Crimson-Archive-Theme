#!/usr/bin/env python3
"""Build wallpaper and preview exports from the checked-in source assets."""
from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont, ImageOps
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent.parent
BRAND_SRC = ROOT / "assets" / "brand-src"
WALLPAPER_SRC = ROOT / "assets" / "wallpaper-src"
BG = ROOT / "backgrounds"
W, H = 2560, 1440
OBSIDIAN = (18, 17, 21)
GOLD = (224, 186, 118)


def font_serif(size: int):
    for path in ["/usr/share/fonts/truetype/ebgaramond/EBGaramond12-Regular.ttf",
                 "/usr/share/fonts/truetype/ebgaramond/EBGaramond08-Regular.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def font_sans(size: int):
    for path in ["/usr/share/fonts/opentype/inter/Inter-Medium.otf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def source_image(name: str) -> Image.Image:
    return Image.open(BRAND_SRC / name).convert("RGBA")


def paste_logo_scaled(base: Image.Image, name: str,
                      box: tuple[int, int, int, int]) -> None:
    """Preserve original aspect ratio; box gives the maximum dimensions."""
    logo = source_image(name)
    logo.thumbnail((box[2], box[3]), Image.Resampling.LANCZOS)
    base.alpha_composite(logo, (box[0], box[1]))


def add_preview() -> None:
    wallpaper = Image.open(BG / "01-observatory.webp").convert("RGBA")
    wallpaper = wallpaper.resize((1920, 1080), Image.Resampling.LANCZOS)
    veil = Image.new("RGBA", (1920, 1080))
    draw = ImageDraw.Draw(veil)
    draw.rounded_rectangle((55, 74, 1100, 855), radius=26,
                           fill=(14, 13, 17, 214),
                           outline=(224, 186, 118, 74), width=2)
    wallpaper.alpha_composite(veil)
    paste_logo_scaled(wallpaper, "crimson-archive-transparent-dark.png",
                      (126, 110, 745, 236))
    draw = ImageDraw.Draw(wallpaper)
    draw.text((138, 398), "AN INSTRUMENT", font=font_serif(75),
              fill=(243, 238, 230, 255))
    draw.text((138, 480), "FOR INQUIRY.", font=font_serif(75),
              fill=(243, 238, 230, 255))
    draw.text((140, 588), "Obsidian  /  Crimson  /  Antique gold",
              font=font_sans(24), fill=(190, 179, 180, 255))
    draw.line((140, 679, 980, 679), fill=(224, 186, 118, 110), width=2)
    swatches = [("#121115", "OBSIDIAN"), ("#E19BAD", "CRIMSON"),
                ("#E0BA76", "GOLD"), ("#F3EEE6", "IVORY"),
                ("#C4A3FF", "VIOLET")]
    for index, (color, label) in enumerate(swatches):
        x = 140 + 171 * index
        draw.rounded_rectangle((x, 711, x + 104, 738), radius=5,
                               fill=color, outline="#4A404B", width=1)
        draw.text((x, 753), label, font=font_sans(15),
                  fill=(190, 179, 180, 255))
    draw.text((140, 818), "CONCEPT PREVIEW  ·  NOT A LIVE OMARCHY SCREENSHOT",
              font=font_sans(14), fill=(168, 153, 157, 255))
    wallpaper.convert("RGB").save(ROOT / "preview.png", optimize=True)


def add_unlock() -> None:
    logo = source_image("crimson-archive-monogram-dark.png")
    logo.thumbnail((490, 490), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    canvas.alpha_composite(logo, ((512 - logo.width) // 2,
                                  (512 - logo.height) // 2))
    canvas.save(ROOT / "unlock.png", optimize=True)

    preview = Image.new("RGBA", (1920, 1080), (*OBSIDIAN, 255))
    ornaments = Image.new("RGBA", (1920, 1080))
    draw = ImageDraw.Draw(ornaments)
    for index, radius in enumerate((430, 545, 690, 850)):
        draw.ellipse((960 - radius, 540 - radius * 0.84,
                      960 + radius, 540 + radius * 0.84),
                     outline=(*GOLD, max(9, 37 - index * 8)),
                     width=2 if index == 0 else 1)
    draw.line((100, 98, 480, 98), fill=(*GOLD, 65), width=2)
    draw.line((100, 98, 100, 370), fill=(*GOLD, 65), width=2)
    preview.alpha_composite(ornaments)

    panel = Image.new("RGBA", (1920, 1080))
    draw = ImageDraw.Draw(panel)
    draw.rounded_rectangle((570, 180, 1350, 900), radius=34,
                           fill=(18, 17, 21, 231),
                           outline=(224, 186, 118, 101), width=3)
    preview.alpha_composite(panel)
    mark = Image.open(ROOT / "unlock.png").convert("RGBA")
    mark = mark.resize((450, 450), Image.Resampling.LANCZOS)
    preview.alpha_composite(mark, (735, 220))
    draw = ImageDraw.Draw(preview)
    title = "CRIMSON ARCHIVE"
    width = draw.textbbox((0, 0), title, font=font_sans(34))[2]
    draw.text(((1920 - width) // 2, 728), title, font=font_sans(34),
              fill=(243, 238, 230, 255))
    draw.text((610, 850), "ILLUSTRATIVE UNLOCK PREVIEW",
              font=font_sans(17), fill=(190, 179, 180, 255))
    preview.convert("RGB").save(ROOT / "preview-unlock.png", optimize=True)


def verify_manifest(path: Path, root: Path) -> None:
    manifest = json.loads(path.read_text())
    for relative_path, expected in manifest.items():
        actual = hashlib.sha256((root / relative_path).read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(f"Source asset checksum mismatch: {relative_path}")


def build_wallpapers() -> None:
    manifest_path = ROOT / "assets" / "WALLPAPER_SOURCE_SHA256.json"
    verify_manifest(manifest_path, ROOT)
    sources = [
        ("01-observatory-embossed.png", "01-observatory.webp"),
        ("02-instrument-embossed.png", "02-instrument-room.webp"),
        ("03-parchment-embossed.png", "03-parchment-study.webp"),
    ]
    for source_name, output_name in sources:
        with Image.open(WALLPAPER_SRC / source_name) as source:
            # Fit the generated 16:9 masters to the project's 2560x1440 export.
            wallpaper = ImageOps.fit(source.convert("RGB"), (W, H),
                                     method=Image.Resampling.LANCZOS,
                                     centering=(0.5, 0.5))
            output = BG / output_name
            wallpaper.save(output, "WEBP", quality=89, method=6)
            print(f"{output.relative_to(ROOT)} — {output.stat().st_size // 1024} KiB")


def main() -> None:
    BG.mkdir(parents=True, exist_ok=True)
    verify_manifest(ROOT / "assets" / "SOURCE_SHA256.json", ROOT)
    build_wallpapers()
    add_preview()
    add_unlock()
    print("Generated wallpapers, previews, and unlock art.")


if __name__ == "__main__":
    main()
