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

# 事件到条件的映射：合并高/中/低 × 赢/输 的反馈事件
# 使用 BIDS 注释中的 “value” 字段（BrainVision S-codes）
conditions = {
    'low_win':    ['Stimulus/S  6'],
    'low_loss':   ['Stimulus/S  7'],
    'mid_win':    ['Stimulus/S 16', 'Stimulus/S 26'],
    'mid_loss':   ['Stimulus/S 17', 'Stimulus/S 27'],
    'high_win':   ['Stimulus/S 36'],
    'high_loss':  ['Stimulus/S 37'],
}

# Epoch 参数（反馈锁定）
epochs_tmin = -0.2
epochs_tmax = 0.8
baseline = None  # M3 对比：传统均值基线 vs 基线回归

# ICA（可在报告查看）
ica = True
ica_algorithm = 'fastica'  # 可改为 'picard' 或 'infomax'（需额外依赖）
ica_n_components = 15

# 报告
reports_gen_figures = True
parallel = False
N_JOBS = 1

