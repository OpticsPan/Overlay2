"""Rotate the unchanged patent crop for readable presentation; no image editing."""
import base64
from pathlib import Path
from PIL import Image

root=Path(__file__).resolve().parents[3]
source=root/'references/patents/WO2020094369A1/figures/p0022-0007.png'
width,height=Image.open(source).size
data=base64.b64encode(source.read_bytes()).decode()
svg=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{height}" height="{width}" viewBox="0 0 {height} {width}"><title>WO2020094369A1 Fig. 3, physical page 22; original crop rotated clockwise 90 degrees</title><image width="{width}" height="{height}" transform="translate({height} 0) rotate(90)" xlink:href="data:image/png;base64,{data}"/></svg>\n'
Path(__file__).with_suffix('.svg').write_text(svg)
