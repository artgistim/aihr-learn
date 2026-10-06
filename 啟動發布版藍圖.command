#!/bin/zsh
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

echo "=========================================="
echo " 🔄 正在從母專案同步最新資料並打包..."
echo "=========================================="
python3 "$DIR/export_publish.py"

echo "=========================================="
echo " 🚀 正在啟動「AIHR文章學習_發布版」藍圖..."
echo " 網址: http://127.0.0.1:8768"
echo "=========================================="

# 自動釋放 8768 埠舊程序
lsof -ti :8768 | xargs kill -9 2>/dev/null || true

exec python3 "$DIR/serve_blueprint.py"
