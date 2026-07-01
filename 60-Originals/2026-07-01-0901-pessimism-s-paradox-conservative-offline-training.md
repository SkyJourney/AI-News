---
id: 2026-07-01-0901-pessimism-s-paradox-conservative-offline-training
type: source-original
title: 悲观性悖论：保守离线训练在推理模型在线自适应中加剧奖励黑客攻击
original_title: "Pessimism's Paradox: Conservative Offline Training Amplifies Reward Hacking During Online Adaptation in Reasoning Models"
source_name: arxiv-api
source_url: http://arxiv.org/abs/2606.30627v1
author: ["Subramanyam Sahoo", "Aman Chadha", "Vinija Jain", "Divya Chaudhary"]
published_at: 2026-06-29
fetched_at: 2026-07-01T19:18:41+08:00
language: en
translated: true
translation_engine: haiku
word_count: 6134
images_attempted: 4
images_saved: 4
fallback_notice: null
related_daily: 2026-07-01
related_zettels: []
related_topics: []
tags: [source-original, language-zh]
---
# 悲观性悖论：保守离线训练在推理模型在线自适应中加剧奖励黑客攻击

> 原文：[Pessimism's Paradox: Conservative Offline Training Amplifies Reward Hacking During Online Adaptation in Reasoning Models](http://arxiv.org/abs/2606.30627v1) · arxiv-api · 2026-06-29
> 抓取：2026-07-01T19:18:41+08:00 · 翻译：haiku · 6134 字

## 摘要

保守离线训练通常被主张作为后续在线自适应的安全基础：论点是，如果策略保持接近良好支撑的行为，就不太可能利用学习奖励模型中的缺陷。我们在经验上和机制上对这一直觉提出质疑。我们在直接偏好优化（DPO）下用三个保守主义水平（β∈{βlo,βmid,βhi}\beta\in\{\beta_{\mathrm{lo}},\beta_{\mathrm{mid}},\beta_{\mathrm{hi}}\} 源自经验对数比百分位数）训练了一个 Qwen3-14B 策略，然后在学习奖励集成（3 ×\times Qwen3-1.7B）上进行在线自适应，同时在 GSM8K 精确答案准确度上测量真实性能。我们发现**更高的离线保守主义单调增加奖励黑客攻击损害**，通过 Goodhart 间隙及其曲线下面积（AUGC）测量，在所有三个条件下 Spearman ρ=1.0\rho=1.0。机制分析揭示了一个三链因果链：(i) 高β\beta DPO 压缩策略熵，(ii) 低熵策略生成响应多样性降低，集中在奖励模型训练分布的狭窄区域（较低的成对余弦距离），以及 (iii) 尽管这种接近性，集成不一致性（认知不确定性）随 β\beta 增加并在在线优化期间更快被利用。我们进一步将幂律曲线拟合到（β,AUGC）(\beta,\mathrm{AUGC}) 数据，并识别出一个实际最优保守主义水平 β⋆\beta^{\star}，在对齐保真度和黑客攻击易受性之间取得平衡。我们的结果表明，该领域需要**校准的**而非**最大的**保守主义。

offline reinforcement learning, reward hacking, Goodhart's law,
direct preference optimisation, uncertainty quantification,
entropy collapse, safe adaptation, language models

††footnotetext: 代码: [Conservative-Offline-Training-Amplifies-Reward-Hacking-During-Online-Adaptation](https://github.com/SubramanyamSahoo/Conservative-Offline-Training-Amplifies-Reward-Hacking-During-Online-Adaptation)

## 1 引言

安全语言模型对齐的标准做法如下：首先在人类偏好数据上进行离线训练（例如，通过 RLHF（Christiano et al., [2023](#bib.bib1)) 或 DPO（Rafailov et al., [2024](#bib.bib2)））使用保守主义系数 β\beta，对参考策略的偏离进行惩罚，然后可选地使用学习代理奖励进行在线自适应。隐含的契约是，更保守的离线检查点进入在线阶段时更接近奖励模型训练的分布，因此会更不积极地利用它。

具体来说，考虑高β\beta DPO 目标实际上对策略做了什么。它对参考策略πref\pi_{\mathrm{ref}}加强了 KL 约束，将概率质量集中在参考策略已分配高密度的令牌序列的狭窄切片上。结果的策略具有低输出熵和低响应多样性。当这个压缩策略随后针对学习奖励集成进行优化时，两种效应结合。首先，奖励模型在相对多样的人类偏好对集合上训练；压缩策略生成的响应位于该训练分布的稀疏区域，导致高认知不确定性（集成不一致性）。其次，低熵起点的探索方向较少，梯度更新可以改进**真实**性能，因此优化器快速将所有梯度信号导向奖励模型的盲点。最终结果是 Goodhart 间隙——代理奖励和真实奖励之间的分歧——对于高β\beta 策略打开得更快更宽。

本文做出了四项贡献。

1. **实证演示**使用真实模型（Qwen3-14B 策略，Qwen3-1.7B 奖励集成）和真实数据（UltraFeedback，GSM8K）的悖论。

2. **机制归因**通过响应熵坍缩测量和奖励模型 OOD 距离分析。

3. **AUGC 作为β\beta 函数的幂律拟合**，产生一个实际设计原则：存在最优保守主义水平β⋆\beta^{\star}，低于该水平在线安全退化快于离线对齐改进。

4. **算法和基准建议**用于下一代保守对齐方法，明确权衡悲观性与黑客攻击易受性。

## 2 背景与相关工作

### 2.1 直接偏好优化

DPO（Rafailov et al., [2024](#bib.bib2)）通过直接以策略对数比的形式重新参数化 RLHF 目标，绕过了显式奖励模型的需要。给定带有胜出和败出响应的提示偏好数据集 𝒟={(x,yw,yl)}\mathcal{D}=\{(x,y_{w},y_{l})\}，DPO 最小化

ℒDPO(πθ;πref)=−𝔼(x,yw,yl)∼𝒟[logσ(βlogπθ​(yw∣x)πref​(yw∣x)−βlogπθ​(yl∣x)πref​(yl∣x))].\mathcal{L}_{\mathrm{DPO}}(\pi_{\theta};\pi_{\mathrm{ref}})=-\mathbb{E}_{(x,y_{w},y_{l})\sim\mathcal{D}}\Big[\log\sigma\Big(\beta\log\frac{\pi_{\theta}(y_{w}\mid x)}{\pi_{\mathrm{ref}}(y_{w}\mid x)}\\
-\beta\log\frac{\pi_{\theta}(y_{l}\mid x)}{\pi_{\mathrm{ref}}(y_{l}\mid x)}\Big)\Big].

(1)

其中σ\sigma 是逻辑函数，β>0\beta>0 是保守主义系数。较大的β\beta 施加更严格的隐含 KL 约束 KL⁡(πθ∥πref)\operatorname{KL}(\pi_{\theta}\|\pi_{\mathrm{ref}})，将学习的策略拉向参考策略。

### 2.2 RLHF 中的 Goodhart 法则

Goodhart 法则（Goodhart, [1975](#bib.bib6)）指出当一个测量成为目标时，它就不再是一个好的测量。在 RLHF 背景下，Gao et al. ([2022](#bib.bib7)) 将其形式化为真实性能的单调退化，因为策略漂移向最大化代理奖励。Skalse et al. ([2025](#bib.bib8)) 给出了奖励黑客攻击的分类法，并表明当奖励模型有任何缺陷时它几乎不可避免。我们的工作研究了一个较少探索的方面：**离线训练策略**如何调制在线自适应期间黑客攻击的严重性和速度。

### 2.3 奖励模型集成与不确定性

集成是深度神经网络中认知不确定性估计的标准方法（Lakshminarayanan et al., [2017](#bib.bib26)）。在奖励模型背景下，集成不一致性为分布外输入提供了代理，并已用作离线 RL 中的悲观信号（Kumar et al., [2020](#bib.bib11)；Kidambi et al., [2021](#bib.bib13)）。我们的集成（3 ×\times Qwen3-1.7B 用自助重新采样训练）提供了代理奖励信号和我们机制分析中使用的不确定性信号。

### 2.4 离线 RL 与保守方法

DPO 与离线 RL 之间的连接众所周知。CQL（Kumar et al., [2020](#bib.bib11)）对支持外的动作的 Q 值进行惩罚；IQL（Kostrikov et al., [2021](#bib.bib12)）通过用隐式分位数回归替换 Bellman 备份来避免 OOD 动作。Decision Transformer（Chen et al., [2021](#bib.bib15)）将 RL 重新框架化为序列建模，这与 DPO 直接类似。所有这些方法共享编码在方程 1 中的相同保守主义逻辑：更大的保守主义系数 →\to 策略保持更接近参考 →\to（假定）更安全的在线性能。我们展示这个假设在一个特定失败模式下被违反：OOD 驱动的奖励黑客攻击。


## 3 问题公式化

设 πθ\pi_{\theta} 表示被训练的策略，πref\pi_{\mathrm{ref}} 为冻结的 DPO 检查点（其本身使用 πref(0)\pi_{\mathrm{ref}}^{(0)} 作为其参考），r̂ϕ​(x,y)\hat{r}_{\phi}(x,y) 为由集成 ϕ={ϕk}k=1K\phi=\{\phi_{k}\}_{k=1}^{K} 参数化的学习代理奖励。真实奖励 r⋆​(x,y)r^{\star}(x,y) 可验证（GSM8K 精确答案准确度）且仅在评估期间观察，训练期间从不观察。

**定义 3.1（Goodhart 间隙）**

在在线步骤 tt，定义批次平均归一化奖励

r̃proxy​(t)=r̄proxy​(t)|r̄proxy​(0)|+ε, r̃true​(t)=r̄true​(t)|r̄true​(0)|+ε,\tilde{r}_{\mathrm{proxy}}(t)=\frac{\bar{r}_{\mathrm{proxy}}(t)}{\lvert\bar{r}_{\mathrm{proxy}}(0)\rvert+\varepsilon},\quad\tilde{r}_{\mathrm{true}}(t)=\frac{\bar{r}_{\mathrm{true}}(t)}{\lvert\bar{r}_{\mathrm{true}}(0)\rvert+\varepsilon},

其中 ε=ϵfloat32\varepsilon=\epsilon_{\mathrm{float32}}。Goodhart 间隙为

𝒢​(t;β)=r̃proxy​(t)−r̃true​(t).\mathcal{G}(t;\beta)=\tilde{r}_{\mathrm{proxy}}(t)-\tilde{r}_{\mathrm{true}}(t).

(2)

**定义 3.2（AUGC）**

曲线下面积（AUGC）测量在线运行期间的累积黑客攻击损害：

AUGC​(β)=∫0Tmax⁡(𝒢​(t;β), 0)​dt.\mathrm{AUGC}(\beta)=\int_{0}^{T}\max\!\bigl(\mathcal{G}(t;\beta),\,0\bigr)\,\mathrm{d}t.

(3)

本文的中心问题是：**AUGC(β)\mathrm{AUGC}(\beta) 随 β\beta 增加还是减少？**

## 4 实验设置

### 4.1 模型与数据

#### 策略模型

我们使用 Qwen/Qwen3-14B 作为策略，以 4 位 NF4 QLoRA 量化（Dettmers et al., [2023](#bib.bib22)）加载，LoRA 适配器（Hu et al., [2021](#bib.bib21)）应用到所有注意力投影矩阵。LoRA 秩 rr 源自架构：

r=2⌊log2⁡hhidden⌉, α=2​r,r=2^{\lfloor\log_{2}\sqrt{h_{\mathrm{hidden}}}\rceil},\quad\alpha=2r,

(4)

其中 ⌈⋅⌉\lceil\cdot\rceil 表示舍入到最近整数，hhidden\h_{\mathrm{hidden}} 是模型隐藏维度。丢弃率源自数据集：pdrop=clip​(32/n, 0.01, 0.10)p_{\mathrm{drop}}=\mathrm{clip}(32/\sqrt{n},0.01,0.10)，其中 nn 是训练示例数。

#### 奖励集成

三个独立的 Qwen/Qwen3-1.7B 序列分类器（也是 QLoRA）用自助重新采样训练，以产生平均奖励和认知不确定性（集成标准差）。每个成员用 Bradley–Terry 偏好损失训练（Bradley and Terry, [1952](#bib.bib29)）：

ℒBT=−𝔼(x,yw,yl)∼𝒟⁡log⁡σ​(rϕ​(x,yw)−rϕ​(x,yl)).\mathcal{L}_{\mathrm{BT}}=-\operatorname{\mathbb{E}}_{(x,y_{w},y_{l})\sim\mathcal{D}}\log\sigma\!\bigl(r_{\phi}(x,y_{w})-r_{\phi}(x,y_{l})\bigr).

(5)

#### 偏好数据

离线 DPO 和奖励模型训练使用 HuggingFaceH4/ultrafeedback_binarized（Cui et al., [2024](#bib.bib24)），分割 80/10/10。

#### 可验证任务

在线真实奖励在 openai/gsm8k（主要）上评估（Cobbe et al., [2021](#bib.bib25)），在提取 #### 分隔符后的数字后使用精确答案匹配。

### 4.2 推导 β\beta 网格

我们不任意选择 β\beta 值。相反，我们计算冻结参考策略 πref(0)\pi_{\mathrm{ref}}^{(0)} 下的每个示例绝对对数比幅度：

δi=|logπref(0)(yw(i)∣x(i))−logπref(0)(yl(i)∣x(i))|.\delta_{i}=\bigl\lvert\log\pi_{\mathrm{ref}}^{(0)}(y_{w}^{(i)}\mid x^{(i)})-\log\pi_{\mathrm{ref}}^{(0)}(y_{l}^{(i)}\mid x^{(i)})\bigr\rvert.

(6)

三个 β\beta 值取自 {δi}\{\delta_{i}\} 的第 20、50 和 80 百分位数，按中位数绝对对数比归一化：

βj=pctpj​({δi})median​({δi})+ε, (p1,p2,p3)=(20,50,80).\beta_{j}=\frac{\mathrm{pct}_{p_{j}}(\{\delta_{i}\})}{\mathrm{median}(\{\delta_{i}\})+\varepsilon},\quad(p_{1},p_{2},p_{3})=(20,50,80).

(7)

这使三个保守主义水平与实际偏好信号幅度**相称**，而不是任意的数值选择。

### 4.3 离线 DPO 训练

对于每个 β∈{βlo,βmid,βhi}\beta\in\{\beta_{\mathrm{lo}},\beta_{\mathrm{mid}},\beta_{\mathrm{hi}}\}，我们使用方程 1 通过 TRL DPOTrainer（Von Werra et al., [2022](#bib.bib33)）微调独立的 LoRA 适配器。每设备批大小、梯度累积、学习率和梯度剪裁都源自硬件属性和训练集大小（详见附录 C 的推导公式）。

### 4.4 在线自适应循环

离线 DPO 后，每个检查点使用目标进行在线自适应

ℒonline=−𝔼τ∼πθ​[Â​(x,y)⋅log⁡πθ​(y∣x)]+κ​(β)⋅𝔼​[(log⁡πθ​(y∣x)−log⁡πref​(y∣x))2].\mathcal{L}_{\mathrm{online}}=-\mathbb{E}_{\tau\sim\pi_{\theta}}\!\Bigl[\hat{A}(x,y)\cdot\log\pi_{\theta}(y\mid x)\Bigr]\\
+\kappa(\beta)\cdot\mathbb{E}\!\Bigl[\bigl(\log\pi_{\theta}(y\mid x)-\log\pi_{\mathrm{ref}}(y\mid x)\bigr)^{2}\Bigr].

(8)

其中归一化优势为

Â​(x,y)=r̂​(x,y)−μr̂σr̂+ε,\hat{A}(x,y)=\frac{\hat{r}(x,y)-\mu_{\hat{r}}}{\sigma_{\hat{r}}+\varepsilon},

(9)

自适应 KL 系数为

κ​(β)=βQpKL​(|log⁡πθ−log⁡πref|)+ε.\kappa(\beta)=\frac{\beta}{Q_{p_{\mathrm{KL}}}\!\bigl(\lvert\log\pi_{\theta}-\log\pi_{\mathrm{ref}}\rvert\bigr)+\varepsilon}.

(10)

这里 QpKLQ_{p_{\mathrm{KL}}} 表示当前批上绝对 KL 值的经验 pKLp_{\mathrm{KL}} 百分位数。这种归一化使 KL 惩罚对于策略的发散水平为尺度不变。

## 5 机制分析

为了解释悖论，我们识别了三个因果联系，如图 2 所示：熵压缩、OOD 距离放大和不确定性驱动的利用。

5.1 链接 1：熵压缩

我们测量每个 DPO 检查点在固定探针集上的平均令牌级熵，该集包含 nprobe=⌈|Dtest|⌉\n_{\mathrm{probe}}=\lceil\sqrt{|D_{\mathrm{test}}|}\rceil 个 GSM8K 提示：

H(β)=−1|𝒳probe|​∑x∈𝒳probe1|x|​∑t∑v∈𝒱πθ(β)​(v∣x<t)​log⁡πθ(β)​(v∣x<t).H^{(\beta)}=-\frac{1}{|\mathcal{X}_{\mathrm{probe}}|}\sum_{x\in\mathcal{X}_{\mathrm{probe}}}\frac{1}{|x|}\sum_{t}\sum_{v\in\mathcal{V}}\pi_{\theta}^{(\beta)}(v\mid x_{<t})\log\pi_{\theta}^{(\beta)}(v\mid x_{<t}).

(11)

**命题 5.1（熵–保守主义单调性）**

在 DPO 损失景观的温和正则性条件下，平衡策略熵 H(β)H^{(\beta)} 在 β\beta 中非递增：

β1≤β2⇒H(β1)≥H(β2).\beta_{1}\leq\beta_{2}\;\Rightarrow\;H^{(\beta_{1})}\geq H^{(\beta_{2})}.

我们进一步观察**熵坍缩**：在在线自适应后，高β\beta 策略的熵比低β\beta 策略减少更多。这被测量为 ΔH(β)=HDPO(β)−Honline(β)\Delta H^{(\beta)}=H_{\mathrm{DPO}}^{(\beta)}-H_{\mathrm{online}}^{(\beta)}。

### 5.2 链接 2：奖励模型的 OOD 距离

设 𝐡ϕ​(x,y)∈ℝd\mathbf{h}_{\phi}(x,y)\in\mathbb{R}^{d} 表示奖励集成成员 ϕ0\phi_{0} 对于输入 (x,y)(x,y) 的平均池化倒数第二层隐藏状态。我们将分布外距离测量为生成响应的隐藏状态与 UltraFeedback 训练分布质心之间的余弦距离：

dcos(β)=1−𝐡ϕ​(x,y(β))⊤​μref‖𝐡ϕ​(x,y(β))‖2​‖μref‖2,d_{\cos}^{(\beta)}=1-\frac{\mathbf{h}_{\phi}(x,y^{(\beta)})^{\top}\,\mu_{\mathrm{ref}}}{\|\mathbf{h}_{\phi}(x,y^{(\beta)})\|_{2}\,\|\mu_{\mathrm{ref}}\|_{2}},

(12)

其中 μref=1nref​∑i=1nref𝐡ϕ​(xi,yiuf)\mu_{\mathrm{ref}}=\frac{1}{n_{\mathrm{ref}}}\sum_{i=1}^{n_{\mathrm{ref}}}\mathbf{h}_{\phi}(x_{i},y_{i}^{\mathrm{uf}}) 是从 nref=⌈|Dtrain|⌉\n_{\mathrm{ref}}=\lceil\sqrt{|D_{\mathrm{train}}|}\rceil 个 UltraFeedback 训练示例计算的参考质心。我们也计算平均成对余弦距离作为响应多样性度量。

### 5.3 链接 3：不确定性驱动的利用

集成不确定性信号为

û​(x,y)=1K−1​∑k=1K(rϕk​(x,y)−r̄​(x,y))2,\hat{u}(x,y)=\sqrt{\frac{1}{K-1}\sum_{k=1}^{K}\bigl(r_{\phi_{k}}(x,y)-\bar{r}(x,y)\bigr)^{2}},

(13)

其中 r̄​(x,y)=K−1​∑krϕk​(x,y)\bar{r}(x,y)=K^{-1}\sum_{k}r_{\phi_{k}}(x,y)。当 û\hat{u} 高时，各个成员对响应的真实奖励强烈不一致。在线优化器最大化 r̄\bar{r}，但不一致意味着景观不可靠。策略快速找到欺骗一些但不是所有集成成员的响应——一种经典的分布式奖励黑客攻击形式（Pan et al., [2022](#bib.bib9)）。

我们计算每个 β\beta 条件的 û\hat{u} 和 𝒢\mathcal{G} 时间序列之间的 Pearson 相关性 ρUQ​(β)\rho_{\mathrm{UQ}}(\beta)，并在总结表中报告关系（表 1）。

## 6 理论：最优保守主义

建立了经验和机制案例后，我们现在问：**最优的 β\beta 是什么？**

**定义 6.1（最优保守主义）**

设 𝒜​(β)\mathcal{A}(\beta) 表示离线对齐质量（例如，相对于 πref(0)\pi_{\mathrm{ref}}^{(0)} 的胜率），AUGC(β)\mathrm{AUGC}(\beta) 在线黑客攻击损害。最优保守主义 β⋆\beta^{\star} 求解

β⋆=arg​minβ>0⁡AUGC​(β)−λ⋅𝒜​(β),\beta^{\star}=\operatorname*{arg\,min}_{\beta>0}\mathrm{AUGC}(\beta)-\lambda\cdot\mathcal{A}(\beta),

其中 λ>0\lambda>0 权衡对齐与黑客攻击风险。

对于经验近似，我们将幂律拟合到观察的 (β,AUGC)(\beta,\mathrm{AUGC}) 数据：

AUGC​(β)≈a⋅βb+c, a,b,c>0.\mathrm{AUGC}(\beta)\approx a\cdot\beta^{b}+c,\quad a,b,c>0.

(14)

参数 (a,b,c)(a,b,c) 通过最小二乘优化获得，初始化源自数据范围（见附录 E）。实际 β⋆\beta^{\star} 定义为 AUGC 超过 1.5×minβ′AUGC(β′)1.5\times\min_{\beta^{\prime}}\mathrm{AUGC}(\beta^{\prime}) 的最小 β\beta：

β⋆=inf{β:AUGC​(β)>1.5⋅(c+a⋅βminb)}.\beta^{\star}=\inf\!\bigl\{\beta:\mathrm{AUGC}(\beta)>1.5\cdot(c+a\cdot\beta_{\min}^{b})\bigr\}.

(15)

**命题 6.2（幂律黑客攻击损害）**

如果方程 14 成立且 b>1b>1，则边际黑客攻击成本在 β\beta 中超线性增长：

∂2∂β2​AUGC​(β)=a​b​(b−1)​βb−2>0\frac{\partial^{2}}{\partial\beta^{2}}\mathrm{AUGC}(\beta)=a\,b\,(b-1)\,\beta^{b-2}>0.

这意味着超过 β⋆\beta^{\star}，保守主义的小幅增加会导致不成比例的大的黑客攻击风险。
## 7 结果

### 7.1 Goodhart 间隙轨迹

图 3 显示了所有三个 β\beta 水平的在线自适应步骤中的 Goodhart 间隙 𝒢(t;β)\mathcal{G}(t;\beta)。黑客攻击阈值 τhack\tau_{\mathrm{hack}} 设置为所有正间隙值的第 75 百分位数，源自数据（不是手调）。关键观察：(a) Goodhart 间隙在整个过程中主要为负，表明代理奖励高估了真实性能；(b) 低 β\beta （β=0.310\beta=0.310）显示最不稳定的轨迹，振荡到 −3×106−3\times 10^{6}，而中间 β\beta 和高 β\beta 保持接近零；以及 (c) 累积黑客攻击损害（AUGC）仍然由 β\beta 单调排序（31.1、43.0、145.8），确认了悖论。

### 7.2 AUGC 总结

表 1 报告了每个 β\beta 条件的 AUGC、平均不确定性、黑客攻击起始步骤和 UQ 间隙 Pearson 相关性。β\beta 和 AUGC 之间的 Spearman 秩相关性为 ρ=1.0\rho=1.0（完美单调排序），确认了悖论。

### 7.3 熵坍缩

图 4 总结了熵测量。左面板显示 DPO 检查点熵在所有三个 β\beta 水平上几乎相同（≈0.81\approx 0.81–0.82），在较高的 β\beta 时只有轻微下降，与命题 5.1 大体一致。右面板揭示了意外的模式：低 β\beta 显示小**正**熵坍缩（≈+0.004\approx{+}0.004），中间 β\beta 接近零，高 β\beta 显示**负**坍缩（≈−0.0025\approx{-}0.0025），意味着最保守的策略在在线自适应期间**获得**熵而不是失去它。

### 7.4 OOD 距离和 β⋆\beta^{\star} 曲线

图 5 显示了拟合的幂律曲线叠加在三个 AUGC 数据点上。安全区域 [0,β⋆][0,\beta^{\star}] 和危险区域 (β⋆,∞)(\beta^{\star},\infty) 被着色。拟合优度 R2=1.0R^{2}=1.0（在三个数据点处精确拟合），但幂律形式为实际设计指导提供平滑外推。

## 8 讨论

### 8.1 为什么悖论很重要

传统的保守离线 RL 论证是一个**支持**论证：在行为策略的支持中训练数据，奖励模型在那里很好地泛化。我们的悖论揭示了一个微妙的冲突：高β\beta DPO 策略的支持可能与奖励模型训练数据的支持相当不同，即使 DPO 策略保持接近 πref\pi_{\mathrm{ref}}。这发生是因为 DPO 将质量集中在 πref\pi_{\mathrm{ref}} 分配高密度的低熵区域，但奖励模型在多样的人类偏好数据上训练。"DPO 策略生成的内容"和"奖励模型训练的内容"的交集对于高 β\beta **较小**，而不是较大。

### 8.2 与保守离线对在线框架的连接

配套论文（研讨会草稿）提出了一个适用于离线 RL 和离线 BO 的统一保守循环。我们的发现提供了该循环何时可能失效的具体经验例证：当离线阶段使用代理奖励（DPO）其隐含奖励模型与在线使用的奖励模型**不同**时。离线对齐步骤使用一个质量测量压缩策略；在线步骤优化不同的（学习的）测量。不匹配是悖论的根源。

### 8.3 局限性

我们的研究使用单个硬件目标（H100 80GB）、三个 β\beta 值和特定的策略/奖励模型组合（Qwen3-14B/Qwen3-1.7B）。幂律拟合在三个点处精确，从构造；R²=1.0\R^{2}=1.0 声明不应被解释为函数形式的强证据，仅作为内插装置。需要更广泛的研究，涉及更多 β\beta 值、多个模型族和多个下游任务来推广发现。

## 9 结论

我们展示了保守离线训练可以放大而不是减弱在线自适应期间的奖励黑客攻击。机制是一个三链链：高β\beta DPO 压缩策略熵，推动生成的响应超出奖励模型的训练分布，创造可利用的认知不确定性。我们将 Goodhart 间隙及其曲线下面积形式化为主要评估指标，从幂律拟合推导最优保守主义水平 β⋆\beta^{\star}，并为校准保守主义提供算法建议。这些发现指向对安全离线对在线对齐的更丰富的观点：一种明确考虑离线对齐信号和在线代理奖励之间分布不匹配的观点。

## 参考文献

R. A. Bradley and M. E. Terry (1952)
Rank analysis of incomplete block designs: i. the method of paired comparisons.
Biometrika 39 (3/4),  pp. 324–345.
引用者：§4.1.

L. Chen, K. Lu, A. Rajeswaran, K. Lee, A. Grover, M. Laskin, P. Abbeel, A. Srinivas, and I. Mordatch (2021)
Decision transformer: reinforcement learning via sequence modeling.
外部链接：2106.01345，[链接](https://arxiv.org/abs/2106.01345)
引用者：§2.4.

P. Christiano, J. Leike, T. B. Brown, M. Martic, S. Legg, and D. Amodei (2023)
Deep reinforcement learning from human preferences.
外部链接：1706.03741，[链接](https://arxiv.org/abs/1706.03741)
引用者：§1.

K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, C. Hesse, and J. Schulman (2021)
Training verifiers to solve math word problems.
外部链接：2110.14168，[链接](https://arxiv.org/abs/2110.14168)
引用者：§4.1.

G. Cui, L. Yuan, N. Ding, G. Yao, B. He, W. Zhu, Y. Ni, G. Xie, R. Xie, Y. Lin, Z. Liu, and M. Sun (2024)
UltraFeedback: boosting language models with scaled ai feedback.
外部链接：2310.01377，[链接](https://arxiv.org/abs/2310.01377)
引用者：§4.1.

T. Dettmers, A. Pagnoni, A. Holtzman, and L. Zeltmoyer (2023)
QLoRA: efficient finetuning of quantized llms.
外部链接：2305.14314，[链接](https://arxiv.org/abs/2305.14314)
引用者：§4.1.

L. Gao, J. Schulman, and J. Hilton (2022)
Scaling laws for reward model overoptimization.
外部链接：2210.10760，[链接](https://arxiv.org/abs/2210.10760)
引用者：§2.2.

C. A. E. Goodhart (1975)
Problems of monetary management: the UK experience.
Papers in Monetary Economics 1.
注：通常引用为 "Goodhart's Law"（1984 再版）
引用者：§2.2.

E. J. Hu, Y. Shen, Y. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, and W. Chen (2021)
LoRA: low-rank adaptation of large language models.
外部链接：2106.09685，[链接](https://arxiv.org/abs/2106.09685)
引用者：§4.1.

R. Kidambi, A. Rajeswaran, P. Netrapalli, and D. Joachims (2021)
MOReL : model-based offline reinforcement learning.
外部链接：2005.05951，[链接](https://arxiv.org/abs/2005.05951)
引用者：§2.3.

I. Kostrikov, A. Nair, and S. Levine (2021)
Offline reinforcement learning with implicit q-learning.
外部链接：2110.06169，[链接](https://arxiv.org/abs/2110.06169)
引用者：§2.4.

A. Kumar, A. Zhou, G. Tucker, and S. Levine (2020)
Conservative q-learning for offline reinforcement learning.
外部链接：2006.04779，[链接](https://arxiv.org/abs/2006.04779)
引用者：§2.3, §2.4.

B. Lakshminarayanan, A. Pritzel, and B. Blundell (2017)
Simple and scalable predictive uncertainty estimation using deep ensembles.
外部链接：1612.01474，[链接](https://arxiv.org/abs/1612.01474)
引用者：§2.3.

C. Lyle, Z. Zheng, E. Nikishin, B. A. Pires, R. Pascanu, and W. Dabney (2023)
Understanding plasticity in neural networks.
外部链接：2303.01486，[链接](https://arxiv.org/abs/2303.01486)
引用者：附录 G.

A. Pan, K. Bhatia, and J. Steinhardt (2022)
The effects of reward misspecification: mapping and mitigating misaligned models.
外部链接：2201.03544，[链接](https://arxiv.org/abs/2201.03544)
引用者：§5.3.

R. Rafailov, A. Sharma, E. Mitchell, S. Ermon, C. D. Manning, and A. Finn (2024)
Direct preference optimization: your language model is secretly a reward model.
外部链接：2305.18290，[链接](https://arxiv.org/abs/2305.18290)
引用者：§1, §2.1.

J. Skalse, N. H. Howe, D. Krasheninnikov, and D. Krueger (2025)
Defining and characterizing reward hacking.
外部链接：2209.13085，[链接](https://arxiv.org/abs/2209.13085)
引用者：§2.2.

L. Von Werra, Y. Belkada, L. Tunstall, E. Beeching, T. Thrush, N. Lambert, and S. Huang (2022)
TRL: transformer reinforcement learning.
注：[https://github.com/huggingface/trl](https://github.com/huggingface/trl)
引用者：§4.3.
