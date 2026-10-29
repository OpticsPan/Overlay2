"""Render a content-sized overview. Requires Matplotlib, fontconfig, Noto Sans CJK SC.

SVG stores glyph outlines. --preview-dir optionally writes PNG and layout checks.
"""
import argparse
import json
from pathlib import Path
import subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

DPI, WIDTH, PAD = 100, 1000, 18
MAIN, SUPPORT, SOURCE, EXECUTION, RESULT = '#365E7A', '#74728D', '#8A7255', '#AC6C36', '#4E7B62'
FONT_PATH = subprocess.check_output(['fc-match', '-f', '%{file}', 'Noto Sans CJK SC'], text=True).strip()
METRICS = RendererAgg(WIDTH, 1600, DPI)


def font(px):
    return FontProperties(fname=FONT_PATH, size=px * 72 / DPI)


def text_width(text, px):
    return METRICS.get_text_width_height_descent(text, font(px), False)[0]


def wrap(text, width, px):
    """Wrap with actual font widths and preserve intentional line breaks."""
    lines = []
    for paragraph in text.split('\n'):
        current = ''
        for char in paragraph:
            if current and text_width(current + char, px) > width:
                lines.append(current)
                current = char
            else:
                current += char
        lines.append(current)
    return lines


def node(x, y, width, title, body, color=MAIN, fill='#EDF4F9', title_px=23):
    titles, lines = wrap(title, width - 2 * PAD, title_px), wrap(body, width - 2 * PAD, 19)
    title_line = title_px * 1.35
    height = 2 * PAD + len(titles) * title_line + 8 + len(lines) * 27
    return dict(x=x, y=y, w=width, h=height, title=titles, body=lines,
                title_px=title_px, title_line=title_line, color=color, fill=fill)


def middle(item):
    return item['y'] + item['h'] / 2


def build(preview_dir=None):
    descriptions = [
        ('目标与工艺背景', '产品、层间关系与设备路径\n评价阶段与指标口径'),
        ('当前对象量测与历史信息', '对准、形状及状态观测\n加工历史与既有校正'),
        ('误差估计与曝光时预测', '区分空间、层来源与动态分量\n预测曝光时的误差状态'),
        ('校正协调与受约束优化', '协调多路贡献，避免重复补偿\n结合产品窗口与执行能力'),
        ('控制轮廓生成与执行', '平台 / 光学的时间设定点\n计入狭缝作用及动态限制'),
        ('曝光及后续工艺', '形成图案，经历后续加工\n工艺路径与评价阶段相对应'),
        ('结果量测与残差评价', '区分量测阶段与执行贡献\n评价套刻及相关成像表现'),
    ]
    chain, y = [], 100
    for index, (title, body) in enumerate(descriptions):
        item = node(310, y, 400, title, body)
        chain.append(item)
        y += item['h'] + (64 if index == 4 else 44)
    reference = node(24, chain[1]['y'], 236, '参考与模型支撑',
        '量测参考\n传感器与坐标校准\n\n预测依据\n校准指纹与模型参数\n\n执行能力\n自由度与调节范围\n动态响应及空间分辨率', SUPPORT, '#F2F1F7', 21)
    prevention = node(24, chain[5]['y'], 236, '源头抑制与状态准备',
        '结构设计\n支撑、夹持与隔离\n\n运行调节与准备\n调温、重夹与状态检查', SOURCE, '#F7F3ED', 21)
    executed = node(752, chain[4]['y'] - 18, 224, '执行侧信息回传',
        '已采用的校正\n未执行分量', EXECUTION, '#FAF1E8', 21)
    feedback = node(752, chain[6]['y'], 224, '加工后结果反馈',
        '更新后续校正\n或相关模型参数', RESULT, '#EDF5EF', 21)
    nodes = chain + [reference, prevention, executed, feedback]
    height = max(n['y'] + n['h'] for n in nodes) + 128
    fig, ax = plt.subplots(figsize=(WIDTH / DPI, height / DPI), dpi=DPI)
    fig.subplots_adjust(0, 0, 1, 1)
    fig.patch.set_facecolor('white')
    ax.set(xlim=(0, WIDTH), ylim=(height, 0))
    ax.axis('off')
    plt.rcParams['svg.fonttype'] = 'path'
    plt.rcParams['svg.hashsalt'] = 'overlay-r2-overview'
    drawn_text, routes = [], []

    def label(x, y, text, px=19, color='#233E50', ha='center', owner=None):
        artist = ax.text(x, y, text, fontproperties=font(px), ha=ha, va='center', color=color)
        if owner is not None:
            drawn_text.append((artist, owner))

    def line(points, color=MAIN, dashed=False, arrow=True):
        routes.append(points)
        style = (0, (4, 4)) if dashed else 'solid'
        if len(points) > 2:
            ax.plot(*zip(*points[:-1]), color=color, lw=1.4, linestyle=style, zorder=1)
        if arrow:
            ax.add_patch(FancyArrowPatch(points[-2], points[-1], arrowstyle='-|>',
                mutation_scale=13, linewidth=1.4, color=color, linestyle=style,
                shrinkA=0, shrinkB=0, zorder=1))
        else:
            ax.plot(*zip(*points[-2:]), color=color, lw=1.4, linestyle=style, zorder=1)

    label(WIDTH / 2, 34, '整机套刻管理的功能关系', 27)
    label(WIDTH / 2, 68, '研究归纳 · 箭头表示功能依赖，不代表固定执行周期', 18, '#596977')
    for item in nodes:
        ax.add_patch(FancyBboxPatch((item['x'], item['y']), item['w'], item['h'],
            boxstyle='round,pad=0,rounding_size=9', facecolor=item['fill'],
            edgecolor=item['color'], linewidth=1.2, zorder=2))
        cursor = item['y'] + PAD
        for text in item['title']:
            label(item['x'] + item['w'] / 2, cursor + item['title_line'] / 2,
                  text, item['title_px'], item['color'], owner=item)
            cursor += item['title_line']
        cursor += 8
        for text in item['body']:
            label(item['x'] + item['w'] / 2, cursor + 13.5, text, owner=item)
            cursor += 27
    for first, second in zip(chain, chain[1:]):
        line([(510, first['y'] + first['h']), (510, second['y'])])
    # Shared support bus supplies measurement, prediction, optimization and execution.
    line([(260, middle(reference)), (282, middle(reference))], SUPPORT, True, False)
    line([(282, middle(chain[1])), (282, middle(chain[4]))], SUPPORT, True, False)
    for item in chain[1:5]:
        line([(282, middle(item)), (310, middle(item))], SUPPORT, True)
    line([(260, middle(prevention)), (282, middle(prevention)),
          (282, middle(chain[5])), (310, middle(chain[5]))], SOURCE)
    # Adopted settings are not independent post-exposure overlay measurements.
    line([(710, middle(chain[4])), (752, middle(chain[4]))], EXECUTION)
    line([(864, executed['y']), (864, middle(chain[3])),
          (710, middle(chain[3]))], EXECUTION)
    # Process results feed estimation; the label also identifies parameter updates.
    line([(710, middle(chain[6])), (752, middle(chain[6]))], RESULT)
    line([(864, feedback['y']), (864, feedback['y'] - 24),
          (990, feedback['y'] - 24), (990, middle(chain[2])),
          (710, middle(chain[2]))], RESULT)
    legend_y = height - 83
    for x, text, color, dashed in [(90, '主线传递', MAIN, False),
            (365, '参考与模型支撑', SUPPORT, True), (700, '源头作用', SOURCE, False)]:
        line([(x, legend_y), (x + 40, legend_y)], color, dashed)
        label(x + 51, legend_y, text, 18, color, 'left')
    legend_y += 35
    for x, text, color in [(225, '执行侧反馈', EXECUTION), (565, '加工后反馈', RESULT)]:
        line([(x, legend_y), (x + 40, legend_y)], color)
        label(x + 51, legend_y, text, 18, color, 'left')
    fig.canvas.draw()
    renderer, failures, margins = fig.canvas.get_renderer(), [], []
    for artist, item in drawn_text:
        bounds = artist.get_window_extent(renderer).transformed(ax.transData.inverted())
        margins.append(min(bounds.x0 - item['x'], item['x'] + item['w'] - bounds.x1,
                           min(bounds.y0, bounds.y1) - item['y'],
                           item['y'] + item['h'] - max(bounds.y0, bounds.y1)))
        if (bounds.x0 < item['x'] + PAD - 1 or bounds.x1 > item['x'] + item['w'] - PAD + 1
                or min(bounds.y0, bounds.y1) < item['y'] + 7
                or max(bounds.y0, bounds.y1) > item['y'] + item['h'] - 7):
            failures.append(artist.get_text())
    if failures:
        raise ValueError(f'Text exceeds node padding: {failures}')
    for index, first in enumerate(nodes):
        for second in nodes[index + 1:]:
            assert not (max(first['x'], second['x']) < min(first['x'] + first['w'], second['x'] + second['w'])
                        and max(first['y'], second['y']) < min(first['y'] + first['h'], second['y'] + second['h'])), 'Overlapping nodes'
    for points in routes:
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            assert 0 <= min(x1, x2) <= max(x1, x2) <= WIDTH
            assert 0 <= min(y1, y2) <= max(y1, y2) <= height
            for item in nodes:
                horizontal_hit = (y1 == y2 and item['y'] < y1 < item['y'] + item['h']
                    and max(min(x1, x2), item['x']) < min(max(x1, x2), item['x'] + item['w']))
                vertical_hit = (x1 == x2 and item['x'] < x1 < item['x'] + item['w']
                    and max(min(y1, y2), item['y']) < min(max(y1, y2), item['y'] + item['h']))
                assert not (horizontal_hit or vertical_hit), 'Connector crosses a node'
    output = Path(__file__).with_suffix('.svg')
    fig.savefig(output, format='svg', metadata={'Date': None})
    output.write_text('\n'.join(row.rstrip() for row in output.read_text().splitlines()) + '\n')
    checks = dict(width=WIDTH, height=round(height, 2), nodes=len(nodes),
                  text_lines=len(drawn_text), text_overflow=failures,
                  body_font_px=19, main_title_font_px=23, layout_padding_px=PAD,
                  minimum_measured_text_margin_px=round(min(margins), 2),
                  overlapping_nodes=0, connector_node_crossings=0)
    if preview_dir:
        preview_dir = Path(preview_dir)
        preview_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(preview_dir / 'architecture.png', dpi=DPI)
        (preview_dir / 'layout-check.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2) + '\n')
    plt.close(fig)
    print(json.dumps(checks, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview-dir', type=Path)
    build(parser.parse_args().preview_dir)
