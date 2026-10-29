"""Render the approved R3 report narrative; this is not a machine control diagram.

Requires Matplotlib, fontconfig and Noto Sans CJK SC. SVG embeds glyph outlines.
Run with --preview-dir to save a PNG and measured layout checks outside the report.
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

DPI, WIDTH, PAD = 100, 1080, 20
BLUE, PURPLE, GREEN, GRAY = '#365E7A', '#716487', '#457763', '#747C85'
FONT_PATH = subprocess.check_output(
    ['fc-match', '-f', '%{file}', 'Noto Sans CJK SC'], text=True).strip()
METRICS = RendererAgg(WIDTH, 1800, DPI)


def font(px):
    return FontProperties(fname=FONT_PATH, size=px * 72 / DPI)


def width(text, px):
    return METRICS.get_text_width_height_descent(text, font(px), False)[0]


def wrap(text, available, px):
    lines = []
    for paragraph in text.split('\n'):
        current = ''
        for char in paragraph:
            if current and width(current + char, px) > available:
                lines.append(current)
                current = char
            else:
                current += char
        lines.append(current)
    return lines


def node(x, y, w, title, body, color=BLUE, fill='#EFF5F9',
         title_px=25, body_px=22, badge=None):
    titles = wrap(title, w - 2 * PAD, title_px)
    lines = wrap(body, w - 2 * PAD, body_px)
    header = 34 if badge else 0
    h = 2 * PAD + header + len(titles) * title_px * 1.4 + 12 + len(lines) * body_px * 1.45
    return dict(x=x, y=y, w=w, h=h, titles=titles, lines=lines,
                title_px=title_px, body_px=body_px, badge=badge, color=color, fill=fill)


def bottom(n):
    return n['y'] + n['h']


def cx(n):
    return n['x'] + n['w'] / 2


def build(preview_dir=None):
    l0 = node(40, 110, 1000, 'L0｜先看整机关系（第2章）',
              '量测与参考 → 预测 → 校正协调 → 执行 → 结果反馈\n关联校准支撑、源头措施与工艺评价')
    group_top = bottom(l0) + 62
    card_y = group_top + 100
    descriptions = [
        ('第4章', '量测与校准', '观测与参考\n是否可靠？'),
        ('第5章', '流程与\n控制协调', '数据与多路校正\n是否一致？'),
        ('第6章', '热管理', '掩模 · 物镜\n晶圆及相关边界'),
        ('第7章', '机械边界与\n参考稳定', '支撑／接口变化\n如何影响参考？'),
        ('第8章', '补偿执行与\n能力', '校正能否实现？\n有何附带影响？'),
    ]
    card_width, gap = 177.6, 16
    cards = [node(64 + i * (card_width + gap), card_y, card_width,
                  title, body, fill='white', title_px=22, body_px=19, badge=badge)
             for i, (badge, title, body) in enumerate(descriptions)]
    # Equal card heights and title areas preserve alignment without shrinking text.
    title_slots = max(len(n['titles']) for n in cards)
    for n in cards:
        n['titles'] += [''] * (title_slots - len(n['titles']))
        n['h'] = 2 * PAD + 34 + title_slots * 22 * 1.4 + 12 + max(len(c['lines']) for c in cards) * 19 * 1.45
    group = dict(x=40, y=group_top, w=1000, h=bottom(cards[0]) + 24 - group_top)
    bus_y = group_top + group['h'] + 26
    l2 = node(40, bus_y + 66, 1000, 'L2｜解释解决策略',
              '源头抑制／子系统补偿／二者结合\n说明选择理由、处理路径和剩余误差', PURPLE, '#F4F1F8')
    l3 = node(40, bottom(l2) + 46, 1000, 'L3｜解释子系统职责与能力',
              '测什么 → 算什么 → 调什么 → 怎样协同\n明确输入输出及量测、建模校准、执行、协同能力', PURPLE, '#F4F1F8')
    final_y = bottom(l3) + 76
    verification = node(40, final_y, 650, '回到整机验证｜第10章',
                        '各专题就近说明效果与局限，第10章统一评价\n区分模型结果、执行结果与工艺结果', GREEN, '#EEF6F1', 24, 21)
    l4 = node(730, final_y, 310, 'L4接口｜第9章',
              '登记待研究问题与证据入口\n当前不展开技术细节', GRAY, '#F5F6F7', 23, 20)
    nodes = [l0, *cards, l2, l3, verification, l4]
    height = max(bottom(n) for n in nodes) + 105
    fig, ax = plt.subplots(figsize=(WIDTH / DPI, height / DPI), dpi=DPI)
    fig.subplots_adjust(0, 0, 1, 1)
    fig.patch.set_facecolor('white')
    ax.set(xlim=(0, WIDTH), ylim=(height, 0))
    ax.axis('off')
    plt.rcParams['svg.fonttype'] = 'path'
    plt.rcParams['svg.hashsalt'] = 'overlay-r3-narrative-review'
    texts, routes = [], []

    def label(x, y, text, px=21, color='#273C4B', owner=None):
        a = ax.text(x, y, text, fontproperties=font(px), ha='center', va='center', color=color, zorder=4)
        texts.append((a, owner))

    def box(n, color=None, fill=None):
        ax.add_patch(FancyBboxPatch((n['x'], n['y']), n['w'], n['h'],
            boxstyle='round,pad=0,rounding_size=10', linewidth=1.25,
            edgecolor=color or n['color'], facecolor=fill or n['fill'], zorder=2))

    def route(points, color=BLUE, dashed=False, arrow=True):
        routes.append(points)
        style = (0, (4, 4)) if dashed else 'solid'
        if len(points) > 2:
            ax.plot(*zip(*points[:-1]), color=color, lw=1.5, linestyle=style, zorder=3)
        if arrow:
            ax.add_patch(FancyArrowPatch(points[-2], points[-1], arrowstyle='-|>',
                mutation_scale=14, lw=1.5, color=color, linestyle=style, shrinkA=0, shrinkB=0, zorder=3))
        else:
            ax.plot(*zip(*points[-2:]), color=color, lw=1.5, linestyle=style, zorder=3)

    label(540, 35, '总体叙述脉络', 30)
    label(540, 75, 'R3 · 问题归属与正文展开 · L4仅保留接口', 20, GRAY)
    box(group, BLUE, '#F5F8FB')
    label(540, group_top + 38, 'L1｜识别问题与管理归属（第3章）', 25, BLUE, group)
    label(540, group_top + 69, '先说明背景、产生位置、观测位置和协同关系，再进入对应专题', 21, owner=group)
    for n in nodes:
        box(n)
        y = n['y'] + PAD
        if n['badge']:
            label(cx(n), y + 11, n['badge'], 20, GRAY, n)
            y += 34
        for text in n['titles']:
            label(cx(n), y + n['title_px'] * 0.7, text, n['title_px'], n['color'], n)
            y += n['title_px'] * 1.4
        y += 12
        for text in n['lines']:
            label(cx(n), y + n['body_px'] * 0.725, text, n['body_px'], owner=n)
            y += n['body_px'] * 1.45
    route([(540, bottom(l0)), (540, group_top)])
    for n in cards:
        route([(cx(n), bottom(n)), (cx(n), bus_y)], arrow=False)
    route([(cx(cards[0]), bus_y), (cx(cards[-1]), bus_y)], arrow=False)
    route([(540, bus_y), (540, l2['y'])], PURPLE)
    label(770, bus_y + 34, '各专题章均按下方顺序展开', 20, PURPLE)
    route([(540, bottom(l2)), (540, l3['y'])], PURPLE)
    route([(cx(verification), bottom(l3)), (cx(verification), final_y)], GREEN)
    route([(cx(l4), bottom(l3)), (cx(l4), final_y)], GRAY, dashed=True)
    label(230, bottom(l3) + 40, '正文验证出口', 20, GREEN)
    label(754, bottom(l3) + 40, '后续专题', 20, GRAY)
    label(540, height - 65, '实线：叙述推进与章节展开     虚线：后续技术专题入口', 20, GRAY)
    label(540, height - 28, '本图表达报告组织逻辑；各专题可跨越多个L0功能环节。', 20, GRAY)

    fig.canvas.draw()
    renderer, overflows, margins, bounds_list = fig.canvas.get_renderer(), [], [], []
    for artist, owner in texts:
        if not artist.get_text():
            continue
        bounds = artist.get_window_extent(renderer).transformed(ax.transData.inverted())
        x0, x1 = bounds.x0, bounds.x1
        y0, y1 = sorted([bounds.y0, bounds.y1])
        bounds_list.append((artist.get_text(), (x0, y0, x1, y1)))
        assert 0 <= x0 < x1 <= WIDTH and 0 <= y0 < y1 <= height, 'Text outside canvas'
        if owner:
            margin = min(x0 - owner['x'], owner['x'] + owner['w'] - x1,
                         y0 - owner['y'], bottom(owner) - y1)
            margins.append(margin)
            if margin < PAD - 1:
                overflows.append(artist.get_text())
    assert not overflows, f'Text intrudes into padding: {overflows}'
    for i, first in enumerate(nodes):
        for second in nodes[i + 1:]:
            assert not (max(first['x'], second['x']) < min(first['x'] + first['w'], second['x'] + second['w'])
                        and max(first['y'], second['y']) < min(bottom(first), bottom(second))), 'Node overlap'
    for points in routes:
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            for n in nodes:
                hit_x = y1 == y2 and n['y'] < y1 < bottom(n) and max(min(x1, x2), n['x']) < min(max(x1, x2), n['x'] + n['w'])
                hit_y = x1 == x2 and n['x'] < x1 < n['x'] + n['w'] and max(min(y1, y2), n['y']) < min(max(y1, y2), bottom(n))
                assert not (hit_x or hit_y), 'Connector crosses node'
            for text, (tx0, ty0, tx1, ty1) in bounds_list:
                hit_x = y1 == y2 and ty0 < y1 < ty1 and max(min(x1, x2), tx0) < min(max(x1, x2), tx1)
                hit_y = x1 == x2 and tx0 < x1 < tx1 and max(min(y1, y2), ty0) < min(max(y1, y2), ty1)
                assert not (hit_x or hit_y), f'Connector crosses text: {text}'
    output = Path(__file__).with_suffix('.svg')
    fig.savefig(output, format='svg', metadata={'Date': None})
    output.write_text('\n'.join(s.rstrip() for s in output.read_text().splitlines()) + '\n')
    checks = dict(width=WIDTH, height=round(height, 2), nodes=len(nodes), topic_groups=1,
                  text_lines=len(bounds_list), text_overflow=overflows,
                  minimum_text_margin_px=round(min(margins), 2), overlapping_nodes=0,
                  connector_node_crossings=0, connector_text_crossings=0,
                  main_body_font_px=22, smallest_font_px=19)
    if preview_dir:
        preview_dir = Path(preview_dir)
        preview_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(preview_dir / 'narrative-logic.png', dpi=DPI)
        (preview_dir / 'layout-check.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2) + '\n')
    plt.close(fig)
    print(json.dumps(checks, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview-dir', type=Path)
    build(parser.parse_args().preview_dir)
