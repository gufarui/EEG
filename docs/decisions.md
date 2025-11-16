# 决策记录（Decision Log）

本文件用于记录各阶段的参数选择与其理由，便于课堂汇报与复现。

- 事件映射：反馈事件基于 S 编码合并为 high/mid/low × win/loss，见 `pipeline/config.py` 与 `src/events.py`。
- 参考/滤波：ERP 采用平均参考；0.1–30 Hz 带通；50 Hz 陷波。与作者略有差异，用于检验稳健性。
- 基线：M2 暂不做基线；M3 对比传统均值基线与基线回归。
- ICA：优先 fastica（默认）；如需与 ICLabel 更一致可改为 infomax/picard（需额外依赖）。
