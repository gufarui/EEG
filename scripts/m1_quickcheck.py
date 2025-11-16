#!/usr/bin/env python
"""
Milestone 1（快速核对）
- 读取 1 名受试者 BIDS 数据
- 绘制 10 秒连续数据与反馈事件概览
输出两张图至 figures/ 目录。
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
from src.preprocessing import read_raw_bids, PreprocParams, preprocess_raw
from src.events import get_feedback_events


def main(subject: str) -> None:
    # 确保输出目录存在
    ensure_dirs()

    # 1) 读取原始 BIDS 数据
    raw = read_raw_bids(subject)

    # 2) 轻量滤波（仅用于可视化，不用于最终 ERP）
    raw_p = preprocess_raw(
        raw, PreprocParams(l_freq=1.0, h_freq=40.0, notch=50.0, use_icalabel=False)
    )

    # 3) 绘制 10 秒连续数据（方便检查通道/噪声/事件标记位置）
    fig1 = raw_p.plot(duration=10.0, n_channels=32, show=False)
    out1 = FIGURES_DIR / f"m1_continuous_{subject}.png"
    fig1.savefig(out1, dpi=150)

    # 4) 反馈事件概览（仅保留 win/loss 事件，按 low/mid/high 合并）
    events, event_id = get_feedback_events(raw)
    fig2 = mne.viz.plot_events(events, event_id=event_id, show=False)
    out2 = FIGURES_DIR / f"m1_events_{subject}.png"
    fig2.savefig(out2, dpi=150)

    # 5) 写入简要报告（事件计数与输出图路径）
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    counts = {name: int((events[:, 2] == code).sum()) for name, code in event_id.items()}
    report = RESULTS_DIR / f"m1_summary_{subject}.txt"
    with open(report, "w", encoding="utf-8") as f:
        f.write(f"Subject: {subject}\n")
        f.write("Event counts (feedback only):\n")
        for k in sorted(counts):
            f.write(f"  {k}: {counts[k]}\n")
        f.write(f"Figures:\n  {out1}\n  {out2}\n")

    print(f"Saved: {out1}")
    print(f"Saved: {out2}")
    print(f"Saved: {report}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sub", dest="subject", default="28", help="BIDS 受试者编号（如 28）")
    args = parser.parse_args()
    main(args.subject)
