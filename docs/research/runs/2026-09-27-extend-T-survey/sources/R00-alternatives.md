# R00：多层 Picard 与替代随机方法

检索/核验日期：2026-09-27。只做文献和可行性筛选，没有运行算法或证明新定理。

## 多层 Picard：可以跨过单树小时间限制，但 T 仍进入成本常数

1. Beck–Hornung–Hutzenthaler–Jentzen–Kruse, *Overcoming the curse of dimensionality in the numerical approximation of Allen–Cahn partial differential equations via truncated full-history recursive multilevel Picard approximations*, [arXiv:1907.06729](https://arxiv.org/pdf/1907.06729)。核验 PDF 的 Theorem 1.1、主定理 4.5 及 §5 的 Allen–Cahn 特化。对有界初值、具有多项式增长导数且满足 coercivity 的反应项，以及相应经典解的增长条件，任意固定有限 T 可以获得 RMSE ε 的近似；成本关于维度和 ε⁻¹ 是多项式。这里的 cubic 不要求全局 Lipschitz；截断由先验解界支持。不能把这一结论读成成本关于 T 也是多项式或统一有界。
2. Giles–Jentzen–Welti, *Generalised multilevel Picard approximations*, [arXiv:1911.03188](https://arxiv.org/pdf/1911.03188)。核验 Corollary 1.2、Theorem 3.17/Corollary 3.18 和式 (236)：全局 Lipschitz、无梯度半线性热方程的固定 T 误差/复杂度结论；常数含随 LT 增长的项。原预印本是 2019 年，不能因 [Oxford 接收记录](https://ora.ox.ac.uk/objects/uuid%3A10bde33d-4d1e-4882-add1-f53ec4bbbeca) 为 2026 年而称其为新机制。
3. Neufeld–Wu, *Multilevel Picard approximations for high-dimensional semilinear second-order PDEs with gradient-dependent nonlinearities*, [arXiv:2310.12545](https://arxiv.org/pdf/2310.12545)。核验 Theorems 3.3/3.4 和 Assumptions 2.1、2.4、2.6：有梯度、非恒定系数的扩展具有正则性、Lipschitz/增长及非退化条件。它不是任意高阶 jet 非线性的现成定理。HTML 版本访问失败，改读 PDF。
4. Nguyen, *Multilevel Picard approximations of high-dimensional semilinear partial differential equations with gradient-dependent nonlinearities in Lp-sense*, [arXiv:2410.00203v2](https://arxiv.org/html/2410.00203v2)。核验 Theorem 1.1、式 (5)–(7)、Setting 2.1。适用于 p≥2 和指定 Lipschitz/增长条件，用 Beta(1/2,1/2) 时间抽样；不能据“任意固定 T”推断实际长时间便宜，Setting 2.1 的权函数下界本身含很强的 T 依赖。2024 年预印本、2026 年期刊出版记录应分开。

对本项目的定位：MLP 是必须纳入的长 T 基线，不是声称原创的一条新算法。对 Allen–Cahn 可以用已有截断理论；对一般 coding-tree 任意高阶导数 PDE，必须另立适用性论证。它改变了估计对象及迭代组织，通常有可控截断/迭代偏差；不受原始单树绝对值展开的同一个临界时间定理直接约束。

## 分裂法：可信的比较方向，定理核验尚未完成

Faou, *Analysis of splitting methods for reaction-diffusion problems using stochastic calculus*, Mathematics of Computation 78 (2009), 1467–1483, [出版页](https://www.ams.org/mcom/2009-78-267/S0025-5718-08-02185-6/)，[DOI](https://doi.org/10.1090/S0025-5718-08-02185-6)。本轮可核验主来源摘要：反应–扩散分裂的概率表示、确定性误差界与混合 Monte Carlo 方法。多个全文入口失败，不能给它编造具体定理假设或误差阶。因此 D10 保留为 provisional。

项目可检验的具体提案：对 Allen–Cahn 精确推进反应子流，再通过热半群处理扩散；把时间离散、空间/回归、Monte Carlo 和非线性 plug-in 偏差逐项计入总误差。反应子流保持区间不等于整个随机数值方法无偏，更不等于高维成本已解决。它作为允许可控偏差时的基线有价值，尚不足以声称研究新颖性。

## 补充观察线索：局部随机回归

Fang–Sheng–Su–Zhou, *A derivative-free stochastic method for high-dimensional semilinear parabolic equations*, [arXiv:2510.02635v2](https://arxiv.org/html/2510.02635v2)。核验 Theorem 3.1、Remark 3.1 与局部回归构造。它利用 martingale/FBSDE 关系和局部线性回归估计梯度，可作为导数代价过高时的替代方法观察项，不另占本轮十个方向。注意 Theorem 3.1 写的是均方误差上界 CΔt + CΔt exp(−cM)，不能直接改说 RMSE 为 O(Δt)。C 依赖 T；邻域有效样本量及维度依赖仍须审查，iid 噪声假设也不是自动满足。

## 直接相关补充：SCaSML 残差纠正已有先例

Fan–Sun–Yang–Lu, *Physics-Informed Inference Time Scaling for Solving High-Dimensional PDE via Defect Correction*, [arXiv:2504.16172v3](https://arxiv.org/html/2504.16172v3)，版本日期2025-12-23。核验 Fact 3.1 的精确半线性 defect PDE，§3.1 的 MLP 实现，以及 Assumption 4.1 / E.2 和 Theorem 4.2 的条件与结论陈述。假设同时控制全域 residual 和 W^{1,∞} 近似误差；小训练损失不保证满足。本文是 D03 的直接近邻，不能把“围绕近似解求残差，再用MC/MLP纠正”称为新机制。其误差率定理还依赖附录正则性/可积性条件，本轮不声称完成整篇证明复核，也不将它当作原始 NPP 任意阶 code 的长T矩定理。项目可研究的差异收缩为：保留耗散的原树改写、all-code矩证书及参考解成本。训练网络不是本工作树本轮任务。

## 检索记录与边界

检索词族包括：branching diffusion long maturity time stepping；branching Monte Carlo reaction diffusion splitting；fully nonlinear PDE branching time patching；multilevel Picard gradient dependent arbitrary terminal time；Allen–Cahn non globally Lipschitz truncated MLP；generalised MLP Giles Welti；Faou splitting stochastic calculus；branching control variates long time；coding trees stability 2025 2026。

优先读作者论文/预印本与出版社页面，未把搜索摘要当成完整证明。没有覆盖所有 BSDE、神经算子、确定性高维方法或所有期刊版本。本轮有限检索不支持“此前无人做过”的结论；算法常数、代码复现实效及发表级新颖性均需后续验证。
