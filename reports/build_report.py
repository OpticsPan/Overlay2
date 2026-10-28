"""Render the report using Pandoc, Matplotlib formula SVGs, and WeasyPrint."""
import argparse
import os
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--weasyprint', default='weasyprint')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
source = root / 'reports/advanced-overlay-management/report.md'
work = root / 'work/report-build'
work.mkdir(parents=True, exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR', str(work / 'matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME', str(work / 'cache'))
from matplotlib.mathtext import math_to_image
from matplotlib.font_manager import FontProperties
counter = 0

def formula(match):
    global counter
    counter += 1
    display = match.group(1) is not None
    tex = (match.group(1) if display else match.group(2)).strip().replace('\n', ' ')
    asset = work / f'formula-{counter}.svg'
    math_to_image('$' + tex + '$', asset, prop=FontProperties(size=12), format='svg')
    # SVG files are temporary presentation artifacts; Markdown remains authoritative.
    return ('\n\n' if display else '') + f'<img class="formula {"display" if display else "inline"}" src="{asset.as_uri()}" alt="formula {counter}">' + ('\n\n' if display else '')
text = re.sub(r'\$\$(.*?)\$\$|\$([^$\n]+)\$', formula, source.read_text('utf-8'), flags=re.S)
prepared = work / 'prepared.md'
prepared.write_text(text, 'utf-8')
html = work / 'report.html'
subprocess.run(['pandoc', str(prepared), '--from=markdown', '--standalone', '--toc', '--toc-depth=2', '--embed-resources', '--metadata=toc-title:目录', '--css', str(root / 'reports/templates/report.css'), '--resource-path', str(source.parent) + ':' + str(root), '-o', str(html)], check=True)
html_text = html.read_text('utf-8')
html_text = re.sub(r'<figure>(.*?)</figure>', lambda m: '<figure' + (' class="rotated"' if '图2 跨曝光场' in m.group(1) else '') + '>' + m.group(1) + '</figure>', html_text, flags=re.S)
html.write_text(html_text, 'utf-8')
subprocess.run([args.weasyprint, str(html), str(source.with_suffix('.pdf'))], check=True)
print(source.with_suffix('.pdf'))
