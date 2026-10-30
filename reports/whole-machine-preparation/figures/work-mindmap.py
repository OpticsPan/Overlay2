"""Render the report's task hierarchy as a readable, deterministic mind map.

Source: work-mindmap.json. Requires Matplotlib and Noto Sans CJK SC.
The SVG outlines glyphs; PNG provides a portable view. --preview-dir saves
measured layout checks to ignored work/. No patent image is changed.
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
from matplotlib.patches import FancyBboxPatch, PathPatch, FancyArrowPatch
from matplotlib.path import Path as MPath

DPI=100
HERE=Path(__file__).parent
FONT=subprocess.check_output(['fc-match','-f','%{file}','Noto Sans CJK SC'],text=True).strip()
METRICS=RendererAgg(1800,2200,DPI)
PALETTE={'blue':('#346180','#F0F6FA'),'purple':('#75608E','#F6F2F9'),'green':('#3E7765','#F0F7F3')}
INK='#223B50'
def font(px):return FontProperties(fname=FONT,size=px*72/DPI)
def width(s,px):return METRICS.get_text_width_height_descent(s,font(px),False)[0]
def build(preview_dir=None):
    data=json.loads((HERE/'work-mindmap.json').read_text())
    pad,body_size,title_size,line=24,26,29,44
    id_width=max(width(t[0],body_size) for g in data['groups'] for t in g['tasks'])+16
    card_width=max(480,max(width(g['title'],title_size)+2*pad for g in data['groups']),max(id_width+width(t[1],body_size)+2*pad for g in data['groups'] for t in g['tasks']))
    card_width=round(card_width+1)
    root_width,gap,margin=240,64,30
    W=2*card_width+root_width+2*gap+2*margin
    center=W/2
    nodes=[];y=128
    for row in range(4):
        gs=[g for g in data['groups'] if g['row']==row]
        heights=[2*pad+44+len(g['tasks'])*line for g in gs]
        row_height=max(heights)
        for g,h in zip(gs,heights):
            x=margin if g['side']=='left' else W-margin-card_width
            nodes.append(dict(g,x=x,y=y+(row_height-h)/2,w=card_width,h=h))
        y+=row_height+28
    footer=y+14;H=footer+155
    root=dict(x=center-root_width/2,y=(128+y-28)/2-96,w=root_width,h=192)
    fig,ax=plt.subplots(figsize=(W/DPI,H/DPI),dpi=DPI)
    fig.subplots_adjust(0,0,1,1);ax.set_xlim(0,W);ax.set_ylim(H,0);ax.axis('off')
    plt.rcParams.update({'svg.fonttype':'path','svg.hashsalt':'duv-preparation-mindmap-v1'})
    texts=[];curves=[];owners=nodes+[root];bboxes=[]
    def label(x,y,s,px,color=INK,ha='left',owner=None):
        a=ax.text(x,y,s,ha=ha,va='center',fontproperties=font(px),color=color,zorder=3)
        texts.append((a,owner));return a
    def box(n,edge,fill,radius=14):
        ax.add_patch(FancyBboxPatch((n['x'],n['y']),n['w'],n['h'],boxstyle=f'round,pad=0,rounding_size={radius}',edgecolor=edge,facecolor=fill,linewidth=1.6,zorder=2))
    label(center,42,data['title']+' · 思维导图',36,ha='center')
    label(center,88,data['subtitle'],23,'#687785',ha='center')
    for n in nodes:
        edge,fill=PALETTE[n['color']];left=n['side']=='left'
        start=(root['x'] if left else root['x']+root['w'],root['y']+root['h']/2)
        end=(n['x']+n['w'] if left else n['x'],n['y']+n['h']/2)
        dx=end[0]-start[0]
        path=MPath([start,(start[0]+dx*.65,start[1]),(end[0]-dx*.45,end[1]),end],[MPath.MOVETO,MPath.CURVE4,MPath.CURVE4,MPath.CURVE4])
        ax.add_patch(PathPatch(path,facecolor='none',edgecolor=edge,linewidth=1.7,alpha=.65,zorder=1));curves.append(path)
        box(n,edge,fill)
        label(n['x']+pad,n['y']+pad+17,n['title'],title_size,edge,owner=n)
        ax.plot([n['x']+pad,n['x']+n['w']-pad],[n['y']+pad+44]*2,color=edge,alpha=.2,lw=1,zorder=2)
        for i,(task,short) in enumerate(n['tasks']):
            ty=n['y']+pad+44+line*(i+.5)
            label(n['x']+pad,ty,task,body_size,edge,owner=n)
            label(n['x']+pad+id_width,ty,short,body_size,owner=n)
    box(root,'#274C67','#274C67',18)
    for i,s in enumerate(['整机套刻管理','研发准备']):label(center,root['y']+45+i*40,s,29,'white',ha='center',owner=root)
    label(center,root['y']+139,'基于R3研究',22,'#E1EBF2',ha='center',owner=root)
    label(center,footer,'推进顺序｜先取得可信证据，再逐步接通整机闭环',25,ha='center')
    stage_gap=30;sw=(W-2*margin-4*stage_gap)/5;sy=footer+30
    stage_nodes=[]
    for i,(sid,stitle) in enumerate(data['stages']):
        n=dict(x=margin+i*(sw+stage_gap),y=sy,w=sw,h=66);stage_nodes.append(n);box(n,'#9BADBA','#F7F9FB',9)
        label(n['x']+sw/2,sy+18,sid,22,'#346180',ha='center',owner=n)
        label(n['x']+sw/2,sy+46,stitle,22,ha='center',owner=n)
        if i<4:ax.add_patch(FancyArrowPatch((n['x']+sw+5,sy+33),(n['x']+sw+stage_gap-5,sy+33),arrowstyle='-|>',mutation_scale=13,color='#718696',lw=1.3))
    label(center,H-22,'连线表示任务归属；硬件按缺口比选，任务依赖与验收见正文。',22,'#687785',ha='center')
    fig.canvas.draw();renderer=fig.canvas.get_renderer();margins=[]
    for text,n in texts:
        bb=text.get_window_extent(renderer).transformed(ax.transData.inverted())
        x0,x1=bb.x0,bb.x1;y0,y1=sorted([bb.y0,bb.y1]);bboxes.append((x0,y0,x1,y1,text.get_text()))
        assert 0<=x0<x1<=W and 0<=y0<y1<=H,text.get_text()
        if n:
            m=min(x0-n['x'],n['x']+n['w']-x1,y0-n['y'],n['y']+n['h']-y1)
            assert m>=5,(text.get_text(),m);margins.append(m)
    for i,n in enumerate(owners):
        for m in owners[i+1:]:
            assert not(max(n['x'],m['x'])<min(n['x']+n['w'],m['x']+m['w']) and max(n['y'],m['y'])<min(n['y']+n['h'],m['y']+m['h']))
    for path in curves:
        # Sample cubic Bezier curves in data coordinates; no connector may cover text.
        a,b,c,d=path.vertices
        for i in range(301):
            t=i/300;p=(1-t)**3*a+3*(1-t)**2*t*b+3*(1-t)*t*t*c+t**3*d
            assert not any(x0<p[0]<x1 and y0<p[1]<y1 for x0,y0,x1,y1,_ in bboxes)
    tasks=[t[0] for g in data['groups'] for t in g['tasks']]
    assert len(tasks)==len(set(tasks))==30
    svg=HERE/'work-mindmap.svg';fig.savefig(svg,format='svg',metadata={'Date':None})
    svg.write_text('\n'.join(s.rstrip() for s in svg.read_text().splitlines())+'\n')
    fig.savefig(HERE/'work-mindmap.png',dpi=DPI)
    checks={'width':W,'height':H,'groups':len(nodes),'tasks':len(tasks),'text_overflow':0,'node_overlap':0,'connector_text_crossings':0,'minimum_text_margin_px':round(min(margins),2),'task_font_px':body_size,'task_font_at_840px_width':round(body_size*840/W,2),'smallest_font_px':22}
    if preview_dir:
        Path(preview_dir).mkdir(parents=True,exist_ok=True)
        (Path(preview_dir)/'layout-check.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
    plt.close(fig);print(json.dumps(checks,ensure_ascii=False))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--preview-dir',type=Path);build(p.parse_args().preview_dir)
