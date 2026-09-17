# PDE 网络的潜表征能否对应 Fourier 模态？

2026-09-16 · 文献调研、最新 main 代码核查与实验建议

> 2026-09-17 更新：用户已将主目标明确为通过 latent 系数干预实现选择性的物理模态编辑。请先读 [新的目标与 backbone 建议](../../nn-fitting/latent-modal-control-target.md)，它依据最新 main `629ed59`。下文及配套结构验证保留为 `9b02157` 的历史调研；其中旧 attention API 和无条件幅值结论不能不加区分地套用到新版 conditioned attention。

**结论：可行，而且值得做；但应把问题从“最大的 latent 特征向量是否等于最大的 Fourier 项”，改成“模型是否形成并使用了与物理频率、模态演化相一致的潜在子空间”。** 前一种匹配可能只是数据分布、坐标缩放或网络结构带来的现象；后一种问题可以通过干预、对照和解析 PDE 来检验。

最接近的先行工作已经有明确名称：**latent Fourier analysis**。因此，不能把“首次把潜空间谱分解用于 PDE”作为贡献。更适合当前项目的切入点，是解释现有 attention / FNO / DeepONet 为什么在热方程和 Allen–Cahn 上表现不同，并找出它们实际学到了、或者结构上无法学到的谱规律。

本文已读取远端最新 main `9b02157`，不是基于最初的旧工作副本。文中的模型训练结果属于已有项目记录；本轮仅新增一次很小的结构验证，没有重新训练模型，也没有得到“latent 已与 Fourier 对齐”的实证结论。

## 1. 可以直接拿去讨论的研究构想

> 我们希望研究 PDE 神经算子的内部表征，而不只比较最终回归误差。具体而言，考察 encoder 将终端条件映射到潜在表征后，是否形成与物理 Fourier 频率子空间对应的结构，以及 decoder 是否利用这些结构恢复解的模态幅值、相位和非线性耦合。首先以具有解析谱传播规律的热方程建立参照，区分输入数据的频谱结构与模型学到的 PDE 作用；随后在 Allen–Cahn 方程中检验高次谐波生成和跨幅值响应。通过潜表征谱分析、解码方向干预、未训练网络与 POD 对照，以及分布变化实验，判断这种对应究竟反映了输入统计、架构先验，还是可泛化的算子规律。

建议题目：**从预测精度到谱机制：PDE 神经算子潜表征的识别与干预**。

这里仍然是在研究回归模型。研究价值来自更明确的解释、适用边界与数学保证；回归任务本身并不妨碍产生有意义的研究。

## 2. 最新 main 里，实际应该分析什么

已核对 [NN 研究说明](../../nn-fitting/README.md)、[operator 实现](../../../../parabolab/deep/opnet.py)、[attention 核心](../../../../parabolab/deep/setnet.py)、[PDE 数据族](../../../../parabolab/deep/families.py) 和 [D03 研究记录](../../../superpowers/specs/2026-09-16-phi-operator-design.md)。相对链接均从本报告目录出发；模型细节以代码为准。

当前任务是固定 PDE 下的函数映射

\[
\phi(\cdot)\longmapsto u(0,\cdot),\qquad u(T,x)=\phi(x),\quad T=0.3.
\]

它已经是函数到函数的 operator learning。三个 backbone 的“latent”并不相同：

- **Attention：** `AttnOperator.core.encoder` 的输出是 `h:(B,S,D)`，默认 `S=101,D=128`。这是带传感器索引的特征集合，每个样本有 12,928 个数，并非一个紧凑低维向量。随后 `norm_c(h)` 进入 cross-attention，与坐标 query 一起生成输出。适合从 `h`、实际供 decoder 使用的 `norm_c(h)`、以及 cross-attention 后的 query features 分层观察。
- **DeepONet：** `branch(phi)` 是默认 64 维的函数编码；`gelu(trunk(t,x))` 给出空间基函数，输出是二者的内积。对 branch 系数变化，经 trunk 直接得到物理空间变化，是最容易建立清晰谱解释的对照。它的单个 trunk 通道仍有换基自由度，不能天然称为某个 Fourier 模态。
- **FNO：** `lift` 和各层的特征为 `(B,W,S)`，默认 `W=32`。`SpectralConv1d` 已直接调用 `rfft/irfft`；观察到 Fourier 成分本身不是自主发现的证据。应检验学到的频率增益、跨频率响应及非线性耦合。输入还包含绝对坐标，且使用有限网格，因此不能无条件声称整个网络严格平移等变。

Attention 的 decoder 还使用输入均值、标准差及坐标统计；不能把整个模型简写为只依赖 `h` 的 `D(h)`。准确写法是

\[
\widehat u(x)=D(h;\mu_\phi,s_\phi,\mu_x,s_x,x).
\]

最新 main 的已有记录显示：FNO 在 heat 上较好，attention 在 Allen–Cahn 上较好。记录也明确承认：关于这一差异的谱机制解释尚未通过机制实验验证。这正是本想法可以接上的问题，而不是需要从头另建一套无关框架。

另外，现有 driver 主要保存误差 CSV，没有模型 checkpoint 保存逻辑。本轮没有取得对应的训练后权重；不能从 CSV 反推内部 latent。开展正式实验前需要保存或重新训练 checkpoint，并保留模型初始化、数据划分、scaler 和配置。

## 3. 文献：哪些已经有人做，哪些能借鉴

检索截至 2026-09-16。以下是有界检索中的主要原始来源，不代表穷尽所有先行工作。

**首先读这三篇。**

1. **Page, Brenner & Kerswell，2021，*Revealing the state space of turbulence using machine learning*.** 对流场 autoencoder 提出 latent Fourier analysis，利用空间平移在潜空间中的作用识别模态，再解码为有意义的结构。这是最直接先行工作。[论文与公开版本](https://arxiv.org/abs/2008.07515)
2. **Page, Holey, Brenner & Kerswell，2024，*Exact coherent structures in two-dimensional turbulence identified with convolutional autoencoders*.** 将上述思路用于更丰富的湍流状态，并借助潜模态寻找不稳定周期轨道。其技术对象是 latent translation operator；退化子空间内部再做 SVD。应重点读 §3.1，而不能把该方法概括成“对 latent 做 PCA”。[原文](https://arxiv.org/html/2309.12754v1) · [正式发表版本](https://doi.org/10.1017/jfm.2024.552)
3. **Ouyang, Ke & Wang，2025，*Fourier-Invertible Neural Encoder (FINE) for Homogeneous Flows*.** 使用可逆滤波、单调激活与显式 Fourier 截断瓶颈，研究平移对称数据的可解释压缩。它是非常接近的架构对照，但 Fourier 被写进模型，不能作为普通 encoder 自主发现 Fourier 的证据。按预印本引用；核对版本为 2025-11-29 的 v3。[原文](https://arxiv.org/html/2505.15329v3)

**把 GAN 的直觉转成可检验方法。**

4. **Härkönen et al.，2020，*GANSpace: Discovering Interpretable GAN Controls*.** 用 PCA 等方法找到可控制生成结果的潜方向。值得迁移的是“提取方向—扰动—观察结果”的流程；视觉语义方向不自动对应 PDE 的数学本征模态。[原文](https://proceedings.neurips.cc/paper/2020/file/6fe43269967adbb64ec6149852b5cc3e-Paper.pdf)
5. **Shen & Zhou，2021，*Closed-Form Factorization of Latent Semantics in GANs*（SeFa）.** 对生成器仿射权重构造的矩阵做谱分解，寻找影响较大的方向。它分解的是权重相关矩阵，不是 latent 数据协方差，更不是 PDE 算子。[论文](https://arxiv.org/abs/2007.06600)

**把 latent 表征与 PDE、动力学连接起来。**

6. **Venturi & Casey，2023，*SVD Perspectives for Augmenting DeepONet Flexibility and Interpretability*.** 将 DeepONet 的空间基、系数与 SVD/POD 联系起来，适合作为当前 DeepONet 分析的直接参照。[论文](https://arxiv.org/abs/2204.12670)
7. **Murata, Fukami & Fukagata，2020，*Nonlinear mode decomposition with convolutional neural networks for fluid dynamics*.** 用 mode-decomposing autoencoder 分析流场；非线性潜模态可混合多个 POD 模态，提醒我们不能预设一对一匹配。[论文](https://doi.org/10.1017/jfm.2019.822)
8. **Lusch, Kutz & Brunton，2018，*Deep learning for universal linear embeddings of nonlinear dynamics*.** 用深度学习寻找适合线性演化描述的 Koopman 表示。可借鉴“让 latent 带有动力学含义”，但 Koopman 特征函数定义在状态空间上，不能直接等同于物理空间中的正弦波。[开放全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC6251871/)
9. **Li et al.，2021，*Fourier Neural Operator for Parametric Partial Differential Equations*.** 在 Fourier 空间参数化积分核。适合当明确使用谱先验的对照。[论文](https://arxiv.org/abs/2010.08895)
10. **Wu et al.，2023，*Solving High-Dimensional PDEs with Latent Spectral Models*.** 在紧凑 latent 空间中学习谱形式的映射。“latent spectral”并不自动意味着找到了物理空间 Fourier 本征函数。[ICML 原文入口](https://proceedings.mlr.press/v202/wu23f.html)
11. **Kontolati et al.，2024，*Learning nonlinear operators in latent spaces for real-time predictions of complex dynamics in physical systems*.** L-DeepONet 将 autoencoder 与 latent operator learning 结合，主要提供预测和效率证据；不是潜协方差恢复物理频谱的定理。[论文](https://www.nature.com/articles/s41467-024-49411-w)
12. **Viknesh & Arzani，2025 预印本、2026 修订，*Differentiable Autoencoding Neural Operator for Interpretable and Integrable Latent Space Modeling*（DIANO）.** 在空间粗化的 latent 表示中放入可微 PDE 求解器，说明“latent 的物理含义”已有更强的结构化路线。其物理约束与 Fourier 层属于预置结构。[当前公开版本](https://arxiv.org/abs/2510.00233)

**用于避免解释过度的基础参照。**

13. **Towne, Schmidt & Colonius，2018，*Spectral proper orthogonal decomposition and its relationship to dynamic mode decomposition and resolvent analysis*.** 区分统计能量、时空相干性与动力学模态。这里 SPOD 的时间频率不能混成空间波数。[论文](https://arxiv.org/abs/1708.04393)
14. **Hyvärinen, Sasaki & Turner，2019，*Nonlinear ICA Using Auxiliary Variables and Generalized Contrastive Learning*.** 可辨识性需要具体假设；普通重建或预测损失不会自动确定物理坐标。[AISTATS 原文](https://proceedings.mlr.press/v89/hyvarinen19a.html)

由这些文献作出的判断：**“latent 能做谱解释”已有直接先例；“当前预测网络的谱解释能否经受干预、幅值变化和模型对照”仍是值得具体研究的问题。** 是否形成论文级新贡献，还要对这一窄问题继续核查，不能由本次检索直接宣称首创。

## 4. 原始想法需要修正的数学对象

### 4.1 对什么做 eigen decomposition？

一个 latent 向量 `z` 本身没有这里想要的特征分解。可以选择以下不同对象，但它们回答不同问题。

**协方差：** 对独立函数样本编码为 \(z_i\in\mathbb R^d\)，中心化后

\[
C_z=\frac{1}{N-1}\sum_i(z_i-\bar z)(z_i-\bar z)^T.
\]

特征向量是数据变化最大的潜方向。对 attention，必须声明是把 `S×D` 展平后做样本 PCA，还是对一个函数的空间特征矩阵 `H∈R^{S×D}` 做 SVD：前者分析函数之间的差异，后者分析一个函数内部的空间变化。二者不能混称。

**空间平移：** 在周期域定义 \((T_\delta\phi)(x)=\phi(x+\delta)\)，拟合

\[
E(T_\delta\phi)\approx R_\delta E(\phi).
\]

这里的特征值相位用于标记空间频率。这是与 Fourier 联系最直接的路线，已有 Page 等的先行工作。

**时间演化：** 对完整状态快照拟合 \(E(v_{\tau+\Delta\tau})\approx K E(v_\tau)\)。这里研究的是演化谱。当前模型训练的是固定时刻 \(\phi\mapsto u(0)\)，没有训练 latent 时间推进器；不能把 encoder 层编号视为物理时间，也不能直接声称已经研究 Koopman 谱。

**解码敏感性：** `J_D` 往往是长方形矩阵，应做 SVD，或者分析 \(J_D^T WJ_D\)。它表示局部输出变化强度，依赖基点与物理范数。若分析所谓“核”，也必须先说明是 attention 权重、特征 Gram 矩阵还是积分算子；它们既不一定对称，也不一定正定。

### 4.2 “最大的 Fourier 项”不等于“最大的本征值”

设 \(\widehat\phi_k\) 是 Fourier 系数。最大的 \(|\widehat\phi_k|^2\) 表示某个输入的主导能量。热方程生成元的本征值则是 \(-\nu k^2\)，时间推进倍率是 \(e^{-\nu k^2\tau}\)，样本协方差还取决于输入系数方差。三种排序可能不同。

应分别问：哪个频率能量大？哪个频率衰减慢？网络是否正确表示该频率的传播？不要先假设它们是同一个排序。

### 4.3 必须把方向放回同一个物理空间

潜方向 \(v\in\mathbb R^d\) 与 \(e^{ikx}\) 不是同一空间里的对象。可以在指定样本及固定旁路统计量下计算

\[
\delta u_v(x)=\frac{D(z+\varepsilon v;x)-D(z-\varepsilon v;x)}{2\varepsilon}
\approx J_D(z)v,
\]

再对这个物理场做 Fourier 分析。`D(v)` 通常不是一个合理的“模态”，尤其在有偏置、非线性及条件输入时。

实值场的同一频率对应 \(\operatorname{span}\{\cos(k\omega x),\sin(k\omega x)\}\)。相位变化会旋转这两个方向，应比较子空间、投影误差或主角度，而不是逐根特征向量的符号和编号。

### 4.4 为什么 PCA 匹配既不是必要条件，也不是充分证据

**坐标反例。** 设 \(u=a_1\varphi_1+a_2\varphi_2\)，两基为 Fourier 模式，\(\operatorname{Cov}(a)=\operatorname{diag}(4,1)\)。令

\[
E(u)=(a_1/2,a_2),\qquad D(z)=2z_1\varphi_1+z_2\varphi_2.
\]

重建完全正确，但 latent 协方差为单位阵，任何旋转都是合法 PCA 基。更一般地，\(E'=AE,D'=D\circ A^{-1}\) 保持模型输出不变，却将协方差变为 \(AC_zA^T\)。因此，raw latent PCA 的排序不是表示固有的物理属性。

**数据反例。** 若样本总是 \(u=a(\sin x+\sin2x)\)，物理数据的第一主成分就是混合波，即使 encoder 是恒等映射也不会得到单个 Fourier 波。相反，周期、空间平移平稳数据具有卷积型协方差 \(C(x,y)=c(x-y)\)，Fourier 已经能对角化它；未学习 PDE 的数据 PCA 就可能“匹配成功”。

这些是本报告的初等解析说明，不是新发现的可辨识性定理。

## 5. 当前模型上，一个比“看起来像 Fourier”更有力的发现

### 5.1 Attention 的幅值旁路限制

代码把 \(\phi\) 标准化为 \((\phi-\mu_\phi)/s_\phi\)，`AttnOperator` 又固定 `stderr=0, params=0`。在同一坐标和 query 下，对于 \(\alpha>0\)，只要两次标准差均未触发数值下限，\(\alpha\phi+\beta\) 的标准化输入完全相同。因此

\[
h(\alpha\phi+\beta)=h(\phi),\qquad
\widehat{\mathcal G}(\alpha\phi+\beta)
=\alpha\widehat{\mathcal G}(\phi)+\beta.
\]

这是**当前实现的结构性约束**，适用于确定性前向计算；它不是训练后偶然发生的现象。只分析 `h` 会遗漏绝对幅值和均值通过输出旁路进入模型的事实。

热方程保持这种仿射关系，Allen–Cahn 一般不保持。令 \(v(\tau,x)=u(T-\tau,x)\)，则

\[
v_\tau=\tfrac12v_{xx}+v-v^3.
\]

对 \(v(0,x)=a\cos(\kappa x)\)，利用 \(\cos^3\theta=(3\cos\theta+\cos3\theta)/4\)，第三谐波的初始生成速率为

\[
\left.\partial_\tau\widehat v_{\cos(3\kappa)}\right|_{\tau=0}
=-\frac{a^3}{4}.
\]

幅值翻倍时，该速率变为八倍；当前 attention 的整幅输出只能同比变为两倍。故它不能对任意幅值和时间准确表示这一非线性算子族。这里的公式是短时导数；不能把它当成 \(\tau=0.3\) 时的精确有限时间解。

也可以针对固定终止时间做小幅值展开。令 \(\lambda_n=1-(n\kappa)^2/2\)，在固定有限 \(\tau>0\) 下，第三谐波满足

\[
c_3(\tau,a)=-\frac{a^3}{4}
\frac{e^{3\lambda_1\tau}-e^{\lambda_3\tau}}{3\lambda_1-\lambda_3}
+O(a^5),\qquad 3\lambda_1-\lambda_3=2+3\kappa^2>0.
\]

这是将 \(v=a v_1+a^3v_3+\cdots\) 代入方程后积分三次项得到的局部幅值展开，不是任意幅值下的精确解。因此，在当前固定 `T=0.3` 上也可以检验：模型的 `c3(a)/a` 被迫不变，而真解在小幅值区间的首项正比于 `a²`。

还可给出不依赖训练细节的误差下界。若真实算子为 \(S\)，取 \(\Delta=S(\alpha\phi)-\alpha S(\phi)\)，则任意满足上述齐次约束的模型 \(F\) 均有

\[
\max\{\|F(\phi)-S(\phi)\|,\|F(\alpha\phi)-S(\alpha\phi)\|\}
\ge \frac{\|\Delta\|}{1+\alpha}.
\]

这是直接由三角不等式得到的结构性限制；具体数值仍需可信的参考解。本轮未计算这一有限时间下界。

现有训练输入全部按离散峰值归一化到约 `0.9`，没有覆盖同一形状的独立幅值变化，所以这一限制**不否定原有分布内的准确度记录**。它说明原数据尚未检验一个关键物理能力。

### 5.2 本轮实际执行的最小验证

[可复现脚本](check_attention_scaling.py) 在最新代码上建立一个未训练、较小的 attention 网络（`D=16, layers=1, heads=4`），以 float64 检查上述恒等式：

- encoder 特征最大差：`6.66e-16`；
- 输出仿射关系最大残差：`2.78e-17`；
- 解析 Allen–Cahn 初始导数的离散 Fourier 核对：`a=0.2` 时第三谐波系数 `-0.002`，`a=0.4` 时 `-0.016`，比值约 `8`。

完整设置和输出见 [验证记录](attention-scaling-check.json)。这验证的是代码结构与初始导数计算，**没有使用训练后 checkpoint，也不是完整 PDE 演化实验**。一般结构结论来自前面的代数推导。

这个结果可以成为实际研究入口：先建立现有模型的可解释性边界，再测试把幅值统计显式传给 encoder/decoder 后，是否恢复正确的三次谐波响应。增加统计输入是待验证的候选改动，不代表已经解决问题。

## 6. 建议按这个顺序做实验

### 第一阶段：现有模型的事后诊断

先保存三种 backbone 在相同划分上的 checkpoint，固定 scaler、传感器、query、训练配置和随机种子。至少比较 3 个模型初始化，并按独立函数实例划分训练、验证和测试；同一个函数的平移、幅值变体不能跨集合泄漏。

在已有 `K=4` 数据上，分别提取 `h`、`norm_c(h)`、DeepONet branch 和 FNO 各层特征。对高维 attention 特征使用样本矩阵的截断 SVD，避免显式构造巨大的协方差。若保留完整 token 布局，这不是压缩模型；将来做 pooled bottleneck 属于另一个架构实验。

做两个不同读出任务：从 latent 预测输入 Fourier 系数，和从 latent 预测输出 Fourier 系数。先用有正则的线性 probe，只在训练集拟合并在验证集选超参数。同时报告 `h` 单独读出与加入均值、标准差后的读出。**可读出信息不等于模型使用了该信息**，因此后面必须有干预。

对于当前训练族，真实输入系数是 `A*a_k, A*b_k`，不是归一化前的原始高斯系数。相位、实部和虚部也要保留，不能只预测功率谱，否则平移造成的相位变化会被隐藏。

### 第二阶段：用热方程把“统计”与“物理传播”分开

当前周期长度为 16，\(\omega=\pi/8\)。解析答案为

\[
\widehat u_k(0)=g_k(T)\widehat\phi_k,
\qquad g_k(T)=\exp[-\tfrac12(k\omega)^2T].
\]

先用单频正弦、余弦和多频组合检验每个 \(g_k\)。再改变训练输入的频率能量排序：如果 PCA 排序随能量变，属于正常统计行为；真正的热传播倍率应保持不变。

不只看 latent PCA。对端到端函数映射，在 Fourier 系数方向上作小扰动，估计输入频率到输出频率的响应矩阵。热方程的参照为对角矩阵 `diag(g_k)`。这个诊断天然处在物理空间里，较少受隐藏坐标任意缩放的影响。

必要对照包括：原始数据 POD、已知 Fourier 传播、冻结随机 encoder 配相同容量的读出器、训练后的 encoder，以及已经使用 FFT 的 FNO。各方法使用相同数据划分；随机表征与训练表征的 probe 容量一致。未训练网络同样容易读出输入频率时，不能把读出成功归于学习了 PDE。

### 第三阶段：建立 latent 方向与物理变化之间的联系

对 DeepONet，branch 方向经过 trunk 得到精确线性输出方向。对 attention，固定所有旁路量和 query，做中央差分或 Jacobian-vector product，记录每个方向造成的输出频谱；再单独扰动旁路量。比较目标频率的投影能量、非目标频率泄漏、相位响应和模型误差变化。

不同 latent 方向的长度不可直接比较。应匹配它们解码后造成的物理 \(L^2\) 扰动大小，并明确所用积分权重。剔除几乎不影响输出的方向，不能让零响应因数值归一化获得漂亮的“纯度”。

做与同维随机子空间相比较的消融；同时用真实输入扰动检验是否仍在数据流形附近。一个潜方向影响输出，只支持模型内部机制；将其与真实 PDE 响应对照，才能进一步讨论物理意义。

如果采用 Page 式平移分析，可用潜编码矩阵 \(Z\) 和平移后的 \(Z_\delta\) 拟合 \(R_\delta=Z_\delta Z^+\)，或用验证集选择正则强度。高维 token 表征要先在训练集选定降维空间；均值偏置需要明确处理。除了拟合误差，还检查未见过的平移量和 \(R_{\delta+\eta}\approx R_\delta R_\eta\)。单一步长可能混叠多个波数，不能仅凭一组特征值宣布匹配成功。

### 第四阶段：Allen–Cahn 的非线性耦合与反证

先做同形状、不同幅值的 \(a\cos(k\omega x)\) 实验，不再统一归一化至峰值 0.9。用可靠周期参考解测量第三谐波及其幅值依赖，并保留短时解析导数作检查。比较原 attention 与向网络显式提供 `mu_phi,s_phi` 的变体，其他训练条件保持一致。

随后测试多个频率混合与训练分布外的能谱。Allen–Cahn 的 \(v^3\) 会让 Fourier 系数出现三重卷积，因而“一个 latent 方向对应多个输出频率”可能是正确的物理耦合；不能一律视为解释失败。应区分正确耦合、额外泄漏和压根没有表示出的频率。

新幅值族若仍使用 coding-tree 标签，需要重新检查该配置下标签的可用性与采样误差；第一轮机制核对可以直接使用解析热解和经过收敛检查的周期 Allen–Cahn 参考解。这样先把网络表征问题与 Monte Carlo 噪声问题分开。

时间演化谱/Koopman 是后续扩展：需要多个时间点、与时间有关的模型输入及训练目标。当前 FNO 的 `forward` 不使用 query 中的时间列，不具备这项实验条件。

## 7. 实施前必须处理的项目细节

**输入自带 Fourier 结构。** 当前 `K=4`，所有 \(\phi\) 位于最多八维的 Fourier 线性张成空间内；峰值归一化进一步限制可见幅值，正余弦高斯系数已经提供随机相位。先在这里验证工具合理，但论文不能仅靠这个数据族宣称发现通用数学结构。下一步至少换能谱权重、增加独立幅值、检验未见平移，并报告训练支持范围。

**周期网格重复端点。** 当前 101 点网格包含 `-8` 和 `8`，它们是同一周期位置。直接把全部 101 点交给常规 FFT，会把采样周期解释成 `101*dx`，与物理周期 16 不同。历史模型输入保持原样；事后谱分析可去掉重复端点，或在实际坐标上按已知正余弦基做加权投影。正式周期实验另建不重复端点的数据配置，不混改历史 benchmark。

对当前无零频项的四阶输入，101 点的等权样本均值实际上是 `phi(-8)/101`，并不等于连续场的零频系数。这使均值旁路也含有端点/相位信息。解释 encoder 和旁路时应分别使用模型实际统计量与物理积分统计量。

**参考解的边界条件。** `fd_reference_1d` 在扩展域上使用零通量边界，它不是严格的周期参考求解器。内部区间短时误差可能很小，但强行做精确平移等变或高次谐波结论时，需要周期边界参考，或独立证明边界误差相对目标效应可忽略。

**噪声与小模态。** 高频信号可能比 MC 噪声更弱。应在参考解上评估谱误差，必要时增加独立采样重复；不能把噪声主方向解释为 PDE 模态。

**降维与检验分离。** PCA、方向选择、probe、匹配和阈值都只用训练/验证数据。测试集只用于最终评估。通过重新排序测试结果来寻找最佳 Fourier 匹配会夸大解释性。

## 8. 怎样判断结果值不值得继续

建议先做一个小规模试验，再根据数值噪声确定并冻结阈值。以下是建议的探索性门槛，不是普适标准，也不是本轮测得的结果：

- 热方程的单频传播倍率在未见函数上的相对误差约 5% 以内，并报告最差频率；目标频率响应不能淹没在噪声中。
- 解码方向在指定频率子空间的能量占比达到约 90%，同时输出扰动显著非零；在多个种子、样本和足够小的步长上稳定。
- 训练后表征相对于随机 encoder 和 POD 的优势，有独立测试证据；仅“也能画出正弦波”不够。
- Allen–Cahn 的幅值与谐波响应经真实参考解检验，清楚记录原架构限制及候选改动的改善或失败。

若只能从 `h` 读出输入的四个频率，结论是“保留了输入频率信息”。若解码干预可选择性改变输出频率，结论可提升为“存在可控的谱表征”。若进一步恢复热传播和非线性耦合，并跨幅值、能谱分布成立，才有更强的依据说“模型学到了可迁移的算子结构”。这些仍是有明确测试范围的结论，不能等同于普遍理解 PDE。

最有希望的贡献有两个层次：一是用统一诊断区分数据频谱、网络表征和 PDE 动力学；二是以当前归一化旁路为具体例子，给出表达能力限制，并验证针对性的修正。第二层尤其容易形成明确的“问题—数学解释—实验反证—修正验证”链条。它的全球新颖性还没有得到确认。

## 9. 一个可作为理论起点的精确命题

以下是在理想假设下的推导，用来说明什么条件足以得到 Fourier 对应，不声称当前模型已经满足。

设周期为 \(L\)，\(\omega=2\pi/L\)。潜空间有线性平移表示 \(R_\delta\)，decoder 在平移不动点 \(z_*\) 邻域可微，并满足

\[
R_\delta z_*=z_*,\qquad D(R_\delta z)=T_\delta D(z)
\quad\text{对所有 }\delta.
\]

求导得

\[
J_D(z_*)R_\delta=T_\delta J_D(z_*).
\]

若复化后的向量满足 \(R_\delta v_k=e^{ik\omega\delta}v_k\)，且 \(w_k=J_D(z_*)v_k\ne0\)，则 \(T_\delta w_k=e^{ik\omega\delta}w_k\)，所以 \(w_k\) 属于物理 Fourier 波数 \(k\) 的子空间。对于非零波数，实值版本对应正余弦二维平面；零频对应常数的一维空间。

关键条件是：所有平移、固定基点、局部解码等变和非零导数。在一般基点，求导把两个不同基点的 Jacobian 联系起来，不能推出同一基点的切向量是纯 Fourier 波。当前 attention 在零幅值附近还有标准差下限，其性质也要另行核查。

有限幅值解码更不能直接推出纯波。比如 \(R_\delta z=e^{ik\omega\delta}z\)，

\[
D(z)(x)=\operatorname{Re}\{ze^{ik\omega x}+z^2e^{i2k\omega x}\}
\]

严格满足平移等变，却同时含 \(k\) 和 \(2k\)。这解释了为什么潜在波数、物理波数与非线性谐波不能简单一一对应。

## 10. 本轮证据边界与下一步

已完成：原始论文检索、最近先行工作核对、最新 main 架构读取、PCA 解释边界的解析说明、attention 幅值约束推导及小型数值核对、分阶段实验方案。

未完成且未声称完成：训练后 latent 可视化/谱对齐、多个 checkpoint 的干预实验、Allen–Cahn 有限时间幅值扫描、统计显著性评估、Lean 形式化或论文新颖性证明。

**建议下一步：先把当前 attention 的幅值—谐波实验和 heat 的频率响应实验做出来，同时保存各模型 latent。** 它们成本可控、参照明确，也最能判断这条路线是否超出了“做了一张好看的 PCA 图”。
