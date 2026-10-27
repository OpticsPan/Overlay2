# US20190041758A1 — Methods of determining a mechanical property of a layer applied to a substrate, control system for a lithographic apparatus and lithographic apparatus

原件：[PDF](original.pdf)；SHA-256 `8293b7e808d497bb5a8563e65ae2c8ad46fdaaa2f42cf2ac6730cd76734701ad`。物理页码从封面计1。

转换：本地MinerU 4.0.12，standard / auto；保留原语言。资料来源与文件校验值见[清单](../manifest.json)。机器输出未逐字校勘，关键文字、公式与图表回看原件。

校核提示（独立于机器提取正文）：[转换质量与已知问题](../QUALITY.md)。

<a id="p0001"></a>

## PDF第1页

[回看原页](original.pdf#page=1)

The OCR result should be empty, as the image contains only a stylistic horizontal line that must be ignored according to Rule 2. No text or placeholder characters should be output.

US 20190041758A1

(19) United States

(12) Patent Application Publication VAN DIJK et al.

(54) METHODS OF DETERMINING A MECHANICAL PROPERTY OF A LAYER APPLIED TO A SUBSTRATE, CONTROL SYSTEM FOR A LITHOGRAPHIC APPARATUS AND LITHOGRAPHIC APPARATUS

(71) Applicant: ASML NETHERLANDS B.V., Veldhoven (NL)

(72) Inventors: Leon Paul VAN DIJK, Eindhoven (NL); Mahdi SADEGHINIA, Eindhoven (NL); Richard Johannes Franciscus VAN HAREN, Waalre (NL); Ilya MALAKHOVSKY, Eindhoven (NL); Ronald Henricus Johannes OTTEN, Rosmalen (NL)

(73) Assignee: ASML NETHERLANDS B.V., Veldhoven (NL)

(21) Appl. No.: 16/039,073

(22) Filed: Jul. 18, 2018

(30) Foreign Application Priority Data
Aug. 1, 2017 (EP) ...... 17184214 (10) Pub. No.: US 2019/0041758 A1

(43) Pub. Date: Feb. 7, 2019

## Publication Classification

(51) Int. Cl.
G03F 7/20 (2006.01)
G03F 1/24 (2006.01)
G01L 5/00 (2006.01)

(52) U.S. Cl.
CPC ...... G03F 7/7065 (2013.01); G03F 7/70633 (2013.01); G01L 5/0047 (2013.01); G03F 1/24 (2013.01); G03F 7/70683 (2013.01)

## (57) ABSTRACT

A method for determining a mechanical property of a layer applied to a substrate and associated control system for controlling a lithographic process. The method includes obtaining measured out-of-plane deformation of the substrate, the out-of-plane deformation including deformation normal to a substrate plane defined by, or parallel to, a substrate surface. The measured out-of-plane deformation is fitted to a second order polynomial in two coordinates associated with the substrate plane and the mechanical property (e.g. anisotropic Young's moduli) of the layer is determined based on characteristics of the fitted second order polynomial. The mechanical property of the layer can be used to calibrate an in-plane distortion model of the substrate for predicting in-plane distortion based on the measured out-of-plane deformation.

![原件图像块，PDF第1页](figures/p0001-0001.png)

[回看原页](original.pdf#page=1)

<a id="p0002"></a>

## PDF第2页

[回看原页](original.pdf#page=2)

Patent Application Publication

Feb. 7, 2019 Sheet 1 of 4

US 2019/0041758 A1

![原件图像块，PDF第2页](figures/p0002-0002.png)

[回看原页](original.pdf#page=2)

<a id="p0003"></a>

## PDF第3页

[回看原页](original.pdf#page=3)

Patent Application Publication

Feb. 7, 2019 Sheet 2 of 4

US 2019/0041758 A1

![原件图像块，PDF第3页](figures/p0003-0003.png)

[回看原页](original.pdf#page=3)

Fig. 3

![原件图像块，PDF第3页](figures/p0003-0004.png)

[回看原页](original.pdf#page=3)

<a id="p0004"></a>

## PDF第4页

[回看原页](original.pdf#page=4)

Patent Application Publication

Feb. 7, 2019 Sheet 3 of 4

US 2019/0041758 A1

![原件图像块，PDF第4页](figures/p0004-0005.png)

[回看原页](original.pdf#page=4)

Fig. 5A

![原件图像块，PDF第4页](figures/p0004-0006.png)

[回看原页](original.pdf#page=4)

Fig. 5B

![原件图像块，PDF第4页](figures/p0004-0007.png)

[回看原页](original.pdf#page=4)

Fig. 6

<a id="p0005"></a>

## PDF第5页

[回看原页](original.pdf#page=5)

Patent Application Publication

Feb. 7, 2019 Sheet 4 of 4

US 2019/0041758 A1

![原件图像块，PDF第5页](figures/p0005-0008.png)

[回看原页](original.pdf#page=5)

Fig. 7

<a id="p0006"></a>

## PDF第6页

[回看原页](original.pdf#page=6)

US 2019/0041758 A1

Feb. 7, 2019

1

## METHODS OF DETERMINING A MECHANICAL PROPERTY OF A LAYER APPLIED TO A SUBSTRATE, CONTROL SYSTEM FOR A LITHOGRAPHIC APPARATUS AND LITHOGRAPHIC APPARATUS

[0001] This application claims the benefit of priority of European patent application no. 17184214, filed Aug. 1, 2017. The content of the foregoing application is incorporated herein in its entirety by reference.

## FIELD

[0002] The present disclosure relates to control apparatuses and control methods usable, for example, to maintain performance in the manufacture of devices by a patterning process, such as lithography. The present disclosure further relates to methods of manufacturing devices using lithographic techniques. The present disclosure further relates to computer program products for use in implementing such methods.

## BACKGROUND

[0003] A lithographic process is one in which a lithographic apparatus applies a desired pattern onto a substrate, usually onto a target portion of the substrate, after which various processing chemical and/or physical processing steps work through the pattern to create functional features of a complex product. The accurate placement of patterns on the substrate is a significant challenge for reducing the size of circuit components and other products that may be produced by lithography. In particular, the challenge of measuring accurately the features on a substrate which have already been laid down is a significant step in being able to position successive layers of features in superposition accurately enough to produce working devices with a high yield. So-called overlay should, in general, be achieved within a few tens of nanometers in, e.g., today's sub-micron semiconductor devices, down to a few nanometers in the most critical layers.

## SUMMARY

[0004] Consequently, modern lithography apparatuses involve extensive measurement or ‘mapping’ operations prior to the step of actually exposing or otherwise patterning the substrate at a target location. So-called advanced alignment models have been and continue to be developed to model and correct more accurately non-linear distortions of the substrate ‘grid’ that are caused by processing steps and/or by the lithographic apparatus itself.

[0005] Stress and in-plane distortions of the substrate can, in some cases, be determined via measurements of the shape (e.g., slope) of a clamped or unclamped substrate. Such in-plane distortions may result from one or more stress inducing layers being applied to the substrate. However, inaccuracies in such a determination may result from a failure to account for anisotropy in the stress (and therefore strain) induced by such stress inducing layers.

[0006] The present disclosure describes improved systems for control of performance in one or more parameters such as overlay in lithographic processes.

[0007] More specifically, the present disclosure describes improved measurement of in-plane distortion in a substrate.

[0008] According to an aspect, there is provided a method of determining a mechanical property of a layer applied to a substrate, the method comprising: measuring out-of-plane deformation of the substrate, the out-of-plane deformation comprising deformation normal to a substrate plane defined by, or parallel to, a substrate surface; fitting the measured out-of-plane deformation to a second order polynomial in two coordinates associated with the substrate plane; and determining the mechanical property of the layer based on characteristics of the fitted second order polynomial.

[0009] According to an aspect, there is provided a control system for controlling a lithographic process, the control system comprising: storage for receiving out-of-plane deformation data describing out-of-plane deformation of the substrate, the out-of-plane deformation comprising deformation normal to a substrate plane defined by, or parallel to, a substrate surface; and a processor operable to: fit the measured out-of-plane deformation to a second order polynomial in two coordinates associated with the substrate plane; determine the mechanical property of the layer based on characteristics of the fitted second order polynomial; and use the determined mechanical property of the layer to calibrate an in-plane distortion model operable to predict in-plane distortion based on measured out-of-plane deformation of the substrate.

[0010] According to an aspect, there is provided a lithographic apparatus including a control system as described herein.

[0011] According to an aspect, there is provided a computer program product containing one or more sequences of machine-readable instructions for implementing calculating steps in a method as described herein.

[0012] These and other aspects and advantages of the apparatus and methods disclosed herein will be appreciated from a consideration of the following description and drawings of exemplary embodiments.

## BRIEF DESCRIPTION OF THE DRAWINGS

[0013] Embodiments of the invention will now be described, by way of example only, with reference to the accompanying schematic drawings in which corresponding reference symbols indicate corresponding parts, and in which:

[0014] FIG. 1 depicts a lithographic apparatus suitable for use in an embodiment of the present invention;

[0015] FIG. 2 depicts a lithographic cell or cluster in which an inspection apparatus according to an embodiment of the present invention may be used;

[0016] FIG. 3 illustrates schematically measurement and exposure processes in the apparatus of FIG. 1;

[0017] FIG. 4 is a flow diagram describing a method of determining corrections for in-plane distortion of a substrate;

[0018] FIG. 5A is a representation of example Young's moduli of an isotropic stressed substrate;

[0019] FIG. 5B is a representation of example Young's moduli of an anisotropic stressed substrate as may be observed during production;

[0020] FIG. 6 is a flowchart describing a method according to an embodiment of the invention; and

[0021] FIG. 7 is a representation of an exemplary measured out-of-plane substrate shape corresponding to the Young's moduli depicted in FIG. 5B.

<a id="p0007"></a>

## PDF第7页

[回看原页](original.pdf#page=7)

US 2019/0041758 A1

Feb. 7, 2019

2

## DETAILED DESCRIPTION

[0022] Before describing embodiments of the invention in detail, it is instructive to present an example environment in which embodiments of the present invention may be implemented.

[0023] FIG. 1 schematically depicts a lithographic apparatus LA. The apparatus includes an illumination system (illuminator) IL configured to condition a radiation beam B (e.g., UV radiation or DUV radiation), a patterning device support or support structure (e.g., a mask table) MT constructed to support a patterning device (e.g., a mask) MA and connected to a first positioner PM configured to accurately position the patterning device in accordance with certain parameters; two substrate tables (e.g., a wafer table) WTa and WTb each constructed to hold a substrate (e.g., a resist coated wafer) W and each connected to a second positioner PW configured to accurately position the substrate in accordance with certain parameters; and a projection system (e.g., a refractive projection lens system) PS configured to project a pattern imparted to the radiation beam B by patterning device MA onto a target portion C (e.g., including one or more dies) of the substrate W. A reference frame RF connects the various components, and serves as a reference for setting and measuring positions of the patterning device and substrate and of features on them.

[0024] The illumination system may include various types of optical components, such as refractive, reflective, magnetic, electromagnetic, electrostatic or other types of optical components, or any combination thereof, for directing, shaping, or controlling radiation. For example, in an apparatus using extreme ultraviolet (EUV) radiation, reflective optical components will normally be used.

[0025] The patterning device support holds the patterning device in a manner that depends on the orientation of the patterning device, the design of the lithographic apparatus, and other conditions, such as for example whether or not the patterning device is held in a vacuum environment. The patterning device support can use mechanical, vacuum, electrostatic or other clamping techniques to hold the patterning device. The patterning device support MT may be a frame or a table, for example, which may be fixed or movable as required. The patterning device support may ensure that the patterning device is at a desired position, for example with respect to the projection system.

[0026] The term “patterning device” used herein should be broadly interpreted as referring to any device that can be used to impart a radiation beam with a pattern in its cross-section such as to create a pattern in a target portion of the substrate. It should be noted that the pattern imparted to the radiation beam may not exactly correspond to the desired pattern in the target portion of the substrate, for example if the pattern includes phase-shifting features or so called assist features. Generally, the pattern imparted to the radiation beam will correspond to a particular functional layer in a device being created in the target portion, such as an integrated circuit.

[0027] As here depicted, the apparatus is of a transmissive type (e.g., employing a transmissive patterning device). Alternatively, the apparatus may be of a reflective type (e.g., employing a programmable mirror array of a type as referred to above, or employing a reflective mask). Examples of patterning devices include masks, programmable mirror arrays, and programmable LCD panels. Any use of the terms “reticle” or “mask” herein may be considered synonymous with the more general term “patterning device.” The term “patterning device” can also be interpreted as referring to a device storing in digital form pattern information for use in controlling such a programmable patterning device.

[0028] The term “projection system” used herein should be broadly interpreted as encompassing any type of projection system, including refractive, reflective, catadioptric, magnetic, electromagnetic and electrostatic optical systems, or any combination thereof, as appropriate for the exposure radiation being used, or for other factors such as the use of an immersion liquid or the use of a vacuum. Any use of the term “projection lens” herein may be considered as synonymous with the more general term “projection system”.

[0029] The lithographic apparatus may also be of a type wherein at least a portion of the substrate may be covered by a liquid having a relatively high refractive index, e.g., water, so as to fill a space between the projection system and the substrate. An immersion liquid may also be applied to other spaces in the lithographic apparatus, for example, between the mask and the projection system. Immersion techniques are well known in the art for increasing the numerical aperture of projection systems.

[0030] In operation, the illuminator IL receives a radiation beam from a radiation source SO. The source and the lithographic apparatus may be separate entities, for example when the source is an excimer laser. In such cases, the source is not considered to form part of the lithographic apparatus and the radiation beam is passed from the source SO to the illuminator IL with the aid of a beam delivery system BD including, for example, suitable directing mirrors and/or a beam expander. In other cases the source may be an integral part of the lithographic apparatus, for example when the source is a mercury lamp. The source SO and the illuminator IL, together with the beam delivery system BD if required, may be referred to as a radiation system.

[0031] The illuminator IL may for example include an adjuster AD for adjusting the angular intensity distribution of the radiation beam, an integrator IN and a condenser CO. The illuminator may be used to condition the radiation beam, to have a desired uniformity and intensity distribution in its cross section.

[0032] The radiation beam B is incident on the patterning device MA, which is held on the patterning device support MT, and is patterned by the patterning device. Having traversed the patterning device (e.g., mask) MA, the radiation beam B passes through the projection system PS, which focuses the beam onto a target portion C of the substrate W. With the aid of the second positioner PW and position sensor IF (e.g., an interferometric device, linear encoder, 2-D encoder or capacitive sensor), the substrate table WTa or WTb can be moved accurately, e.g., so as to position different target portions C in the path of the radiation beam B. Similarly, the first positioner PM and another position sensor (which is not explicitly depicted in FIG. 1) can be used to accurately position the patterning device (e.g., mask) MA with respect to the path of the radiation beam B, e.g., after mechanical retrieval from a mask library, or during a scan.

[0033] Patterning device (e.g., mask) MA and substrate W may be aligned using mask alignment marks M1, M2 and substrate alignment marks P1, P2. Although the substrate alignment marks as illustrated occupy dedicated target portions, they may be located in spaces between target portions (these are known as scribe-lane alignment marks). Similarly,

<a id="p0008"></a>

## PDF第8页

[回看原页](original.pdf#page=8)

US 2019/0041758 A1

Feb. 7, 2019

3

in situations in which more than one die is provided on the patterning device (e.g., mask) MA, the mask alignment marks may be located between the dies. Small alignment marks may also be included within dies, in amongst the device features, in which case it is desirable that the markers be as small as possible and not require any different imaging or process conditions than adjacent features. The alignment system, which detects the alignment markers, is described further below.

[0034] The depicted apparatus could be used in a variety of modes. In a scan mode, the patterning device support (e.g., mask table) MT and the substrate table WT are scanned synchronously while a pattern imparted to the radiation beam is projected onto a target portion C (i.e., a single dynamic exposure). The speed and direction of the substrate table WT relative to the patterning device support (e.g., mask table) MT may be determined by the (de-) magnification and image reversal characteristics of the projection system PS. In scan mode, the maximum size of the exposure field limits the width (in the non-scanning direction) of the target portion in a single dynamic exposure, whereas the length of the scanning motion determines the height (in the scanning direction) of the target portion. Other types of lithographic apparatus and modes of operation are possible, as is well-known in the art. For example, a step mode is known. In so-called “maskless” lithography, a programmable patterning device is held stationary but with a changing pattern, and the substrate table WT is moved or scanned.

[0035] Combinations and/or variations on the above described modes of use or entirely different modes of use may also be employed.

[0036] Lithographic apparatus LA is of a so-called dual stage type which has two substrate tables WTa, WTb and two stations—an exposure station EXP and a measurement station MEA—between which the substrate tables can be exchanged. While one substrate on one substrate table is being exposed at the exposure station, another substrate can be loaded onto the other substrate table at the measurement station and various preparatory steps carried out. This enables a substantial increase in the throughput of the apparatus. On a single stage apparatus, the preparatory steps and exposure steps need to be performed sequentially on the single stage, for each substrate. The preparatory steps may include mapping the surface height contours of the substrate using a level sensor LS and measuring the position of alignment markers on the substrate using an alignment sensor AS. If the position sensor IF is not capable of measuring the position of the substrate table while it is at the measurement station as well as at the exposure station, a second position sensor may be provided to enable the positions of the substrate table to be tracked at both stations, relative to reference frame RF. Other arrangements are known and usable instead of the dual-stage arrangement shown. For example, other lithographic apparatuses are known in which a substrate table and a measurement table are provided. These are docked together when performing preparatory measurements, and then undocked while the substrate table undergoes exposure.

[0037] As shown in FIG. 2, the lithographic apparatus LA forms part of a lithographic cell LC, also sometimes referred to a lithocell or cluster, which also includes apparatuses to perform pre- and post-exposure processes on a substrate.

[0038] Conventionally these include one or more spin coaters SC to deposit resist layers, one or more developers DE to develop exposed resist, one or more chill plates CH and/or one or more bake plates BK. A substrate handler, or robot, RO picks up substrates from input/output ports I/O1, I/O2, moves them between the different process apparatuses and delivers then to the loading bay LB of the lithographic apparatus. These devices, which are often collectively referred to as the track, are under the control of a track control unit TCU which is itself controlled by the supervisory control system SCS, which also controls the lithographic apparatus via lithography control unit LACU. Thus, the different apparatus can be operated to maximize throughput and processing efficiency.

[0039] In order that the substrates that are exposed by the lithographic apparatus are exposed correctly and consistently, it is desirable to inspect exposed substrates to measure one or more properties such as overlay errors between subsequent layers, line thicknesses, critical dimensions (CD), etc. Accordingly a manufacturing facility in which lithocell LC is located also includes metrology system MET which receives some or all of the substrates W that have been processed in the lithocell. Metrology results are provided directly or indirectly to the supervisory control system SCS. If errors are detected, adjustments may be made to exposures of subsequent substrates.

[0040] Within metrology system MET, an inspection apparatus is used to determine the one or more properties of the substrates, and in particular, how the one or more properties of different substrates or different layers of the same substrate vary from layer to layer. The inspection apparatus may be integrated into the lithographic apparatus LA or the lithocell LC or may be a stand-alone device. To enable most rapid measurements, it may be desirable that the inspection apparatus measure one or more properties in the exposed resist layer immediately after the exposure. However, not all inspection apparatuses have sufficient sensitivity to make useful measurements of the latent image. Therefore measurements may be taken after the post-exposure bake step (PEB) which is customarily the first step carried out on exposed substrates and increases the contrast between exposed and unexposed parts of the resist. At this stage, the image in the resist may be referred to as semi-latent. It is also possible to make measurements of the developed resist image—at which point either the exposed or unexposed parts of the resist have been removed. Also, already exposed substrates may be stripped and reworked to improve yield, or discarded, thereby avoiding performing further processing on substrates that are known to be faulty. In a case where only some target portions of a substrate are faulty, further exposures can be performed only on those target portions which are good. The metrology step with metrology system MET can also be done after the resist pattern has been etched into a product layer. The latter possibility limits the possibilities for rework of faulty substrates but may provide additional information about the performance of the manufacturing process as a whole.

[0041] FIG. 3 illustrates steps to expose target portions (e.g. dies) on a substrate W in a dual stage apparatus such as depicted in FIG. 1. A typical process will be described first. The present disclosure is by no means limited to dual stage apparatus of the illustrated type. The skilled person will recognize that similar operations are performed in other

<a id="p0009"></a>

## PDF第9页

[回看原页](original.pdf#page=9)

US 2019/0041758 A1

Feb. 7, 2019

4

types of lithographic apparatus, for example those having a single substrate stage and/or having a metrology stage as described above.

[0042] On the left hand side within a dotted box are steps performed at measurement station MEA, while the right hand side shows steps performed at exposure station EXP. From time to time, one of the tables WTa, WTb will be at the exposure station, while the other is at the measurement station, as described above. For the purposes of this description, it is assumed that a substrate W has already been loaded into the exposure station. At step 200, a new substrate W' is loaded to the apparatus by a mechanism not shown. These two substrates are processed in parallel in order to increase the throughput of the lithographic apparatus.

[0043] Referring initially to the newly-loaded substrate W', this may be a previously unprocessed substrate, prepared with a new photoresist for first time exposure in the apparatus. In general, however, the lithography process described will be merely one step in a series of exposure and processing steps, so 'that substrate W' has been through this apparatus and/or other lithography apparatuses, one or more times already, and may have subsequent processes to undergo as well. Particularly for the problem of improving overlay performance, the task is to help ensure that new patterns are applied in exactly the correct position on a substrate that has already been subjected to one or more cycles of patterning and processing. Each patterning step can introduce positional deviations in the applied pattern, while subsequent processing steps progressively introduce distortions in the substrate and/or the pattern applied to it that must be measured and corrected for, to achieve satisfactory overlay performance.

[0044] The previous and/or subsequent patterning step may be performed in other lithography apparatuses, as just mentioned, and may even be performed in different types of lithography apparatus. For example, some layers in the device manufacturing process which are very demanding in one or more parameters such as resolution and overlay may be performed in a more advanced lithography tool than other layers that are less demanding. Therefore some layers may be exposed in an immersion type lithography tool, while others are exposed in a 'dry' tool. Some layers may be exposed in a tool working at DUV wavelengths, while others are exposed using EUV wavelength radiation. Some layers may be patterned by steps that are alternative or supplementary to exposure in the illustrated lithographic apparatus. Such alternative and supplementary techniques include for example imprint lithography, self-aligned multiple patterning and directed self-assembly. Similarly, other processing steps performed per layer (e.g., CMP and etch) may be performed on different apparatuses per layer.

[0045] At 202, alignment measurements using the substrate marks P1 etc. and image sensors (not shown) are used to measure and record alignment of the substrate relative to substrate table WTa/WTb. In addition, several alignment marks across the substrate W' will be measured using alignment sensor AS. These measurements are used in one embodiment to establish a substrate model (sometimes referred to as the "wafer grid"), which maps very accurately the distribution of marks across the substrate, including any distortion relative to a nominal rectangular grid.

[0046] At step 204, a map of substrate height (Z) against X-Y position is measured using the level sensor LS. Primarily, the height map is used to achieve accurate focusing of the exposed pattern. It may be used for other purposes in addition.

[0047] When substrate W' was loaded, recipe data 206 was received, defining the exposures to be performed, and also properties of the substrate and the patterns previously made and to be made upon it. Where there is a choice of alignment marks on the substrate, and where there is a choice of settings of an alignment sensor, these choices are defined in an alignment recipe among the recipe data 206. The alignment recipe therefore defines how positions of alignment marks are to be measured, as well as which marks.

[0048] At 210, substrates W' and W are swapped, so that the measured substrate W' becomes the substrate W entering the exposure station EXP. In the example apparatus of FIG. 1, this swapping is performed by exchanging the supports WTa and WTb within the apparatus, so that the substrates W, W' remain accurately clamped and positioned on those supports, to preserve relative alignment between the substrate tables and substrates themselves. Accordingly, once the tables have been swapped, determining the relative position between projection system PS and substrate table WTb (formerly WTa) is all that is necessary to make use of the measurement information 202, 204 (along with the recipe data marked as 208) for the substrate W (formerly W') in control of the exposure steps. At step 212, patterning device alignment is performed using the patterning device alignment marks M1, M2. In steps 214, 216, 218, scanning motions and radiation pulses are applied at successive target locations across the substrate W, in order to complete the exposure of a number of patterns.

[0049] By using the alignment data and height map obtained at the measuring station in the performance of the exposure steps, these patterns are accurately aligned with respect to the desired locations, and, in particular, with respect to features previously laid down on the same substrate. The exposed substrate, now labeled W" is unloaded from the apparatus at step 220, to undergo etching or other processes, in accordance with the exposed pattern.

[0050] Substrate distortion may impact overlay performance in a lithographic process. Substrate distortion may result from a thermal treatment of the substrate (e.g. laser anneal) or deposition of one or more stressed thin films. The free-form substrate shape, which may be measured with an off-line metrology tool, may change as a result of this distortion. Typical shapes which may be observed in high volume manufacturing are bowl (convex), umbrella (concave), and/or saddle shapes. Deviations from these shapes result in higher order in-plane distortions. In some cases, these in-plane distortions are slowly spatially varying functions that can be captured by existing alignment models, such as (for example) high order wafer alignment (HOWA) models. An important precondition is that the grid distortions remain global as the polynomial-based HOWA models become less effective for very local distortions. Moreover, alignment marks can get damaged during substrate processing. The resultant inaccuracy in the aligned positions when aligning to such damaged marks cause additional overlay penalties. These penalties become greater when higher-order substrate alignment models are used.

[0051] Another approach is to use substrate shape or deformation measurements. Such substrate shape measurements may comprise out-of-plane deformation measurements; i.e., measurements of the shape of the substrate in the

<a id="p0010"></a>

## PDF第10页

[回看原页](original.pdf#page=10)

US 2019/0041758 A1

Feb. 7, 2019

5

z-direction, normal to the plane of the main substrate surface. The substrate shape measurements may comprise measurements of the free-form (unclamped) substrate shape, or may be obtained from measurement of a clamped substrate. Any reference to the substrate shape encompasses any suitable measurement of the out-of-plane deformation of the substrate by any of these, or other, methodologies. Where the relationship between free-form substrate shape and in-plane distortion (IPD) after clamping is known or can be modelled, predictions (and corrections) can be made to improve overlay performance.

[0052] FIG. 4 conceptually illustrates such a method using a free-form substrate shape measurement according to an embodiment. Following a layer N exposure 405, the shape (out-of-plane deformation or distortion) of the substrate is measured 410. Subsequent to this, a stressor is applied to the substrate; for example an applied layer or thin film deposition 407. Thin film stress typically has an impact on the unclamped, free-form shape of the substrate. This stressor results in a change or distortion of the substrate shape. This distorted substrate is again measured 415. The difference 420 of the measured shape of this distorted substrate 415 and the shape of the substrate 410 before stressor application is determined, this difference 420 being the shape change due to stressor application. A prediction model 425 is then used to determine in-plane distortion (IPD) 430 from the measured shape change 420. Feed-forward corrections 440 for application of layer N+1 445 are determined from the determined in-plane distortion 430. These feed-forward corrections 440 can be used to correct substrate positioning during patterning of layer N+1 445 (and possibly other subsequent layers) on the substrate, thereby improving overlay.

[0053] A successful implementation of substrate-shape based feed forward overlay corrections has the IPD prediction model 425 provide accurate predictions of the actual distortions. Testing of the IPD prediction models in production settings have shown mixed results with regard to correlation between the measured overlay/alignment residuals and the substrate-shape based IPD predictions. One particular exemplary observation was that the predicted in-plane distortion comprised significant swirl patterns which were not observed in the corresponding measured overlay.

[0054] One possible root cause of this absence of correlation is that the IPD prediction model commonly assumes isotropic strain in the thin films applied to the substrate. However such an assumption may not be appropriate. Considering, for example, a typical 20-nm DRAM device pattern, and taking into account the orientation of the printed features and their material properties, it is highly unlikely that the applied film strain will be isotropic.

[0055] IPD prediction models which take into account anisotropic applied film strain have been proposed. The mechanical properties of both an isotropic and anisotropic stressor can be characterized by the Young's moduli and the orientation of main axes. This is illustrated in FIG. 5. FIG. 5A shows an assumed isotropic layer, where the Young's moduli $\mathrm{E}_x$ and $\mathrm{E}_y$ are identical (and aligned on the x/y grid). FIG. 5B shows an anisotropic layer as may actually be observed in a production environment. Here, the Young's moduli $\mathrm{E}_x$ and $\mathrm{E}_y$ are not equal in magnitude and their main axes have a different orientation relative to the isotropic example of FIG. 5A.

[0056] While a particular device pattern may dictate that the IPD prediction model should account for anisotropy in any applied layer, the parameters of the anisotropic applied film stress are not known, nor is there presently any method for determining these parameters without accurate knowledge of a stack of materials on a substrate. It may be possible to calculate these parameters from first principles. However, this would require very accurate knowledge of the stack, both according to design and also how it is actually realized on the substrate. This is cumbersome as separate calculations are involved for any layer/product that requires substrate-shape based overlay corrections and, should there be any changes in the stack, the corresponding calculation(s) would need to be redone following each change.

[0057] FIG. 6 is a flowchart of a method for empirically calibrating an IPD prediction model to account for anisotropic thin film stress, without the need for accurate stack knowledge. The method described in this Figure may comprise a refinement to the method illustrated in FIG. 4, for calibrating the IPD prediction model 425. As such, this method may be performed prior to the step of using the IPD prediction model 425 to determine in-plane distortion 430.

[0058] In a first step 600, the out-of-plane substrate shape is measured. This may be performed using any suitable method. For example, the difference of the measured shape of the free-form (i.e., unclamped) stressed substrate (with stressor, e.g., thin film applied) and the free-form unstressed (flat) substrate may be determined. As an alternative, the unstressed substrate may simply be assumed to be flat and only the stressed substrate measured. Other suitable methods for determining the substrate shape are equally possible, including those which measure the clamped substrate. This step may be the same as, or correspond to, steps 410 and 415 of FIG. 4.

[0059] At step 610, the second order content in the measured substrate shape is determined. This second order content may be found by fitting a second order function to the measured substrate shape data. The second order function may comprise a second order polynomial in two coordinates (x, y) associated with the plane of the substrate. More specifically, in an embodiment, the second order function may take the form of function S(x, y), where:

$$
S (x, y) = c _ {0 0} + c _ {1 0} x + c _ {0 1} y + c _ {2 0} x ^ {2} + c _ {1 1} x y + c _ {0 2} y ^ {2}
$$

[0060] At step 620, the orientation of the two main axes may be determined from the second order shape fit S(x,y). The second order shape fit S(x,y) is not symmetric such that the substrate is distorted more in a first direction than in a second, (e.g., perpendicular) direction. This can originate from anisotropic stress in the top layer, meaning that the Young's moduli are not equal in these directions. FIG. 7 shows an example representation of a substrate shape in the x and y directions (in the substrate plane) with the different shading illustrating variation in the z-direction (i.e., height variation). It can be seen that this height variation (warping) is essentially elliptical in shape, and as such the substrate is warped along two main axes tilted by an angle  $\alpha$  relative to the y axis. The orientation of the major/minor axes of this elliptical shape may be assumed to correspond with the main axes of the anisotropy being determined. In that Figure, the orientation of the two main axes relative to x and y axes can be clearly observed. In this specific illustrative example, the main axes have been rotated by an angle  $\alpha$  of about 36 degrees relative to the y axis. It will be readily apparent to

<a id="p0011"></a>

## PDF第11页

[回看原页](original.pdf#page=11)

US 2019/0041758 A1

Feb. 7, 2019

6

the skilled person that this orientation can be derived analytically from the fit parameters.

[0061] At step 630, once the orientation of the two main axes has been determined, the ratio of the magnitudes of the relevant mechanical property along the two directions, e.g., Young's moduli  $E_{x}$  and  $E_{y}$, can be derived (see FIG. 5B which corresponds to the shape illustrated in FIG. 7). A pure second order shape can only originate from a constant strain. The Young's moduli will not be equal, and therefore the stress in the layer will also be unequal in the two directions. By calculating the resulting substrate shape after applying a constant strain for the substrate (e.g., a constant strain for an applied film) using the anisotropic IPD model for different ratios of  $E_{x}$  to  $E_{y}$, the optimal  $E_{x}:E_{y}$  ratio can be determined. The  $E_{x}:E_{y}$  ratio may be considered optimal when the residual of the predicted second order substrate shape and the fitted second order shape to the measured data, i.e., S(x,y), is minimum. Therefore the Young's moduli  $E_{x}:E_{y}$  ratio may be determined by minimizing this residual substrate shape over different IPD model predictions corresponding to different ratios of  $E_{x}:E_{y}$, and selecting the ratio corresponding to this minimum residual.

[0062] With the orientation and the Young's moduli  $E_{x}:E_{y}$  ratio known, the anisotropic IPD prediction model is fully calibrated and characterized. At step 640, the full substrate shape is fed into the calibrated IPD model, and the in-plane distortion calculated (this step corresponding to step 430).

[0063] At step 650 (corresponding to step 440), feed-forward corrections are determined from the determined in-plane distortion. These feed-forward corrections can be used to correct substrate positioning during patterning of subsequent layers on the substrate.

[0064] It should be noted that only substrate shape data is used in this calibration. No information about the stack is required. Furthermore, the IPD model calibration described is not necessarily required for every substrate of a plurality of substrate. A device pattern can be the same for every substrate of the plurality of substrates and therefore the overall material properties will be substantially the same as well. Generally, the overall second order shape will be substantially identical for every substrate and it is mostly the deviation from the second order shape which causes substrate-to-substrate variation. Therefore the calibration (steps 610 to 630) may be performed on only a single substrate, and only once per product, with the resulting calibrated IPD model used for all subsequent substrates of that product.

[0065] Therefore in summary, an improved, more accurate substrate-shape based IPD prediction model is described in which the model is properly calibrated for anisotropy in a stressor applied to the substrate. This enables improved overlay corrections. In an embodiment, the empirical IPD model calibration requires only substrate shape data and overlay data from only one representative substrate only. In an embodiment, no details of the process stack is required in order to calibrate the IPD prediction model. In addition, substrate shape based IPD predictions can be used to enrich sparsely available overlay measurement data, such that a denser map of overlay data may be obtained (a method sometimes referred to as “hybrid-metrology” as both direct measurement data and indirectly derived data are combined). An example of such a method is described in PCT patent application publication no. WO 2017/144379 and U.S. patent application No. 62/459,327, incorporated herein by reference.

[0066] Further embodiments are disclosed in the list of numbered embodiments below:

1. A method for determining a mechanical property of a layer applied to a substrate, the method comprising: measuring out-of-plane deformation of the substrate, the out-of-plane deformation comprising deformation normal to a substrate plane defined by, or parallel to, a substrate surface; fitting the measured out-of-plane deformation to a second order polynomial in two coordinates associated with the substrate plane; and determining the mechanical property of the layer based on characteristics of the fitted second order polynomial.

2. A method according to embodiment 1, wherein determining the mechanical property of the layer comprises determining the magnitude of the mechanical property in a first direction relative to the magnitude of the mechanical property in a second direction, the second direction comprising at least a component which is perpendicular to the first direction.

3. A method according to embodiment 2, wherein the second direction is perpendicular to the first direction.

4. A method according to embodiment 2 or embodiment 3, wherein determining the magnitude of the mechanical property in a first direction relative to the magnitude of the mechanical property in a second direction comprises minimizing a difference between the fitted second order polynomial and a modelled substrate shape corresponding to application of a constant strain to the layer, for different ratios of the magnitude of the mechanical property in a first direction to the magnitude of the mechanical property in a second direction.

5. A method according to any of embodiments 2 to 4, further comprising determining an orientation of the first direction and/or the second direction; and using the determined orientation in the determining the mechanical property of the layer.

6. A method according to embodiment 5, wherein determining the orientation of the first direction and/or the second direction comprises determining the directions of the axes characterising the out-of-plane deformation.

7. A method according to embodiment 6, wherein the out-of-plane deformation substantially defines an elliptical shape in the substrate plane and the first direction and the second direction are defined by the directions of the major and minor axes of the elliptical shape.

8. A method according to any preceding embodiment, wherein the mechanical property of the layer comprises the Young's modulus of the layer.

9. A method according to any preceding embodiment, wherein the layer is an applied stressor layer which stresses and deforms the substrate.

10. A method according to any preceding embodiment, wherein the second order polynomial comprises the form $S(x,y) = c_{00} + c_{10}x + c_{01}y + c_{20}x^2 + c_{11}xy + c_{02}y^2$, where $x$ and $y$ are the two coordinates associated with the substrate plane.  
11. A method according to any preceding embodiment, comprising using the determined mechanical property of the layer to calibrate an in-plane distortion model operable to predict in-plane distortion based on a measured out-of-plane deformation of the substrate.

12. A method according to embodiment 11, wherein the method is performed and used to calibrate the in-plane distortion model only once based on measurement of out-of-plane deformation from only a single representative sub-

<a id="p0012"></a>

## PDF第12页

[回看原页](original.pdf#page=12)

US 2019/0041758 A1

Feb. 7, 2019

7

strate, the calibrated in-plane distortion model being used to predict in-plane distortion for subsequent substrates on which the same product structure is to be applied as that applied to the single representative substrate.

13. A method according to embodiment 11 or embodiment 12, comprising: using the in-plane distortion model to predict in-plane distortion based on measured out-of-plane deformation of the substrate; and using the predicted in-plane distortion to determine corrections for one or more subsequent production steps on the substrate.

14. A control system for controlling a lithographic process, the control system comprising: storage for receiving out-of-plane deformation data describing out-of-plane deformation of the substrate, the out-of-plane deformation comprising deformation normal to a substrate plane defined by, or parallel to, the substrate surface; and a processor operable to: fit the measured out-of-plane deformation to a second order polynomial in two coordinates associated with the substrate plane; determine the mechanical property of the layer based on characteristics of the fitted second order polynomial; and use the determined mechanical property of the layer to calibrate an in-plane distortion model operable to predict in-plane distortion based on measured out-of-plane deformation of the substrate.

15. A control system according to embodiment 14, wherein the processor is operable to determine the mechanical property of the layer by determining the magnitude of the mechanical property in a first direction relative to the magnitude of the mechanical property in a second direction, the second direction being perpendicular to the first direction.

16. A control system according to embodiment 15, wherein the second direction is perpendicular to the first direction.  
17. A control system according to embodiment 15 or embodiment 16, wherein the processor is operable to determine the magnitude of the mechanical property in a first direction relative to the magnitude of the mechanical property in a second direction by minimizing a difference between the fitted second order polynomial and a modelled substrate shape corresponding to application of a constant strain to the layer, for different ratios of the magnitude of the mechanical property in a first direction to the magnitude of the mechanical property in a second direction.

18. A control system according to any of embodiments 15 to 17, wherein the processor is operable to determine an orientation of the first direction and/or the second direction, and use the determined orientation in determining the mechanical property of the layer.

19. A control system according to embodiment 18, wherein the determination of the orientation of the first direction and/or the second direction comprises a determination of the directions of the axes characterising the out-of-plane deformation.

20. A control system according to embodiment 19, wherein the out-of-plane deformation substantially defines an elliptical shape in the substrate plane and the first direction and the second direction are defined by the directions of the major and minor axes of the elliptical shape.

21. A control system according to any of embodiments 14 to 20, wherein the mechanical property of the layer comprises the Young's modulus of the layer.

22. A control system according to any of embodiments 14 to 21, wherein the layer is an applied stressor layer which stresses and deforms the substrate.

23. A control system according to any of embodiments 14 to 22, wherein the second order polynomial comprises the form $S(x,y) = c_{00} + c_{10}x + c_{01}y + c_{20}x^2 + c_{11}xy + c_{02}y^2$, where $x$ and $y$ are the two coordinates associated with the substrate plane. 24. A control system according to any of embodiments 14 to 23, wherein the processor is operable to calibrate the in-plane distortion model only once based on measurement of out-of-plane deformation from only a single representative substrate, the control system being further operable to use the calibrated in-plane distortion model to predict in-plane distortion for subsequent substrates on which the same product structure is to be applied as that applied to the single representative substrate.

25. A control system according to any of embodiments 14 to 24, wherein the processor is further operable to: use the in-plane distortion model to predict in-plane distortion based on measured out-of-plane deformation of the substrate; and use the predicted in-plane distortion to determine corrections for one or more subsequent production steps on the substrate.

26. A lithographic apparatus comprising: the control system according to embodiment 25; and a patterning system being operable to form device features on the substrate in a patterning process using the determined corrections.

27. A computer program product containing one or more sequences of machine-readable instructions for implementing the steps of a method of any of embodiments 1 to 13.
28. A computer program product containing one or more sequences of machine-readable instructions for causing a processing device or system of processing devices to implement the control system of any of embodiments 14 to 25.

[0067] In association with the hardware of the lithographic apparatus and the lithocell LC, an embodiment may include a computer program containing one or more sequences of machine-readable instructions for causing the processors of the lithographic manufacturing system to implement methods of model mapping and control as described above. This computer program may be executed for example in a separate computer system employed for the image calculation/control process. Alternatively, the calculation steps may be wholly or partly performed within a processor a metrology tool, and/or the control unit LACU and/or supervisory control system SCS of FIGS. 1 and 2. There may also be provided a data storage medium (e.g., semiconductor memory, magnetic or optical disk) having such a computer program stored therein in non-transient form.

[0068] Although specific reference may have been made above to the use of embodiments of the invention in the context of optical lithography, it will be appreciated that embodiments of the invention may be used in other patterning applications, for example imprint lithography. In imprint lithography, topography in a patterning device defines the pattern created on a substrate. The topography of the patterning device may be pressed into a layer of resist supplied to the substrate whereupon the resist is cured by applying electromagnetic radiation, heat, pressure or a combination thereof. The patterning device is moved out of the resist leaving a pattern in it after the resist is cured.

[0069] The foregoing description of the specific embodiments will so fully reveal the general nature of the invention that others can, by applying knowledge within the skill of the art, readily modify and/or adapt for various applications such specific embodiments, without undue experimentation, without departing from the general concept of the present

<a id="p0013"></a>

## PDF第13页

[回看原页](original.pdf#page=13)

US 2019/0041758 A1

Feb. 7, 2019

8

invention. Therefore, such adaptations and modifications are intended to be within the meaning and range of equivalents of the disclosed embodiments, based on the teaching and guidance presented herein. It is to be understood that the phraseology or terminology herein is for the purpose of description by example, and not of limitation, such that the terminology or phraseology of the present specification is to be interpreted by the skilled artisan in light of the teachings and guidance.

[0070] The breadth and scope of the present invention should not be limited by any of the above-described exemplary embodiments, but should be defined only in accordance with the following claims and their equivalents.

1. A method comprising:

obtaining a measured out-of-plane deformation of a substrate, the out-of-plane deformation comprising deformation normal to a substrate plane defined by, or parallel to, a substrate surface;

fitting the measured out-of-plane deformation to a second order polynomial in two coordinates associated with the substrate plane; and

determining a mechanical property of a layer applied to the substrate based on characteristics of the fitted second order polynomial.

2. The method according to claim 1, wherein determining the mechanical property of the layer comprises determining the magnitude of the mechanical property in a first direction relative to the magnitude of the mechanical property in a second direction, the second direction comprising at least a component which is perpendicular to the first direction.

3. The method according to claim 2, wherein the second direction is perpendicular to the first direction.

4. The method according to claim 2, wherein determining the magnitude of the mechanical property in a first direction relative to the magnitude of the mechanical property in a second direction comprises minimizing a difference between the fitted second order polynomial and a modelled substrate shape corresponding to application of a constant strain to the layer, for different ratios of the magnitude of the mechanical property in a first direction to the magnitude of the mechanical property in a second direction.

5. The method according to claim 2, further comprising: determining an orientation of the first direction and/or the second direction; and

using the determined orientation in the determining the mechanical property of the layer.

6. The method according to claim 5, wherein determining the orientation of the first direction and/or the second direction comprises determining the directions of the axes characterizing the out-of-plane deformation.

7. The method according to claim 6, wherein the out-of-plane deformation substantially defines an elliptical shape in the substrate plane and the first direction and the second direction are defined by the directions of the major and minor axes of the elliptical shape.

8. The method according to claim 1, wherein the mechanical property of the layer comprises the Young's modulus of the layer.

9. The method according to claim 1, wherein the layer is an applied stressor layer which stresses and deforms the substrate.

10. The method according to claim 1, wherein the second order polynomial comprises the form $S(x,y) = c_{00} + c_{10}x +$ $c_{01}y+c_{20}x^{2}+c_{11}xy+c_{02}y^{2}$ , where x and y are the two coordinates associated with the substrate plane.

11. The method according to claim 1, comprising using the determined mechanical property of the layer to calibrate an in-plane distortion model configured to predict in-plane distortion based on a measured out-of-plane deformation of the substrate.

12. The method according to claim 11, wherein the method is performed and used to calibrate the in-plane distortion model only once based on measurement of out-of-plane deformation from only a single representative substrate, the calibrated in-plane distortion model being used to predict in-plane distortion for subsequent substrates on which the same product structure is to be applied as that applied to the single representative substrate.

13. The method according to claim 11, comprising:

using the in-plane distortion model to predict in-plane distortion based on measured out-of-plane deformation of the substrate; and

using the predicted in-plane distortion to determine corrections for one or more subsequent production steps on the substrate.

14. A control system for controlling a lithographic process, the control system comprising:

storage configured to receive out-of-plane deformation data describing out-of-plane deformation of the substrate, the out-of-plane deformation comprising deformation normal to a substrate plane defined by, or parallel to, the substrate surface; and

a processor system configured to:

fit the measured out-of-plane deformation to a second order polynomial in two coordinates associated with the substrate plane;

determine a mechanical property of a layer applied to the substrate based on characteristics of the fitted second order polynomial; and

use the determined mechanical property of the layer to calibrate an in-plane distortion model configured to predict in-plane distortion based on measured out-of-plane deformation of the substrate.

15. The control system according to claim 14, wherein the processor system is configured to determine the mechanical property of the layer by determining the magnitude of the mechanical property in a first direction relative to the magnitude of the mechanical property in a second direction, the second direction being perpendicular to the first direction.

16. The control system according to claim 15, wherein the processor system is configured to determine the magnitude of the mechanical property in a first direction relative to the magnitude of the mechanical property in a second direction by minimizing a difference between the fitted second order polynomial and a modelled substrate shape corresponding to application of a constant strain to the layer, for different ratios of the magnitude of the mechanical property in a first direction to the magnitude of the mechanical property in a second direction.

17. A lithographic apparatus comprising:

the control system according to claim 14; and

a patterning system configured to form device features on the substrate in a patterning process based an output from in-plane distortion model.

<a id="p0014"></a>

## PDF第14页

[回看原页](original.pdf#page=14)

US 2019/0041758 A1

9

Feb. 7, 2019

18. A computer program product containing one or more sequences of machine-readable instructions configured to cause a computer system to at least:

obtain out-of-plane deformation data of a substrate describing out-of-plane deformation of the substrate, the out-of-plane deformation comprising deformation normal to a substrate plane defined by, or parallel to, a substrate surface;

fit the measured out-of-plane deformation to a second order polynomial in two coordinates associated with the substrate plane; and

determine a mechanical property of a layer applied to the substrate based on characteristics of the fitted second order polynomial.

19. The computer program product of claim 18, wherein the instructions are further configured to cause the computer system to use the determined mechanical property of the layer to calibrate an in-plane distortion model configured to predict in-plane distortion based on measured out-of-plane deformation of the substrate.

20. The computer program product of claim 18, wherein the instructions are further configured to cause the computer system to use the in-plane distortion model to produce one or more corrections for use by a patterning system configured to form device features on the substrate in a patterning process based the one or more corrections.

\* \* \* \* \*

