#!/bin/zsh
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

echo "=========================================="
echo " 正在同步「AIHR文章學習_發布版」至 GitHub..."
echo " 目標倉庫: git@github.com:artgistim/aihr-learn.git"
echo "=========================================="

# 1. 確保 git 已初始化
if [ ! -d ".git" ]; then
    echo "📦 初始化 Git 儲存庫..."
    git init
    git branch -M main
fi

# 2. 設定 remote
if ! git remote | grep -q "origin"; then
    echo "🔗 設定 remote origin..."
    git remote add origin git@github.com:artgistim/aihr-learn.git
else
    git remote set-url origin git@github.com:artgistim/aihr-learn.git
fi

# 3. 檢查遠端 repository 是否已在 GitHub 建立
echo "🔍 檢查遠端倉庫連線..."
if ! git ls-remote git@github.com:artgistim/aihr-learn.git >/dev/null 2>&1; then
    echo ""
    echo "⚠️  【尚未在 GitHub 建立儲存庫】"
    echo "請先前往瀏覽器建立該儲存庫（10 秒即可完成）："
    echo "👉 網址: https://github.com/new"
    echo "👉 Repository name 請輸入: aihr-learn"
    echo "👉 選擇 Public（若要免費 GitHub Pages .io）或 Private"
    echo "👉 不要勾選 Add README，直接點選 Create repository"
    echo ""
    echo "建立完成後，請重新執行本腳本即可自動推上去！"
    exit 1
fi

# 4. 先依母資料庫重打包，避免把還沒裝上靜態讀取的 index.html 推上去
echo "📄 正在依目前資料庫重新產生 index.html..."
python3 "$DIR/export_publish.py"

# 5. 提交與推送
echo "📝 正在提交最新檔案..."
git add .
if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "無新變更需要 commit。"
else
    git commit -m "feat: 發布 AIHR 文章學習與決策藍圖 (全量靜態自給自足版)"
fi

echo "🚀 正在推送到 GitHub main 分支..."
git push -u origin main

echo ""
echo "=========================================="
echo "🎉 推送成功！"
echo "GitHub 儲存庫: https://github.com/artgistim/aihr-learn"
echo "=========================================="
