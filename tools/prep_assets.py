#!/usr/bin/env python3
"""Grade the parish photographs into the site palette and write them to assets/.

Sources are the church's own images, pulled from theprayerpalace.com. Each one is
cropped, resized to the size it is actually displayed at, graded, and written as WebP.

The grade is a duotone lift: luminance is mapped between a deep blue shadow and a warm
bone highlight, then a fraction of the original colour is mixed back so that faces keep
their skin. A full duotone reads as a filter; 35% of the original reads as a grade.
"""
import os, sys
from PIL import Image, ImageEnhance, ImageOps

SRC = sys.argv[1] if len(sys.argv) > 1 else "src"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

SHADOW = (10, 18, 34)      # deep blue-black
HIGHLIGHT = (242, 238, 226)  # warm bone


def duotone(im, keep=0.35, shadow=SHADOW, highlight=HIGHLIGHT):
    """Map luminance onto a shadow-highlight ramp, then mix the original back in."""
    im = im.convert("RGB")
    lum = ImageOps.grayscale(im)
    ramp = ImageOps.colorize(lum, black=shadow, white=highlight)
    return Image.blend(ramp, im, keep)


def cover(im, w, h):
    """Resize and centre-crop to exactly w x h, the way CSS object-fit: cover does."""
    sw, sh = im.size
    scale = max(w / sw, h / sh)
    im = im.resize((max(1, round(sw * scale)), max(1, round(sh * scale))), Image.LANCZOS)
    sw, sh = im.size
    left, top = (sw - w) // 2, (sh - h) // 2
    return im.crop((left, top, left + w, top + h))


def grade(src, name, size, crop=None, keep=0.35, contrast=1.06, quality=82):
    im = Image.open(os.path.join(SRC, src))
    if crop:
        im = im.crop(crop)
    im = cover(im.convert("RGB"), *size)
    im = duotone(im, keep=keep)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    dst = os.path.join(OUT, name + ".webp")
    im.save(dst, "WEBP", quality=quality, method=6)
    print(f"{name:22} {size[0]}x{size[1]}  {os.path.getsize(dst)//1024:>4} KB   <- {src}")


def lift_alpha(src, name, size, crop=None, quality=90, ink=True if False else False):
    """Rebuild a light-on-dark logo as a clean transparent PNG-style asset.

    The supplied logo has a semi-opaque black panel baked into it, so it carries a dark
    rectangle onto any background it is placed on. The mark itself is light, so taking
    alpha from luminance drops the panel and keeps the chrome.
    """
    im = Image.open(os.path.join(SRC, src)).convert("RGBA")
    if crop:
        im = im.crop(crop)
    rgb = im.convert("RGB")
    alpha = ImageOps.grayscale(rgb)
    alpha = alpha.point(lambda v: 0 if v < 24 else min(255, int((v - 24) * 1.45)))
    if ink:
        # Same silhouette, dark, for placing on a light ground.
        out = ImageOps.colorize(ImageOps.grayscale(rgb), black=(96, 104, 116), white=(18, 26, 44))
    else:
        out = rgb.copy()
    out = out.convert("RGB")
    out.putalpha(alpha)
    out.thumbnail(size, Image.LANCZOS)
    dst = os.path.join(OUT, name + ".webp")
    out.save(dst, "WEBP", quality=quality, method=6)
    print(f"{name:22} {out.size[0]}x{out.size[1]}  {os.path.getsize(dst)//1024:>4} KB   <- {src}")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)

    # Brand marks keep their own colour. Alpha is rebuilt from luminance to drop the
    # black panel baked into the supplied file.
    lift_alpha("logo2x.png", "logo", (520, 350))
    lift_alpha("logo2x.png", "mark", (300, 300), crop=(14, 24, 300, 336))
    # An ink variant of the wordmark, for the bar once the ground turns to paper.
    lift_alpha("logo2x.png", "logo-ink", (520, 350), ink=True)

    # The sanctuary. These carry chapters 03 and 04, so they run wide. Both sources are
    # promo slides with service times set over them; the crops cut the overlay away and
    # keep only what is genuinely in the room.
    grade("gal-21.jpg", "sanctuary-wall", (1400, 532), crop=(0, 0, 1500, 570), keep=0.42)
    grade("gal-23.jpg", "sanctuary-light", (980, 800), crop=(520, 0, 1500, 802), keep=0.20)

    # The founding family.
    grade("si-45.png", "pastor-tom", (760, 760), keep=0.45)
    grade("gal-24.jpg", "pastor-paul", (480, 660), crop=(588, 130, 905, 600), keep=0.42)

    # The work of the church.
    grade("si-41.jpg", "cross", (900, 900), keep=0.50, contrast=1.10)
    grade("bg-02.jpg", "congregation", (900, 900), keep=0.38)
    grade("si-42.jpg", "welcome", (900, 900), keep=0.38)
    grade("gal-10.jpg", "jamaica", (900, 620), crop=(0, 0, 740, 802), keep=0.42)
