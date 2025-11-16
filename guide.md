# EEG 学期项目开发指南（更新版）

## 一、课程目标与评分要求概述

### 1. 课程要求
* **项目成绩≥4.0**，并参加所有里程碑会议。
* 作业和讲座不是强制要求，但完成它们有助于顺利完成项目。

### 2. 评分标准

项目总分按照五个等权重部分评定：

1. **代码可读性与文档** – 代码结构清晰、充分注释并配备 README。
2. **可重复性与模块化** – 控制软件版本，保证脚本在不同机器上可运行。
3. **合理性检查与可视化及讨论** – 包括断言、单元测试、可视化，并解释选择原因。
4. **结果可视化与解释** – 图表美观、突出关键信息并有解释。
5. **项目范围** – 分析深度和广度及其创新性。

## 二、里程碑与项目时间表

| 里程碑 | 建议时间 | 关键任务 | 交付物 |
|---|---|---|---|
| **Milestone 1 – 选题与简介** | 第 3 周 | 选择论文与数据集，概述任务和研究问题，确认团队成员。根据 Team “Starling” 幻灯片，研究问题是：*任务价值是否调节奖励相关 ACC 活动*；需重现的结果是计算各任务及线索条件下的 RewP 差值（平均赢 ERP 减去平均输 ERP）。| 1 页幻灯片：团队名称、论文与数据集简介、主要研究问题、预期分析方法及引用图示。 |
| **Milestone 2 – 流程规划** | 第 6 周 | 梳理原作者的预处理及分析流程并形成表格；设计自定义分析流程并说明与作者流程的异同；展示一段连续数据并标注事件。| 幻灯片：流程对比表、关键研究问题、一幅含事件标记的连续 EEG 图。|
| **Milestone 3 – 首个受试者分析** | 第 10 周 | 完成一名受试者的预处理、事件切分、ERP 与时频分析，并更新流程表。| 幻灯片：更新后的流程表、首位受试者 ERP/时频结果。|
| **Milestone 4 – 群体分析与合理性检查** | 第 13‑15 周 | 将流程应用于所有受试者；展示 ICA 拓扑、ERP 与基线、与论文结果比较等。| 幻灯片：合理性检查结果汇总。|
| **Milestone 5 – 扩展与展望** | 课程末期 | 评估复现结果，并提出至少一项扩展分析（解码、时频、线性模型或源定位）。| 幻灯片：复现总结与扩展方案。|
| **最终报告** | 学期结束 | 完整报告（20‑40 页）、代码仓库或压缩包、详细文档及说明。| PDF 或 Notebook 报告 + Git 仓库/Zip 包。|

## 三、原论文与任务概述

### 1. 实验设计与主要研究问题

所选论文《Task‑level value affects trial‑level reward processing》研究奖励相关 ACC 活动是否受任务平均价值的调节。实验包含 3 种任务，每个任务有 6 个彩色形状线索。受试者按键后得到一种果子的反馈作为赢/输结果。时间流程如 Milestone 1 幻灯片所示：

* 400–600 ms 的注视十字；
* 1000 ms 的红点提示；
* 50 ms 的“嘀嗒”声；
* 参与者有最多 2000 ms 做出左/右反应；
* 400–600 ms 注视十字；
* 1000 ms 显示代表奖惩的水果图案。

**研究问题**：考察奖励相关 ACC 活动——即反馈相关正波（RewP，也称 reward positivity）——是否随着任务平均价值增加而降低。具体而言：高价值任务（奖励概率 0.8）是否比低价值任务（奖励概率 0.5）产生更小的 RewP？

**复现目标**：使用 ERP 分析重现论文中的主要结果：对每个任务和线索条件，计算平均赢 ERP 减去平均输 ERP 的差值，并比较任务间差异。Milestone 1 幻灯片中提供了原文 ERP 图和 topography，可作为对比参考。

### 2. 数据集特点

数据集 ds004147 (Average Task Value) 包含 12 名参与者的 EEG 数据，记录了 31 个通道，遵循 BIDS 规范。任务包含高、中、低三种价值条件，每个受试者有 144×3=432 次试次。数据可从 NEMAR/OpenNeuro 下载，解压后约 4 GB，并附有原作者的 MATLAB 代码仓库链接。论文使用该仓库进行预处理与分析，但课程鼓励使用不同流程以验证结果。

## 四、作者分析流程梳理（基于 MATLAB 代码仓库）

原作者提供的 MATLAB 仓库（`chassall/averagetaskvalue`）包含一系列脚本，主要步骤如下：

1. **数据整理与 BIDS 化** (`analysis_01_bidsify.m`)：读取原始 EEG 数据并转换为 BIDS 结构，设置元数据。
2. **预处理** (`analysis_02_preprocess.m` 等)：
   - 重新参考至平均参考；
   - 高通滤波（0.1 Hz）和低通滤波（30 Hz）用于 ERP 分析；
   - notch 滤波处理工频噪声；
   - 使用 ICA 手动识别并去除眨眼等伪影；
   - 对于时频分析，使用较宽带宽（1–50 Hz）并对数据下采样至 250 Hz。
3. **事件处理与分段**：根据反馈刺激的标记将数据分段为试次，对每种任务和反馈类型创建 epoch，时间窗约 −200 ms 到 +800 ms，并执行基线校正（−200~0 ms）。
4. **ERP 计算**：对每个条件求平均波形，通过减法 (Win–Loss) 计算 RewP；在关键电极 FCz、Cz 等处统计振幅，并使用 200–350 ms 范围作为 RewP 峰值；统计比较不同任务间差异。
5. **统计分析**：使用配对 t 检验和重复测量 ANOVA 分析条件差异，并报告效应量。
6. **可视化**：绘制 ERP 波形、topography 和箱线图，展示 RewP 随任务价值的变化。

## 五、自定义分析流程设计

设计与作者不同但合理的分析流程，以验证结果并提高可靠性。
| 步骤 | 作者流程 | Starling 设计 |
|---|---|---|
| **坏通道检测** | 手动检查并删除明显噪声通道。 | 使用 MNE 的 `find_bad_channels` 与 `autoreject` 自动检测坏通道，并在必要时参考 EOG/EMG 信号进一步确认。|
| **参考选择** | 平均参考。 | 先使用平均参考，后尝试鼻尖或外耳参考，比较 RewP 的稳健性。|
| **滤波** | 0.1–30 Hz 带通；工频 notch 滤波。 | 使用 0.5–35 Hz 带通提升高频成分；利用 `mne.filter.notch_filter` 执行 50 Hz notch；同时使用 `mne.preprocessing.maxwell_filter` 或 `zapline` 去除电源噪声。|
| **去除伪影** | 手动选择 ICA 组件。 | 采用 `ICA` 配合 `ICLabel` 自动分类伪影成分（眨眼、心电等），并结合 `autoreject` 进行自动试次拒绝，减少主观性。|
| **下采样** | ERP 保持原采样率，时频分析下采样至 250 Hz。 | 全程使用原采样率（512 Hz），在时频分析时按需下采样；比较不同采样率对时间分辨率的影响。|
| **事件与 epoch 划分** | −200 ms 至 800 ms，基线 −200~0 ms；依据任务和反馈类型编码事件。 | 使用相同时间窗但尝试 **基线回归 (baseline regression)** 方法代替传统减法；事件编码保持一致。|
| **平均与统计** | 对每个条件计算均值 ERP；用 t 检验和 ANOVA。 | 采用**稳健均值 (median)** 或 **加权平均** 抵消异常值；利用集群非参数置换检验或线性混合模型比较任务差异。|
| **时频分析** | 使用 Morlet Wavelet；分析 2–30 Hz。 | 使用 **多重 taper (multitaper)** 方法计算功率与相位，并考虑 2–50 Hz 的更宽频率范围；用基于回归的方法提取与任务价值相关的功率调制。|
| **统计建模** | 配对 t 检验、ANOVA。 | 在群体水平使用 **线性混合效应模型**（随机截距），预测 RewP 振幅或功率，固定效应包括任务价值和反馈类型。|
| **可视化** | 绘制 ERP 波形和 topography；箱线图展示振幅分布。 | 除传统图形外，使用时间–频率功率图、单试次 RewP 散点图；展示伪影清理前后的比较；采用 seaborn 风格增强美观性。|

该流程在保持核心分析步骤一致的同时，引入了自动化伪影处理、不同滤波参数、稳健统计和基线回归等改进，以检验结果对分析选择的敏感性并减少主观因素。

## 六、技术实现与代码建议

为了实现上述流程，建议使用 **MNE‑Python** 框架配合 `mne-bids`、`autoreject`、`mne-icalabel` 等工具。以下提供关键步骤的代码示例，供后续 Notebook 或脚本使用。

### 1. 环境配置

1. 使用 Conda 创建独立环境并安装依赖：

   ```bash
   conda create -n eeg_project python=3.10 -y
   conda activate eeg_project
   pip install mne mne-bids mne-icalabel autoreject statsmodels seaborn jupyterlab
   ```

2. 在项目根目录启动 `jupyter-lab`，按模块化方式编写 notebook 或脚本。建议的目录结构与此前指南相同（`data/`, `src/`, `notebooks/`, `figures/` 等）。

**目录说明：**

```
.
├── data/
│   ├── raw/
│   │   └── ds004147/                 # 原始 BIDS 数据（你已移动到此处）
│   └── processed/                    # 我们自研管线的中间产物（可选）
├── derivatives/
│   └── mne-bids-pipeline/            # mne-bids-pipeline 自动生成的派生结果与报告
├── pipeline/
│   ├── config.py                      # mne-bids-pipeline 配置
│   └── README.md
├── src/                               # 函数库（供脚本/Notebook 复用）
│   ├── config.py
│   ├── preprocessing.py
│   ├── events.py
│   ├── erp.py
│   ├── tfr.py
│   └── stats.py
├── scripts/                           # 可复现脚本（各里程碑入口）
│   ├── m1_quickcheck.py
│   ├── m2_pipeline_demo.py
│   └── run_m12.sh                     # 一键运行 M1+M2
├── notebooks/                         # 每个里程碑一个 Notebook（展示/解释）
├── figures/                           # 生成的图（临时产物，可不入库）
├── results/                           # CSV/统计文本等结构化结果
├── docs/
│   ├── decisions.md
│   └── milestones/
│       ├── m1/README.md
│       ├── m2/README.md
│       ├── m3/README.md
│       ├── m4/README.md
│       └── m5/README.md
├── ppt/
├── Makefile                           # make m1/m2/m12/pipeline
├── guide.md
├── README.md
├── requirements.txt
└── environment.yml
```

### 2. 数据导入与坏通道检测

```python
from mne_bids import BIDSPath, read_raw_bids
import mne
from autoreject import AutoReject
from mne.preprocessing import ICA, create_eog_epochs
import mne_icalabel

# 指定 BIDS 根目录和受试者列表
bids_root = 'data/raw/ds004147'
subjects = ['27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38']
task = 'casinos'

def preprocess_raw(subject):
    # 读取原始数据
    bids_path = BIDSPath(root=bids_root, subject=subject, task=task, suffix='eeg', extension='.vhdr')
    raw = read_raw_bids(bids_path, preload=True)

    # 重命名和重新参考
    raw.set_eeg_reference('average')

    # 滤波：0.5–35 Hz 带通 + notch 50 Hz
    raw.filter(0.5, 35., fir_design='firwin')
    raw.notch_filter(50., fir_design='firwin')

    # 自动检测坏通道并修补
    ar = AutoReject(n_interpolate=[1, 2, 3, 4], consensus=[0.6, 0.7, 0.8], verbose=False)
    _, reject_log = ar.fit(raw.copy().get_data().T).transform(raw.get_data().T, return_log=True)
    bads = reject_log.bad_channels
    raw.info['bads'] = bads
    raw.interpolate_bads(reset_bads=True)

    return raw

# 示例：预处理一个受试者
raw = preprocess_raw('27')
```

### 3. ICA 去伪影与 ICLabel 分类

```python
def apply_ica(raw):
    ica = ICA(n_components=15, random_state=97, max_iter='auto')
    ica.fit(raw)

    # 使用 ICLabel 自动分类组件
    labels = mne_icalabel.label_components(raw, ica, method='ica_labels')
    # 排除眨眼、心电等组件
    exclude_idx = [i for i, label in enumerate(labels[0]) if label in ('eye blink', 'heart beat')]
    ica.exclude = exclude_idx
    raw_ica = ica.apply(raw.copy())
    return raw_ica

raw_clean = apply_ica(raw)
```

### 4. 事件提取与 Epoch 划分

```python
# 获取事件和 event_id（根据注释手册自定义）
events, event_id = mne.events_from_annotations(raw_clean)

# 定义时间窗和基线，采用 baseline regression 方式
epochs = mne.Epochs(raw_clean, events, event_id, tmin=-0.2, tmax=0.8, baseline=None,
                    detrend=1, preload=True)
```

若采用传统基线减法，可将 `baseline=(-0.2, 0)`；若选择基线回归，可利用 `mne.baseline.create_baseline` 后再回归掉基线趋势。

### 5. ERP 与 RewP 计算

```python
import numpy as np
from mne import combine_evoked

# 定义条件分组：如 high_win、high_loss、mid_win、mid_loss、low_win、low_loss
conditions = {
    'high_win': 1,
    'high_loss': 2,
    # 根据 event_id 实际编码补充
}

# 创建每个条件的平均 ERP
evokeds = {name: epochs[name].average(method='median') for name in conditions}

# 计算每个任务的 RewP 差波（Win-Loss）
evoked_diff_high = combine_evoked([evokeds['high_win'], evokeds['high_loss']], weights=[1, -1])

# 绘制波形
evoked_diff_high.plot(picks='FCz', titles='RewP: High Value (Win-Loss)')

# 计算峰值振幅（200–350 ms）
latency_window = (0.2, 0.35)
peak_amp, peak_time = evoked_diff_high.get_peak(ch_type='eeg', tmin=latency_window[0], tmax=latency_window[1])
print('RewP amplitude:', peak_amp, 'at', peak_time)
```

### 6. 时频分析

```python
from mne.time_frequency import tfr_multitaper

freqs = np.logspace(np.log10(2), np.log10(50), 20)
n_cycles = freqs / 2.
power = tfr_multitaper(epochs, freqs=freqs, n_cycles=n_cycles, time_bandwidth=4.0,
                       return_itc=False, decim=2)
power.plot(picks='FCz', baseline=(-0.2, 0), mode='zscore', title='Time-frequency (multitaper)')
```

### 7. 统计分析

在群体水平可使用非参数置换检验比较不同任务下 RewP 振幅差异：

```python
from mne.stats import permutation_cluster_test

# 假设 diff_high 和 diff_low 为不同任务的差波数组（n_subjects × n_times）
T_obs, clusters, p_vals, h0 = permutation_cluster_test([diff_high, diff_low], n_permutations=1000,
                                                       tail=0, n_jobs=1)
```

若采用线性混合模型（LMM）：

```python
import pandas as pd
import statsmodels.formula.api as smf

# 构造数据框 df，包含 subject、task_value、高低反馈、RewP 振幅
model = smf.mixedlm("rewp_amp ~ C(task) + C(feedback)", df, groups=df["subject"])
result = model.fit()
print(result.summary())
```

### 8. 批处理与结果整合

编写循环函数处理所有受试者，保存每个条件的 ERP 与时频结果到 `data/processed`，并在群体层面计算 grand average 与统计。各代码模块（如 `preprocessing.py`、`analysis_erp.py`）应编写成函数，便于重复调用。

## 七、里程碑工作建议

### Milestone 1

* 阅读并理解论文，整理实验流程和主要发现。
* 准备幻灯片：写明团队成员；引用论文题目、期刊信息以及 DOI；简述任务流程（可使用幻灯片中的示意图）；提出研究问题和待复现的主要结果（Win-Loss RewP 差值）。
* 下载 ds004147 数据集并使用 MNE-BIDS 检查数据结构。

**必须完成的动作**
1. 明确论文与数据集：`Task-level value affects trial-level reward processing` + `ds004147`（BIDS）。  
2. 写出**中心假设**：任务平均价值调节 trial-level 的奖励相关 ACC 活动（RewP = win − loss），高价值任务 RewP 更小。  
3. 环境就绪：创建 `conda` 环境并安装 `mne` 与 `mne-bids`。  
4. 最小可运行核对：读取 1 名受试者的连续 EEG，显示事件并导出两张核对图。

**建议脚本**：`m1_quickcheck.py`（最简读取 + 事件 + 连续片段）。  
**必须产出**：`figures/m1_events_28.png`、`figures/m1_continuous_28.png`、1 张幻灯片（团队、实验总思路、一句话研究问题、主要分析=ERP/RewP）。  
**验收标准**：脚本跑通并生成 2 图；幻灯片四项内容齐全.

---
### Milestone 2

* 根据上述作者流程梳理表和 Starling 设计表，制作一份**流程对比表**，采用 Milestone 2 模板的格式；至少涵盖坏通道处理、滤波、伪影清除、事件标注、平均与统计等多行，并在“Starling”列填入自定义方法。
* 在 Notebook 中加载一名受试者的连续数据，应用初步滤波和伪影处理，使用 `mne.viz.plot_raw` 标注事件并截图放入幻灯片。
* 幻灯片需说明中央研究问题和分析思路，图文并茂。此阶段不必完成所有预处理，只需展示计划和初步探索。

**必须完成的动作**
1. **作者流程梳理**：列出 6 行（BIDS 化、预处理、检查、行为、ERP、时频/建模）。  
2. **我们的流程**（不同且合理）：  
   - 自动坏通道检测 + 插值（PSD/相关性阈值）。  
   - 参考与滤波：平均参考；0.1–30 Hz FIR。  
   - 伪影去除：ICA 拟合 + ICLabel 自动标注（M3 启用自动剔除）。  
   - 事件映射：解析注释字符串，得到 `high|mid|low × win|loss`。  
   - 分段与基线：创建 `Epochs`（−0.2~0.8 s），M3 做**基线回归**。  
3. 展示 1 名受试者的连续数据第一印象。

**作者流程 vs 我们流程（对照表）**

| 步骤 | 作者流程（从仓库脚本与文献归纳） | 我们流程（用于课程要求的“不同但合理”） |
|---|---|---|
| 数据组织 | `analysis_01_bidsify.m` 进行 BIDS 化 | 数据已为 BIDS；直接 `mne-bids` 读取 |
| 坏通道 | 以人工/经验为主 | PSD/相关性阈值自动检测 + `raw.interpolate_bads()` |
| 参考与滤波 | 典型 0.1–30 Hz，平均参考 | **固定** 0.1–30 Hz FIR + 平均参考（参数可复现） |
| 伪影去除 | ICA + 人工判读 | ICA + **ICLabel 自动标注**（M3 启用剔除阈值） |
| 事件编码 | 触发号/脚本内部映射 | **解析注释字符串**，得到 `high|mid|low × win|loss` |
| 分段与基线 | Epochs + 传统基线减法 | Epochs + **基线回归**（M3 执行） |
| ERP/时频 | MATLAB 计算 | M3/M4 在 MNE 中实现 |
| 统计 | 经典 t 检验 | **置换 / 线性混合模型**（M4 执行） |

**建议脚本**：`m2_pipeline_demo.py`。  
**必须产出**：`figures/m2_events_{sub}.png`、`figures/m2_continuous_{sub}.png`、`figures/m2_ica_components_{sub}.png`、`figures/m2_evoked_fcz_{sub}.png`、1 张幻灯片（一句话研究问题 + 对照表 + 连续 EEG 图）。  
**验收标准**：四类图片全部生成；对照表≥6 行；幻灯片内容齐全。

---
### Milestone 3

* 按自定义流程完成一名受试者的完整分析，生成 ERP 和时频结果；记录所有参数选择。
* 更新流程对比表，指出根据实践调整的部分（例如滤波参数、ICA 组件数）。
* 在幻灯片中展示初步结果，特别是 FCz RewP 波形和功率谱，并对比期望的论文结果。

**必须完成的动作**
1. 完整预处理：坏通道插值、滤波、ICA+ICLabel 自动剔除（列出组件编号）。  
2. 固定事件-条件映射：`high_win / high_loss / low_win / low_loss / mid_*`；ROI 以 FCz 为主。  
3. **基线回归**：对（−0.2–0 s）执行回归去偏，保留回归后波形。  
4. **RewP 初步计算**：FCz 200–350 ms 均值振幅；每个价值条件 `RewP = mean(win) − mean(loss)`；输出表与图。

**作者流程 vs 我们流程（M3 已落地的差异点）**

| 项目 | 作者流程 | 我们在 M3 的实现 |
|---|---|---|
| 伪影去除 | ICA 人工挑选 | ICA + **ICLabel 自动剔除**，记录组件编号 |
| 基线处理 | 均值基线减法 | **基线回归**（−0.2–0 s） |
| ERP 计算 | 条件平均提取 RewP | FCz 200–350 ms **均值振幅**；`RewP = win − loss` |
| 稳健性 | 均值 | **中位/稳健平均**可切换（记录选择） |

**建议脚本**：`m3_single_subject.py`。  
**必须产出**：`figures/m3_erp_fcz_{sub}.png`、`results/m3_rewp_{sub}.csv`、1 张幻灯片（对照表 + 首个受试者 ERP/TRF 图）。  
**验收标准**：脚本对 1 名受试者可复现运行；CSV 与图表生成完整。

---


### Milestone 4

* 批处理所有受试者，生成群体平均 ERP 和差波，绘制 grand average 与差异图。
* 进行合理性检查：包括 ICA 组件可视化（验证眼动伪影被移除）、基线选择对波形的影响、与原论文图形的比较等。
* 汇总发现的异常或问题，如某些受试者噪声过大或事件标记错位，并在幻灯片中讨论解决方案。

**必须完成的动作**
1. **批处理所有受试者**：预处理 + ERP；合并 RewP 为 `results/group_rewp.csv`。  
2. **合理性检查**：ICA 拓扑图（2–3 人）、ERP 含基线对比（基线回归 vs 传统）、与作者结果对比（方向/幅度趋势）。  
3. **群体统计**：置换检验或线性混合模型，比较 `high vs low` 的 RewP；输出效应量与显著性。

**与作者结果对比（M4 群体层面）**

| 比较维度 | 作者报告 | 我们的群体结果 | 结论 |
|---|---|---|---|
| RewP 方向 | 高价值任务 RewP 更小 | 由 `group_rewp.csv` 汇总并填入 | 是否一致 |
| RewP 幅度 | 文献的范围/趋势 | 我们估计值与置信区间 | 差异原因讨论 |
| 统计方法 | 经典检验 | **置换/混合模型** | 方法差异影响评述 |

**建议脚本**：`m4_batch_group.py`。  
**必须产出**：`figures/m4_ica_topo_examples.png`、`figures/m4_erp_baseline_compare.png`、`figures/m4_group_rewp_boxplot.png`、`results/group_rewp.csv`、`results/group_stats.txt`、1–2 张幻灯片。  
**验收标准**：批处理成功；CSV/统计文本与三类 sanity check 图齐全。

---

### Milestone 5

* 根据群体结果，评估是否成功复现论文中“任务价值调节 RewP”的发现；如果结果不一致，分析可能原因（不同滤波、基线方法、分析策略等）。
* 选择至少一项扩展分析。例如：
  - **时间–回归编码模型 (TRF)**：建立回归模型预测连续 EEG 信号，解释变量包括反馈概率和任务价值。
  - **解码分析**：使用机器学习模型（如 SVM 或 Logistic Regression）在单试次数据中区分赢 vs 输，比较不同任务价值条件下的分类性能。
  - **源定位**：应用最小范数估计法在受试者标准脑模板上定位 RewP 产生的脑区。
* 在幻灯片中说明扩展方法的动机、实现方式、初步结果或预期，并讨论其对原研究问题的补充。

**必须完成的动作**
1. **复现状态结论**：基于群体统计与关键图明确“已复现/未复现”。  
2. **扩展分析（至少 1 项并给出初步结果）**：解码（AUC 曲线）、线性混合模型（参数与CI）、时频（θ 功率 200–350 ms）、源定位（最小范数差图）。

**建议脚本**：`m5_outlook_decoding.py` / `m5_outlook_lmm.py` / `m5_outlook_tfr.py` / `m5_outlook_source.py`（四选一即可）。  
**必须产出**：幻灯片 1（复现状态与证据图）、幻灯片 2（扩展方法与初步图）。  
**验收标准**：两张幻灯片均给出清晰结论与下一步计划，包含图与文字。
