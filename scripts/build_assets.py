#!/usr/bin/env python3
"""Rebuild the Crimson Archive Omarchy wallpapers from approved brand sources.

Only Pillow and stdlib are used. No fonts are bundled; only system fonts are used
when rendering informational labels in the exported preview and wallpapers.
Run this from anywhere: python scripts/build_assets.py
"""
from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
from math import sqrt, sin, cos, pi
import hashlib
import json
import random

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "brand-src"
BG = ROOT / "backgrounds"
W, H = 2560, 1440
OBSIDIAN = (18, 17, 21)
PARCHMENT = (245, 240, 230)
GOLD = (224, 186, 118)
CRIMSON = (225, 155, 173)
PAPER_INK = (117, 83, 28)


def font_serif(n: int):
    for p in ["/usr/share/fonts/truetype/ebgaramond/EBGaramond12-Regular.ttf",
              "/usr/share/fonts/truetype/ebgaramond/EBGaramond08-Regular.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"]:
        if Path(p).exists():
            return ImageFont.truetype(p, n)
    return ImageFont.load_default(size=n)


def font_sans(n: int):
    for p in ["/usr/share/fonts/opentype/inter/Inter-Medium.otf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if Path(p).exists():
            return ImageFont.truetype(p, n)
    return ImageFont.load_default(size=n)


def image(name: str) -> Image.Image:
    return Image.open(SRC / name).convert("RGBA")


def feather_mask(size: int, fade: int = 140) -> Image.Image:
    """Fade only outside edges, keeping the original central art intact."""
    reduced = 420
    small = Image.new("L", (reduced, reduced))
    px = small.load()
    scaled_fade = fade * reduced / size
    for y in range(reduced):
        for x in range(reduced):
            d = min(x, y, reduced - 1 - x, reduced - 1 - y)
            t = max(0, min(1, d / scaled_fade))
            smooth = t * t * (3 - 2 * t)
            px[x, y] = int(smooth * 255)
    return small.resize((size, size), Image.Resampling.BICUBIC)


def radial_glow(base: Image.Image, center: tuple[int, int], radius: int,
                color: tuple[int, int, int], alpha: int) -> None:
    """Subtle, efficient low-resolution rgba ambient light overlay."""
    scale = 6
    gw = (W + scale - 1) // scale
    gh = (H + scale - 1) // scale
    glow = Image.new("RGBA", (gw, gh))
    p = glow.load()
    cx, cy = center
    for y in range(gh):
        dy = ((y + 0.5) * scale - cy) / radius
        for x in range(gw):
            dx = ((x + 0.5) * scale - cx) / radius
            rr = dx * dx + dy * dy
            if rr < 1:
                intensity = (1 - rr) ** 2
                p[x, y] = (*color, int(alpha * intensity))
    glow = glow.resize((W, H), Image.Resampling.BICUBIC)
    base.alpha_composite(glow)


def circle_grid(base: Image.Image, center: tuple[int,int], radii,
                tint=(224,186,118), alpha=35) -> None:
    layer=Image.new("RGBA", (W,H))
    dr=ImageDraw.Draw(layer)
    cx, cy=center
    for i, rx in enumerate(radii):
        ry=rx * (0.99 if i % 2 else 0.91)
        a = max(8, alpha - (i*5))
        dr.ellipse((cx-rx, cy-ry, cx+rx, cy+ry),
                   outline=(*tint,a), width=2 if i == 0 else 1)
    for angle in [0, pi/2, pi, 3*pi/2]:
        x0 = int(cx + (min(radii)-13) * cos(angle))
        y0 = int(cy + (min(radii)-13) * sin(angle))
        x1 = int(cx + (max(radii)+16) * cos(angle))
        y1 = int(cy + (max(radii)+16) * sin(angle))
        dr.line((x0,y0,x1,y1), fill=(*tint,alpha//2), width=1)
    base.alpha_composite(layer)


def stars(base: Image.Image, seed: int, x_min=910, x_max=2500,
          y_min=100, y_max=1330, light=False) -> None:
    rng=random.Random(seed)
    layer=Image.new("RGBA", (W,H))
    dr=ImageDraw.Draw(layer)
    for i in range(140):
        x=rng.randrange(x_min, x_max)
        y=rng.randrange(y_min,y_max)
        r=rng.choice([1,1,1,1,2])
        c=(117,83,28,25) if light else (255,252,246,rng.randrange(22,73))
        dr.ellipse((x-r,y-r,x+r,y+r),fill=c)
    base.alpha_composite(layer)


def watermark_rule(base, light=False):
    lay=Image.new("RGBA",(W,H))
    d=ImageDraw.Draw(lay)
    gold=(117,83,28,80) if light else (224,186,118,61)
    d.line((136,1314,1050,1314), fill=gold, width=2)
    d.line((136,1314,136,1285),fill=gold,width=2)
    for x in [1082,1105,1128]:
        d.ellipse((x-2,1312,x+2,1316),fill=gold)
    base.alpha_composite(lay)


def paste_logo(base, name, box, opacity=255):
    logo=image(name)
    tw,th=box[2],box[3]
    scaled=logo.resize((tw,th), Image.Resampling.LANCZOS)
    if opacity != 255:
        a=scaled.getchannel("A").point(lambda v: v * opacity // 255)
        scaled.putalpha(a)
    base.alpha_composite(scaled, (box[0],box[1]))


def observatory():
    """Hero art right, empty left for launchers/work; not an app screenshot."""
    b=Image.new("RGBA",(W,H),(*OBSIDIAN,255))
    radial_glow(b,(1890,670),1120,(125,32,55),60)
    radial_glow(b,(2210,560),760,(107,48,156),42)
    circle_grid(b,(1980,670),[645,845,1100],GOLD,32)
    stars(b,143,1200,2490)
    art=image("crimson_archive_cosmic_astrolabe_emblem.png")
    size=1270
    art=art.resize((size,size),Image.Resampling.LANCZOS)
    mask=feather_mask(size,145)
    art.putalpha(mask)
    b.alpha_composite(art,(1245,55))
    # faint structural rules keep the left clear without introducing fake data.
    detail=Image.new('RGBA',(W,H))
    d=ImageDraw.Draw(detail)
    d.line((132,130,132,1220),fill=(224,186,118,42),width=2)
    d.line((132,130,595,130),fill=(224,186,118,42),width=2)
    d.ellipse((126,124,138,136),fill=(224,186,118,123))
    d.line((132,1220,605,1220),fill=(224,186,118,53),width=2)
    b.alpha_composite(detail)
    # The supplied hero already contains the official name on the right;
    # keep left clean so there are no duplicated logos in a scene.
    watermark_rule(b)
    return b.convert('RGB')


def instrument():
    """Clean Instrument mode with official monogram and conceptual line-work."""
    b=Image.new('RGBA',(W,H),(*OBSIDIAN,255))
    radial_glow(b,(1890,720),1080,(121,49,70),39)
    radial_glow(b,(1950,690),650,(224,186,118),13)
    circle_grid(b,(1830,705),[565,680,810,970],GOLD,51)
    stars(b,1738,980,2480)
    detail=Image.new('RGBA',(W,H))
    d=ImageDraw.Draw(detail)
    # Discrete celestial axes, intentionally NOT labelled as measured data.
    d.line((1640,704,2005,704),fill=(224,186,118,30),width=1)
    d.line((1830,520,1830,890),fill=(224,186,118,30),width=1)
    d.line((138,164,750,164),fill=(224,186,118,62),width=2)
    d.line((138,164,138,510),fill=(224,186,118,62),width=2)
    d.ellipse((132,158,144,170), fill=(224,186,118,144))
    for tick in range(12):
        x=200+tick*47
        d.line((x,164,x,177 if tick%3==0 else 171),fill=(224,186,118,50),width=1)
    b.alpha_composite(detail)
    # A dark, calm medallion protects logo clear-space against orbit lines.
    med=Image.new('RGBA',(W,H))
    md=ImageDraw.Draw(med)
    md.ellipse((1462,337,2198,1073),fill=(18,17,21,252),outline=(224,186,118,62),width=2)
    b.alpha_composite(med)
    paste_logo(b,'crimson-archive-monogram-dark.png',(1595,466,470,470))
    paste_logo(b,'crimson-archive-transparent-dark.png',(164,1020,655,207))
    watermark_rule(b)
    return b.convert('RGB')


def parchment():
    b=Image.new('RGBA',(W,H),(*PARCHMENT,255))
    radial_glow(b,(1960,760),1180,(221,198,169),46)
    center=(1820,720)
    circle_grid(b,center,[570,700,850,1040],(117,83,28),34)
    stars(b,1945,1050,2450,light=True)
    # Hairline grid is fine and almost invisible; still conceptual only.
    grid=Image.new('RGBA',(W,H))
    d=ImageDraw.Draw(grid)
    for x in range(100,2500,152):
        d.line((x,128,x,1300),fill=(117,83,28,11),width=1)
    for y in range(128,1300,152):
        d.line((96,y,2490,y),fill=(117,83,28,11),width=1)
    d.line((136,150,136,1200),fill=(117,83,28,48),width=2)
    b.alpha_composite(grid)
    # Keep a full clear-space buffer around the production monogram.
    back=Image.new('RGBA',(W,H))
    bd=ImageDraw.Draw(back)
    bd.ellipse((1470,366,2160,1056),fill=(245,240,230,250),outline=(117,83,28,42),width=2)
    b.alpha_composite(back)
    paste_logo(b,'crimson-archive-monogram-light.png',(1601,495,432,432))
    # Official transparent light logo needs to be included only as source SVG,
    # so we use the same original PNG monogram and real editorial caption.
    d=ImageDraw.Draw(b)
    d.text((178,1045),'THE ARCHIVE',font=font_serif(93),fill=(33,27,30,255))
    d.text((182,1170),'PARCHMENT  /  FIELD NOTES',font=font_sans(24),fill=(117,83,28,255),spacing=4)
    watermark_rule(b,light=True)
    return b.convert('RGB')


def add_preview():
    wallpaper=Image.open(BG/'01-observatory.webp').convert('RGBA')
    wallpaper=wallpaper.resize((1920,1080),Image.Resampling.LANCZOS)
    # Readability veil restricted to the left half of this *illustrative* image.
    veil=Image.new('RGBA',(1920,1080))
    d=ImageDraw.Draw(veil)
    d.rounded_rectangle((55,74,1100,855),radius=26,fill=(14,13,17,214),outline=(224,186,118,74),width=2)
    wallpaper.alpha_composite(veil)
    paste_logo_scaled(wallpaper,'crimson-archive-transparent-dark.png',(126,110,745,236))
    d=ImageDraw.Draw(wallpaper)
    d.text((138,398),'AN INSTRUMENT',font=font_serif(75),fill=(243,238,230,255))
    d.text((138,480),'FOR INQUIRY.',font=font_serif(75),fill=(243,238,230,255))
    d.text((140,588),'Obsidian  /  Crimson  /  Antique gold',font=font_sans(24),fill=(190,179,180,255))
    d.line((140,679,980,679),fill=(224,186,118,110),width=2)
    sw=[('#121115','OBSIDIAN'),('#E19BAD','CRIMSON'),('#E0BA76','GOLD'),('#F3EEE6','IVORY'),('#C4A3FF','VIOLET')]
    for i,(hexcolor,label) in enumerate(sw):
        x=140+171*i
        d.rounded_rectangle((x,711,x+104,738),radius=5,fill=hexcolor,outline='#4A404B',width=1)
        d.text((x,753),label,font=font_sans(15),fill=(190,179,180,255))
    d.text((140,818),'CONCEPT PREVIEW  ·  NOT A LIVE OMARCHY SCREENSHOT',font=font_sans(14),fill=(168,153,157,255))
    wallpaper.convert('RGB').save(ROOT/'preview.png',optimize=True)


def paste_logo_scaled(base:Image.Image, name:str,box:tuple[int,int,int,int]):
    # Preserve original aspect ratio; box gives a maximum size not a crop.
    im=image(name)
    im.thumbnail((box[2],box[3]),Image.Resampling.LANCZOS)
    base.alpha_composite(im,(box[0],box[1]))


def add_unlock():
    im=image('crimson-archive-monogram-dark.png')
    im.thumbnail((490,490),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(512,512),(0,0,0,0))
    canvas.alpha_composite(im,((512-im.width)//2,(512-im.height)//2))
    canvas.save(ROOT/'unlock.png',optimize=True)
    pv=Image.new('RGBA',(1920,1080),(*OBSIDIAN,255))
    # Preview-unlock is deliberately illustrative, not a fabricated screenshot.
    # Quiet reticle is not scientific data, and the actual logo appears once.
    ornaments=Image.new('RGBA',(1920,1080))
    od=ImageDraw.Draw(ornaments)
    for i,r in enumerate((430,545,690,850)):
        od.ellipse((960-r,540-r*0.84,960+r,540+r*0.84),
                   outline=(*GOLD,max(9,37-i*8)),width=2 if i==0 else 1)
    od.line((100,98,480,98),fill=(*GOLD,65),width=2)
    od.line((100,98,100,370),fill=(*GOLD,65),width=2)
    pv.alpha_composite(ornaments)
    lay=Image.new('RGBA',(1920,1080))
    d=ImageDraw.Draw(lay)
    d.rounded_rectangle((570,180,1350,900),radius=34,fill=(18,17,21,231),outline=(224,186,118,101),width=3)
    pv.alpha_composite(lay)
    mark=Image.open(ROOT/'unlock.png').convert('RGBA').resize((450,450),Image.Resampling.LANCZOS)
    pv.alpha_composite(mark,(735,220))
    d=ImageDraw.Draw(pv)
    title='CRIMSON ARCHIVE'
    w=d.textbbox((0,0),title,font=font_sans(34))[2]
    d.text(((1920-w)//2,728),title,font=font_sans(34),fill=(243,238,230,255))
    d.text((610,850),'ILLUSTRATIVE UNLOCK PREVIEW',font=font_sans(17),fill=(190,179,180,255))
    pv.convert('RGB').save(ROOT/'preview-unlock.png',optimize=True)


def main():
    BG.mkdir(parents=True,exist_ok=True)
    manifests=json.loads((ROOT/'assets/SOURCE_SHA256.json').read_text())
    for rel,digest in manifests.items():
        actual=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
        if actual != digest:
            raise RuntimeError(f'Source asset altered: {rel}')
    for name,renderer in [('01-observatory.webp',observatory),
                          ('02-instrument-room.webp',instrument),
                          ('03-parchment-study.webp',parchment)]:
        p=BG/name
        renderer().save(p,'WEBP',quality=89,method=6)
        print(f'{p.relative_to(ROOT)} — {p.stat().st_size//1024} KiB')
    add_preview()
    add_unlock()
    print('Generated previews and unlock art.')

if __name__ == '__main__':
    main()
