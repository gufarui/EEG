#!/usr/bin/env python
"""
Milestone 2（流程演示）
- 读取 1 名受试者 BIDS 数据
- 初步预处理（平均参考、陷波、0.1–30 Hz 滤波）
- ICA 拟合与（若可用）ICLabel 自动标注，输出组件图
- 提取反馈事件并分段（-0.2～0.8 s，暂不做基线以便后续比较）
- 计算条件 ERP 与差波（Win-Loss），绘制 FCz 波形
生成图：
- figures/m2_continuous_{sub}.png
- figures/m2_events_{sub}.png
- figures/m2_ica_components_{sub}.png
- figures/m2_evoked_fcz_{sub}.png
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import mne

# 兼容从 scripts/ 目录运行：将仓库根目录加入 sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import ensure_dirs, FIGURES_DIR, RESULTS_DIR
from src.preprocessing import read_raw_bids, PreprocParams, preprocess_raw, fit_ica, apply_ica
from src.events import get_feedback_events
from src.erp import make_epochs, compute_evokeds_by_condition, compute_rewp


def main(subject: str) -> None:
    ensure_dirs()

    # 1) 读取数据 + 基础预处理（用于 ERP 的参数）
    params = PreprocParams(l_freq=0.1, h_freq=30.0, notch=50.0, use_icalabel=True)
    raw = read_raw_bids(subject)
    raw_p = preprocess_raw(raw, params)

    # 2) 连续数据截图（方便核对）
    fig = raw_p.plot(duration=10.0, n_channels=32, show=False)
    out_cont = FIGURES_DIR / f"m2_continuous_{subject}.png"
    fig.savefig(out_cont, dpi=150)

    # 3) ICA（若安装了 mne-icalabel，会自动标注并剔除眼动/心电）
    ica = fit_ica(raw_p, params)
    raw_ica = ica.apply(raw_p.copy())
    # 绘制 ICA 组件拓扑图
    comp_fig = ica.plot_components(show=False)
    out_ica = FIGURES_DIR / f"m2_ica_components_{subject}.png"
    comp_fig.savefig(out_ica, dpi=150)

    # 简化：绘制 PSD 作为噪声概览
    psd_fig = raw_p.plot_psd(show=False)
    out_psd = FIGURES_DIR / f"m2_psd_{subject}.png"
    psd_fig.savefig(out_psd, dpi=150)

    # 4) 反馈事件与概览图
    events, event_id = get_feedback_events(raw)
    ev_fig = mne.viz.plot_events(events, event_id=event_id, show=False)
    out_events = FIGURES_DIR / f"m2_events_{subject}.png"
    ev_fig.savefig(out_events, dpi=150)

    # 5) 分段（-0.2~0.8 s），此处 baseline=None（M3 再做基线回归对比）
    epochs = make_epochs(raw_ica, events, event_id, tmin=-0.2, tmax=0.8, baseline=None)

    # 6) 条件 ERP 与差波（Win-Loss），并绘制 FCz
    conds = ["high_win", "high_loss", "mid_win", "mid_loss", "low_win", "low_loss"]
    evokeds = compute_evokeds_by_condition(epochs, conds)
    diffs = compute_rewp(evokeds, prefix="rewp")

    # 绘制 FCz 波形：各条件与差波叠加
    # 为清晰仅绘制条件平均，差波可单独另存
    picks = ["FCz"]
    ev_dict = {k: evokeds[k] for k in conds if k in evokeds}
    if ev_dict:
        import matplotlib.pyplot as plt
        out_evoked = FIGURES_DIR / f"m2_evoked_fcz_{subject}.png"
        plt.figure(figsize=(8, 4))
        for k, ev in ev_dict.items():
            y = ev.copy().pick("FCz").data[0] * 1e6  # 转为微伏
            t = ev.times
            plt.plot(t, y, label=k)
        plt.axvline(0, color='k', linestyle='--', linewidth=1)
        plt.axhline(0, color='gray', linestyle='-', linewidth=0.5)
        plt.xlim(-0.2, 0.8)
        plt.xlabel('时间 (s)')
        plt.ylabel('电位 (μV) @ FCz')
        plt.title('条件 ERP（FCz）')
        plt.legend(loc='best', fontsize=8)
        plt.tight_layout()
        plt.savefig(out_evoked, dpi=150)
        plt.close()

    # 7) 写入简要报告
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    report = RESULTS_DIR / f"m2_summary_{subject}.txt"
    with open(report, "w", encoding="utf-8") as f:
        f.write(f"Subject: {subject}\n")
        f.write("Conditions present in epochs: \n")
        for k in ev_dict.keys():
            f.write(f"  {k}: n={len(epochs[k])}\n")
        f.write("Figures:\n")
        for p in [out_cont, out_psd, out_ica, out_events, 'out_evoked' in locals() and out_evoked or None]:
            if p:
                f.write(f"  {p}\n")

    print("Saved:", out_cont)
    print("Saved:", out_psd)
    print("Saved:", out_ica)
    print("Saved:", out_events)
    if ev_dict:
        print("Saved:", out_evoked)
    print("Saved:", report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sub", dest="subject", default="28", help="BIDS 受试者编号（如 28）")
    args = parser.parse_args()
    main(args.subject)
