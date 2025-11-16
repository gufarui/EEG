from __future__ import annotations

"""
ERP/差波计算相关工具，包含：分段、条件平均、RewP 计算与峰值提取。
"""

from typing import Dict, List, Tuple

import numpy as np
import mne


def make_epochs(
    raw: mne.io.BaseRaw,
    events: np.ndarray,
    event_id: Dict[str, int],
    tmin: float = -0.2,
    tmax: float = 0.8,
    baseline: Tuple[float, float] | None = None,
) -> mne.Epochs:
    """创建 Epochs（默认不做基线以便后续比较不同基线策略）。"""
    return mne.Epochs(
        raw,
        events,
        event_id=event_id,
        tmin=tmin,
        tmax=tmax,
        baseline=baseline,
        preload=True,
        detrend=1,
    )


def compute_evokeds_by_condition(epochs: mne.Epochs, conditions: List[str]) -> Dict[str, mne.Evoked]:
    """对给定条件列表计算稳健平均（median），返回 Evoked 字典。"""
    return {name: epochs[name].average(method="median") for name in conditions if name in epochs.event_id}


def compute_rewp(evokeds: Dict[str, mne.Evoked], prefix: str) -> Dict[str, mne.Evoked]:
    """按 high/mid/low 计算 Win-Loss 差波，键名形如 f"{prefix}_high"。"""
    out: Dict[str, mne.Evoked] = {}
    for level in ("high", "mid", "low"):
        w = f"{level}_win"
        l = f"{level}_loss"
        if w in evokeds and l in evokeds:
            out[f"{prefix}_{level}"] = mne.combine_evoked([evokeds[w], evokeds[l]], weights=[1, -1])
    return out


def peak_in_window(
    evoked: mne.Evoked, tmin: float = 0.2, tmax: float = 0.35, ch: str = "FCz"
) -> Tuple[float, float]:
    """在给定时间窗内提取目标通道（默认 FCz）的峰值幅度与时间（秒）。"""
    amp, t = evoked.copy().pick(ch).get_peak(tmin=tmin, tmax=tmax)
    return float(amp), float(t)
