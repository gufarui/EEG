# -*- coding: utf-8 -*-
# mne-bids-pipeline minimal configuration for ds004147 (EEG)

from pathlib import Path

# 根路径：按课程要求使用 BIDS 结构
bids_root = Path(__file__).resolve().parents[1] / 'data' / 'raw' / 'ds004147'
deriv_root = Path(__file__).resolve().parents[1] / 'derivatives' / 'mne-bids-pipeline'

# 受试者与任务
subjects = None  # None = 自动发现所有 sub-*
task = 'casinos'

# 通道类型与参考
ch_types = ['eeg']
eeg_reference = 'average'

# 滤波与陷波（ERP）
l_freq = 0.1
h_freq = 30.0
notch_freq = 50.0

# 事件到条件（本版本 pipeline 更稳妥的写法：直接列出数据中存在的事件名列表）
# 注意保留空格：单数字为 'S  6'、'S  7'，两位数为 'S 16' 等。
conditions = [
    'Stimulus/S  6',  # low win
    'Stimulus/S  7',  # low loss
    'Stimulus/S 16',  # mid low-cue win
    'Stimulus/S 17',  # mid low-cue loss
    'Stimulus/S 26',  # mid high-cue win
    'Stimulus/S 27',  # mid high-cue loss
    'Stimulus/S 36',  # high win
    'Stimulus/S 37',  # high loss
]

# Epoch 参数（反馈锁定）
epochs_tmin = -0.2
epochs_tmax = 0.8
baseline = None  # M3 对比：传统均值基线 vs 基线回归

# ICA（可在报告查看）
ica = True
ica_algorithm = 'fastica'  # 可改为 'picard' 或 'infomax'（需额外依赖）
ica_n_components = 15

# 报告与并行
reports_gen_figures = True
# mne-bids-pipeline 新版不再支持变量 `parallel`，请使用 `parallel_backend`。
# 常见取值：'loky'（默认）、'threading'、'multiprocessing'。保持 'loky' 并用 CLI 的 --n_jobs 控制并行数。
parallel_backend = 'loky'
# 注意：不要在配置中设置 N_JOBS（已在新版移除）。如需并行，请使用命令行参数 `--n_jobs`。
