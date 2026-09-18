# PDE latent 模态控制：第一轮实现计划

2026-09-17 · v0.2 · 大方向已确认；实现已通过 tiny smoke，尚未执行科学训练。

目标依据：[研究目标](latent-modal-control-target.md)。工作区为
`parabolab-latent-fourier`，分支 `research/nn-latent-fourier`。

## 1. 第一轮只回答一个问题

一个已经准确求解 PDE 的 encoder–decoder，是否具有一套在训练后确定、测试时固定的 latent 编辑规则，使我们在解码前就能预报指定 Fourier 模态的变化，并在新样本上兑现？

先诊断只按回归任务训练的模型。方向识别可以使用 Fourier 目标校准，但不得因此宣称模型进行了无监督模态发现。若之后加入模态控制损失或结构约束，应作为另一条实验臂，回答“能否构造这种能力”。

第一轮只做固定时间的单模态幅值控制。相位、组合、非线性 PDE 与时间推进按阶段加入；不同时搜索所有 backbone、方向算法和损失。

## 2. 现有代码与需要补齐的接口

本次已读取 `parabolab/deep/opnet.py`、`setnet.py`、`optrain.py`、`families.py`、`corpus.py` 及现有实验 driver。代码基线为 `56e09b0` 加当前未提交的文档改动，未重新运行历史 benchmark。

- 已有函数输入到解输出的模型：`DeepONet`、`AttnOperator`、`FNO1d`。当前统一入口是 `forward(phi_grid, cond, q_tx)`，尚无统一的独立 encode/decode 接口。
- `DeepONet.branch` 的输出可作为 latent，其 decoder 对该向量仿射。它适合做结构对照；控制成功仍须检查 learned trunk 能否表示相应 Fourier 波形。
- `attn_nocond` 的 encoder 输出是 token 张量；其 decoder 还使用样本的输入均值、标准差和坐标统计量。必须显式记录完整表示及这些上下文，不能只保存 token 后声称完整表示被检验。
- 现有 `phi_operator.py`/`backbone_benchmark.py` 主要输出误差记录，没有发现与这些训练对应的 checkpoint 保存逻辑。本轮不能直接从 CSV 恢复 latent；实现时先检查是否另有可验证权重，否则重新训练并保存。
- 现有 Fourier 数据将峰值归一化到 0.9，且传统网格包含重复周期端点。新的独立模态编辑数据与谱测量协议需要显式处理这两点，不能悄悄改变旧 benchmark。

## 3. 最小实验：解析热方程

保持项目的终端值约定，固定周期区间 `[-8, 8)`、`T=0.3`、评价时刻 `t=0`：

\[
u_t+\tfrac12u_{xx}=0,\qquad u(T,x)=\phi(x),\qquad \omega=\pi/8.
\]

\[
\phi(x)=\sum_{k=1}^4[a_k\cos(k\omega x)+b_k\sin(k\omega x)],\qquad
u(0,x)=\sum_{k=1}^4\rho_k[a_k\cos(k\omega x)+b_k\sin(k\omega x)],
\quad \rho_k=e^{-(k\omega)^2T/2}.
\]

直接复用 `families.heat_fourier_1d` 的解析参照，并由谱公式独立核对。这里输入与输出是不同函数，仍是在学习 PDE 解算子；热方程只是便于验证的第一站。

首轮训练使用精确标签，以隔离表示与 MC 噪声。通过后在相同函数划分上接入上游 MC 标签，评价能力是否保留。这两种证据分别报告；只完成精确标签实验不能声称已经验证了 MC→NN 全流程。

### 数据起点

- 128 个无重复端点的输入传感器；主谱测量采用 256 个无重复端点的 query。坐标相位按实际 x 定义，FFT 实现须补偿网格原点。
- 各正余弦系数独立取自 `Uniform(-0.25, 0.25)`；无额外逐样本峰值归一化。调用旧 builder 时令外部幅值 A=1，避免 A 与系数冗余。
- 正式数据：1024 个训练函数、128 个模型验证函数、256 个控制校准函数、256 个完整分布求解测试函数。
- 另有 256 个编辑测试基底函数，各系数取自 `Uniform(-0.125, 0.125)`，使 0、0.5、1.5、2 倍编辑后的真实条件仍在训练系数范围内。普通求解精度仍在完整分布测试集上报告，不能只报告这个较小幅值组。
- 按函数 ID 分组；同一函数及其派生编辑保持在同一划分。独立随机流、函数系数 hash、划分清单全部保存。模型验证集选 checkpoint；校准集内部再划分控制拟合/选择子集；最终测试不参与任何选择。
- 主实验只声明在 k=1…4 的已见频率、未见函数组合上迁移。未见频率和越界幅值可以单列探索，不混入主成功结论。

以上数值是具体的起点。允许用独立 pilot 检查成本与数值误差，但正式测试前必须锁定配置；看过测试结果再改变规则需要新版本与新测试集。

## 4. 模型顺序与 latent 合同

首轮复用 `deeponet_nocond` 与 `attn_nocond` 的现有规模，不做结构搜索：前者是线性 decoder 对照，后者是没有显式 Fourier 层的待检验模型。训练只输入函数采样及必要坐标，不额外提供原 Fourier 系数。

`fno_nocond` 保留为后续预测对照：若两者的求解精度不足，可在新实验臂上检查 FNO。其频谱层已写入 Fourier 先验，相关成功不能用来证明网络自主发现了该基。

建议统一接口：

```python
state = net.encode(phi_grid, cond)  # features + explicitly named context
u = net.decode(state, q_tx)
```

`forward` 通过这两步实现。无编辑时输出应在明确数值容差内与原实现相同；保存/加载 checkpoint 后亦应一致。`context` 包含所有 decoder 需要的非编辑量，禁止 decode 时隐藏地重新读取原函数或重算归一化。

DeepONet 在 branch 向量上干预；全局训练 scalers 固定。Attention 在 `core.encoder` 后、`norm_c` 前的 h 上干预，固定 query、参数、mu_x、s_x、mu_y、s_y。

Attention 有 `D(h; s, mu)=s D_norm(h)+mu` 的样本输出缩放。对非零 Fourier 模态，采用固定的归一化方向 v，再执行 `h' = h + (delta/s) v`。这是明确的、依赖已记录尺度的固定控制规则；不声称同一个原始 h 增量对不同尺度样本产生相同物理增量。均值只影响零频，首轮不把修改 mu 当作模态控制成果。标准差下限触发样本单列。

本轮 delta 始终指 `t=0` 解的实 Fourier 系数增量，读出也预测该时刻的输出系数。若用它构造终端条件对照，对应的终端增量为 `delta/rho_k`。Token 方向是固定 128 点传感器网格上的模板；主指标在固定 256 点 query 网格上计算，暂不声称跨分辨率、任意坐标或多时间控制。

这一步仍检验 token 编辑能否选择性改变一个模态；仅靠 s 带来的整体幅值变化无法通过非目标泄漏检查。

## 5. 训练后识别控制方向，测试前冻结

第一版实现一种可复现的方法即可：**低维候选空间中的全局 Fourier 目标校准**。

1. 冻结 E、D。在控制校准集提取 latent；用中心化 PCA/SVD 建立候选空间 U。维数只在预设 `{16, 32, 64}` 中由校准选择子集选取，并受样本数/latent 维数限制。PCA 只提供搜索空间，不把单个主成分命名为 Fourier 模态。
2. 从候选坐标拟合一个仿射读出，预测输出的八个实 Fourier 系数。Attention 读出先预测 `c/s`，再乘已记录的 s；真实 Fourier 标签仅在校准时使用。校准数据的系数由解析解给出。
3. 在校准样本的 decoder Jacobian 上求一组共享方向，使 `J_D(z) v_j` 接近指定实基函数。实现使用 `calibration_delta` 的有限差分，只计算 U 中各基方向的输出响应，不显式存整个高维 Jacobian。Attention 使用固定 context 下的归一化 latent 编辑。以带 ridge 的最小二乘求固定方向；ridge 强度由校准选择子集确定。
4. 用校准选择子集的有限幅度编辑选控制配置，不能仅根据局部 Jacobian 拟合误差选。保存 U、均值、读出、方向、尺度约定、超参数和校准误差，然后冻结。

这里 Fourier 波形参与了方向识别，所以结论是“普通回归训练后的表示支持经校准的模态控制”。它不等于“PCA 无监督找到了 Fourier 基”。若 U 内失败，仅能否定当前候选空间和控制方法，不能据此断言所有 latent 控制均不存在。

高维 token 可能允许直接注入输出模板。除主指标外，需用同维随机候选子空间检查 PCA 子空间是否确有优势，并记录编辑表示与真实修改输入的重新编码表示之间的差异。Attention 重新编码时 s、mu 可能改变，须连同完整上下文解释，不能要求原始 h 逐元素相等。若仅 decoder 可控而没有 encoder 一致性的证据，报告就限于该控制结论；“encoder 学会模态分解”仍是未解决的更强问题。

正式测试按以下顺序执行：

1. 只运行 encoder 与固定读出，得到预测模态系数 c_tilde。
2. 给定目标实模态 j 和倍数 alpha，计算 `delta=(alpha-1)*c_tilde[j]`，保存预报 `delta*phi_j(x)` 及“其他模态增量为零”。
3. 按已冻结规则编辑 latent，保存编辑记录，再 decode 原始/编辑表示。
4. 用实际输出和独立真值验证预报。测试真值不得参与第 1–2 步；测试时不优化方向，不用 decoder 搜索编辑量，不用完整输出 FFT 反推控制。

先验证固定增量的加法控制，再做 `{0, 0.5, 1.5, 2}` 倍控制。零幅值或近零模态另报绝对误差；不能依靠除以极小数的相对误差判断成功。

## 6. 验收：准确、可预报、选择性、可迁移

记原预测为 u_hat、真实解为 u_ref、实际变化为 Delta_u。对倍数 alpha，第 j 个实基的理想变化为 `d_true=(alpha-1)*c_ref[j]*phi_j`，解码前预报为 `d_pred=delta*phi_j`。P_j 是该基函数的正交投影。

至少分别测量：

- 求解误差：u_hat 对 u_ref 的相对 L2；读出误差：c_tilde 对真实谱系数的误差。
- 预报误差：Delta_u 对 d_pred 的误差，判断实际变化是否兑现解码前的预报。
- 真正的控制误差：P_j Delta_u 对 d_true 的误差，判断是否真的实现所要求的翻倍，而非读出与编辑同时错向同一目标。
- 非目标泄漏：(I-P_j)Delta_u 的范数，包括 DC、另一正余弦分量和所有可分辨的高次频率，不能只检查原来的八个系数。
- 完整编辑结果：u_edited 对 `u_ref+d_true` 的误差，同时保留原始求解误差以便解释误差来源。

每个模型种子、目标模态和 alpha 分别报告。相对效应误差使用组内“误差平方和/目标效应平方和”的平方根，避免逐样本近零分母；同时报告按训练集模态 RMS 归一化的逐样本绝对误差分位数、低效应样本数量和结果。预报误差对 d_pred 归一化，控制误差/泄漏对 d_true 归一化；恒等/零效应实验只用绝对误差。

建议的首轮工程门槛：求解相对 RMS 误差 ≤1%；读出、预报、目标控制及泄漏相对 RMS 误差各 ≤5%，分别在八个模态和所有非恒等编辑倍率上通过，且三个训练种子均报告并满足主门槛。逐样本 P90/P95、最差频率也要展示，不能仅靠总体平均掩盖失败。门槛是实验提案，不是理论标准；在 pilot 上确认测量误差与目标效应可分辨后冻结。

这些门槛若在 pilot 不可达，应先说明是基础精度、测量误差还是控制能力受限，再决定修订方案。不能在正式测试后放宽门槛并继续沿用旧测试集。

## 7. 必要对照与结果分流

必须保留以下对照：

- **显式 Fourier 编解码＋解析热传播：** 验证基的顺序、相位、尺度、编辑与指标。成功由结构保证，只作为测量正对照。
- **重新编码真实修改后的输入：** 用真实修改的 phi' 检查 `D(E(phi'))` 是否准确，以区分“新解本来就预测不准”与“latent 编辑规则失败”。这是离线对照，不用于产生正式 latent 编辑。
- **DeepONet 线性 decoder：** 提供可加解码结构参照；不能将它与非线性 decoder 的有限扰动结果混为同一种发现。
- **多个随机方向及未训练模型：** 相同候选空间、相同校准预算；随机控制的输出效应尺度仅在校准集匹配，测试冻结。未训练模型的可控性与求解精度分开报告，避免把模型先验误说成 PDE 训练所得。

结果分流：

1. 求解不准：先解决预测前提，暂不作 latent 解释性结论。
2. 求解准、读出差：简单谱读出假设未通过，先检查表示及信息路径。
3. 读出准、编辑失败，而重新编码通过：信息存在，但当前固定控制规则不能可靠实现它；可考虑状态依赖的控制或受约束训练，并明确新目标/实验版本。
4. 微小编辑通过、翻倍失败：只支持局部控制。
5. 全部通过：支持该模型在指定热方程数据族和幅度范围内具有可预测的模态控制；不外推到所有 PDE，也不把热方程正对照当作原创性证明。

## 8. 按阶段实现与交付

### A. 数据、测量和接口

- [x] 新增 `parabolab/deep/modal_data.py`：独立实验数据、解析谱参照、函数划分与 hash。
- [x] 在 `opnet.py` / `setnet.py` 为两种模型增加明确的 encode/decode 接口及上下文记录；保持原 forward 行为。
- [x] 新增 `parabolab/deep/modal_control.py`：谱投影、指标、校准表示及固定编辑接口。
- [x] 新增解析投影、扰动、forward 等价、控制器、driver 和 checkpoint 往返 smoke tests。完整科学验收仍由阶段 C 承担。

交付：解析正对照通过，模型无编辑行为保持一致，解码前记录与解码后验收可分开执行。

### B. 单种子 pilot

- [x] 新增 `examples/latent_modal_control.py` 和配置；保存训练数据标识、初始化种子、checkpoint、scalers、controller 和测量记录。完整 latent context 由 encode/decode contract 定义，未逐样本持久化。
- [x] `--tiny` 已在 CPU 上以 12/4/8/6 个函数、4 步训练跑通 DeepONet 和 attention；它只验证代码路径。64/16/32/32、2000 步的 GPU pilot 尚未运行。
- [ ] 默认配置与正式超参数范围根据 pilot 冻结。若小数据 pilot 预测尚未达到科学门槛，明确标记，不靠解释性图绕过它。

交付：一次从函数输入、latent 编辑、预报记录到误差报告的完整演示，并测得实际时间/内存。未经测量不承诺总耗时。

### C. 正式热方程验证

- [ ] 使用全新数据与固定配置，两种模型各三个初始化种子；训练步数上限沿用现有 20000 步起点，验证选 checkpoint。第一轮最多六次正式模型训练，不做无界搜索。
- [ ] 冻结控制器后评估完整测试集和编辑测试集，保存逐样本、逐模态、逐倍率、逐种子指标。
- [ ] 报告原曲线、目标编辑、实际编辑、预报/实际系数变化，以及所有非目标频率泄漏。所有图须区分解析目标与实测输出。

交付：成功或失败均可复核的结果报告，以及按第 7 节作出的下一阶段决定。

### D. 有证据后扩展

先在相同热方程函数划分上替换成 MC 训练标签，保留精确测试真值，量化噪声带来的变化。上游采样能力若需改动，交给 `../parabolab`，此工作区只消费标签。

之后按问题选择相位/组合控制，或受约束训练；组合检查真实输出的交互残差，不能把潜向量加法天然可交换当成成功证据。

最后再进入周期 Allen–Cahn：输出表示编辑与改变输入后的非线性响应分开评价。必须先建立并核对周期参照；当前扩展区间上的零通量 FD 参照不能自动当作精确周期参照。若因幅值归一化导致非线性算子表达能力不足，属于此阶段需要单独修正的架构问题。

## 9. 在训练机器上运行

在这个 worktree 根目录安装当前代码，避免 Python 导入同级 MC worktree：

```bash
conda activate parabolab
python -m pip install -e .
python -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'cpu')"
```

新机器可以先用 `conda env create -f environment.yml` 创建环境。`environment.yml` 默认安装 CPU torch；GPU 机器应按其驱动安装兼容的 CUDA torch wheel，再执行 editable install。

先做与本地相同的无结果要求 smoke：

```bash
python -m pytest tests/test_deep_modal_control.py -q
python examples/latent_modal_control.py --tiny --device cpu --out-dir /tmp/parabolab-modal-smoke
```

然后在 GPU 上跑一个单种子 pilot：

```bash
python examples/latent_modal_control.py \
  --backbones deeponet attn --seeds 0 \
  --n-train 64 --n-valid 16 --n-calib 32 --n-test 32 \
  --steps 2000 --batch-size 16 --queries-per-step 64 \
  --device cuda --out-dir examples/latent_modal_control_run/pilot-seed0
```

pilot 确认资源、checkpoint 和指标文件正常后，正式默认配置为：

```bash
python examples/latent_modal_control.py \
  --device cuda --out-dir examples/latent_modal_control_run/formal-v1
```

默认正式配置顺序训练 DeepONet/attention 各三个种子，每次 20,000 步，使用 1024/128/256/256 个训练/验证/校准/测试函数。每个训练模型同时评价 Fourier 校准方向、输出效应匹配的随机 PCA 子空间方向和未训练同结构网络；调试时可用 `--skip-controls` 跳过后两项。输出包含 `config.json`、训练与未训练模型的 `.pt` checkpoint、各 controller 的 `.npz`、带 `variant` 列的 `metrics.csv` 和 `summary.json`。脚本不生成 MC 标签，也不会自动将 tiny/pilot 结果判作研究成功。

当前只执行了代码 smoke，没有执行 GPU pilot、正式训练、MC 标签生成或新数学证明；具体架构升级仍由阶段 C 的证据决定。
