# 光刻机套刻误差分配与建模控制文献调研报告

**文档定位**：面向光刻机总体工程、精密运动控制、光学像质补偿及晶圆厂先进过程控制（APC）团队的技术交接与研究路线参考文档。

## 1. 核心背景：从套刻误差预算（Overlay Budget）到边缘放置误差（EPE）

在先进集成电路制造中，套刻精度（Overlay）衡量硅片上下相邻图形层之间的平面位置对准误差，通常要求控制在最小特征尺寸（或半节距 Half-Pitch）的 $20\%$ 以内（[Advance Overlay Correction beyond 32nm DRAM Process](https://www.researchgate.net/publication/253248919_Advance_Overlay_Correction_beyond_32nm_DRAM_Process)）。随着工艺节点从 28 nm/14 nm 浸没式光刻（ArF Immersion）推进至 7 nm/5 nm 乃至 1.4 nm 极紫外光刻（0.33 NA 及 0.55 High-NA EUV），传统单一的套刻误差预算已演进为**边缘放置误差（Edge Placement Error, EPE）**框架下的多耦合预算管理（[Overlay deviation caused by mask heating during EUV exposure, SPIE 13687](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13687/136870K/Overlay-deviation-caused-by-mask-heating-during-EUV-exposure/10.1117/12.3072300.full)）。

### 1.1 EPE 与套刻误差的数学合成关系
根据 IMEC 与 ASML 在 7 nm 及以下节点建立的 EPE 预算准则（[Overlay and edge placement control strategies for the 7nm node using EUV and ArF lithography](https://www.researchgate.net/publication/280245696_Overlay_and_edge_placement_control_strategies_for_the_7nm_node_using_EUV_and_ArF_lithography)），图形边缘的实际偏移由全局套刻、局部定位偏差、关键尺寸（CD）误差及线宽粗糙度（LWR/LER）共同决定（[Metrology, Inspection, and Process Control XXXVIII, SPIE 12955](https://spie.org/Publications/Proceedings/Volume/12955)）：

$$\text{EPE}_{3\sigma} \approx \sqrt{\sigma_{\text{Overlay, Global}}^2 + \sigma_{\text{Placement, Local}}^2 + \left(\frac{\sigma_{\text{CD, Global}}}{2}\right)^2 + \left(\frac{\sigma_{\text{LWR/LCDU}}}{2}\right)^2}$$

在多重图形工艺（如 LELE、SADP/SAQP）及跨世代混用曝光（如 0.33 NA EUV、0.55 NA High-NA EUV 与 193i 浸没式混用）中，单机台套刻（Single Machine Overlay, SMO）与跨机台匹配套刻（Matched-Machine Overlay, MMO）指标已全面收紧至亚纳米至 $1.5\text{ nm}$ 量级。例如，ASML TWINSCAN NXT:2100i 的 SMO 指标已达 $0.9\text{ nm}$、MMO 达 $1.3\text{ nm}$（[Photolithography Explained: Contact Printing to DUV Immersion and Overlay](https://safeguard.sh/resources/blog/photolithography-explained-from-contact-printing-to-duv-immersion-multi-patterning-photoresists-and-overlay)），而 NXE:3600D EUV 系统的 MMO 指标已演进至 $1.1\text{ nm}$（[ASML EUV Update at SPIE](https://semiwiki.com/semiconductor-services/techinsights/314387-asml-euv-update-at-spie/)）。

### 1.2 全链路套刻误差预算树（Overlay Error Budget Tree）
学术界与工业界（ASML、Zeiss、KLA 及国内光电所、上海微电子等）通常将总套刻预算拆解为五大核心子系统分支：
1. **双工件台与掩模台同步运动误差（Stage Synchronization & Metrology）**：扫描过程中的低频移动平均误差（MA）、高频移动标准差（MSD）及六自由度激光干涉仪/光栅尺解算残差。
2. **投影物镜畸变与波前像差（Projection Lens Distortion & Aberration）**：静态场内畸变、奇次 Zernike 波前像差引起的图形位移（Pattern Shift）以及曝光热效应导致的动态透镜/反射镜畸变。
3. **掩模与防尘薄膜误差（Reticle & Pellicle Contribution）**：电子束掩模写入位置误差（RWE）、掩模装夹滑移与重力变形（[Reticle side wall clamping, TU/e](https://pure.tue.nl/ws/files/3578336/756525.pdf)）、防尘薄膜（Pellicle）应力畸变（[BACUS Newsletter July 2018, SPIE](https://spie.org/documents/Membership/BacusNewsletters/BACUS-Newsletter-July-2018.pdf)）以及 EUV 曝光掩模吸热膨胀。
4. **对准与套刻量测系统误差（Alignment & Overlay Metrology）**：对准标记工艺不对称性引起的晶圆诱导位移（WIS）、传感器工具诱导位移（TIS）（[Accuracy In Optical Overlay Metrology](https://semiengineering.com/accuracy-in-optical-overlay-metrology/)）及采样稀疏性残差。
5. **晶圆装夹与前道工艺形变（Wafer Geometry & Process Deformation）**：静电卡盘/真空卡盘装夹平面度误差（[SPIE Vol. 9424](https://spie.org/Publications/Proceedings/Volume/9424)）、薄膜沉积高低温应力引起的非线性面内变形（IPD）及刻蚀图形漂移（[Reducing the impact of etch-induced pattern shift on overlay, ResearchGate](https://www.researchgate.net/publication/315442219_Reducing_the_impact_of_etch-induced_pattern_shift_on_overlay_by_using_lithography_and_etch_tool_corrections)）。

## 2. 重点研究方向与代表性文献综述

### 2.1 方向一：整机套刻顶层架构、跨机台匹配（MMO）与对准系统综述
顶层误差分配的核心在于确定单机台基线误差（Baseliner）与跨机台/跨层匹配误差的边界，并明确对准系统的预算占比。

* **整机步进扫描预算奠基研究**：M. van den Brink 等人在早期步进扫描光刻机研发中，系统对比了离轴对准（Off-axis）与经物镜对准（TTL）、明场与暗场对准的误差传递特性，确立了步进扫描系统将总套刻预算分解至对准传感器、运动台与光学系统的经典工程范式（[Performance of a step-and-scan system for DUV lithography, SPIE Vol. 3051](https://www.researchgate.net/publication/241516869_Performance_of_a_step-and-scan_system_for_DUV_lithography)）。
* **对准系统与量产套刻控制综述**：国内学者针对先进节点对准与套刻难题发表了多篇系统性综述。邱俊等系统梳理了光刻对准技术从早期宽带明场向多波长衍射相位光栅（如 ASML 12 波长对准系统）演进的技术路径与抗工艺不对称机制（[光刻对准关键技术的发展与挑战, 《光学学报》 2023](https://www.researching.cn/ArticlePdf/m00006/2025/45/4/0405001.pdf)）；《光学学报（网络版）》2025 年封面文章进一步从量产视角剖析了对准/套刻标识细分、工艺与设备匹配误差以及三维堆叠器件微米尺度形变的系统分解与协同补偿策略（[光刻制造工艺：面向量产的对准套刻问题和技术, 《光学学报（网络版）》 2025](https://clp.ac.cn/M/News/Details?id=PT250705000006mJpLr)）。
* **EUV 与 ArF 浸没式跨机台匹配（MMO）分配**：在量产导入阶段，关键层在 EUV（如 NXE 系列）与 ArF 浸没式机台间混合曝光。研究表明，MMO 的核心瓶颈在于场内高阶残差与随机误差；通过引入 18 参数逐场校正（CPE, Correction Per Exposure）与掩模配准误差修正（RegC），可将跨世代机台匹配套刻控制在目标预算内（[Improvement of EUV mix-match overlay for production implementation](https://www.researchgate.net/publication/299644652_Improvement_of_EUV_mix-match_overlay_for_production_implementation)）。对于 0.33 NA 与 0.55 High-NA EUV 的混用，半场拼接区（In-die Stitching Area）的 $Y$ 向套刻误差成为预算分配的新焦点（[Overlay deviation caused by mask heating during EUV exposure, SPIE 13687](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13687/136870K/Overlay-deviation-caused-by-mask-heating-during-EUV-exposure/10.1117/12.3072300.full)）。

### 2.2 方向二：工件台与掩模台同步动态误差分配（MA/MSD 与干涉测量）
在步进扫描曝光过程中，掩模台与工件台需以比例速度（通常为 $4:1$ 或 High-NA 下的非对称比例）进行高速高加速同步扫描，加速度可达 $2g$ 以上，产生的反作用力高达 $5000\sim 10000\text{ N}$（[Position Control in Lithography Systems, IEEE Control Systems Magazine](https://www.scribd.com/document/972116626/Position-Control-in-Lithographic-Equipment)；[光刻机精密机电部件的调试与校准技术研究](https://www.researchgate.net/publication/403312741_guangkejijingmijidianbujiandediaoshiyuxiaozhunjishuyanjiu)）。

* **MA 与 MSD 的频域解耦与分配法则**：扫描狭缝内的瞬态位置同步误差 $e(t)$ 通过狭缝积分时间 $T = W_{\text{slit}} / v_{\text{scan}}$ 转化为两项核心指标（[Influence of the vibration of extreme ultraviolet lithographic tool, Optics Express 2023](https://opg.optica.org/abstract.cfm?uri=oe-31-14-22358)）：
  $$\text{MA}(t) = \frac{1}{T}\int_{t-T/2}^{t+T/2} e(\tau)\,d\tau, \quad \text{MSD}(t) = \sqrt{\frac{1}{T}\int_{t-T/2}^{t+T/2} \left[e(\tau) - \text{MA}(t)\right]^2 d\tau}$$
  文献通过傅里叶频域解析指出：**低频振动主要引起移动平均误差（MA），直接形成像面图形平移（即套刻误差）**；而**高频振动在狭缝窗口内相互抵消，对 MA 几乎无贡献，主要转化为恒定的移动标准差（MSD）**，导致空间像对比度下降、线宽（CD）漂移及线边缘粗糙度（LER）恶化（[Optics Express 2023](https://opg.optica.org/abstract.cfm?uri=oe-31-14-22358)）。
* **面向台振动的计算光刻协同优化（SMO/OPC）**：针对运动台物理抑制极限，近年研究提出将台同步误差（特别是 $0\sim 6\text{ nm}$ 范围的 MSD 波动）直接纳入光源-掩模联合优化（SMO）和光学邻近效应修正（OPC）代价函数中，在不牺牲工艺窗口（PW）的前提下放宽对机械台高频振动硬件指标的苛刻要求，实现“机械控制-计算光刻”的跨学科预算重分配（[Source and mask optimization for stability of reticle and wafer stages, Optics Express 2024](https://opg.optica.org/abstract.cfm?uri=oe-32-19-33603)；[Study on the imaging of bright-field and dark-field for contact holes, JVST B 2026](https://pubs.aip.org/avs/jvb/article/44/3/032601/3384787/Study-on-the-imaging-of-bright-field-and-dark)）。
* **六自由度双频激光干涉仪测量误差预算**：运动台位置闭环精度受限于位移测量系统。中国科学院光电技术研究所杜婧等详细拆解了光刻像质与畸变检测台中双频激光干涉仪的误差预算表（[光刻投影物镜畸变检测中的位移测量误差分析, 《光电工程》 2023](https://www.researching.cn/ArticlePdf/m00029/2023/50/2/220226.pdf)）：
  * **仪器误差合成（$3\sigma \approx 1.55\text{ nm}$）**：包含波长稳定性误差（$0.25\text{ nm}$）、电细分误差（$0.31\text{ nm}$）、光学非线性误差（$1.5\text{ nm}$）、数据采集误差（$0.01\text{ nm}$）及光束平行度误差（$0.04\text{ nm}$）。
  * **几何误差模型降维**：对比发现，未采用六自由度全局位置解算模型时，阿贝误差（Abbe Error）和余弦误差（Cosine Error）的 $3\sigma$ 分别高达 $1.2\text{ nm}$ 和 $5.5\text{ nm}$；引入六自由度解算与反射镜面形测校补偿后，阿贝误差降至 $0.25\text{ nm}$，余弦误差降至 $0.31\text{ nm}$，极大释放了整机定位预算压力（[光刻投影物镜畸变检测中的位移测量误差分析, 《光电工程》 2023](https://www.researching.cn/ArticlePdf/m00029/2023/50/2/220226.pdf)）。

### 2.3 方向三：光学波前像差、掩模畸变与热致套刻误差
光学与掩模子系统的套刻误差具有显著的**图形依赖性（Pattern Dependency）**和**时变热漂移特性**，无法仅靠常规晶圆线性对准消除。

* **波前像差诱导套刻误差（Aberration-Induced Overlay）**：投影物镜的波前像差通常用正交 Zernike 多项式表征。其中奇次像差（如彗差 Coma、三叶草像差 Trefoil）会破坏衍射光瞳的对称性，导致不同空间频率（Pitch）和不同特征图形产生非均匀的平面位置偏移。A. J. E. M. Janssen 等人建立了基于相移光栅（PSG）目标与 Zernike 灵敏度矩阵的晶圆级像差反演与套刻预测模型，通过曝光 420 组采样整个光瞳的 PSG 目标，利用最小二乘法精确分离出各阶 Zernike 系数对套刻误差的独立贡献（[Wafer-based aberration metrology for lithographic systems, Applied Optics 2014](https://opg.optica.org/abstract.cfm?uri=ao-53-12-2562)）。Yulu Chen 等人进一步针对 EUV 光刻开展了像差诱导套刻的整体分析与金属-通孔层（Metal-to-Via）边缘放置误差评估（[Holistic analysis of aberration induced overlay error in EUV lithography, SPIE 2018](https://www.researchgate.net/publication/323863217_Holistic_analysis_of_aberration_induced_overlay_error_in_EUV_lithography)；[Impact of aberrations in EUV lithography: metal to via EPE, SPIE 10583](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/10583/105830Q/Impact-of-aberrations-in-EUV-lithography--metal-to-via/10.1117/12.2299872.full)）。
* **掩模写入误差（RWE）与防尘薄膜（Pellicle）畸变**：Zeiss 与 ASML 联合研究利用 PROVE 193nm 光刻级掩模配准测量机与 BMMO 测试掩模，量化了电子束掩模写入误差（RWE）对晶圆对准标记位置及最终套刻的传递机制（[Proceedings of SPIE 11178, Zeiss 2019](https://asset-downloads.zeiss.com/catalogs/download/smt2/20a20e0a-dff8-4477-b03a-e1db12899c8c/vol11178pmj2019111780r_625586_0.pdf)）。同时，防尘薄膜（Pellicle）装夹及应力会引入显著的场内（Intra-field）非线性变形，若在离线掩模配准中忽略 Pellicle 贡献，会导致掩模级配准数据与晶圆级实测套刻失去相关性（[BACUS Newsletter July 2018, SPIE](https://spie.org/documents/Membership/BacusNewsletters/BACUS-Newsletter-July-2018.pdf)；[Mask contribution on CD and OVL errors budgets for double patterning lithography](https://www.researchgate.net/publication/224234268_Mask_contribution_on_CD_and_OVL_errors_budgets_for_double_patterning_lithography)）。
* **EUV 曝光掩模吸热实时变形（Mask Heating）**：在 EUV 曝光中，入射极紫外光被反射式掩模部分吸收，引起局部热量累积与瞬态热膨胀，产生实时面内位移（In-plane displacement）。2025 年最新 SPIE 论文专门分离并量化了 EUV 掩模热效应对套刻的独立贡献，指出传统基于曝光后晶圆量测的前馈补偿存在滞后与耦合偏差，必须建立独立的掩模热变形物理预测模型进行解耦补偿（[Overlay deviation caused by mask heating during EUV exposure, SPIE 13687](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13687/136870K/Overlay-deviation-caused-by-mask-heating-during-EUV-exposure/10.1117/12.3072300.full)）。

### 2.4 方向四：高阶套刻建模（HOWC/CPE）、晶圆几何形变与 APC 级联控制
当硬件原始误差无法进一步压缩时，套刻预算分配的核心转向**“可建模补偿项（Correctables）”与“不可校正残差（Uncorrectable Residuals）”**的划分（[SPIE Vol. 9424](https://spie.org/Publications/Proceedings/Volume/9424)）。

* **高阶场内/场间多项式与 Zernike-Legendre 级联建模**：传统 6 参数（平动、旋转、倍率）线性模型已无法应对 22 nm 以下节点的非线性网格扭曲。工业界广泛引入高阶晶圆与高阶视场模型（如 W3F3、区段对准 Zone Alignment 及逐场校正 CPE）（[High-Volume Manufacturing Device Overlay Process Control](https://semiengineering.com/high-volume-manufacturing-device-overlay-process-control/)；[Advance Overlay Correction beyond 32nm DRAM Process](https://www.researchgate.net/publication/253248919_Advance_Overlay_Correction_beyond_32nm_DRAM_Process)）。针对高阶多项式各阶项之间强相关性（High Correlation）导致 Lot-to-Lot APC 预测失稳的问题，学者提出了基于 **Zernike-Legendre 正交多项式的级联分析（Cascading Analysis）** 方法，按“线性项 $\rightarrow$ 高阶项”序列分步拟合与滤波，大幅降低了批次间模型系数的协方差波动，提升了量产 APC 稳定性（[High order overlay modeling and APC simulation with Zernike-Legendre polynomials, SPIE](https://www.researchgate.net/publication/283883365_High_order_overlay_modeling_and_APC_simulation_with_Zernike-Legendre_polynomials)）。
* **图案化晶圆几何形状（PWG）前馈与分组控制**：热退火、高应力薄膜沉积及晶圆装夹（Chucking）会引发弹性或塑性滑移线变形（[SPIE Vol. 9424](https://spie.org/Publications/Proceedings/Volume/9424)）。KLA 等团队提出利用图案化晶圆几何量测（Patterned Wafer Geometry, PWG）获取全晶圆局部曲率与应力分布，通过形状指标对晶圆进行聚类分组（Wafer Clustering），并将几何引起的面内位移直接前馈（Feed-forward）给光刻机高阶校正致动器，显著压缩了工艺诱导的套刻预算占比（[Metrology, Inspection, and Process Control for Microlithography XXXI, SPIE Vol. 10145](https://spie.org/Publications/Proceedings/Volume/10145)）。

### 2.5 方向五：套刻量测准确性（IBO vs. DBO）与工艺不对称误差分离
套刻量测系统自身的测量不确定度（通常要求占总套刻预算的 $10\% \sim 15\%$ 以内）直接决定了反馈控制的上限。

* **IBO 与 DBO/SCOL 技术路线演进**：李一鸣等在《激光与光电子学进展》特邀综述中系统对比了基于图像的套刻测量（IBO，如 Box-in-Box、AIM 标记）与基于衍射的套刻测量（DBO / $\mu$DBO / SCOL 散射测量）（[光刻套刻误差测量技术, 《激光与光电子学进展》 2022](https://www.researching.cn/ArticlePdf/m00002/2022/59/9/0922023.pdf)）。研究表明，DBO 通过检测预设偏置（$\pm d$）叠层光栅的 $\pm 1$ 阶衍射光强非对称性来解算位移，相比 IBO 具有更高的测量重复精度且更小占地面积（$\mu$DBO），已成为先进节点主流方案（[光刻套刻误差测量技术, 《激光与光电子学进展》 2022](https://www.researching.cn/ArticlePdf/m00002/2022/59/9/0922023.pdf)）。
* **标记不对称性（Target Asymmetry）诱导的量测失真**：在真实工艺中，CMP 抛光或刻蚀会导致底层光栅出现侧壁角不对称（SWA Asymmetry）、顶底倾斜或沟槽深度不均。这种结构非对称性会与真实的套刻位移信号混叠，在光瞳散射测量（Pupil Scatterometry）或明场成像中产生数纳米级的虚假套刻读数（且随晶圆位置动态变化，无法通过静态校准消除）（[Accuracy In Optical Overlay Metrology](https://semiengineering.com/accuracy-in-optical-overlay-metrology/)）。为此，研究界通过严格耦合波分析（RCWA）建立二维/三维周期结构全波电磁仿真模型，并结合多波长、多偏振角分辨光谱与光瞳景观指标（Pupil Landscape Metrics），实现工艺不对称噪声与真实套刻误差的解耦（[Accuracy In Optical Overlay Metrology](https://semiengineering.com/accuracy-in-optical-overlay-metrology/)；[基于二维周期结构衍射的套刻测量技术研究](https://www.opticsjournal.net/Articles/GetArticlePDF/OJ60a404ed4ed74cf3)；[套刻标记光学模型建立及性能参数仿真方法, 2025](https://www.researching.cn/ArticlePdf/m00006/2025/45/4/0405001.pdf)）。

## 3. 核心代表性文献汇总对比表

下表按研究模块整理了本报告调研的代表性中英文核心文献，供后续深入精读与模型复现使用：

| 研究模块 | 代表性论文 / 报告题目 | 作者 / 机构 / 来源 | 核心研究方法与预算分配贡献 |
| :--- | :--- | :--- | :--- |
| **顶层预算与整机架构** | [Performance of a step-and-scan system for DUV lithography](https://www.researchgate.net/publication/241516869_Performance_of_a_step-and-scan_system_for_DUV_lithography) | M. van den Brink 等 (ASML, SPIE Vol. 3051) | 奠定步进扫描光刻机顶层套刻误差预算拆解框架，对比 TTL 与离轴对准、明暗场对准的误差贡献。 |
| **EPE 与跨代匹配策略** | [Overlay and edge placement control strategies for the 7nm node using EUV and ArF lithography](https://www.researchgate.net/publication/280245696_Overlay_and_edge_placement_control_strategies_for_the_7nm_node_using_EUV_and_ArF_lithography) | Jan Mulkens 等 (ASML, SPIE) | 基于 10nm 实测数据外推 7nm 预算，建立多重图形与 EUV 单次曝光的 EPE 与高阶套刻分配准则。 |
| **EUV/ArF 混用匹配 (MMO)** | [Improvement of EUV mix-match overlay for production implementation](https://www.researchgate.net/publication/299644652_Improvement_of_EUV_mix-match_overlay_for_production_implementation) | SPIE Advanced Lithography | 评估 EUV 与 ArF 浸没式跨机台匹配套刻（MMO），验证 18 参数 CPE 与掩模配准修正（RegC）对随机与场内分量的抑制。 |
| **量产对准与套刻综述** | [光刻制造工艺：面向量产的对准套刻问题和技术](https://clp.ac.cn/M/News/Details?id=PT250705000006mJpLr) | 《光学学报（网络版）》2025 封面综述 | 系统梳理量产中对准/套刻标识细分、设备匹配误差、3D 器件微米级形变及 AI 赋能的套刻分解补偿框架。 |
| **运动台动态同步 (MA/MSD)** | [Influence of the vibration of extreme ultraviolet lithographic tool](https://opg.optica.org/abstract.cfm?uri=oe-31-14-22358) | Optics Express, Vol. 31(14), 2023 | 推导掩模台与工件台振动幅频特性与 MA/MSD 的解析关系，明确低频振动决定 MA（套刻）、高频振动决定 MSD（对比度/LER）。 |
| **台振动与计算光刻协同** | [Source and mask optimization for stability of reticle and wafer stages](https://opg.optica.org/abstract.cfm?uri=oe-32-19-33603) | Optics Express, Vol. 32(19), 2024 | 将运动台相对振动误差（MSD 0~6 nm）纳入 SMO 联合优化模型，实现机械控制预算与光学工艺窗口的跨层折中。 |
| **干涉仪六自由度误差分配** | [光刻投影物镜畸变检测中的位移测量误差分析](https://www.researching.cn/ArticlePdf/m00029/2023/50/2/220226.pdf) | 杜婧 等 (中科院光电所, 《光电工程》 2023) | 给出双频激光干涉仪仪器误差（$3\sigma=1.55\text{ nm}$）与几何误差预算详表，证明六自由度全局模型可将阿贝/余弦误差压缩一个量级。 |
| **波前像差诱导套刻** | [Wafer-based aberration metrology for lithographic systems using PSG targets](https://opg.optica.org/abstract.cfm?uri=ao-53-12-2562) | A. J. E. M. Janssen 等 (TU/e & ASML, Applied Optics 2014) | 构建 Zernike 波前像差到图形位移的灵敏度矩阵，利用 420 组相移光栅（PSG）最小二乘反演像差诱导套刻误差。 |
| **掩模写入与薄膜畸变** | [Mask-to-mask overlay compared to on-wafer scanner overlay measurements](https://asset-downloads.zeiss.com/catalogs/download/smt2/20a20e0a-dff8-4477-b03a-e1db12899c8c/vol11178pmj2019111780r_625586_0.pdf) | Zeiss & ASML (SPIE Vol. 11178, 2019) | 利用 PROVE 机台与 BMMO 掩模量化掩模写入误差（RWE）对晶圆对准标记及最终场内套刻的传递函数。 |
| **EUV 掩模热膨胀套刻** | [Overlay deviation caused by mask heating during EUV exposure](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13687/136870K/Overlay-deviation-caused-by-mask-heating-during-EUV-exposure/10.1117/12.3072300.full) | SPIE Vol. 13687, 2025 | 剥离并量化 EUV 曝光中掩模吸热膨胀引起的实时面内套刻漂移，剖析 High-NA 半场拼接区套刻分布。 |
| **高阶正交多项式与 APC** | [High order overlay modeling and APC simulation with Zernike-Legendre polynomials](https://www.researchgate.net/publication/283883365_High_order_overlay_modeling_and_APC_simulation_with_Zernike-Legendre_polynomials) | SPIE Advanced Lithography | 采用正交 Zernike-Legendre 多项式与级联分析（Cascading Analysis）消除高阶项共线性，提升 Lot-to-Lot APC 鲁棒性。 |
| **套刻量测综述与误差源** | [光刻套刻误差测量技术](https://www.researching.cn/ArticlePdf/m00002/2022/59/9/0922023.pdf) | 李一鸣 等 (《激光与光电子学进展》 2022) | 全面综述 DBO（$\mu$DBO/SCOL）与 IBO 测量原理、设备架构及标记工艺不对称性引起的量测误差抑制思路。 |

## 4. 工程落地方法论：套刻误差分配与仿真建模实施路线

基于上述文献调研，建议团队按以下四步开展光刻机套刻误差分配课题的立项与攻关：

### 4.1 第一步：建立时空频域解耦的混合误差合成律
摒弃简单的全随机平方和根（RSS）叠加，按误差的**空间尺度（Spatial Scale）**与**时间平稳性（Temporal Stability）**构建三级合成方程：
1. **系统可校正偏置（Systematic Correctables）**：包含掩模配准误差（RegC）、静态镜头畸变、晶圆一阶/高阶热膨胀。此类误差不直接计入最终残差预算，而是转化为**致动器行程预算（Actuator Stroke Budget）**与**建模拟合残差（Modeling Residual）**。
2. **场间（Inter-field）与场内（Intra-field）空间正交分解**：
   $$e_x(X, Y, x, y) = e_{\text{Inter}, x}(X, Y) + e_{\text{Intra}, x}(x, y) + \epsilon_{\text{unmodeled}}(X, Y, x, y)$$
   其中 $(X, Y)$ 为曝光场中心在晶圆坐标系下的坐标，采用高阶多项式或 Zernike 基函数展开；$(x, y)$ 为场内视场坐标（狭缝方向 $x$ 与扫描方向 $y$），采用 Legendre 多项式展开（[High order overlay modeling and APC simulation with Zernike-Legendre polynomials, SPIE](https://www.researchgate.net/publication/283883365_High_order_overlay_modeling_and_APC_simulation_with_Zernike-Legendre_polynomials)）。
3. **动态与随机残差合成（Covariance-Aware RSS）**：对统计独立的传感器底噪、运动台高频 MA 残差采用 RSS 合成；对具有物理同源性的强耦合项（如扫描加减速同时激发的掩模台俯仰与物镜框架微振动），引入协方差项 $2\text{Cov}(e_i, e_j)$。

### 4.2 第二步：典型先进浸没式/EUV 光刻机套刻预算拆解基准模板
在工程设计初期，可参考如下归一化占比结构建立顶层分配基准（具体数值依目标节点如 $\text{SMO} \le 1.0\text{ nm}$ 或 $\text{MMO} \le 1.5\text{ nm}$ 按比例缩放）：

* **双工件台与掩模台同步及测量子系统（占比约 $30\% \sim 35\%$）**：涵盖扫描段 MA 低频跟踪残差、干涉仪/光栅尺六自由度解算残差（阿贝、余弦、反射镜面形及环境折射率补偿残差）以及双台交换（Chuck-to-Chuck）底座匹配残差。
* **对准传感器与全晶圆网格建模子系统（占比约 $25\% \sim 30\%$）**：涵盖多波长对准传感器重复性、TIS/WIS 校准残差、高阶晶圆网格（HOWC）采样稀疏性带来的插值残差。
* **投影物镜与动态热像差子系统（占比约 $15\% \sim 20\%$）**：涵盖静态场内畸变补偿残差、奇次 Zernike 波前像差导致的跨节距图形位移（Pattern Shift）以及曝光过程中物镜吸热（Lens Heating）动态补偿残差。
* **掩模制造、装夹与热变形子系统（占比约 $10\% \sim 15\%$）**：涵盖掩模电子束写入残差（经 RegC 前馈后）、高速扫描下的掩模夹持微滑移（Slip）、防尘薄膜（Pellicle）重力/气流变形以及掩模热膨胀残差。
* **套刻量测与 APC 反馈环路不确定度（占比约 $10\% \sim 15\%$）**：涵盖 DBO/IBO 量测设备重复精度（TMU）及标记不对称性残差。

### 4.3 第三步：构建“机电-光学-控制”全链路蒙特卡洛（Monte Carlo）仿真平台
建议基于 Python 或 MATLAB 模块化搭建套刻误差分配验证平台，包含四个核心算子模块：
1. **运动台频域传递算子**：输入设定扫描速度 $v_{\text{scan}}$（如 $500\text{ mm/s}$）、狭缝宽度 $W_{\text{slit}}$（如 $1.8\text{ mm}$）及伺服控制闭环灵敏度函数，通过 $\text{sinc}(\pi \nu T)$ 滤波器计算各频段机械振动向 MA 和 MSD 的映射（[Optics Express 2023](https://opg.optica.org/abstract.cfm?uri=oe-31-14-22358)）。
2. **光学灵敏度映射算子**：导入 37 项或 64 项 Zernike 波前像差系数波动矩阵，乘以目标掩模图形的像差灵敏度向量（Aberration Sensitivity Vector），生成场内各视场点的图形位移向量（[Applied Optics 2014](https://opg.optica.org/abstract.cfm?uri=ao-53-12-2562)）。
3. **晶圆应力与装夹变形生成器**：使用有限元或高阶 Zernike 面内形变函数模拟前道沉积/刻蚀应力及卡盘吸附变形，叠加在对准标记位置上。
4. **高阶对准与 CPE 解算器**：模拟稀疏对准采样（如每晶圆选测 40~80 个点），执行 Zernike-Legendre 级联回归，分离出可由扫描台姿态微调和物镜致动器补偿的成分，输出最终全晶圆 $\text{Mean} + 3\sigma$ 套刻残差图（Wafer Vector Map）。

### 4.4 第四步：开展“精度-产能（WPH）-硬件成本”帕累托多目标优化
将套刻误差分配从静态表格升级为多目标优化问题：
* **对准采样点数 vs. 产能（WPH）折中**：增加晶圆对准标记采样数量能有效抑制高阶网格建模残差，但会延长晶圆测量台（Measure Stage）作业时间。通过仿真确定满足目标 $3\sigma$ 预算的最少采样点空间分布（Optimal Sampling Scheme）。
* **扫描速度/加减速曲线 vs. MA/MSD 折中**：降低扫描速度可减小同步跟踪误差，但直接牺牲曝光吞吐量（WPH）。结合 SMO/OPC 对 MSD 的容忍度提升（[Optics Express 2024](https://opg.optica.org/abstract.cfm?uri=oe-32-19-33603)），求解给定 WPH 约束下的最优扫描运动规划。
