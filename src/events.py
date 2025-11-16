from __future__ import annotations

from typing import Dict, Tuple

import re
import numpy as np
import mne


def _extract_s_code(name: str) -> int | None:
    """
    从注释名称中提取 BrainVision 风格的事件编号（形如 "S 36"、"Stimulus/S 36"）。
    返回整数编号（如 36），若无法解析则返回 None。
    """
    # 提取形如 "S 36" 或 "S36" 的数字部分
    m = re.search(r"S\s*(\d+)", name)
    if m:
        return int(m.group(1))
    # 某些情况下注释就是数字字符串
    m = re.search(r"\b(\d+)\b", name)
    return int(m.group(1)) if m else None


def _s_code_to_condition(code: int) -> str | None:
    """
    将事件编号映射到反馈条件名称（基于 `events.json` 的文档）。
    - low 任务：S6=win, S7=loss
    - mid 任务：S16/S26=win, S17/S27=loss（低/高线索均合并为 mid）
    - high 任务：S36=win, S37=loss
    其他编号（注视/提示音/按键等）返回 None（不用于反馈分段）。
    """
    if code in (6,):
        return "low_win"
    if code in (7,):
        return "low_loss"
    if code in (16, 26):
        return "mid_win"
    if code in (17, 27):
        return "mid_loss"
    if code in (36,):
        return "high_win"
    if code in (37,):
        return "high_loss"
    return None


def get_feedback_events(raw: mne.io.BaseRaw) -> Tuple[np.ndarray, Dict[str, int]]:
    """
    从 Raw 注释中提取“反馈呈现”的事件，并构建用于 Epochs 的 `events` 与 `event_id`。

    返回
    - events: `n_events × 3` 的整型数组（MNE 规范），第3列为统一后的条件编码
    - event_id: 条件名到编码的映射，如 {"high_win": 301, ...}

    说明
    - 本函数依据 `data/raw/ds004147/..._events.json` 对 S 编码进行分组：
      low(S6/S7)、mid(S16/S17/S26/S27)、high(S36/S37)，并只保留反馈相关事件。
    - 为了在一个条件下合并多个原始 S 编码，我们为条件分配新的整型编码：
      低/中/高 × 赢/输 → 101/102/201/202/301/302。
    """
    events_raw, event_id_raw = mne.events_from_annotations(raw)

    # 生成原始注释名到 S 编码的映射
    desc_to_s: Dict[str, int] = {}
    for desc in event_id_raw.keys():
        s_code = _extract_s_code(desc)
        if s_code is not None:
            desc_to_s[desc] = s_code

    # 构造条件名称与新编码
    cond_code = {
        "low_win": 101,
        "low_loss": 102,
        "mid_win": 201,
        "mid_loss": 202,
        "high_win": 301,
        "high_loss": 302,
    }

    # 将原始 events 映射到新条件编码，过滤非反馈事件
    new_rows = []
    for onset, _, orig_code in events_raw:
        # 由 orig_code 反查描述字符串，再解析出 S 编码
        # event_id_raw: {desc: code}
        desc = next((k for k, v in event_id_raw.items() if v == orig_code), None)
        if desc is None:
            continue
        s_code = desc_to_s.get(desc)
        if s_code is None:
            continue
        cond = _s_code_to_condition(s_code)
        if cond is None:
            continue  # 非反馈相关事件
        new_rows.append([onset, 0, cond_code[cond]])

    events = np.array(new_rows, dtype=int)
    event_id = {k: v for k, v in cond_code.items()}
    return events, event_id
