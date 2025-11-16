# 默认受试者编号，可通过 `make SUB=35 m12` 覆盖
SUB ?= 28

.PHONY: m1 m2 m12 pipeline

# Milestone 1：两张核对图
m1:
	python scripts/m1_quickcheck.py --sub $(SUB)

# Milestone 2：预处理/ICA/事件/Epochs/ERP 图
m2:
	python scripts/m2_pipeline_demo.py --sub $(SUB)

# 一键跑 M1+M2
m12: m1 m2

# 运行 mne-bids-pipeline（可选，生成派生与 HTML 报告）
pipeline:
	python -m mne_bids_pipeline run --config pipeline/config.py --n_jobs 1

