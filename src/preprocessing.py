from __future__ import annotations

"""
预处理相关工具：BIDS 读取、参考/滤波、ICA + ICLabel 去伪影。
所有函数均配有中文注释，便于课程中团队成员理解与复现。
"""

from dataclasses import dataclass
from typing import Optional

import mne
from mne.preprocessing import ICA

try:
    import mne_icalabel
except Exception:  # pragma: no cover - 依赖可选，不存在时仅禁用自动标注
    mne_icalabel = None  # type: ignore

from .config import BIDS_ROOT


@dataclass
class PreprocParams:
    """预处理参数集合。

    - l_freq/h_freq: 带通滤波上下限（Hz），ERP 建议 0.1–30。
    - notch: 工频陷波（Hz，50 或 60），None 表示不做。
    - ref: 参考方式，默认平均参考。
    - ica_n_components: ICA 成分数（经验 15 左右可够用）。
    - use_icalabel: 若安装了 mne-icalabel，则自动标注眼动/心电等成分并剔除。
    """

    l_freq: float = 0.1
    h_freq: float = 30.0
    notch: Optional[float] = 50.0
    ref: str = "average"
    ica_n_components: int = 15
    use_icalabel: bool = True


def read_raw_bids(subject: str, task: str = "casinos") -> mne.io.BaseRaw:
    """使用 mne-bids 读取某受试者的 BIDS 原始 EEG。

    参数
    - subject: 受试者编号（不含 'sub-' 前缀），如 '28'。
    - task: 任务名，默认为 'casinos'。
    """
    from mne_bids import BIDSPath, read_raw_bids

    bids_path = BIDSPath(root=BIDS_ROOT, subject=subject, task=task, datatype="eeg")
    raw = read_raw_bids(bids_path=bids_path, verbose=False)
    return raw


def preprocess_raw(raw: mne.io.BaseRaw, params: PreprocParams) -> mne.io.BaseRaw:
    """基础预处理：参考、陷波、带通滤波。

    处理步骤
    1) 设置 EEG 平均参考（可复现）
    2) 可选 50/60 Hz 陷波去工频噪声
    3) 0.1–30 Hz 带通滤波以保留 ERP 相关频段
    """
    raw = raw.copy().load_data()

    if params.ref == "average":
        raw.set_eeg_reference("average")

    # 若未设置电极位置信息，使用标准 10-20 布局（ICLabel 需要拓扑信息）
    try:
        has_montage = raw.get_montage() is not None
    except Exception:
        has_montage = False
    if not has_montage:
        try:
            raw.set_montage("standard_1020", match_case=False)
        except Exception:
            pass

    if params.notch:
        raw.notch_filter(freqs=[params.notch], picks="eeg")

    raw.filter(l_freq=params.l_freq, h_freq=params.h_freq, picks="eeg")
    return raw


def fit_ica(raw: mne.io.BaseRaw, params: PreprocParams) -> ICA:
    """拟合 ICA 并（若可用）用 ICLabel 自动标注设置 `ica.exclude`（不直接应用）。"""
    ica = ICA(n_components=params.ica_n_components, random_state=97, max_iter="auto")
    ica.fit(raw)
    if params.use_icalabel and mne_icalabel is not None:
        try:
            labels = mne_icalabel.label_components(raw, ica, method="iclabel")
            classes = labels[0]
            exclude = [
                i for i, lab in enumerate(classes) if lab in ("eye blink", "heart beat", "eye movement")
            ]
            ica.exclude = exclude
        except Exception:
            # 若缺少后端（pytorch/onnxruntime）或出现其它错误，则跳过自动标注
            pass
    return ica


def apply_ica(raw: mne.io.BaseRaw, params: PreprocParams) -> mne.io.BaseRaw:
    """基于 `fit_ica` 的结果应用 ICA，返回新的 Raw。"""
    ica = fit_ica(raw, params)
    return ica.apply(raw.copy())
