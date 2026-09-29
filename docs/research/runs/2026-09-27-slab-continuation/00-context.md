# 分段 continuation：研究契约

2026-09-27；执行已完成调研中的D01。用户授权“开始研究”，本轮顺序为理论→Lean→代码论证。D03仅作机制对照，不同时开启另一个大项目。

目标是在保持Allen–Cahn反应、扩散和时间单位不变的情况下，通过真正计算中间terminal函数，延长原coding-tree局部求解器的可用时间。先完成一个有明确适用范围的非恒定例，不承诺通用任意高阶PDE。

关键代码事实：现有SemilinearMechanism在一维标量反应下只生成Dx(1)。对f(u)=u−u³，去掉已知零的高阶f导数并提出code标量后，归一化可达observable为(Id,Dx,F0,F1,F2,F3)。此特定类只需C¹终值接口。一般FullyNonlinearMechanism的高阶闭合问题仍未解决。

研究分两层：通用同树terminal-code扰动界；原Allen–Cahn局部树的显式矩证书及可计算平滑接口。需要区别C⁰/PDE误差稳定性与C¹/树矩可行性，不能用一个过大的code扰动常数替代全部传播分析。

历史证据未重跑：raw flat同表示L1上限约1.44551，共同指数时钟L2更小；bounded majority可在T=2处理行波但成本指数增长。上轮调研与全部旧文件保持不变，新证据写入本目录。

环境：Python /opt/miniconda3/envs/parabolab/bin/python；Lean/mathlib v4.33.0。现有工作树已含85个修改或未跟踪证据文件，初始hash和patch已保存。只新增本run、新的独立Lean模块，以及必要且不破坏既有合同的实现/测试。新增模块尽量不改动hash绑定入口。

初始研究假说：显式局部矩包络能在每段保持；独立采样的有限维平滑接口能控制累计误差，完整成本按每段实际树数统计。若接口误差或投影假设不闭合，保留失败，不将oracle续接当成实际算法。
