# 转换检查记录（2026-11-09）

题名：On the Systematic Use of Budget-Based Design
作者：H.J.M. Freriks、W.P.M.H. Heemels、G.J. Muller、J.H. Sandee
原件：INCOSE 2006 会议论文，16个物理页，印刷页码788—803。
来源：OpticsPan/Overlay2，main在本次检查时的提交61883f6693a9edf02a54b9d563dd0a33463892c8。
上传时间：2026-11-09 09:06:32（Asia/Shanghai）；该提交只新增这一份PDF。
原件SHA-256：b5f559746fd8698e02eb88cdb39d71d03968a39f344127a7a3eab69cf6a3874f

## 转换方式
- 使用本机既有MinerU 4.0.12，standard档位，ocr_mode=auto，实际parse_mode=txt。
- 本地模型执行；未调用远程解析服务。image_analysis=False，保留原图，不生成图像解说。
- 保留英文机器正文。附加中文物理页入口、原PDF链接和来源说明；不静默改写机器正文。
- 本地保留机器结构及分析中间结果；仓库备份Markdown、图片、来源清单和本记录，不上传模型、缓存或运行日志。
- 依据用户本次补充的持续授权，将本批Markdown、5张图片及转换／质量记录纳入仓库备份；已有PDF保留原路径及字节。

## 完整性检查
- pypdf与pypdfium2独立读取原件均为16页；MinerU页面索引为连续的0—15。
- Markdown含16个物理页入口，各页均有正文；5个图片引用对应5个有效图像文件。
- 下载文件的Git blob SHA-1与GitHub返回值一致；交付原PDF与下载文件SHA-256一致。
- 首页题名、作者、会议日期及末页作者简介已与PDF文字层核对。

## 代表性抽查
- 物理第8页：对照原页图像，平方和公式4²+4²+2²=6²以及80 nm文字在Markdown中保留。
- 物理第9页图3：对照原页与MinerU裁切，套刻预算结构、箭头、80/60/30/12 nm及75 nrad等标注可辨认。
- 物理第13页图5：对照原页与MinerU裁切，功率曲线、坐标及红色平均值线保留；原图本身分辨率有限。

## 边界
- 未进行全文逐字校勘，页序和链接检查不代表文字识别准确率认证。
- 图内文字主要保存在图片中，不保证可通过Markdown正文搜索找到。
- 关键引文、技术数值与公式引用仍可通过每页原PDF链接复核。

[返回全文](mineru.md) · [原始PDF](../../patents/On%20the%20Systematic%20Use%20of%20Budget-Based%20Design.pdf) · [论文清单](../manifest.json)
