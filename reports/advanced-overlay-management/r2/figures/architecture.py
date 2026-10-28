"""Rebuild the report architecture SVG; requires Matplotlib and Noto Sans CJK SC."""
from pathlib import Path
import subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.font_manager import FontProperties
font_path = subprocess.check_output(['fc-match', '-f', '%{file}', 'Noto Sans CJK SC'], text=True).strip()
font=FontProperties(fname=font_path)
plt.rcParams['svg.fonttype']='path'
fig,ax=plt.subplots(figsize=(10,12)); fig.patch.set_facecolor('white');ax.set_xlim(0,100);ax.set_ylim(0,120);ax.axis('off')
def box(x,y,w,h,title,body,fill='#EEF4F8'):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.5,rounding_size=1.2',facecolor=fill,edgecolor='#496579',linewidth=1.3))
 ax.text(x+w/2,y+h-3.5,title,ha='center',va='center',fontproperties=font,fontsize=15,color='#16394B',weight='bold')
 ax.text(x+w/2,y+h/2-2,body,ha='center',va='center',fontproperties=font,fontsize=12,linespacing=1.6,color='#263A45')
def arr(points,color='#496579'):
 for a,b in zip(points[:-2],points[1:-1]): ax.plot([a[0],b[0]],[a[1],b[1]],color=color,lw=1.4)
 ax.add_patch(FancyArrowPatch(points[-2],points[-1],arrowstyle='-|>',mutation_scale=13,linewidth=1.4,color=color))
box(11,103,78,14,'目标、工艺背景与曝光准备','评价阶段 · 产品 / 设备路径 · 版图与成像模型','#E8EEF6')
box(11,82,36,15,'可信量测','对准 / 套刻 / 形状\n传感器、配方与数据质量')
box(53,82,36,15,'误差状态与校准','公共 / 局部 / 动态分量\n校准参考、模型与热历史')
box(11,58,78,16,'校正决策与协调','源头抑制或补偿 · 校正职责分配\n多路数据贡献分离 · 模型参数更新','#E8EEF6')
box(11,34,36,16,'源头抑制','热状态、支撑与夹持\n降低误差产生或变化')
box(53,34,36,16,'子系统补偿','平台轨迹、投影光学\n受执行范围与动态能力约束')
box(11,10,78,16,'曝光结果与验证','曝光 / 后续工艺 → 量测与残差评价\n更新校正、校准或模型参数','#EAF3EC')
arr([(29,103),(29,97)]);arr([(71,103),(71,97)])
arr([(47.5,89),(52.5,89)])
arr([(71,81.5),(71,74.5)]);arr([(29,81.5),(29,74.5)])
arr([(29,57.5),(29,50.5)]);arr([(71,57.5),(71,50.5)])
arr([(29,33.5),(29,26.5)]);arr([(71,33.5),(71,26.5)])
arr([(89.5,17),(96,17),(96,89),(89.5,89)],'#66846A')
ax.text(97,55,'验\n证\n反\n馈',fontproperties=font,fontsize=11,ha='center',va='center',color='#48674D',linespacing=1.5)
fig.subplots_adjust(0,0,1,1)
output = Path(__file__).with_suffix('.svg')
fig.savefig(output, format='svg')
output.write_text('\n'.join(line.rstrip() for line in output.read_text().splitlines()) + '\n')
plt.close(fig)
