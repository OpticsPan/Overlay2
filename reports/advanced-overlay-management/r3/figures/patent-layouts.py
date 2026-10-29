"""Embed unchanged patent PNGs with display rotation for web reading."""
from pathlib import Path
import base64
import struct
root = Path(__file__).resolve().parents[4]
layouts = {
    'noise-layout': 'US11513444B2/figures/p0009-0013.png',
    'sampling-layout': 'US9772561B2/figures/p0002-0001.png',
    'layer-layout': 'EP4632488A1/figures/p0020-0009.png',
}
for name, relative in layouts.items():
    data = (root / 'references/patents' / relative).read_bytes()
    w, h = struct.unpack('>II', data[16:24])
    encoded = base64.b64encode(data).decode('ascii')
    Path(__file__).with_name(name + '.svg').write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {h} {w}">'
        f'<title>{relative}; unchanged source image, rotated for layout</title>'
        f'<image width="{w}" height="{h}" transform="translate({h},0) rotate(90)" '
        f'xlink:href="data:image/png;base64,{encoded}"/></svg>', encoding='utf-8')
