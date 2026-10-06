#!/bin/zsh
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

# 自動釋放 8768 埠舊程序
lsof -ti :8768 | xargs kill -9 2>/dev/null || true

echo "=========================================="
echo " 正在啟動「AIHR文章學習_發布版」藍圖..."
echo " 網址: http://127.0.0.1:8768"
echo "=========================================="

exec python3 "$DIR/serve_blueprint.py"
