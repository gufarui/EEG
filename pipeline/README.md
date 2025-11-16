# mne-bids-pipeline 使用说明（最小）

前置：
- 数据位于 `data/raw/ds004147`（BIDS 结构）
- 已安装 `mne-bids-pipeline`：`pip install mne-bids-pipeline`

运行：
- `mne_bids_pipeline run --config pipeline/config.py --n_jobs 1`
  - 或：`python -m mne_bids_pipeline run --config pipeline/config.py --n_jobs 1`

输出：
- 派生结果与 HTML 报告位于 `derivatives/mne-bids-pipeline/`

备注：
- 如需变更滤波、ICA 算法或条件映射，直接编辑 `pipeline/config.py` 并重跑。
