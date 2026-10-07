# AIHR 文章學習與決策藍圖（獨立發布版）

本資料夾為專屬的獨立發布套件，已將文章資料庫、最新中文翻譯文章與互動藍圖前端完整打包。

---

## 🌟 特色

1. **雙模支援 (Hybrid Support)**：
   - **本機動態模式**：雙擊 `啟動發布版藍圖.command` 即可在本地瀏覽器秒開（連接埠 `8768`）。
   - **純靜態自給自足模式**：`index.html` 內嵌完整的文章備份資料。即使沒有 Python 後端（如上傳至 GitHub / GitHub Pages / 任何靜態 Hosting），直接點開也能完整檢索 104 篇文章與高質感中文表格對照！
2. **獨立乾淨**：不依賴母專案的其他草稿與大型檔案，隨時可單獨版控。

---

## 🚀 本地快速啟動

雙擊資料夾內的 `啟動發布版藍圖.command`，瀏覽器將自動開啟 `http://127.0.0.1:8768`。

---

## 🔒 同步至 GitHub 私人版面 (Private Repo) 指南

### 方案 A：建立 GitHub Private 儲存庫（最推薦）
1. 在 GitHub 建立一個新的 Private Repository（例如命名為 `aihr-ex-study-private`）。
2. 在終端機進入本資料夾：
   ```bash
   cd /Users/tim.cho/Documents/project_me/y2026_ex_study/AIHR文章學習_發布版
   git init
   git add .
   git commit -m "feat: 初次發布 AIHR 文章學習與決策藍圖"
   git branch -M main
   git remote add origin https://github.com/<你的帳號>/aihr-ex-study-private.git
   git push -u origin main
   ```

### 方案 B：有專屬網址連結可以直接看 (GitHub Pages 私人模式)
- **如果你有 GitHub Pro / Team / Enterprise**：
  進入該 Repo 的 **Settings -> Pages**，將 Source 設為 `Deploy from a branch (main / root)`，並將可見性保持為 **Private**。
  你將獲得一個專屬的私有連結（只有你登入 GitHub 才能訪問）。
- **如果是 GitHub Free 帳號**：
  可搭配免費的 **Vercel** 或 **Cloudflare Pages** 連結該 Private Repo，並在後台開啟密碼保護 (Password Protection) 或私人存取。
