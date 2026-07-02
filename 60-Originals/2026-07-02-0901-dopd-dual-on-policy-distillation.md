---
id: 2026-07-02-0901-dopd-dual-on-policy-distillation
type: source-original
title: DOPD：双策略在线蒸馏
original_title: 'DOPD: Dual On-policy Distillation'
source_name: huggingface-daily-papers
source_url: 'https://huggingface.co/papers/2606.30626'
author:
  - 'Xinlei Yu'
  - 'Gen Li'
  - 'Qingyi Si'
  - 'Guibin Zhang'
  - 'Yuqi Xu'
  - 'Congcong Wang'
  - 'Shuai Dong'
  - 'Kaiwen Tuo'
  - 'Xiangyu Zeng'
  - 'Kaituo Feng'
  - 'Qunzhong Wang'
  - 'Yang Shi'
  - 'Xiaobin Hu'
  - 'Xiangyu Yue'
  - 'Jiaqi Wang'
  - 'Shuicheng Yan'
published_at: 2026-06-29
fetched_at: '2026-07-02T09:12:56+08:00'
language: en
translated: true
translation_engine: haiku
word_count: 62676
images_attempted: 18
images_saved: 18
fallback_notice: null
related_daily: 2026-07-02
related_zettels: []
related_topics: []
tags:
  - 'source-original'
  - 'language-en'
---
# DOPD：双策略在线蒸馏

> 原文：[DOPD: Dual On-policy Distillation](https://huggingface.co/papers/2606.30626) · huggingface-daily-papers · 2026-06-29
> 抓取：2026-07-02T09:12:56+08:00 · 翻译：haiku · 62676 字

![图 1](_assets/2026-07-02/2026-07-02-0901-dopd-dual-on-policy-distillation-001.png)

![图 2](_assets/2026-07-02/2026-07-02-0901-dopd-dual-on-policy-distillation-002.png)

![图 3](_assets/2026-07-02/2026-07-02-0901-dopd-dual-on-policy-distillation-003.png)

![图 4](_assets/2026-07-02/2026-07-02-0901-dopd-dual-on-policy-distillation-004.png)

![图 5](_assets/2026-07-02/2026-07-02-0901-dopd-dual-on-policy-distillation-005.png)

![图 6](_assets/2026-07-02/2026-07-02-0901-dopd-dual-on-policy-distillation-006.png)

![图 7](_assets/2026-07-02/2026-07-02-0901-dopd-dual-on-policy-distillation-007.png)

![图 8](_assets/2026-07-02/2026-07-02-0901-dopd-dual-on-policy-distillation-008.png)

![图 9](_assets/2026-07-02/2026-07-02-0901-dopd-dual-on-policy-distillation-009.png)

![图 10](_assets/2026-07-02/2026-07-02-0901-dopd-dual-on-policy-distillation-010.png)

![图 11](_assets/2026-07-02/2026-07-02-0901-dopd-dual-on-policy-distillation-011.png)

![图 12](_assets/2026-07-02/2026-07-02-0901-dopd-dual-on-policy-distillation-012.png)

![图 13](_assets/2026-07-02/2026-07-02-0901-dopd-dual-on-policy-distillation-013.png)

![图 14](_assets/2026-07-02/2026-07-02-0901-dopd-dual-on-policy-distillation-014.png)

![图 15](_assets/2026-07-02/2026-07-02-0901-dopd-dual-on-policy-distillation-015.png)

![图 16](_assets/2026-07-02/2026-07-02-0901-dopd-dual-on-policy-distillation-016.png)

![图 17](_assets/2026-07-02/2026-07-02-0901-dopd-dual-on-policy-distillation-017.png)

![图 18](_assets/2026-07-02/2026-07-02-0901-dopd-dual-on-policy-distillation-018.png)

# DOPD：双策略在线蒸馏

Xinlei Yu

  
Gen Li

  
Qingyi Si

  
Guibin Zhang

  
Yuqi Xu

  
Congcong Wang

  
Shuai Dong

  
Kaiwen Tuo

  
Xiangyu Zeng

  
Kaituo Feng

  
Qunzhong Wang

  
Yang Shi

  
Xiaobin Hu

  
Xiangyu Yue

  
Jiaqi Wang

  
Shuicheng Yan

1 NUS  2 MMLab, CUHK  3 PKU  4 Explore Academy, JD

###### 摘要
策略在线蒸馏（OPD） offers superior capacity transfer by supervising 学生采样的轨迹 with dense token 级信号.
To furnish high-quality supervision sources and thereby elevate the performance frontier of distillation, an intuitive direction is to infuse 特权信息 to either teacher or student itself.
However, this additional input induces a potential failure mode we dub 特权幻觉: a pattern that conflates the 可转移的能力差距 that students are meant to close, and the 信息不对称差距 that can only be mimicked but never replicated.
This issue is further amplified by the inherent non-uniformity of token 级监督, where only a small subset of tokens carries pivotal capability-bearing signals.
To this end, we propose DOPD, an advantage-aware dual distillation paradigm that dynamically routes token 级监督 between privileged teacher and privileged student policies based on their 优势差距 and 相对概率.
Each token receives supervision of different strength, objective, and strategy from either teacher or student itself, which transfers credible capability while simultaneously receiving auxiliary signals, to alleviate 特权幻觉.
Extensive experiments on both 大语言模型 (LLM) and 视觉语言模型 (VLM) settings demonstrate that DOPD consistently outperforms Vanilla OPD and other counterparts. Further results on stability, robustness, continual learning, and 分布外 tasks validate its superiority.

Figure 1: Performance comparison of our DOPD with competing approaches across eight benchmarks in terms of average across all benchmarks (upper bigger bars) and individual values of each benchmark (lower small bars). 

## 
1 Introduction

Distillation, as a powerful paradigm for transferring the capabilities of a high-performing teacher policy into a suboptimal student policy, typically relies on off-policy trajectories, which may expose the student to state distributions that are misaligned with its own evolving behavior [18, 32, 13, 56, 52]. By contrast, recent OPD paradigms address this limitation by rolling out from the current student policy and using the teacher to provide token-level supervisory signals [23, 35, 42, 44]. This formulation not only mitigates distribution shift, but also delivers dense per-token teacher supervision via student-sampled on-policy trajectories, yielding higher distillation efficiency and superior performance.

Although OPD has emerged as an effective post-training paradigm, its achievable upper bound is fundamentally constrained by the quality of the supervision source [25, 7, 22]. As demonstrated in Figure 2, for standard strong-to-weak distillation [21, 23, 17, 60, 53, 51, 12, 40], the student is encouraged to imitate a stronger teacher; for self distillation [34, 15, 61, 30, 36], i.e., self-as-teacher pattern, the model improves by regularizing itself under different contexts or conditions.
In both cases, the effectiveness of OPD implicitly relies on the assumption: the supervision signals should reflect a learnable capability beyond the current student policy.
However, this assumption might be fragile [25, 35, 49], especially when 特权信息 is introduced.

特权信息, such as verified reasoning hints for LLMs [30, 61, 15, 49] or structured visual annotations for VLMs [57, 28], can indeed improve the prediction distribution of teacher policy and raise the apparent ceiling of distillation.
Nevertheless, the theoretical gains afforded by 特权信息 training do not necessarily translate into transferable supervisory signals. Rather, they may stem from a hitherto uncharacterized failure mode, i.e., 特权幻觉: the ostensible performance gap between teacher and student in fact conflates two fundamentally distinct components. The first is the intrinsic teacher-student capability gap, which is expected to close through distillation; the second is a gap driven by information asymmetry, which arises from the access to privileged inputs that remain almost unlearnable.
Indiscriminately distilling such a teacher distribution may therefore cause the student to fit privileged outcomes rather than acquire transferable ability.
To summarize, adding privileged inputs theoretically improves the ceiling, but the gains may stem from 特权幻觉 rather than capability optimization, resulting in rapid entropy collapse, reduced exploration, and ultimately poor distillation effectiveness.

As the distillation signals are highly non-uniform across tokens, the concern of privileged illusion becomes more pronounced.
For realistic trajectories, only a small subset of tokens may encode decisive branches, grounded evidence, critical preferences and other capacity-centric information [46, 18], while many others might provide low-value supervision, which might be privilege-dependent.
However, the vanilla and most variants of OPD methods often optimize all tokens with the same supervision source and objective form, implicitly assuming that each token contributes equally to capability transfer [23, 25, 35]. When incorporating privileged inputs, part of the teacher-student performance advantage originates from information gap rather than transferable capability. In this case, dense supervision might bias the student toward learning privilege-related shortcuts that are easier to fit than the underlying transferable capabilities, thereby amplifying the information-asymmetry component of the teacher-student gap.
Thus, indiscriminately and uniformly distilling all tokens from one monolithic policy might intensify the 特权幻觉.

Based on these insights, we propose an advantage-aware dual distillation paradigm, termed as DOPD, exploiting the complementary properties of teacher-based and self-based supervision under the privileged contexts to dynamically route token 级监督 between teacher and student policy according to the privilege 优势差距 and their relative predicted probabilities.
For tokens where the privileged teacher demonstrates a credible capability advantage, we apply stronger teacher distillation to transfer high-value privilege-conditioned capacity. As for tokens that are likely dominated by 特权信息 or less related to capacity, we instead rely on lighter supervision to preserve stability and encourage favorable exploration. In this way, dual distillation jointly adapts the supervision source, strength, and granularity, enabling more effective, stable, and adaptive distillation with less 特权幻觉.

Extensive experiments demonstrate that our method achieves superior distillation performance across a wide range of scenarios, and exhibits excellent robustness, scalability, and generalization.
Specifically, averaged across eight benchmarks, our method outperforms Vanilla OPD by 7.5 and 6.0 points on LLM-based and VLM-based setups respectively, and sustains consistent improvements ranging from 6.2-10.6 points across five model pairs of varying sizes.
Furthermore, our method also delivers more favorable performance in continual learning, 分布外 evaluation, and training stability. Additional token and divergence analyses, sensitivity and ablation studies further corroborate the effectiveness and rationality of our approach.

Figure 2: Comparison of existing (a) standard distillation, (b) self distillation, and (c) adaptive distillation paradigms with our proposed (d) dual distillation paradigm.

## 
2 Related Works

### 
2.1 Teacher-student Distillability

Teacher-student distillation has long been studied as a means of transferring capability from a stronger teacher to a weaker student model [20, 32, 55]. In the era of large models, teacher–student distillability has become a more nuanced question than mere teacher imitation: recent work shows that teachers can transfer not only labels, but also rationales, trajectories, preferences, and broader behavioral patterns to smaller students [13, 8, 1]. However, such transfer is not monotonic in teacher strength. Studies on the capacity gap suggest that an overly powerful teacher may provide signals that are difficult for a limited student to absorb [4, 26, 45].
Recently, some works also report this phenomenon on OPD settings, indicating that a more compatible initial distribution may be needed for better teacher-student distillation [25, 7, 22, 1].
Collectively, these studies suggest that effective distillation depends not only on a more powerful teacher model but also on the content and form of capacity being transferred.

### 
2.2 On-Policy Distillation

OPD has emerged as a compelling post-training paradigm that unifies the distributional consistency of on-policy learning with the dense supervision. As depicted in Figure 2, this field has evolved along three structured research directions:
(a) standard distillation, i.e., strong-to-weak paradigm, where a higher-capacity teacher model transfers knowledge to a weaker student via supervision on student-generated rollouts [1, 21, 23]. Recent efforts are primarily structural modifications to the baseline to enable more stable, faster or more effective: Veto [17], Fast OPD [60], OPCD [53], ExOPD [51], Uni-OPD [12], Lightning OPD [40], Vision-OPD [57], and VA-OPD [28].
(b) self distillation, repurposing a single model as both teacher and student under different context conditions, including: SDFT [34], SDPO [15], OPSD [61], PI-Distill [30], RLSD [49], and GATES [36].
(c) adaptive distillation, which dynamically modulates supervision strategy based on student state, or other training signals: EOPD [18], TA-OPD [38], TIP [46], REOPOLD [22], and TSD-KD [19].

Despite remarkable progress attained by such methods, they remain subject to fundamental limitations.
In Vanilla OPD, student performance is subject to an inherent theoretical ceiling dictated by the performance of teacher policy [35, 25, 23]. This constraint becomes particularly pronounced in challenging tasks, where the teacher itself exhibits subpar performance.
While several lines of research have made preliminary attempts to leverage 特权信息 [34, 49, 61, 15, 30, 36, 57, 28], these approaches generally operate under the implicit assumption that transferable capabilities can be enhanced via the direct integration of 特权信息, and the supervision signals should be received uniform distillation mechanisms consistently from monolithic source. Critically, these methods fundamentally overlook the risk of 特权幻觉, thus may fail to explicitly identify and distill genuine inherent capacity.

## 
3 Methodology

(a) Performance vs. Training Step

(b) Entropy vs. Training Step

Figure 3: Comparison of (a) performance and (b) entropy on OPD variants with 特权信息. Here, T., S., and Priv. denote teacher policy, student policy and with 特权信息, respectively.

### 
3.1 Background

#### 
3.1.1 特权幻觉

Existing OPD fundamentally relies on the assumption that a stronger teacher provides richer and more informative supervision [23, 21].
Thus, in many practical scenarios, an intuitive exploration is to equip teachers or student itself with privileged inputs [35].
For instance, verified hints in reasoning-centric tasks [61, 30, 15], or bounding boxes of objects in visual perception scenarios [28, 57].
Here, as exampled in Figure 11 and 12, we employ a moderate form of 特权信息 that delivers essential cues while refraining from directly disclosing detailed execution procedures and final answers (influence of various forms of 特权信息 will be discussed in Section 4.3.2).
However, when augmented with 特权信息, the prediction advantage may arise from information asymmetry rather than genuine inherent capability. Uncurated distilling such signals can encourage the student to imitate privileged outcomes instead of acquiring practical and transferable abilities, or triggers distillability due to irreparable teacher-student gap, leading to inferior and unstable distillation process, and unfavorable entropy collapse [6, 54].

As illustrated in Figure 3, we compare the impact of 特权信息 inclusion on both performance and entropy trends. We evaluate three OPD variants, in which 特权信息 is granted to the teacher policy only, the student policy only, and both policies, respectively. We observe that introducing 特权信息 to either the teacher or the student separately delivers modest performance improvements over Vanilla OPD in the very early training phase, yet the information asymmetry between the two policies gives rise to late-stage performance degradation coupled with entropy collapse.
When both policies are granted access to 特权信息, the superficial advantage conferred by information asymmetry vanishes. Furthermore, uniform distillation across all tokens under this setting fails to enable the student to genuinely internalize the core competencies. Instead, the student merely passively adapts to the 特权信息, ultimately yielding only marginal performance improvements less than Vanilla OPD.

In summary, the results reveal that straightforward incorporation of 特权信息 might create a failure phenomenon termed 特权幻觉: privileged inputs may yield an ostensible advantage, however, such gains often stem from information asymmetry rather than from a genuine enhancement of capability.

(a) Qwen3-8B Qwen3-1.7B (LiveBench)

(b) Qwen3-VL-8B Qwen3-VL-2B (MMStar)

Figure 4: Token ablations on random tokens, and tokens with high or low 优势差距.

#### 
3.1.2 Privilege 优势差距

As mentioned above, a key limitation of existing OPD methods is their inability to disentangle capability gaps from information gaps.
Thus, we argue that, when both with privileged inputs, the relative advantage between a teacher policy and a student policy offers a proxy for privilege-conditioned prediction gap. Consequently, a large 优势差距 indicates capability discrepancy under controlled privileged conditions, whereas a small gap suggests that the advantage of teacher policy is primarily attributable to 特权信息. This perspective motivates a privilege advantage-aware distillation paradigm that selectively transfers knowledge when the supervision signal reflects authentic competence rather than 特权幻觉.

For a given original input 𝐱\mathbf{x}, the student policy samples an output sequence from the conditional distribution.
To conduct privilege advantage-aware distillation, we aim to investigate the distribution disparity between the teacher policy ΠT\Pi_{T} and student policy ΠS\Pi_{S} when both have access to privileged inputs, termed the privilege 优势差距 𝒜\mathcal{A}. Then, we perform forward passes on the two policies respectively, and take the absolute value of their log-probability difference as the final privilege 优势差距:

𝒜=⋃log⁡ΠT​(𝐲n​\mid​𝐱,𝐩,𝐲&lt;n)−log⁡ΠS​(𝐲n​\mid​𝐱,𝐩,𝐲&lt;n)⋃=⋃log⁡ΠT​(𝐲n​\mid​𝐱,𝐩,𝐲&lt;n)ΠS​(𝐲n​\mid​𝐱,𝐩,𝐲&lt;n)⋃,\mathcal{A}=|\log\Pi_{T}\left(\mathbf{y}_{n}\mid\mathbf{x},\mathbf{p},\mathbf{y}_{&lt;n}\right)-\log\Pi_{S}\left(\mathbf{y}_{n}\mid\mathbf{x},\mathbf{p},\mathbf{y}_{&lt;n}\right)|=\left|\log\frac{\Pi_{T}\left(\mathbf{y}_{n}\mid\mathbf{x},\mathbf{p},\mathbf{y}_{&lt;n}\right)}{\Pi_{S}\left(\mathbf{y}_{n}\mid\mathbf{x},\mathbf{p},\mathbf{y}_{&lt;n}\right)}\right|,

(1)

where 𝐲n\mathbf{y}_{n} denotes the current token to be evaluated by the two policies, and 𝐩\mathbf{p} denotes the 特权信息 provided as auxiliary contexts along with previous tokens.
The quantity 𝒜\mathcal{A} captures the prediction discrepancy stemming from the performance gap between teacher and student policies under identical privileged conditions, which constitutes the idealized learning content.

To further verify the rationality of privilege 优势差距 to separate capacity and information gap, we conduct comprehensive ablation studies and empirical analyses across both large LLMs and VLMs. Specifically, we construct three variants of the Vanilla OPD paradigm, each discarding particular tokens without distillation loss: (1) a reference baseline that randomly drops 20% of tokens; (2) a variant that prunes the 20% of tokens with the smallest 优势差距; (3) a variant that prunes the 20% of tokens with the largest 优势差距.
As illustrated in Figure 4, ablating high-advantage tokens incurs substantial performance degradation and a marked reduction in distillation efficiency. At the 100th optimization step, removing high-advantage tokens achieves only approximately 50% of the performance gain obtained by Vanilla OPD. In contrast, pruning random or low-advantage tokens exerts negligible performance impact relative to the Vanilla OPD baseline. This performance disparity is even more pronounced in multimodal models, achieves only about 20% of the improvement achieved by Vanilla OPD. It is also noteworthy that despite underperforming relative to all counterparts, the variant with high-advantage tokens removed still yields tangible distillation gains by 3.4 and 1.5 points, indicating that the remaining tokens, though less critical, remain indispensable to distillation.

#### 
3.1.3 Takeaway

Based on these backgrounds, we summarize the following takeaway to support our proposed method:

### 
3.2 DOPD: Dual On-policy Distillation

#### 
3.2.1 Divergence

As discussed in prior work [15, 18, 25], to learn a student from a teacher under the OPD framework, we first consider three common divergence-based objectives derived from Kullback-Leibler (KL) divergence: forward KL, reverse KL, and Jensen-Shannon (JS) divergence. For notational simplicity, we omit the distinction between privileged and non-privileged observations and denote 𝐭\mathbf{t} as the current contexts of the teacher and student policies.

Forward KL Divergence.
It encourages the student to cover the full support of the teacher distribution by penalizing actions that receive non-negligible probability under the teacher but are underestimated by the student. As a result, this objective promotes comprehensive imitation of the action preferences of teacher:

KLforward(ΠT\|ΠS)=𝔼𝐲​ΠT​(\mid​𝐭)(logΠT​(𝐲​\mid​𝐭)ΠS​(𝐲​\mid​𝐭)⌋.KL_{\mathrm{forward}}\left(\Pi_{T}\,\middle\|\,\Pi_{S}\right)=\mathbb{E}_{\mathbf{y}\sim\Pi_{T}\left(\cdot\mid\mathbf{t}\right)}\left[\log\frac{\Pi_{T}\left(\mathbf{y}\mid\mathbf{t}\right)}{\Pi_{S}\left(\mathbf{y}\mid\mathbf{t}\right)}\right].

(2)

Reverse KL Divergence.
It encourages the student to concentrate probability mass on actions strongly favored by the teacher, while assigning little emphasis to low-probability regions of the teacher distribution. Such mode-seeking behavior often leads to sharper student policies, but may also discard informative secondary modes encoded by the teacher:

KLreverse(ΠS\|ΠT)=𝔼𝐲​ΠS​(\mid​𝐭)(logΠS​(𝐲​\mid​𝐭)ΠT​(𝐲​\mid​𝐭)⌋.KL_{\mathrm{reverse}}\left(\Pi_{S}\,\middle\|\,\Pi_{T}\right)=\mathbb{E}_{\mathbf{y}\sim\Pi_{S}\left(\cdot\mid\mathbf{t}\right)}\left[\log\frac{\Pi_{S}\left(\mathbf{y}\mid\mathbf{t}\right)}{\Pi_{T}\left(\mathbf{y}\mid\mathbf{t}\right)}\right].

(3)

JS Divergence.
It introduces an intermediate average distribution, and calculate the KL divergence of teacher and student relative to this medium, without directional bias in forward or reverse directions.
Their combination provides a more balanced optimization signal, thereby improving the stability of policy distillation:

J​S=12​K​L​(ΠT​\|​ΠM)+12​K​L​(ΠS​\|​ΠM),whereΠM=12​ΠT+12​ΠS.JS=\frac{1}{2}KL\left(\Pi_{T}\,\middle\|\,\Pi_{M}\right)+\frac{1}{2}KL\left(\Pi_{S}\,\middle\|\,\Pi_{M}\right),\text{where}\quad\Pi_{M}=\frac{1}{2}\Pi_{T}+\frac{1}{2}\Pi_{S}.

(4)

#### 
3.2.2 OPD

As a promising post-training paradigm, OPD holds its core advantage in performing knowledge transfer with samples drawn from the target student policy to effectively mitigate performance bias caused by distribution shift, and provide richer supervision signals than conventional reinforcement learning paradigms [23, 35, 25]. Specifically, given the student policy, for particular inputs 𝐱\mathbf{x}, it samples the sequence of predicted trajectory 𝐲​ΠS​(\mid​𝐱)\mathbf{y}\sim\Pi_{S}\left(\cdot\mid\mathbf{x}\right). Then, the teacher policy, typically a stronger model, will offer token 级信号 as optimization. Thus, the optimization objective of Vanilla OPD could be summarized as:

𝔼𝐱​𝒟(𝔼𝐲​ΠS(1⋃𝐲⋃\slimits@n=1⋃𝐲⋃ℒn(𝐲n;𝐭&lt;n)⌋⌋,\mathbb{E}_{\mathbf{x}\sim\mathcal{D}}\left[\mathbb{E}_{\mathbf{y}\sim\Pi_{S}}\left[\frac{1}{|\mathbf{y}|}\tsum\slimits@_{n=1}^{|\mathbf{y}|}\mathcal{L}_{n}\left(\mathbf{y}_{n};\mathbf{t}_{&lt;n}\right)\right]\right],

(5)

where 𝐭\mathbf{t} denotes the conditioning context, which comprises the original inputs, previously generated tokens, and auxiliary information if available, and ℒ\mathcal{L} quantifies the token-level divergence between the teacher and student policies. Conventionally, this penalty term takes the form of divergence-based objectives, e.g., widely adopted reverse KL, as well as alternative divergence variants or combinations thereof. Fundamentally, nearly all advancements in OPD center on minimizing the objective formalized in Equation 5, so as to yield a student model whose behavioral distribution aligns more closely with that of the teacher.

In addition, OPD approaches have different granularity of teacher supervision, ranging from coarse to fine: sampled-token, Top-K token, and full-vocabulary distillation.
Sampled-token distillation confines its distillation objective exclusively to the predicted target token, while Top-K token distillation expands the scope of supervision to cover the k tokens with the highest predictive probabilities.
By contrast, full-vocabulary distillation aligns the complete probability distribution across the entire vocabulary.
The density of informative supervisory signals increases monotonically, which theoretically leads to higher efficiency, however, this gain comes at the cost of higher computational overhead and potential risk of training instability, which stems from overfitting to the inherently noisy distributions of low-probability tokens [61, 25, 15].
Accordingly, the selection of distillation paradigm in practical deployment is typically tailored to specific downstream objectives and computational budgets.

Figure 5: Overview of our proposed DOPD.

#### 
3.2.3 Advantage-aware Dual Distillation

As discussed above in Section 3.1, not all tokens should receive supervision of identical objective and strength or from the same source.
When 特权信息 is introduced, the apparent superiority of teacher may originate either from privilege-conditioned capability discrepancy or from information asymmetry.
Therefore, indiscriminately distilling the privileged teacher distribution may transfer shortcut-like privileged cues, while overly conservative self-teaching may fail to capture genuinely beneficial knowledge.
To address this issue, we propose advantage-aware dual distillation, which dynamically selects both the supervision source and the distillation form according to the token-level privilege 优势差距.

Concretely, for each on-policy sampling trajectory 𝐲\mathbf{y}, we perform additional privileged forward passes: one with the privileged student policy and the other with the privileged teacher policy. For the n-th token, we denote their token-level probabilities as: qS=ΠS​(𝐲n​\mid​𝐱,𝐩,𝐲&lt;n)q_{S}=\Pi_{S}\left(\mathbf{y}_{n}\mid\mathbf{x},\mathbf{p},\mathbf{y}_{&lt;n}\right) and qT=ΠT​(𝐲n​\mid​𝐱,𝐩,𝐲&lt;n)q_{T}=\Pi_{T}\left(\mathbf{y}_{n}\mid\mathbf{x},\mathbf{p},\mathbf{y}_{&lt;n}\right), while corresponding token-level log-probabilities as: ℓS=log⁡ΠS​(𝐲n​\mid​𝐱,𝐩,𝐲&lt;n)\ell_{S}=\log\Pi_{S}\left(\mathbf{y}_{n}\mid\mathbf{x},\mathbf{p},\mathbf{y}_{&lt;n}\right) and ℓT=log⁡ΠT​(𝐲n​\mid​𝐱,𝐩,𝐲&lt;n)\ell_{T}=\log\Pi_{T}\left(\mathbf{y}_{n}\mid\mathbf{x},\mathbf{p},\mathbf{y}_{&lt;n}\right).
Here, the privileged student policy shares parameters with the deployed student policy, but receives the privileged input 𝐩\mathbf{p} during training, while the privileged teacher policy remains frozen. As we formally defined in Equation 1 of Section 3.1.2, we use the two privileged policies to calculate the privilege 优势差距 𝒜\mathcal{A}. For a scored n-th token, we compare its 𝒜n\mathcal{A}_{n}, qSq_{S}, and qTq_{T} with their average 𝒜¯\bar{\mathcal{A}}, qS¯\bar{q_{S}}, and qT¯\bar{q_{T}}, respectively. In practice, to ensure stability, we first discard the top 5% of outliers and perform normalization within the batch, then use them to calculate the average.
Based on all these relationships, it yields four token regimes, each corresponding to a distinct learning strategy.

Low 𝒜\mathcal{A} with High qSq_{S} &amp; qTq_{T}.
When the two privileged policies have low 优势差距 with both high predicted probability, i.e., 𝕀LH=(𝒜n&lt;𝒜¯)​(qS+qT​qS¯+qT¯)\mathbb{I}^{\mathrm{LH}}=\left(\mathcal{A}_{n}&lt;\bar{\mathcal{A}}\right)\wedge\left(q_{S}+q_{T}\geq\bar{q_{S}}+\bar{q_{T}}\right), the privileged teacher and privileged student make consistent and confident predictions.
In this case, the bottleneck is mainly attributed to the absence of 特权信息 rather than an inherent capability gap.
Thus, directly enforcing full teacher imitation is unnecessary and may over-transfer privileged shortcuts.
We instead apply a light teacher distillation objective, using Top-K reverse KL to absorb useful privileged knowledge in a conservative manner:

ℒL​H=βl​K​Lreverse​(ΠS​(\mid​𝐱,𝐲&lt;n)​\|​ΠT​(\mid​𝐱,𝐩,𝐲&lt;n)).\mathcal{L}^{LH}=\beta_{l}\,KL_{\mathrm{reverse}}\left(\Pi_{S}\left(\cdot\mid\mathbf{x},\mathbf{y}_{&lt;n}\right)\,\middle\|\,\Pi_{T}\left(\cdot\mid\mathbf{x},\mathbf{p},\mathbf{y}_{&lt;n}\right)\right).

(6)

where βl\beta_{l} denotes the intensity coefficient with light distillation.

Low 𝒜\mathcal{A} with Low qSq_{S} &amp; qTq_{T}.
When the two privileged policies have low 优势差距 with both low predicted probability, i.e., 𝕀LL=(𝒜n&lt;𝒜¯)​(qS+qT&lt;qS¯+qT¯)\mathbb{I}^{\mathrm{LL}}=\left(\mathcal{A}_{n}&lt;\bar{\mathcal{A}}\right)\wedge\left(q_{S}+q_{T}&lt;\bar{q_{S}}+\bar{q_{T}}\right), both privileged policies assign low probability to the current token.
Such tokens are likely to lie beyond the reliable competence region of both models, where aggressive teacher forcing may introduce noisy or even misleading supervision.
Therefore, we use the privileged student as a weak self-regularizing anchor, using Top-K reverse KL with a smaller coefficient, to stabilize training without forcing the student to imitate uncertain teacher predictions:

ℒL​L=βwKLreverse(ΠS(\mid𝐱,𝐲&lt;n)\|sg(ΠS(\mid𝐱,𝐩,𝐲&lt;n)⌋),\mathcal{L}^{LL}=\beta_{w}\,KL_{\mathrm{reverse}}\left(\Pi_{S}\left(\cdot\mid\mathbf{x},\mathbf{y}_{&lt;n}\right)\,\middle\|\,sg\left[\Pi_{S}\left(\cdot\mid\mathbf{x},\mathbf{p},\mathbf{y}_{&lt;n}\right)\right]\right),

(7)

where sg(⌋sg[\cdot] denotes stop-gradient to avoid changing the gradient simultaneously to cause target drift, βw\beta_{w} denotes the intensity coefficient with weak distillation, and βw&lt;βl\beta_{w}&lt;\beta_{l}. In this regime, the privileged student is not treated as a knowledge source, but as a parameter-shared consistency anchor that prevents policy drift.

High 𝒜\mathcal{A} with High qTq_{T}.
When the two privileged policies have high 优势差距 with high predicted probability of the teacher policy, i.e., 𝕀HT=(𝒜n​𝒜¯)​(qT​qS)\mathbb{I}^{\mathrm{HT}}=\left(\mathcal{A}_{n}\geq\bar{\mathcal{A}}\right)\wedge\left(q_{T}\geq q_{S}\right), the privileged teacher exhibits a clear and confident advantage over the privileged student.
Since both policies observe the same 特权信息, a large privilege 优势差距 suggests that, the teacher provides a potentially useful capability signal beyond what the student currently captures.
Accordingly, these tokens contain critical transferable knowledge and should receive stronger supervision.
We therefore perform full-vocabulary teacher distillation with unit weight, using JS divergence to balance support coverage and mode concentration:

ℒH​T=J​S​(ΠS​(\mid​𝐱,𝐲&lt;n)​\|​ΠT​(\mid​𝐱,𝐩,𝐲&lt;n)).\mathcal{L}^{HT}=JS\left(\Pi_{S}\left(\cdot\mid\mathbf{x},\mathbf{y}_{&lt;n}\right)\,\middle\|\,\Pi_{T}\left(\cdot\mid\mathbf{x},\mathbf{p},\mathbf{y}_{&lt;n}\right)\right).

(8)

Compared with Top-K strategy, full-vocabulary alignment provides denser distributional signals, enabling the student to acquire both dominant decisions and informative secondary preferences from the teacher.

High 𝒜\mathcal{A} with High qSq_{S}.
When the two privileged policies have high 优势差距 with high predicted probability of the student policy, i.e., 𝕀HS=(𝒜n​𝒜¯)​(qT&lt;qS)\mathbb{I}^{\mathrm{HS}}=\left(\mathcal{A}_{n}\geq\bar{\mathcal{A}}\right)\wedge\left(q_{T}&lt;q_{S}\right), the privileged student assigns relative larger confidence while the privileged teacher does not provide a comparably reliable signal.
In this regime, strongly constraining the student toward the teacher may suppress potentially valid exploratory behavior.
We therefore adopt a light privileged-student distillation objective with Top-K reverse KL, which softly encourages consistency between the deployed student and its privileged counterpart while avoiding over-regularization:

ℒH​S=βlKLreverse(ΠS(\mid𝐱,𝐲&lt;n)\|sg(ΠS(\mid𝐱,𝐩,𝐲&lt;n)⌋).\mathcal{L}^{HS}=\beta_{l}\,KL_{\mathrm{reverse}}\left(\Pi_{S}\left(\cdot\mid\mathbf{x},\mathbf{y}_{&lt;n}\right)\,\middle\|\,sg\left[\Pi_{S}\left(\cdot\mid\mathbf{x},\mathbf{p},\mathbf{y}_{&lt;n}\right)\right]\right).

(9)

Total Objective.
Finally, we combine the four token-wise objectives through indicator masks:

ℒDOPD=\displaystyle\mathcal{L}^{\mathrm{DOPD}}=
𝕀LH​ℒLH+𝕀LL​ℒLL+𝕀HT​ℒHT+𝕀HS​ℒHS,\displaystyle\;\mathbb{I}^{\mathrm{LH}}\mathcal{L}^{\mathrm{LH}}+\mathbb{I}^{\mathrm{LL}}\mathcal{L}^{\mathrm{LL}}+\mathbb{I}^{\mathrm{HT}}\mathcal{L}^{\mathrm{HT}}+\mathbb{I}^{\mathrm{HS}}\mathcal{L}^{\mathrm{HS}},

(10)

where the masks are determined by the privilege 优势差距 and relative probability comparisons described above, which exhaustively partitions the token space under the defined conditions. Thus, the overall optimization objective could be formulated as:

𝔼𝐱​𝒟(𝔼𝐲​ΠS(1⋃𝐲⋃\slimits@n=1⋃𝐲⋃ℒnD​O​P​D(𝐲n;𝐱,𝐩,𝐲&lt;n)⌋⌋,\mathbb{E}_{\mathbf{x}\sim\mathcal{D}}\left[\mathbb{E}_{\mathbf{y}\sim\Pi_{S}}\left[\frac{1}{|\mathbf{y}|}\tsum\slimits@_{n=1}^{|\mathbf{y}|}\mathcal{L}_{n}^{DOPD}\left(\mathbf{y}_{n};\mathbf{x},\mathbf{p},\mathbf{y}_{&lt;n}\right)\right]\right],

(11)

Through this adaptive routing mechanism, DOPD assigns strong full-vocabulary teacher supervision only to tokens where the privileged teacher demonstrates a credible capability advantage, applies light teacher distillation when the signal mainly reflects 特权信息, relies on weak privileged-student regularization for uncertain regions, and preserves student exploration when the privileged student is already confident.
Consequently, the proposed objective mitigates the entanglement between capability transfer and privileged-information imitation, yielding a more selective, stable, and generalizable OPD paradigm.

## 
4 Experiments

### 
4.1 Settings

#### 
4.1.1 Models

We perform all the experiments on Qwen3 [48] and Qwen3-VL [3] families of non-thinking versions as both teacher and student policies. Specifically, the main experiments and all analyses are conducted on Qwen3-8B to Qwen3-1.7B pair, and for VLM scenario is based on Qwen3-VL-8B to Qwen3-VL-2B pair. Besides, to verify the generalization ability of our method, we also add Qwen3-8B to Qwen3-0.6B, Qwen3-4B to Qwen3-0.6B, Qwen3-4B to Qwen3-1.7B, and Qwen3-1.7B to Qwen3-0.6B pairs.

For the training datasets of LLM-based OPD, we use the high-quality mixture dataset from RaR-Science-20K [9], DAPO-Math-17K [54], and Skywork-OR1-Coding-14K [10], covering general, reasoning, and coding tasks. For VLM-based training datasets, we utilize ViRL39K [24] dataset, covering general, visual reasoning and visual understanding tasks. For the corresponding privileged input, we use GPT-5.4 [29] (2026-03-05) to generate step-wise decomposition hints and structured visual annotations respectively, where the generation prompts are provided in Figure 13.
As illustrated in Figure 11, for LLM tasks, we utilize verified rationales as 特权信息, with step-wise decomposition hints, but without direct execution trace or final answer.
While as shown in Figure 12, for VLM tasks, 特权信息 denotes structured visual annotations, here we use query-related bounding boxes, with object labels and quadruple coordinates to provide explicit visual context.
To guarantee the data quality, we use GPT-5.4 again to recheck the generated privileged contents, and directly discard relatively low-quality samples, eventually resulting in 32K and 25K high-quality training data for LLM and VLM, respectively.

#### 
4.1.2 Benchmarks

To evaluate the effectiveness of our method, we employ eight benchmarks for LLM-based OPD, covering three core abilities: (1) general: C-Eval [14], and LiveBench [39]; (2) reasoning: MATH500 [11], AIME25 [2], ZebraLogic [27], and AutoLogi [62]; and (3) coding: BFCLv3 [47], and LCBv5 [16]. For VLM-based OPD, we also include eight benchmarks on three aspects: (1) general: RealWorldQA [41], and MMStar [5]; (2) visual reasoning: MathVision [37], DynaMath [63], and LogicVista [43]; and (3) visual understanding: MMMU [58], MMMU-Pro [59], and VSI-Bench [50]. All benchmarks are evaluated using their official metrics and evaluations to ensure fair and consistent comparison.

Table 1: Performance comparison of our proposed DOPD with counterparts on general, reasoning, and coding tasks. Δ\Delta indicates the performance gap between the student and teacher policies with gray cells, while blue for over 50% mitigation and green for complete gap removal by employing the OPD paradigms. The best and second best values are bolded and underlined, respectively.

Method
Type
General
Reasoning
Coding
Average

C-Eval
LiveBench
MATH500
AIME25
ZebraLogic
AutoLogi
BFCLv3
LCBv5

Teacher Policy
-
77.1
53.5
86.9
20.2
25.0
76.3
60.0
23.6
52.8

Student Policy
60.4
35.4
72.7
9.5
12.1
59.8
51.9
11.3
39.1

Δ\Delta Performance Gap

+16.7
+18.1
+14.2
+10.7
+12.9
+16.5
+8.1
+12.3
+13.7

Vanilla OPD [23]

Standard
65.2
40.9
75.6
16.7
15.8
64.3
55.4
17.6
43.9

OPCD [53]

66.1
41.6
75.3
19.5
17.0
65.2
54.7
15.8
44.3

ExOPD [51]

68.3
44.7
76.7
18.5
19.9
68.0
57.2
22.6
47.0

Uni-OPD [12]

66.5
42.3
77.5
20.0
22.3
67.2
56.1
20.8
46.6

SDFT [34]

Self
63.4
38.7
73.8
15.0
15.4
62.6
53.2
12.1
41.8

OPSD [61]

64.6
39.7
73.8
15.2
14.7
63.1
54.2
14.5
42.5

SDPO [15]

65.4
38.8
74.0
16.4
15.1
62.9
52.3
17.7
42.8

EOPD [18]

Adaptive
67.5
45.7
75.9
17.6
19.3
67.1
56.8
19.0
46.1

TIP [46]

67.0
43.1
74.3
17.2
18.7
65.5
54.5
17.9
44.8

DOPD (Ours)
Dual
71.3
49.8
81.5
23.3
26.9
71.0
60.2
27.1
51.4

Table 2: Performance comparison of our proposed DOPD with counterparts on general, visual reasoning, and visual understanding tasks. ∗The codes of VA-OPD are not officially released, so we use the results of our reproduced version. 

Method
General
Visual Reasoning
Visual Understanding
Average

RealWorldQA
MMStar
MathVision
DynaMath
LogicVista
MMMU
MMMU-Pro
VSI-Bench

Teacher Policy
71.3
70.7
53.8
67.6
55.0
69.6
55.8
59.7
62.9

Student Policy
63.6
58.4
32.0
53.8
35.5
53.2
36.4
53.6
48.3

Δ\Delta Performance Gap

+7.7
+12.3
+21.8
+13.8
+19.5
+16.4
+19.4
+6.1
+14.6

Vanilla OPD [23]

64.7
61.8
37.1
56.2
40.2
58.0
46.7
54.1
52.4

Uni-OPD [12]

65.0
65.3
43.0
58.2
42.5
59.1
47.0
53.7
54.2

Vision-OPD [57]

66.2
66.4
38.0
57.6
43.1
64.9
52.3
56.1
55.6

VA-OPD∗ [28]

67.0
66.2
38.7
57.7
43.1
66.1
54.2
57.5
56.3

DOPD (Ours)
67.4
67.2
45.6
60.5
47.7
67.0
53.9
57.8
58.4

#### 
4.1.3 Baselines

We compare our DOPD with other nine LLM-based counterparts, including three main paradigms of OPD as we discussed in Section 2: (a) standard distillation: Vanilla OPD [23], OPCD [53], ExOPD [51], and Uni-OPD [12]; (b) self distillation: SDFT [34], OPSD [61], and SDPO [15]; and (c) adaptive distillation: EOPD [18] and TIP [46].
For VLM-based methods, we benchmark DOPD with other four methods: Vanilla OPD [23], Uni-OPD [12], Vision-OPD [57], and VA-OPD [28]. For fair comparison, we rerun all the baselines on Qwen3/Qwen3-VL models.

#### 
4.1.4 Implementations

All experiments are conducted on 8 NVIDIA H200 141GB GPUs. During distillation, the teacher policy is frozen for stability, while the student policy is optimized by AdamW optimizer and cosine scheduler with a learning rate of 510−65\times 10^{-6}. The batch sizes are set to 128 and 64 for LLM and VLM with 4 rollout samples, optimizing for a maximum of 200 and 300 steps, respectively.
The K is set to 128 for Top-K distillation, and βw\beta_{w} and βl\beta_{l} are 0.3 and 0.6 to regulate the strength of distillation.

### 
4.2 Main Results

#### 
4.2.1 Distillation Performance

As the main LLM-based OPD results reported in Table 1, DOPD substantially narrows the performance gap between the student and teacher policies, with a gain of 12.3 points and an 89.8% recovery of the original teacher-student gap. Notably, due to the introduction of 特权信息 that increases the upper limit of distillation, DOPD not only approaches the teacher policy on average, but also surpasses the teacher on four challenging benchmarks, especially on reasoning and coding tasks.
Compared with standard (i.e., strong-to-weak) and adaptive distillation counterparts, DOPD consistently achieves the best performance across all eight benchmarks and improves over the three strongest baselines, ExOPD [51]/Uni-OPD [12]/EOPD [18] by 4.4/4.8/5.3 points on average, respectively.
Self-distillation baselines provide relatively modest improvements, suggesting that existing methods relying solely on the self-distillation of the student is possibly insufficient for closing the teacher-student gap.

We further validate the effectiveness on VLM-based OPD, as listed in Table 2. Specifically, our proposed DOPD again brings a substantial improvement over the student policy by a 10.1-point absolute gain and a 69.2% recovery of the teacher-student gap. Compared with existing VLM-oriented OPD baselines, DOPD achieves the best average performance, outperforming Vanilla OPD [23], and other three baselines, Uni-OPD [12], Vision-OPD [57], and VA-OPD [28], by 6.0 and 4.2/2.8/2.1 points, respectively.
It is worth mentioning that all methods, including ours, have shown more significant improvements in visual understanding than reasoning and other visual tasks, which may be related to the distillation paradigm of the visual center, mainly distilling accurate and grounded focus from teacher on the visual evidence.

These results demonstrate that advantage-aware dual distillation is more effective than either static teacher imitation, self-refinement, or single-sided adaptive weighting, indicating that DOPD transfers not only surface-level output preferences but also more essential ability from teacher policy.
In addition, beyond text-only distillation, the proposed paradigm also provides robust and consistent gains for vision ability distillation.

Table 3: Generalization comparison of our proposed DOPD and Vanilla OPD based on five pairs of teacher-student models, including Qwen3-8B/4B/1.7B Qwen3-0.6B, and Qwen3-8B/4B Qwen3-1.7B.

Model Pair
Method
General
Reasoning
Coding
Average

C-Eval
LiveBench
MATH500
AIME25
ZebraLogic
AutoLogi
BFCLv3
LCBv5

Qwen3-8B
77.1
53.5
86.9
20.2
25.0
76.3
60.0
23.6
52.8

Base
Qwen3-4B
72.2
48.3
84.6
18.9
35.0
75.8
57.4
21.3
51.6

Model
Qwen3-1.7B
60.4
35.4
72.7
9.5
12.1
59.8
51.9
11.3
39.1

Qwen3-0.6B
42.0
21.8
55.2
2.0
4.1
37.2
44.0
3.5
26.2

Qwen3-8B

Δ\Delta Performance Gap

+35.1
+31.7
+31.7
+18.2
+20.9
+39.1
+16.0
+20.1
+26.6

\downarrow\downarrow
Vanilla OPD
44.8
24.5
59.3
4.6
5.9
46.5
46.1
6.1
29.7

Qwen3-0.6B
DOPD (Ours)
56.7
35.5
70.9
17.0
19.6
54.3
55.5
12.7
40.3

Qwen3-8B

Δ\Delta Performance Gap

+16.7
+18.1
+14.2
+10.7
+12.9
+16.5
+8.1
+12.3
+13.7

\downarrow\downarrow
Vanilla OPD
65.2
40.9
75.6
16.7
15.8
64.3
55.4
17.6
43.9

Qwen3-1.7B
DOPD (Ours)
71.3
49.8
81.5
23.3
26.9
71.0
60.2
27.1
51.4

Qwen3-4B

Δ\Delta Performance Gap

+30.2
+26.5
+29.4
+16.9
+30.9
+38.6
+13.4
+17.8
+25.4

\downarrow\downarrow
Vanilla OPD
44.8
24.0
60.9
7.4
7.9
47.4
46.5
8.6
30.9

Qwen3-0.6B
DOPD (Ours)
54.0
33.8
72.7
16.3
25.1
51.6
52.2
13.7
39.9

Qwen3-4B

Δ\Delta Performance Gap

+11.8
+12.9
+11.9
+9.4
+22.9
+16.0
+5.5
+10.0
+12.5

\downarrow\downarrow
Vanilla OPD
65.3
41.0
76.3
17.1
16.8
65.6
53.5
16.6
44.0

Qwen3-1.7B
DOPD (Ours)
69.9
48.1
80.2
22.0
29.1
70.8
57.2
24.4
50.2

Qwen3-1.7B

Δ\Delta Performance Gap

+18.4
+13.6
+17.5
+7.5
+8.0
+22.6
+7.9
+7.8
+12.9

\downarrow\downarrow
Vanilla OPD
47.3
29.5
60.1
7.8
9.9
43.3
47.1
8.2
31.7

Qwen3-0.6B
DOPD (Ours)
55.6
35.6
66.7
14.6
16.4
49.4
53.0
13.7
38.1

(a) Performance Gain vs. Teacher-student Size Ratio

(b) Gap Reduction vs. Teacher-student Size Ratio

Figure 6: Scalability comparison of proposed DOPD and Vanilla OPD on (a) performance gain and (b) teacher-student gap reduction ratio. Here, the solid and dashed lines represent the 0.6B and 1.7B student policy, respectively. 

#### 
4.2.2 Robustness &amp; Scalability

To further examine whether DOPD generalizes across different teacher-student scales, we conduct experiments with five teacher-student pairs .
Table 3 shows that DOPD consistently outperforms Vanilla OPD [23] on every model pair, demonstrating that its effectiveness is not tied to a specific teacher or student size.
Our proposed method achieves consistent and significant performance improvements, averaging 11.1–14.1 points across all pairs, a two- to over three-fold improvement relative to Vanilla OPD.

More importantly, our method remains robust as the teacher-student size ratio increases.
As mentioned in previous studies [23, 25, 31], a larger size ratio implies greater initial distribution inconsistency between teachers and students, which may lead to suboptimal distillation effects.
For instance, in the largest scale-mismatch setting, i.e., Qwen3-8B Qwen3-0.6B, Vanilla OPD only reaches a 3.5-point gain; In contrast, DOPD achieves a 14.1-point gain and recovers 53.0% of the teacher-student gap.
Similar trends can be observed for Qwen3-4B Qwen3-0.6B.
As illustrated in Figure 6(a), when the teacher model has larger parameters, and stronger capabilities, the performance improvement of Vanilla OPD actually decreases, suggesting that naive imitation becomes less effective when the capacity mismatch is large.
By contrast, DOPD maintains gradually increasing gains across these settings.
Furthermore, as reported in Figure 6(b), although the gap reduction inevitably decreases as the size ratio increases, due to the larger initial teacher-student gap and the limitations of the ability limit of student model, our model still effectively alleviates this trend.
These results indicate that DOPD provides a more scalable and reliable distillation mechanism, especially when transferring policies from substantially larger teachers to compact students.

(a) Normalized Performance on Three-stage Continual Learning

(b) 分布外 Evaluation

Figure 7: Comparison of proposed DOPD and Vanilla OPD on (a) continual learning, where we conduct a three-stage continual learning with general, reasoning, and coding training sub-datasets sequentially. The solid and dashed lines denote the results on general benchmark (LiveBench) and corresponding specific benchmarks (MATH500 and BFCLv3); and (b) 分布外 tasks, where we optimize the student policy on coding or reasoning dataset, but evaluated on another out-of-domain benchmarks (MATH500 and BFCLv3).

#### 
4.2.3 Continual Learning Evaluation

OPD has been demonstrated to yield superior performance in continual learning, mitigating the catastrophic forgetting [34, 15] inherent to several prevalent post-training paradigms, e.g., SFT and GRPO [33]. Thus, we perform a three-stage experiment to evaluate the continual learning performance, where in the first stage only add general training data, while use reasoning and coding data in the next two stages.

Figure 7(a) indicates OPD-based paradigms have significantly better sustained learning performance and less forgetting, and our DOPD further optimizes this advantage. Specifically, it supports steady and effective capability accumulation: performance improves consistently on each newly introduced data domain, with only tiny performance degradation on previously acquired domains. This finding validates that DOPD enables authentic continual learning, where a single model can incrementally gain multiple capabilities instead of relying on simple capability concatenation or overwriting.

(a) Performance vs. Training Step

(b) Entropy vs. Training Step

Figure 8: Training stability comparison of proposed DOPD and representative baselines, reporting the (a) performance and (b) entropy trends over training steps on LiveBench.

#### 
4.2.4 分布外 Evaluation

We further evaluate the 分布外 generalization. Specifically, we optimize models on either the coding or reasoning training set separately, and assess their performance on the other unseen out-of-domain tasks. For comparative analysis, we select three best-performing baselines: ExOPD [51], Uni-OPD [12], and EOPD [18]. As demonstrated in Figure 7(b), our proposed DOPD outperforms the second-best counterparts by 3.1 and 4.3 points respectively, showcasing superior cross-domain generalization.

### 
4.3 Additional Analyses

#### 
4.3.1 Training Stability

To further assess training stability, we benchmark our method against the best-performing baselines from three distinct distillation paradigms: ExOPD [51] for standard distillation, SDPO [15] for self-distillation, and EOPD [18] for adaptive distillation.
As depicted in Figure 8(a), our method consistently delivers stable and superior performance throughout the entire training process, coupled with higher distillation efficiency. Compared with the three competing paradigms, our method surpasses their step-200 performance as early as step-80.
As shown in Figure 8(b), our method maintains a healthy entropy trajectory: it rises modestly in the early training stage, followed by a gradual decline, and converges to a steady state after step-110. This pattern reflects that the model undergoes stable learning with well-calibrated exploration.
Notably, we observe that the self-distillation paradigm encounters entropy collapse around step-95, alongside a subsequent drop in performance. This degradation is likely attributable to the insufficient and overly homogeneous supervision signals inherent to this paradigm, which render the learned distribution deficient in necessary exploration.
Collectively, these results corroborate that our proposed method achieves superior performance gains in a stable and efficient manner throughout the distillation process.

Table 4: Comparison of various LLM-based 特权信息 incorporation.

Privileged Input
C-Eval
LiveBench

Final Answer
59.5
36.7

Step-wise Hints with Execution
63.1
38.9

Step-wise Hints without Execution
71.3
49.8

Summarized Hints
65.8
43.6

No Privileged Input
63.0
39.4

Table 5: Comparison of various VLM-based 特权信息 incorporation.

Privileged Input
RealWorldQA
MMStar

Final Answer
64.6
63.2

Bounding Box with Caption
65.3
66.9

Bounding Box with Object Label
67.4
67.2

Caption
64.8
65.6

No Privileged Input
63.2
60.0

Figure 9: Token-level visualization of the four token types, where each token is colored based on their privilege 优势差距 𝒜\mathcal{A} and predicted probabilities of teacher qTq_{T} and student qSq_{S} policies.

#### 
4.3.2 特权信息 Analysis

To evaluate the impacts of distinct 特权信息 injection strategies, we conduct comparative experiments to benchmark the performance of five different 特权信息 formulations: final answer, step-wise hints with detailed execution process, step-wise hints without execution, simplest summarized hints, and no privileged input for LLM-based distillation, and final answer, bounding box with descriptive caption, bounding box with object label, caption, and no 特权信息 for VLM-based task.
As summarized in Table 5 and 5, directly providing ground-truth answers incurs the most severe information gap. The student model can only rigidly overfit to the given answers, which induces potential shortcut learning and performance degradation, even underperforming the baseline without any 特权信息.
In contrast, providing only step-level high-level hints without detailed execution steps yields the largest LLM distillation gains of 8.3 and 10.4 points respectively. Meanwhile, providing bounding boxes paired with corresponding object labels proves to be the most suitable 特权信息 modality for VLM, bringing 4.2 and 7.2 points of improvement over the baseline.
Notably, the efficacy of 特权信息 does not lie in the correctness of the final answers, but rather in its ability to deliver capability-oriented guidance to the student model, consistent with our previous discussion in Section 3.1.

#### 
4.3.3 Token Analysis

As detailed and analyzed in Section 3.1 and 3.2, we first compute the privilege 优势差距 𝒜\mathcal{A} and the predicted probabilities qT⇑Sq_{T/S} of both the teacher and student policies for each token, based on which we categorize each token into distinct classes.
To intuitively characterize the functional roles of different token types during distillation, Figure 9 visualizes the distribution of token categories within a real trajectory.
Among low-gap tokens, those with both high probabilities typically correspond to stable and consensus knowledge within 特权信息, whereas tokens with both low probabilities are mostly connectives, transitions or unreliable segments with little valid information.
Among high-gap tokens, tokens with high teacher probability but low student probability generally represent key knowledge arising from the inherent privilege-conditioned ability gap, while tokens with high student probability but low teacher probability likely reflect self-consistent or local branches of exploration.
This token distribution pattern aligns well with our proposed token-level differentiated distillation strategy, enabling targeted and efficient distillation for tokens with distinct functional roles.

To further quantitatively dissect the contributions of individual token types and the adaptive advantage-aware dual distillation mechanism to our proposed method, we conduct token-level ablation analysis.
Each variant performs distillation with signals from only one or combinations of token types, utilizing JS divergence on Top-K tokens. The setting without adaptive distillation corresponds to a baseline where all tokens receive identical distillation weights and strategies, with no token-wise differentiation.
As listed in Table 8, using exclusively tokens with high teacher probability and low student probability already outperforms the equal-distillation setup using all four token types (equivalent to Vanilla OPD) by 4.6 points.
However, naively adding the other three token types under an equal distillation scheme yields only marginal performance gains, and may even cause performance degradation.
In contrast, equipping the framework with the adaptive distillation mechanism allows for adjustment of token-level distillation intensity, supervision granularity, and distillation content. These designed patterns render the distillation process more efficient and stable, delivering an overall improvement of over 8 points than equal distillation, when all four token types are leveraged.

Table 6: Effectiveness of individual or combinations of four tokens, and adaptive mechanism on LiveBench.

Adaptive
Step-40
Step-80
Step-160

 ✓
 ✗
 ✗
 ✗
 ✗
41.0
43.7
45.3

 ✓
 ✓
 ✗
 ✗
 ✗
39.9
42.9
45.0

 ✓
 ✗
 ✓
 ✗
 ✗
38.6
41.0
42.7

 ✓
 ✗
 ✗
 ✓
 ✗
39.2
42.7
44.5

 ✓
 ✓
 ✓
 ✓
 ✗
38.4
40.9
41.3

 ✓
 ✓
 ✗
 ✗
 ✓
41.0
45.4
47.9

 ✓
 ✗
 ✓
 ✗
 ✓
39.7
42.3
44.8

 ✓
 ✗
 ✗
 ✓
 ✓
40.1
44.9
47.6

 ✓
 ✓
 ✓
 ✓
 ✓
45.7
48.4
49.8

Table 7: Impact of different divergence objectives and strategies on LiveBench.

Objective
Strategy
Step-40
Step-80
Step-160

Forward KL
Sampled Token
37.2
39.8
41.1

Top-K Tokens
38.5
40.2
41.3

Full Vocabulary
38.0
40.1
41.5

Reverse KL
Sampled Token
37.0
38.4
40.6

Top-K Tokens
37.8
39.0
40.8

Full Vocabulary
38.5
40.6
41.9

JS Divergence
Sampled Token
37.3
39.2
41.0

Top-K Tokens
38.4
40.9
41.3

Full Vocabulary
39.2
41.6
42.5

Table 8: Ablation study on our DOPD, covering the main designs of advantage-aware dual distillation.

Variant
C-Eval
LiveBench

w/o Privileged Input
63.6
38.3

w/o Distillation from Student Policy
70.4
47.9

w/o Distillation from Teacher Policy
65.9
41.2

w/o Advantage-aware Distillation
67.6
41.3

w/o Adaptive Divergence Objectives
70.0
46.7

w/o Adaptive Divergence Strategies
70.8
46.1

DOPD (Ours)
71.3
49.8

Figure 10: Sensitivity study on the intensity coefficient of weak βw\beta_{w} and light βl\beta_{l} distillation.

#### 
4.3.4 Divergence Analysis

To further investigate the impacts of different divergence objectives (forward KL, reverse KL, and JS divergence) and strategies (sampled token, Top-K tokens, and full vocabulary), all introduced in Section 3.2, we conduct additional comparative experiments.
To isolate the effects of other factors, we apply equal distillation across all tokens. Table 8 summarizes how these design choices shape final distillation performance and efficiency.
Specifically, as the alignment scope expands from sampled to Top-K tokens and further to full vocabulary, performance improves progressively, yet inevitably incurs higher computational memory overhead.
Furthermore, in contrast to findings reported in some prior works [61, 18], JS divergence delivers relatively superior performance than forward or reverse KL methods under our settings.
Collectively, these results illustrate the inherent trade-off across different divergence configurations, providing empirical justification for our differentiated distillation paradigms.

#### 
4.3.5 Sensitivity &amp; Ablation Studies

As illustrated in Figure 10, we conduct an analysis focusing on the distillation intensity assigned to different token categories. We observe that setting βw=0.3\beta_{w}=0.3 and βl=0.6\beta_{l}=0.6 strikes a favorable trade-off across token-wise distillation strengths: it amplifies the contribution of critical tokens while preserving the auxiliary role of other tokens in stabilizing and providing additional optimization signals.

Furthermore, to further disentangle the contributions of individual design components in our framework, we conduct ablation studies on two core elements: the sources of distillation signals and divergence-based designs.
As presented in Table 8, privileged input is indispensable to our paradigm, as it directly underpins the advantage-aware calculation of our approach. Signals derived from the teacher policy serve as the primary driver of performance gains, while the student policy also fulfills an irreplaceable role throughout the distillation process. In addition, our token-wise divergence design tailored for distinct token categories is empirically validated to be effective.

## 
5 Conclusion

In this work, we revisit OPD under privileged contexts and identify fundamental limitations: the apparent superiority of a privileged teacher does not always correspond to transferable capability, but may instead arise from information asymmetry, and these supervision signals are not evenly distributed across tokens.
Motivated by these observations, we propose DOPD, an advantage-aware dual on-policy distillation framework that adaptively routes token 级监督 between teacher-driven capability transfer and auxiliary self-optimization from the student.
By leveraging the privilege 优势差距 and relative token probabilities, DOPD selectively applies strong full-vocabulary teacher distillation to capability-bearing tokens, while imposing light or weak distillation on tokens without a capacity 优势差距.
Extensive experiments across LLM and VLM settings demonstrate that DOPD consistently outperforms Vanilla OPD and strong competitive baselines, yielding superior distillation performance, robustness, continual-learning behavior, 分布外 generalization, and training stability.

## 
6 Limitations and Future Directions

Notwithstanding the efficacy of our proposed DOPD, we acknowledge that several minor limitations remain.
First, our method hinges on the availability and quality of 特权信息, the construction of which incurs additional costs for annotation, generation, and filtering processes.
Second, it introduces extra computational overhead relative to Vanilla OPD, requiring one additional forward pass of the student model.
Third, while the current routing strategy is intuitive, and empirically stable, it still relies on heuristic mechanisms.

Future research may further advance DOPD along directions: developing more reliable and cost-effective mechanisms for obtaining 特权信息 or discovering alternative strategy to detect available 优势差距, with more principled or learnable distillation routing. More broadly, the paradigm of dynamic distillation from both teacher and student offers a useful lens for selective capacity transfer beyond LLMs and VLMs, inviting future work on more interpretable, efficient, and trustworthy distillation paradigms.

## References

- 
Agarwal et al. [2024]

Rishabh Agarwal, Nino Vieillard, Yongchao Zhou, Piotr Stanczyk, Sabela Ramos Garea, Matthieu Geist, and Olivier Bachem.

On-policy distillation of language models: Learning from self-generated mistakes.

In *International Conference on Learning Representations (ICLR)*, volume 2024, pages 21246–21263, 2024.

- 
AIME [2025]

AIME.

Aime problems and solutions, 2025.

URL https://artofproblemsolving.com/wiki/index.php/AIME_Problems_and_Solutions.

- 
Bai et al. [2025]

Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui Chen, Zesen Cheng, Lianghao Deng, Wei Ding, Chang Gao, Chunjiang Ge, et al.

Qwen3-vl technical report.

*arXiv preprint arXiv:2511.21631*, 2025.

- 
Busbridge et al. [2025]

Dan Busbridge, Amitis Shidani, Floris Weers, Jason Ramapuram, Etai Littwin, and Russ Webb.

Distillation scaling laws.

*arXiv preprint arXiv:2502.08606*, 2025.

- 
Chen et al. [2024]

Lin Chen, Jinsong Li, Xiaoyi Dong, Pan Zhang, Yuhang Zang, Zehui Chen, Haodong Duan, Jiaqi Wang, Yu Qiao, Dahua Lin, et al.

Are we on the right way for evaluating large 视觉语言模型s?

*Advances in Neural Information Processing Systems (NeurIPS)*, 37:27056–27087, 2024.

- 
Cui et al. [2025]

Ganqu Cui, Yuchen Zhang, Jiacheng Chen, Lifan Yuan, Zhi Wang, Yuxin Zuo, Haozhan Li, Yuchen Fan, Huayu Chen, Weize Chen, et al.

The entropy mechanism of reinforcement learning for reasoning language models.

*arXiv preprint arXiv:2505.22617*, 2025.

- 
Fu et al. [2026]

Yuqian Fu, Haohuan Huang, Kaiwen Jiang, Jiacai Liu, Zhuo Jiang, Yuanheng Zhu, and Dongbin Zhao.

Revisiting on-policy distillation: Empirical failure modes and simple fixes.

*arXiv preprint arXiv:2603.25562*, 2026.

- 
Gu et al. [2024]

Yuxian Gu, Li Dong, Furu Wei, and Minlie Huang.

MiniLLM: Knowledge distillation of 大语言模型s.

In *International Conference on Learning Representations (ICLR)*, 2024.

- 
Gunjal et al. [2025]

Anisha Gunjal, Anthony Wang, Elaine Lau, Vaskar Nath, Yunzhong He, Bing Liu, and Sean Hendryx.

Rubrics as rewards: Reinforcement learning beyond verifiable domains.

*arXiv preprint arXiv:2507.17746*, 2025.

- 
He et al. [2025]

Jujie He, Jiacai Liu, Chris Yuhao Liu, Rui Yan, Chaojie Wang, Peng Cheng, Xiaoyu Zhang, Fuxiang Zhang, Jiacheng Xu, Wei Shen, et al.

Skywork open reasoner 1 technical report.

*arXiv preprint arXiv:2505.22312*, 2025.

- 
Hendrycks et al. [2021]

Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt.

Measuring mathematical problem solving with the math dataset.

*arXiv preprint arXiv:2103.03874*, 2021.

- 
Hou et al. [2026]

Wenjin Hou, Shangpin Peng, Weinong Wang, Zheng Ruan, Yue Zhang, Zhenglin Zhou, Mingqi Gao, Yifei Chen, Kaiqi Wang, Hongming Yang, et al.

Uni-opd: Unifying on-policy distillation with a dual-perspective recipe.

*arXiv preprint arXiv:2605.03677*, 2026.

- 
Hsieh et al. [2023]

Cheng-Yu Hsieh, Chun-Liang Li, Chih-Kuan Yeh, Hootan Nakhost, Yasuhisa Fujii, Alex Ratner, Ranjay Krishna, Chen-Yu Lee, and Tomas Pfister.

Distilling step-by-step! outperforming larger language models with less training data and smaller model sizes.

In *Findings of the Association for Computational Linguistics: ACL 2023*, pages 8003–8017, 2023.

- 
Huang et al. [2023]

Yuzhen Huang, Yuzhuo Bai, Zhihao Zhu, Junlei Zhang, Jinghan Zhang, Tangjun Su, Junteng Liu, Chuancheng Lv, Yikai Zhang, Yao Fu, et al.

C-eval: A multi-level multi-discipline chinese evaluation suite for foundation models.

*Advances in Neural Information Processing Systems (NeurIPS)*, 36:62991–63010, 2023.

- 
Hübotter et al. [2026]

Jonas Hübotter, Frederike Lübeck, Lejs Behric, Anton Baumann, Marco Bagatella, Daniel Marta, Ido Hakimi, Idan Shenfeld, Thomas Kleine Buening, Carlos Guestrin, et al.

Reinforcement learning via self-distillation.

*arXiv preprint arXiv:2601.20802*, 2026.

- 
Jain et al. [2025]

Naman Jain, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica.

Livecodebench: Holistic and contamination free evaluation of 大语言模型s for code.

In *International Conference on Learning Representations (ICLR)*, volume 2025, pages 58791–58831, 2025.

- 
Jang et al. [2026]

Ijun Jang, Jewon Yeom, Juan Yeo, Hyunggu Lim, and Taesup Kim.

Stable on-policy distillation through adaptive target reformulation.

*arXiv preprint arXiv:2601.07155*, 2026.

- 
Jin et al. [2026]

Woogyeol Jin, Taywon Min, Yongjin Yang, Swanand Ravindra Kadhe, Yi Zhou, Dennis Wei, Nathalie Baracaldo, and Kimin Lee.

Entropy-aware on-policy distillation of language models.

*arXiv preprint arXiv:2603.07079*, 2026.

- 
Kim and Baek [2026]

Minsang Kim and Seung Jun Baek.

Explain in your own words: Improving reasoning via token-selective dual knowledge distillation.

In *International Conference on Learning Representations (ICLR)*, 2026.

- 
Kim and Rush [2016]

Yoon Kim and Alexander M Rush.

Sequence-level knowledge distillation.

In *Proceedings of Conference on Empirical Methods in Natural Language Processing (EMNLP)*, pages 1317–1327, 2016.

- 
Ko et al. [2025]

Jongwoo Ko, Tianyi Chen, Sungnyun Kim, Tianyu Ding, Luming Liang, Ilya Zharkov, and Se-Young Yun.

DistiLLM-2: A contrastive approach boosts the distillation of LLMs.

In *International Conference on Machine Learning (ICML)*, 2025.

- 
Ko et al. [2026]

Jongwoo Ko, Sara Abdali, Young Jin Kim, Tianyi Chen, and Pashmina Cameron.

Scaling reasoning efficiently via relaxed on-policy distillation.

*arXiv preprint arXiv:2603.11137*, 2026.

- 
Lab [2025]

Thinking Machines Lab.

On-policy distillation, 2025.

URL https://thinkingmachines.ai/blog/on-policy-distillation.

- 
Li et al. [2026a]

Shufan Li, Konstantinos Kallidromitis, Hritik Bansal, Akash Gokul, Yusuke Kato, Kazuki Kozuka, Jason Kuen, Zhe Lin, Kai-Wei Chang, and Aditya Grover.

Lavida: A large diffusion language model for multimodal understanding.

*Advances in Neural Information Processing Systems (NeurIPS)*, 38:105101–105134, 2026a.

- 
Li et al. [2026b]

Yaxuan Li, Yuxin Zuo, Bingxiang He, Jinqian Zhang, Chaojun Xiao, Cheng Qian, Tianyu Yu, Huan-ang Gao, Wenkai Yang, Zhiyuan Liu, et al.

Rethinking on-policy distillation of 大语言模型s: Phenomenology, mechanism, and recipe.

*arXiv preprint arXiv:2604.13016*, 2026b.

- 
Li et al. [2025]

Yuetai Li, Xiang Yue, Zhangchen Xu, Fengqing Jiang, Luyao Niu, Bill Yuchen Lin, Bhaskar Ramasubramanian, and Radha Poovendran.

Small models struggle to learn from strong reasoners.

In *Findings of the Association for Computational Linguistics: ACL 2025*, pages 25366–25394, 2025.

- 
Lin et al. [2025]

Bill Yuchen Lin, Ronan Le Bras, Kyle Richardson, Ashish Sabharwal, Radha Poovendran, Peter Clark, and Yejin Choi.

Zebralogic: On the scaling limits of llms for logical reasoning.

*arXiv preprint arXiv:2502.01100*, 2025.

- 
Liu et al. [2026]

Ruiqi Liu, Xiaolei Lv, Gengsheng Li, Ximo Zhu, Zhiheng Wang, Zhengbo Zhang, Junkai Chen, Zhiheng Li, Bo Li, Jun Gao, et al.

Visual-advantage on-policy distillation for 视觉语言模型s.

*arXiv preprint arXiv:2605.21924*, 2026.

- 
OpenAI [2026]

OpenAI.

Introducing gpt-5.4, 2026.

URL https://openai.com/index/introducing-gpt-5-4.

- 
Penaloza et al. [2026]

Emiliano Penaloza, Dheeraj Vattikonda, Nicolas Gontier, Alexandre Lacoste, Laurent Charlin, and Massimo Caccia.

特权信息 distillation for language models.

*arXiv preprint arXiv:2602.04942*, 2026.

- 
Qin et al. [2026]

Chuanyu Qin, Chenxu Yang, Qingyi Si, Naibin Gu, Dingyu Yao, Zheng Lin, Peng Fu, Nan Duan, and Jiaqi Wang.

Near-future policy optimization.

*arXiv preprint arXiv:2604.20733*, 2026.

- 
Sanh et al. [2019]

Victor Sanh, Lysandre Debut, Julien Chaumond, and Thomas Wolf.

Distilbert, a distilled version of bert: smaller, faster, cheaper and lighter.

*arXiv preprint arXiv:1910.01108*, 2019.

- 
Shao et al. [2024]

Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al.

Deepseekmath: Pushing the limits of mathematical reasoning in open language models.

*arXiv preprint arXiv:2402.03300*, 2024.

- 
Shenfeld et al. [2026]

Idan Shenfeld, Mehul Damani, Jonas Hübotter, and Pulkit Agrawal.

Self-distillation enables continual learning.

*arXiv preprint arXiv:2601.19897*, 2026.

- 
Song and Zheng [2026]

Mingyang Song and Mao Zheng.

A survey of on-policy distillation for 大语言模型s.

*arXiv preprint arXiv:2604.00626*, 2026.

- 
Stein et al. [2026]

Alex Stein, Furong Huang, and Tom Goldstein.

Gates: Self-distillation under privileged context with consensus gating.

*arXiv preprint arXiv:2602.20574*, 2026.

- 
Wang et al. [2024]

Ke Wang, Junting Pan, Weikang Shi, Zimu Lu, Houxing Ren, Aojun Zhou, Mingjie Zhan, and Hongsheng Li.

Measuring multimodal mathematical reasoning with math-vision dataset.

*Advances in Neural Information Processing Systems (NeurIPS)*, 37:95095–95169, 2024.

- 
Wang et al. [2026]

Yuanyi Wang, Su Lu, Yanggan Gu, Pengkai Wang, Yifan Yang, Zhaoyi Yan, Congkai Xie, Jianmin Wu, and Hongxia Yang.

Not all disagreement is learnable: Token teachability in on-policy distillation.

*arXiv preprint arXiv:2605.26844*, 2026.

- 
White et al. [2024]

Colin White, Samuel Dooley, Manley Roberts, Arka Pal, Ben Feuer, Siddhartha Jain, Ravid Shwartz-Ziv, Neel Jain, Khalid Saifullah, Siddartha Naidu, et al.

Livebench: A challenging, contamination-free llm benchmark.

*arXiv preprint arXiv:2406.19314*, 4:2, 2024.

- 
Wu et al. [2026]

Yecheng Wu, Song Han, and Hai Cai.

Lightning opd: Efficient post-training for large reasoning models with offline on-policy distillation.

*arXiv preprint arXiv:2604.13010*, 2026.

- 
xAI [2024]

xAI.

Realworldqa: A benchmark for real-world spatial understanding, 2024.

URL https://huggingface.co/datasets/xai-org/RealworldQA.

- 
Xiao et al. [2026]

Bangjun Xiao, Bingquan Xia, Bo Yang, Bofei Gao, Bowen Shen, Chen Zhang, Chenhong He, Chiheng Lou, Fuli Luo, Gang Wang, et al.

Mimo-v2-flash technical report.

*arXiv preprint arXiv:2601.02780*, 2026.

- 
Xiao et al. [2024]

Yijia Xiao, Edward Sun, Tianyu Liu, and Wei Wang.

Logicvista: Multimodal llm logical reasoning benchmark in visual contexts.

*arXiv preprint arXiv:2407.04973*, 2024.

- 
Xu et al. [2026a]

Anyi Xu, Bangcai Lin, Bing Xue, Bingxuan Wang, Bingzheng Xu, Bochao Wu, Bowei Zhang, Chaofan Lin, Chen Dong, Chenchen Ling, et al.

Deepseek-v4: Towards highly efficient million-token context intelligence.

*arXiv preprint arXiv:2606.19348*, 2026a.

- 
Xu et al. [2025]

Wenda Xu, Rujun Han, Zifeng Wang, Long Le, Dhruv Madeka, Lei Li, William Yang Wang, Rishabh Agarwal, Chen-Yu Lee, and Tomas Pfister.

Speculative knowledge distillation: Bridging the teacher-student gap through interleaved sampling.

In *International Conference on Learning Representations (ICLR)*, 2025.

- 
Xu et al. [2026b]

Yuanda Xu, Hejian Sang, Zhengze Zhou, Ran He, Zhipeng Wang, and Alborz Geramifard.

Tip: Token importance in on-policy distillation.

*arXiv preprint arXiv:2604.14084*, 2026b.

- 
Yan et al. [2024]

Fanjia Yan, Huanzhi Mao, Charlie Cheng-Jie Ji, Tianjun Zhang, Shishir G. Patil, Ion Stoica, and Joseph E.Gonzalez.

Berkeley function calling leaderboard, 2024.

URL https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html.

- 
Yang et al. [2025a]

An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al.

Qwen3 technical report.

*arXiv preprint arXiv:2505.09388*, 2025a.

- 
Yang et al. [2026a]

Chenxu Yang, Chuanyu Qin, Qingyi Si, Minghui Chen, Naibin Gu, Dingyu Yao, Zheng Lin, Weiping Wang, Jiaqi Wang, and Nan Duan.

Self-distilled rlvr.

*arXiv preprint arXiv:2604.03128*, 2026a.

- 
Yang et al. [2025b]

Jihan Yang, Shusheng Yang, Anjali W Gupta, Rilyn Han, Li Fei-Fei, and Saining Xie.

Thinking in space: How multimodal 大语言模型s see, remember, and recall spaces.

In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Conference (CVPR)*, pages 10632–10643, 2025b.

- 
Yang et al. [2026b]

Wenkai Yang, Weijie Liu, Ruobing Xie, Kai Yang, Saiyong Yang, and Yankai Lin.

Learning beyond teacher: Generalized on-policy distillation with reward extrapolation.

*arXiv preprint arXiv:2602.12125*, 2026b.

- 
Yao et al. [2026]

Dingyu Yao, Junhao Zhou, Chenxu Yang, Chuanyu Qin, Haowen Hou, Zheming Liang, Congcong Wang, Yuhang Cao, Shenglong Ye, Shuai Xie, et al.

Joyai-vl-interaction: Real-time vision-language interaction intelligence.

*arXiv preprint arXiv:2606.14777*, 2026.

- 
Ye et al. [2026]

Tianzhu Ye, Li Dong, Xun Wu, Shaohan Huang, and Furu Wei.

On-policy context distillation for language models.

*arXiv preprint arXiv:2602.12275*, 2026.

- 
Yu et al. [2026a]

Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan, Xiaochen Zuo, Yu Yue, Weinan Dai, Tiantian Fan, Gaohong Liu, Lingjun Liu, et al.

Dapo: An open-source llm reinforcement learning system at scale.

*Advances in Neural Information Processing Systems (NeurIPS)*, 38:113222–113244, 2026a.

- 
Yu et al. [2026b]

Xinlei Yu, Zhangquan Chen, Yongbo He, Tianyu Fu, Cheng Yang, Chengming Xu, Yue Ma, Xiaobin Hu, Zhe Cao, Jie Xu, et al.

The latent space: Foundation, evolution, mechanism, ability, and outlook.

*arXiv preprint arXiv:2604.02029*, 2026b.

- 
Yu et al. [2026c]

Xinlei Yu, Chengming Xu, Guibin Zhang, Zhangquan Chen, Yudong Zhang, Yongbo He, Peng-Tao Jiang, Jiangning Zhang, Xiaobin Hu, and Shuicheng Yan.

Vismem: Latent vision memory unlocks potential of 视觉语言模型s.

In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pages 31544–31555, 2026c.

- 
Yuan et al. [2026]

Qianhao Yuan, Jie Lou, Xing Yu, Hongyu Lin, Le Sun, Xianpei Han, and Yaojie Lu.

Vision-opd: Learning to see fine details for multimodal llms via on-policy self-distillation.

*arXiv preprint arXiv:2605.18740*, 2026.

- 
Yue et al. [2024]

Xiang Yue, Yuansheng Ni, Kai Zhang, Tianyu Zheng, Ruoqi Liu, Ge Zhang, Samuel Stevens, Dongfu Jiang, Weiming Ren, Yuxuan Sun, et al.

Mmmu: A massive multi-discipline multimodal understanding and reasoning benchmark for expert agi.

In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pages 9556–9567, 2024.

- 
Yue et al. [2025]

Xiang Yue, Tianyu Zheng, Yuansheng Ni, Yubo Wang, Kai Zhang, Shengbang Tong, Yuxuan Sun, Botao Yu, Ge Zhang, Huan Sun, et al.

Mmmu-pro: A more robust multi-discipline multimodal understanding benchmark.

In *Proceedings of the Annual Meeting of the Association for Computational Linguistics (ACL: Long Papers)*, pages 15134–15186, 2025.

- 
Zhang et al. [2026]

Dongxu Zhang, Zhichao Yang, Sepehr Janghorbani, Jun Han, Andrew Ressler II, Qian Qian, Gregory D Lyng, Sanjit Singh Batra, and Robert E Tillman.

Fast and effective on-policy distillation from reasoning prefixes.

*arXiv preprint arXiv:2602.15260*, 2026.

- 
Zhao et al. [2026]

Siyan Zhao, Zhihui Xie, Mengchen Liu, Jing Huang, Guan Pang, Feiyu Chen, and Aditya Grover.

Self-distilled reasoner: On-policy self-distillation for 大语言模型s.

*arXiv preprint arXiv:2601.18734*, 2026.

- 
Zhu et al. [2025]

Qin Zhu, Fei Huang, Runyu Peng, Keming Lu, Bowen Yu, Qinyuan Cheng, Xipeng Qiu, Xuanjing Huang, and Junyang Lin.

Autologi: Automated generation of logic puzzles for evaluating reasoning abilities of 大语言模型s.

*arXiv preprint arXiv:2502.16906*, 2025.

- 
Zou et al. [2025]

Chengke Zou, Xingang Guo, Rui Yang, Junyu Zhang, Bin Hu, and Huan Zhang.

Dynamath: A dynamic visual benchmark for evaluating mathematical reasoning robustness of vision language models.

In *International Conference on Learning Representations (ICLR)*, volume 2025, pages 48337–48383, 2025.

\beginappendix

## 
7 Details of Privileged Input

Figure 11: Demonstrations of LLM-based privileged input.

Figure 12: Demonstrations of VLM-based privileged input.

Figure 13: Prompts of Privileged Input Generation.