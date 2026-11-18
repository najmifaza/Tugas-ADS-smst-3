"""Render setiap SVG di images/ dan diagrams_upstream/ menjadi PNG 3x, lalu crop ke isi.

Jalankan: python render_png.py
"""

import pathlib
import re
import subprocess

from PIL import Image, ImageChops

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
BASE = pathlib.Path(__file__).resolve().parent.parent


def render(svg):
    html = svg.with_suffix(".html")
    png = svg.with_suffix(".png")
    tmp = svg.with_name("_render.png")
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg.read_text(encoding="utf-8"))
    w, h = int(float(vb.group(1))), int(float(vb.group(2)))
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=3", f"--screenshot={tmp}", f"--window-size={w},{h}",
                    html.resolve().as_uri()], capture_output=True, timeout=120)
    if not tmp.exists():
        return f"{svg.parent.name}/{svg.stem}: GAGAL render"
    im = Image.open(tmp).convert("RGB")
    bb = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255))).getbbox()
    crop = (max(0, bb[0] - 8), max(0, bb[1] - 8), min(im.size[0], bb[2] + 8), min(im.size[1], bb[3] + 8))
    im.crop(crop).save(png)
    tmp.unlink()
    return f"{svg.parent.name}/{svg.stem:26} canvas {w}x{h} -> png {Image.open(png).size}"


if __name__ == "__main__":
    for folder in ("images", "diagrams_upstream"):
        for svg in sorted((BASE / folder).glob("*.svg")):
            print(render(svg))