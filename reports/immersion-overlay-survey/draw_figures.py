"""Editable original technical diagrams, emitted as PNG and SVG.

Requires Pillow and a CJK font. Supply --font / --bold on non-Windows hosts.
No third-party figure is modified. Text boxes grow with measured line heights.
"""
import argparse
import html
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
NAVY, TEAL, GOLD, INK = "#16324f", "#087f8c", "#b67718", "#172e46"
MUTED, LINE, PALE, WHITE = "#52687d", "#98aabd", "#f2f6fa", "#ffffff"
ap = argparse.ArgumentParser()
ap.add_argument("--font", default="C:/Windows/Fonts/msyh.ttc")
ap.add_argument("--bold", default="C:/Windows/Fonts/msyhbd.ttc")
args = ap.parse_args()
fonts = {}


def font(size, bold=False):
    key = (size, bold)
    if key not in fonts:
        fonts[key] = ImageFont.truetype(args.bold if bold else args.font, size)
    return fonts[key]


class Canvas:
    def __init__(self, w, h, title, subtitle):
        self.w, self.h = w, h
        self.im = Image.new("RGB", (w, h), WHITE)
        self.dr = ImageDraw.Draw(self.im)
        self.svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
                    '<rect width="100%" height="100%" fill="white"/>']
        self.bounds = []
        self.text(42, 30, title, 38, NAVY, True)
        self.text(42, 88, subtitle, 23, MUTED)

    def rect(self, x, y, w, h, fill=PALE, stroke=LINE, radius=15, width=2):
        self.dr.rounded_rectangle((x,y,x+w,y+h), radius, fill, stroke, width)
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')

    def text(self, x, y, txt, size=26, color=INK, bold=False):
        f = font(size, bold)
        tw = self.dr.textlength(txt, font=f)
        bb = self.dr.textbbox((x,y), txt, font=f, anchor="lt")
        assert x >= 0 and y >= 0 and x+tw <= self.w-16 and bb[3] < self.h-12, (txt, bb)
        self.bounds.append({"text":txt, "bbox":list(bb)})
        self.dr.text((x,y), txt, fill=color, font=f, anchor="lt")
        self.svg.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="Microsoft YaHei,Noto Sans CJK SC,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" dominant-baseline="text-before-edge">{html.escape(txt)}</text>')

    def line(self, pts, color=LINE, width=3, arrow=False, dash=False):
        if dash:
            for (x1,y1),(x2,y2) in zip(pts,pts[1:]):
                length=math.hypot(x2-x1,y2-y1)
                for start in range(0,int(length),18):
                    t1,t2=start/length,min(start+10,length)/length
                    self.dr.line((x1+(x2-x1)*t1,y1+(y2-y1)*t1,x1+(x2-x1)*t2,y1+(y2-y1)*t2),color,width)
        else:
            self.dr.line(pts,color,width,joint="curve")
        self.svg.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="none" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="10 8"' if dash else '')+'/>')
        if arrow:
            (x0,y0),(x,y)=pts[-2:]
            angle=math.atan2(y-y0,x-x0)
            q=[(x,y),(x-14*math.cos(angle-.4),y-14*math.sin(angle-.4)),(x-14*math.cos(angle+.4),y-14*math.sin(angle+.4))]
            self.dr.polygon(q,fill=color)
            self.svg.append(f'<polygon points="{" ".join(f"{a},{b}" for a,b in q)}" fill="{color}"/>')

    def box(self, x, y, w, title, lines, color=TEAL, fill="#eff8f8", size=26, min_h=0):
        lh=39
        h=max(min_h, 70+lh*len(lines))
        self.rect(x,y,w,h,fill,color)
        assert self.dr.textlength(title,font=font(size,True)) <= w-44, title
        self.text(x+22,y+20,title,size,color,True)
        for i,s in enumerate(lines):
            assert self.dr.textlength(s,font=font(24)) <= w-44, s
            self.text(x+22,y+66+i*lh,s,24,INK)
        return (x,y,w,h)

    def dimension(self, x1,x2,y,label,color=INK):
        self.line([(x1,y),(x2,y)],color,2)
        for x in [x1,x2]:self.line([(x,y-10),(x,y+10)],color,2)
        length=self.dr.textlength(label,font=font(24))
        self.text((x1+x2-length)/2,y-37,label,24,color)

    def save(self, name):
        out=HERE/'figures';out.mkdir(exist_ok=True)
        self.im.save(out/f'{name}.png')
        (out/f'{name}.svg').write_text('\n'.join(self.svg+['</svg>'])+'\n',encoding='utf-8',newline='\n')
        return {"name":name,"size":[self.w,self.h],"text_items":len(self.bounds),"all_text_within_canvas":True}


def architecture():
    c=Canvas(1580,810,"图 0  从产品边缘要求到整机预算与验证","本文综合示意；箭头表示信息或校正的传递，不代表 ASML 内部软件结构。")
    c.box(42,170,390,"产品与层对",["电路类型、实际 CD / pitch","关键边缘间距与 EPE 限值","ADI / AEI、采样与统计量"],NAVY)
    c.box(590,170,390,"总体分配与模型",["DCO → MMO → 产品套刻","误差归属、均值、协方差","校正范围与校正后残差"],NAVY)
    c.box(1138,170,400,"量测与校准",["基准晶圆、对准标记","网格 / 物镜 / 热模型标定","采样覆盖与测量不确定度"],NAVY)
    c.line([(432,260),(590,260)],TEAL,4,True)
    c.line([(1138,260),(980,260)],TEAL,4,True)
    c.box(590,475,390,"机台执行",["运动台、对准、投影物镜","晶圆与掩模夹持 / 热管理","执行能力和在线补偿"],TEAL)
    c.box(1138,475,400,"验证与工艺反馈",["标准片 DCO / MMO","产品 ADI → AEI → EPE","跨批次漂移与模型复核"],TEAL)
    c.line([(785,357),(785,475)],TEAL,4,True)
    c.line([(980,560),(1138,560)],TEAL,4,True)
    c.line([(1338,475),(1338,357)],GOLD,4,True)
    c.text(1357,395,"反馈",23,GOLD)
    c.box(42,475,390,"L4 后续技术接口",["协方差识别、MA / MSD","像差敏感度、采样优化","测量偏差与工艺迁移"],GOLD,"#fff8e9")
    c.line([(432,560),(590,560)],GOLD,3,True)
    c.text(42,742,"输出：可追溯的预算表 + 物理责任边界 + 整机验收条件；不能只靠预算加总证明设备达标。",25,NAVY)
    return c.save('fig0-system-loop')


def geometry():
    c=Canvas(1580,1000,"图 1  节点名称、实际线宽与周期：三个不同层面","自绘概念图；几何数字仅作教学示例，不代表某一商业节点或芯片的真实设计。")
    c.box(42,155,468,"逻辑：CPU / GPU / ASIC",["逻辑单元、互连与嵌入式 SRAM","重点：栅 / 接触孔 / 金属层对"],NAVY)
    c.box(556,155,468,"DRAM：动态随机存储",["典型存储单元为 1T1C","重点：有源区、接触孔与电容"],TEAL)
    c.box(1070,155,468,"NAND：非易失存储",["存储串；3D NAND 沿高度堆叠","层数与横向线宽分别描述"],GOLD,"#fff8e9")
    c.text(42,342,"节点是工艺代际标识；先问电路和层，再问测量对象与真实尺寸。",29,NAVY,True)
    c.rect(42,412,925,402,PALE,LINE)
    c.text(66,435,"俯视：同一层的周期线 / 空图形",27,NAVY,True)
    for x in [140,400,660]:c.rect(x,540,156,165,"#9edbdc",TEAL,0)
    c.dimension(140,296,520,"CD = 24 nm",TEAL)
    c.dimension(296,400,746,"空隙 = 16",MUTED)
    c.dimension(140,400,790,"pitch = 40 nm",NAVY)
    c.text(65,858,"half-pitch = pitch / 2 = 20 nm",29,NAVY,True)
    c.text(65,912,"此例 CD 为 24 nm；只有 1:1 线 / 空时，CD 才等于半节距。",24,MUTED)
    c.rect(1010,412,528,402,PALE,LINE)
    c.text(1034,435,"截面：CD 还要注明高度",27,NAVY,True)
    polygon=[(1150,565),(1330,565),(1380,740),(1100,740)]
    c.dr.polygon(polygon,fill="#b7c8db",outline=NAVY)
    c.svg.append('<polygon points="1150,565 1330,565 1380,740 1100,740" fill="#b7c8db" stroke="#16324f"/>')
    c.dimension(1150,1330,540,"顶部 CD",NAVY)
    c.dimension(1100,1380,785,"底部 CD",NAVY)
    c.text(1034,854,"还需记录：ADI / AEI、材料层",25,MUTED)
    c.text(1034,900,"测量方向、高度、方法及算法",25,MUTED)
    return c.save('fig1-node-cd-pitch')


def epe():
    c=Canvas(1580,980,"图 2  套刻看相对位置，EPE 看具体边缘","一维几何示例：下层参考固定，上层中心右移 2 nm，同时线宽增加 4 nm；边缘误差按 +x 记号。")
    c.text(42,154,"A  中心位置读数（标记示意）",28,NAVY,True)
    c.text(830,154,"B  同样的中心位移，左右边缘结果不同",28,NAVY,True)
    c.rect(42,212,700,500,PALE,LINE)
    c.rect(830,212,708,500,PALE,LINE)
    c.text(74,240,"设计中心",24,NAVY)
    c.text(432,240,"实际中心",24,TEAL)
    c.rect(280,323,160,180,"#dce6f0",NAVY,0)
    c.rect(360,355,160,180,"#a4dddc",TEAL,0)
    c.line([(360,300),(360,610)],NAVY,3,dash=True)
    c.line([(440,300),(440,610)],TEAL,3,dash=True)
    c.dimension(360,440,652,"中心偏移 δx = +2 nm",TEAL)
    c.text(74,555,"中心读数不包含产品线宽变化",25,MUTED)
    # B uses common scale 20 px/nm: ideal [0,20], actual [0,24].
    c.text(860,240,"设计：CD = 20 nm",26,NAVY)
    c.rect(890,304,400,90,"#dce6f0",NAVY,0)
    c.text(860,429,"实际：CD = 24 nm；中心 +2 nm",26,TEAL)
    c.rect(890,488,480,90,"#a4dddc",TEAL,0)
    c.line([(890,286),(890,618)],NAVY,2,dash=True)
    c.line([(1290,286),(1290,618)],NAVY,2,dash=True)
    c.dimension(1290,1370,650,"右边缘 +4 nm",TEAL)
    c.text(860,650,"左边缘 0 nm",24,NAVY)
    c.box(42,762,700,"单条线的几何关系",["eL = δx − δCD / 2 = 0 nm","eR = δx + δCD / 2 = 4 nm"],NAVY)
    c.box(830,762,708,"产品评价还要增加",["局部边缘变化、工艺偏差及相关性","线 / 孔实际间隙或包围量的联合统计"],TEAL)
    return c.save('fig2-overlay-epe')


def budget():
    d=json.loads((HERE/'budget.json').read_text(encoding='utf-8'))['scenarios']
    r=json.loads((HERE/'calculations.json').read_text(encoding='utf-8'))['scenarios']
    def pair(group,key):return f"{d['A'][group][key]:.2f}  |  {d['B'][group][key]:.2f} nm"
    c=Canvas(1810,1340,"图 3  浸没式 ArF 套刻建议预算：1950i 水平与 1980Di 水平","A | B = NXT:1950i 历史基线 | NXT:1980Di；内部配额均为本文建议值，不是 ASML 披露值。")
    c.rect(42,140,1726,102,"#fff8e9",GOLD)
    c.text(64,158,"子项 u = 3σ，晶圆面单轴、曝光对之差、校正后残差；初始假设各桶不相关。",27,GOLD,True)
    c.text(64,201,"均值界 B 在各输出单列；Q = B + R，R = RSS(u)。厂家指标仅作为数值锚点，统计口径尚需对齐。",25,INK)
    c.text(42,280,"整机匹配输出",27,NAVY,True)
    c.text(600,280,"单机基线 + 新增匹配残差",27,NAVY,True)
    c.text(1200,280,"DCO：六类物理贡献",27,TEAL,True)
    # Trunks first, behind nodes. No summation label is attached to a bias term.
    c.line([(480,650),(540,650),(540,440),(600,440)],NAVY,3,True)
    c.line([(540,650),(540,1055)],NAVY,3)
    for y in [735,895,1055]:c.line([(540,y),(600,y)],NAVY,3,True)
    c.line([(1080,440),(1140,440),(1140,1094)],TEAL,3)
    c.line([(1140,440),(1140,394),(1200,394)],TEAL,3,True)
    for y in [534,674,814,954,1094]:c.line([(1140,y),(1200,y)],TEAL,3,True)
    c.box(42,520,438,"MMO 数值锚点",["≤ 5.50 | ≤ 2.50 nm","R = 5.022 | 2.203 nm","B = 0.35 | 0.20 nm","Q = 5.372 | 2.403 nm"],NAVY)
    c.text(60,797,"上层 RSS 只传递 R。",25,NAVY,True)
    c.text(60,842,"B 为该输出的总均值界，",25,MUTED)
    c.text(60,883,"不把下层 B 再加一遍。",25,MUTED)
    c.box(600,340,480,"DCO 数值锚点",["≤ 2.50 | ≤ 1.60 nm","R = 2.130 | 1.307 nm","B = 0.25 | 0.15 nm","Q = 2.380 | 1.457 nm"],NAVY)
    for y,title,key in [(680,"新增网格匹配残差","grid_matching"),(840,"新增物镜指纹差残差","lens_fingerprint"),(1000,"匹配设定 / 迁移残差","matching_setup")]:
        c.box(600,y,480,title,[pair('matching_increment_3sigma',key)],NAVY)
    for i,(title,key) in enumerate([('运动台定位','stage'),('晶圆 / 掩模对准','alignment'),('投影光学','optical_column'),('晶圆热 / 浸没扰动','wafer_heat_immersion'),('晶圆夹持','wafer_clamping'),('掩模夹持 / 热','reticle_clamp_heat')]):
        c.box(1200,340+i*140,568,title,[pair('dco_3sigma',key)],TEAL)
    c.rect(42,1195,1726,99,PALE,LINE)
    c.text(64,1213,"依据：六类物理分支参考 1950i 技术论文图 3；整机锚点来自 ASML 官方资料（正文表 1）。",25,NAVY)
    c.text(64,1255,"本图止于机台层；产品掩模、前道 / 刻蚀、EPE 与量测验收不确定度需另建边界，不是本图结果。",25,MUTED)
    # Confirm that hard-coded display rounding follows the independently recalculated values.
    assert f"{r['A']['mmo_Q']:.3f}" == '5.372' and f"{r['B']['dco_Q']:.3f}" == '1.457'
    return c.save('fig3-immersion-overlay-budget')


if __name__ == '__main__':
    summary=[architecture(),geometry(),epe(),budget()]
    (HERE/'figure-checks.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(summary,ensure_ascii=False))
