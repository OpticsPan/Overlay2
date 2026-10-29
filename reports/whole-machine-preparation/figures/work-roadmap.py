"""Render the proposed DUV preparation work and dependencies, not a machine diagram.

Requires Matplotlib, fontconfig, and Noto Sans CJK SC. The SVG embeds glyphs.
Run with --preview-dir to save a PNG and measured layout checks to ignored work/.
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

DPI, WIDTH, PAD = 100, 1080, 22
FONT = subprocess.check_output(['fc-match', '-f', '%{file}', 'Noto Sans CJK SC'], text=True).strip()
METRICS = RendererAgg(WIDTH, 2200, DPI)
BLUE, PURPLE, GREEN, GRAY, ORANGE = '#365E7A', '#716487', '#457763', '#747C85', '#906A3C'

def font(px):
    return FontProperties(fname=FONT, size=px * 72 / DPI)

def wrap(text, available, px):
    lines = []
    for paragraph in text.split('\n'):
        current = ''
        for char in paragraph:
            if current and METRICS.get_text_width_height_descent(current + char, font(px), False)[0] > available:
                lines.append(current)
                current = char
            else:
                current += char
        lines.append(current)
    return lines

def node(x, y, w, title, body, color=BLUE, fill='#EFF5F9', size=23):
    titles, lines = wrap(title, w-2*PAD, 25), wrap(body, w-2*PAD, size)
    h = 2*PAD + len(titles)*35 + 12 + len(lines)*size*1.45
    return dict(x=x, y=y, w=w, h=h, title=titles, lines=lines, color=color, fill=fill, size=size)

def bottom(n): return n['y']+n['h']
def cx(n): return n['x']+n['w']/2

def build(preview_dir=None):
    plt.rcParams.update({'svg.fonttype':'path', 'svg.hashsalt':'duv-preparation-v1'})
    a=node(100,112,880,'G0｜目标、现状和可追溯数据','A01—A03：评价口径 · 设备配置 · 坐标、历史与校正记录')
    b=node(100,bottom(a)+50,880,'G1｜可信观测与能力缺口','M01—M04／A04：校准参考 · 试验设计 · 主导问题与缺口')
    row=bottom(b)+90
    cards=[
        node(40,row,316,'物理边界','W01—W05\n台—晶圆热机械模型\n支撑、夹持与参考\n热分区及条件性浸没措施',size=21),
        node(382,row,316,'状态与热前馈','R01—R04／L01／H01—H02\n掩模 · 物镜 · 晶圆\n观测、仿真与在线预测\n各对象分别校准和验证',PURPLE,'#F4F1F8',21),
        node(724,row,316,'可用补偿能力','L02—L04／C01\n作用模式、范围与动态\n请求、约束及采用量\n按缺口比较候选操纵器',size=21),
    ]
    h=max(n['h'] for n in cards)
    for n in cards: n['h']=h
    note_y=bottom(cards[0])+24
    integrate=node(100,note_y+150,880,'G2—G3｜按所选问题完成控制整合','C02—C04：多环贡献 · 扫描作用 · 分组与层间窗口\nV03初版：上机前准备适用范围、异常处置与恢复规则',PURPLE,'#F4F1F8')
    verify=node(100,bottom(integrate)+50,880,'G3｜最小闭环与独立结果验证','V01—V02：重放／试验 → 预测 → 采用量 → 工艺结果\n先接通一个可辨、可测、可执行的问题，再逐步扩展',GREEN,'#EFF6F1')
    sustain=node(100,bottom(verify)+50,880,'G4｜跨工况确认与维护交接','V03：模型与配置版本 · 重新校准条件 · 能力恢复',GREEN,'#EFF6F1')
    nodes=[a,b,*cards,integrate,verify,sustain]
    height=bottom(sustain)+100
    fig,ax=plt.subplots(figsize=(WIDTH/DPI,height/DPI),dpi=DPI)
    fig.subplots_adjust(0,0,1,1);ax.set_xlim(0,WIDTH);ax.set_ylim(height,0);ax.axis('off')
    texts=[];routes=[]
    def label(x,y,text,px,color='#243D52',owner=None):
        artist=ax.text(x,y,text,ha='center',va='center',fontproperties=font(px),color=color)
        texts.append((artist,owner))
    def route(points,color=BLUE,arrow=True):
        routes.append(points)
        for i,(p,q) in enumerate(zip(points,points[1:])):
            if arrow and i==len(points)-2:
                ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=14,color=color,linewidth=1.5,shrinkA=0,shrinkB=0))
            else: ax.plot([p[0],q[0]],[p[1],q[1]],color=color,linewidth=1.5)
    label(540,36,'整机需要准备的工作',31)
    label(540,77,'DUV · 研发依赖与阶段出口 · 工程建议',20,GRAY)
    for n in nodes:
        ax.add_patch(FancyBboxPatch((n['x'],n['y']),n['w'],n['h'],boxstyle='round,pad=0,rounding_size=10',linewidth=1.5,edgecolor=n['color'],facecolor=n['fill']))
        y=n['y']+PAD
        for t in n['title']:
            label(cx(n),y+17.5,t,25,n['color'],n);y+=35
        y+=12
        for t in n['lines']:
            label(cx(n),y+n['size']*.725,t,n['size'],owner=n);y+=n['size']*1.45
    route([(540,bottom(a)),(540,b['y'])])
    bus=bottom(b)+45
    route([(540,bottom(b)),(540,bus)],arrow=False)
    route([(cx(cards[0]),bus),(cx(cards[-1]),bus)],arrow=False)
    for n in cards: route([(cx(n),bus),(cx(n),n['y'])])
    # A conditional-design note, visually separate from the required sequence.
    ax.add_patch(FancyBboxPatch((70,note_y),940,64,boxstyle='round,pad=0,rounding_size=8',edgecolor=ORANGE,facecolor='#FCF6ED',linewidth=1.2,linestyle='--'))
    label(540,note_y+32,'硬件改造按已证实缺口决定：RTS、热分区、dHDM等均须比选',21,ORANGE)
    # Routes use the external margins so they do not imply the note is mandatory.
    left,right=22,1058; join=note_y+110
    route([(cx(cards[0]),bottom(cards[0])),(cx(cards[0]),note_y-10),(left,note_y-10),(left,join),(540,join)],arrow=False)
    route([(cx(cards[-1]),bottom(cards[-1])),(cx(cards[-1]),note_y-10),(right,note_y-10),(right,join),(540,join)],arrow=False)
    # Middle branch joins through the same right margin above the conditional note.
    route([(540,bottom(cards[1])),(540,note_y-10),(right,note_y-10)],PURPLE,arrow=False)
    route([(540,join),(540,integrate['y'])],PURPLE)
    route([(540,bottom(integrate)),(540,verify['y'])],GREEN)
    route([(540,bottom(verify)),(540,sustain['y'])],GREEN)
    label(540,height-50,'箭头为工作依赖；分支可并行，最小闭环按问题选择接入。',20,GRAY)
    fig.canvas.draw();renderer=fig.canvas.get_renderer();margins=[];bounds=[]
    for t,n in texts:
        rect=t.get_window_extent(renderer).transformed(ax.transData.inverted());x0,x1=rect.x0,rect.x1;y0,y1=sorted([rect.y0,rect.y1])
        assert 0<=x0<x1<=WIDTH and 0<=y0<y1<=height,t.get_text()
        bounds.append((x0,y0,x1,y1,t.get_text()))
        if n:
            margin=min(x0-n['x'],n['x']+n['w']-x1,y0-n['y'],bottom(n)-y1);margins.append(margin);assert margin>=PAD-1,(t.get_text(),margin)
    for i,n in enumerate(nodes):
        for m in nodes[i+1:]:
            assert not(max(n['x'],m['x'])<min(n['x']+n['w'],m['x']+m['w']) and max(n['y'],m['y'])<min(bottom(n),bottom(m)))
    for points in routes:
        for (x1,y1),(x2,y2) in zip(points,points[1:]):
            for x0,y0,x3,y3,text in bounds:
                hit=(y1==y2 and y0<y1<y3 and max(min(x1,x2),x0)<min(max(x1,x2),x3)) or (x1==x2 and x0<x1<x3 and max(min(y1,y2),y0)<min(max(y1,y2),y3))
                assert not hit,text
    output=Path(__file__).with_suffix('.svg');fig.savefig(output,format='svg',metadata={'Date':None})
    output.write_text('\n'.join(line.rstrip() for line in output.read_text().splitlines())+'\n')
    checks={'width':WIDTH,'height':round(height,2),'nodes':len(nodes),'text_overflow':0,'minimum_text_margin_px':round(min(margins),2),'node_overlap':0,'connector_text_crossings':0,'smallest_font_px':20,'meaning':'Proposed work dependencies, not a physical system diagram'}
    if preview_dir:
        preview_dir=Path(preview_dir);preview_dir.mkdir(parents=True,exist_ok=True)
        fig.savefig(preview_dir/'work-roadmap.png',dpi=DPI)
        (preview_dir/'layout-check.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
    plt.close(fig);print(json.dumps(checks,ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--preview-dir',type=Path);build(p.parse_args().preview_dir)
