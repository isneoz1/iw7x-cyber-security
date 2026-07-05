#!/usr/bin/env python3
"""Generate the Open Graph / social preview image for the iw7x site.

Produces ``docs/og-image.png`` (1200x630) with the brand gradient wordmark,
tagline, a "Built for Kali Linux" badge and the live stats — so shared links
render a polished card on Twitter/X, Discord, Slack, LinkedIn and Facebook.

Run:  python scripts/make_og_image.py
Requires: Pillow  (pip install pillow)
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).resolve().parent.parent / "docs" / "og-image.png"
W, H = 1200, 630

# Brand palette (mirrors docs/index.html / ui.py)
BG = (8, 8, 15)
TEXT = (238, 240, 255)
MUTED = (154, 160, 196)
CYAN = (72, 220, 255)
PINK = (255, 71, 179)
VIOLET = (150, 82, 255)
DRAGON = (142, 208, 255)
GRAD = [(255, 71, 179), (150, 82, 255), (72, 220, 255)]  # pink -> violet -> cyan

FONT_CANDIDATES = {
    "mono_bold": ["C:/Windows/Fonts/consolab.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
                  "/Library/Fonts/Menlo.ttc"],
    "sans_bold": ["C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                  "/Library/Fonts/Arial Bold.ttf"],
    "sans": ["C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
             "/Library/Fonts/Arial.ttf"],
}


def font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES[kind]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def lerp(a, b, f):
    return tuple(int(a[i] + (b[i] - a[i]) * f) for i in range(3))


def grad_at(pos: float):
    pos = max(0.0, min(1.0, pos))
    seg = pos * (len(GRAD) - 1)
    i = int(seg)
    return lerp(GRAD[i], GRAD[min(i + 1, len(GRAD) - 1)], seg - i)


def soft_glow(size, center, radius, color, alpha):
    """A blurred radial glow on its own RGBA layer."""
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = center
    d.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color + (alpha,))
    return layer.filter(ImageFilter.GaussianBlur(radius * 0.55))


def gradient_text(base: Image.Image, xy, text, fnt, horizontal=True):
    """Draw text filled with the pink->violet->cyan gradient."""
    x, y = xy
    bbox = fnt.getbbox(text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    mask = Image.new("L", (tw + 8, th + 8), 0)
    ImageDraw.Draw(mask).text((-bbox[0] + 4, -bbox[1] + 4), text, font=fnt, fill=255)
    grad = Image.new("RGB", (tw + 8, th + 8), (0, 0, 0))
    px = grad.load()
    for i in range(grad.width):
        col = grad_at(i / max(1, grad.width - 1))
        for j in range(grad.height):
            px[i, j] = col
    base.paste(grad, (x - 4, y - 4), mask)
    return tw, th


def main() -> None:
    img = Image.new("RGB", (W, H), BG)

    # Ambient glows
    for layer in (
        soft_glow((W, H), (120, 40), 420, PINK, 70),
        soft_glow((W, H), (W - 120, 60), 440, CYAN, 60),
        soft_glow((W, H), (W // 2, H + 60), 520, VIOLET, 70),
    ):
        img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")

    d = ImageDraw.Draw(img)
    PAD = 80

    # Eyebrow
    eyebrow = "THE WORLD'S CYBERSECURITY ARSENAL  ·  BY NEOZ"
    d.text((PAD, 74), eyebrow, font=font("mono_bold", 22), fill=CYAN)

    # "Built for Kali Linux" badge (top-right)
    badge = "BUILT FOR KALI LINUX"
    bf = font("mono_bold", 22)
    bw = d.textlength(badge, font=bf)
    bx0, by0 = W - PAD - bw - 34, 66
    d.rounded_rectangle([bx0, by0, W - PAD, by0 + 42], radius=21,
                        fill=(18, 28, 42), outline=DRAGON, width=2)
    d.text((bx0 + 17, by0 + 9), badge, font=bf, fill=DRAGON)

    # Wordmark
    wm_font = font("mono_bold", 210)
    gradient_text(img, (PAD, 150), "iw7x", wm_font)
    d = ImageDraw.Draw(img)

    # Tagline
    d.text((PAD, 396), "Every cybersecurity tool in the world.",
           font=font("sans_bold", 48), fill=TEXT)
    gradient_text(img, (PAD, 456), "One Kali terminal. One command.", font("sans_bold", 48))
    d = ImageDraw.Draw(img)

    # Stats row
    y = 546
    parts = [("12,139", CYAN, " TOOLS   "), ("50", CYAN, " CATEGORIES   "),
             ("KALI-READY", DRAGON, "   "), ("MIT · OPEN SOURCE", MUTED, "")]
    x = PAD
    sf_b = font("mono_bold", 30)
    sf = font("mono_bold", 26)
    for value, col, tail in parts:
        d.text((x, y), value, font=sf_b, fill=col)
        x += d.textlength(value, font=sf_b)
        if tail:
            d.text((x, y + 3), tail, font=sf, fill=MUTED)
            x += d.textlength(tail, font=sf)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG")
    print(f"wrote {OUT}  ({OUT.stat().st_size // 1024} KB, {W}x{H})")


if __name__ == "__main__":
    main()
