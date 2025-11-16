#!/usr/bin/env bash
# 一键运行 Milestone 1 与 2
# 用法：bash scripts/run_m12.sh [SUB]
# 例子：bash scripts/run_m12.sh 28

set -euo pipefail
SUB=${1:-28}

echo "[M1] 读取与事件核对：sub-${SUB}"
python3 scripts/m1_quickcheck.py --sub "${SUB}"

echo "[M2] 预处理/ICA/事件/Epochs/ERP：sub-${SUB}"
python3 scripts/m2_pipeline_demo.py --sub "${SUB}"

echo "完成。图像已保存至 figures/ 目录。"
