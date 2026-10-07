#!/usr/bin/env python3
"""AIHR文章學習 發布版 打包與同步產生器。

將當下啟動的藍圖 HTML、SQLite 資料庫與最新中英文文章打包至「AIHR文章學習_發布版」，
並注入「靜態自給自足 (Self-contained Fallback)」機制：
使 index.html 既支援本機 Python 伺服器，也支援上傳至 GitHub / GitHub Pages 純靜態連結直接瀏覽！
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sqlite3
import sys
from pathlib import Path

# 母專案路徑
BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_HTML = BASE_DIR / "EX_Interactive_Lifecycle_Blueprint.html"
SOURCE_DB = BASE_DIR / "AIHR文章學習" / "aihr_articles.db"
SOURCE_EN_DIR = BASE_DIR / "AIHR文章學習" / "articles"
SOURCE_ZH_DIR = BASE_DIR / "AIHR文章學習" / "articles_zh"

# 發布版目標目錄
PUBLISH_DIR = BASE_DIR / "AIHR文章學習_發布版"
PUBLISH_HTML = PUBLISH_DIR / "index.html"
PUBLISH_DB = PUBLISH_DIR / "aihr_articles.db"
PUBLISH_EN_DIR = PUBLISH_DIR / "articles"
PUBLISH_ZH_DIR = PUBLISH_DIR / "articles_zh"


def collect_database_data() -> tuple[list[dict], dict[str, dict]]:
    """從 aihr_articles.db 讀取文章列表與文章全文詳情。"""
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"找不到母資料庫: {SOURCE_DB}，請先執行 build_aihr_db.py")

    conn = sqlite3.connect(SOURCE_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. 文章列表
    list_rows = cursor.execute(
        """
        SELECT slug, source_url, title_en, title_zh, author, published, modified, category,
               substr(summary_en, 1, 280) AS summary_en,
               substr(summary_zh, 1, 280) AS summary_zh,
               has_en, has_zh,
               (SELECT COUNT(*) FROM article_images i WHERE i.slug = articles.slug) AS image_count
        FROM articles
        ORDER BY modified DESC, published DESC, slug
        """
    ).fetchall()

    article_list = []
    for row in list_rows:
        published = (row["published"] or "")[:10]
        modified = (row["modified"] or "")[:10] or published
        article_list.append(
            {
                "slug": row["slug"],
                "title": row["title_en"] or row["title_zh"] or row["slug"],
                "title_zh": row["title_zh"] or "",
                "url": row["source_url"],
                "date": published,
                "updated": modified,
                "author": row["author"] or "",
                "category": row["category"] or "其他",
                "summary_en": row["summary_en"] or "",
                "summary_zh": row["summary_zh"] or "",
                "has_en": bool(row["has_en"]),
                "has_zh": bool(row["has_zh"]),
                "image_count": row["image_count"],
            }
        )

    # 2. 文章全文
    full_rows = cursor.execute("SELECT * FROM articles").fetchall()
    article_details: dict[str, dict] = {}
    for r in full_rows:
        slug = r["slug"]
        img_rows = cursor.execute(
            "SELECT lang, src, alt FROM article_images WHERE slug = ? ORDER BY id",
            (slug,),
        ).fetchall()
        published = (r["published"] or "")[:10]
        modified = (r["modified"] or "")[:10] or published
        article_details[slug] = {
            "slug": slug,
            "title": r["title_en"] or r["title_zh"] or slug,
            "title_zh": r["title_zh"] or "",
            "url": r["source_url"],
            "date": published,
            "updated": modified,
            "author": r["author"] or "",
            "category": r["category"] or "其他",
            "summary_en": r["summary_en"] or "",
            "summary_zh": r["summary_zh"] or "",
            "body_en": r["body_en"] or "",
            "body_zh": r["body_zh"] or "",
            "has_en": bool(r["has_en"]),
            "has_zh": bool(r["has_zh"]),
            "images": [{"lang": im["lang"], "src": im["src"], "alt": im["alt"] or ""} for im in img_rows],
        }

    conn.close()
    return article_list, article_details


def embed_json(value: object) -> str:
    """嵌進 <script> 的 JSON。把 < 與行分隔字元跳脫，避免正文提前結束 script。"""
    text = json.dumps(value, ensure_ascii=False)
    return text.replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def _skip_js_string(src: str, i: int, quote: str) -> int:
    n = len(src)
    i += 1
    while i < n:
        if src[i] == "\\":
            i += 2
            continue
        if src[i] == quote:
            return i + 1
        i += 1
    raise RuntimeError("JavaScript 字串沒有收尾")


def _function_end(src: str, open_brace: int) -> int:
    """open_brace 指向 '{'，回傳函式結束大括號的下一個位置。"""
    n = len(src)
    i = open_brace
    depth = 0
    while i < n:
        ch = src[i]
        nxt = src[i + 1] if i + 1 < n else ""
        if ch == "{":
            depth += 1
            i += 1
            continue
        if ch == "}":
            depth -= 1
            i += 1
            if depth == 0:
                return i
            continue
        if ch in {"'", '"'}:
            i = _skip_js_string(src, i, ch)
            continue
        if ch == "`":
            i = _skip_js_template(src, i)
            continue
        if ch == "/" and nxt == "/":
            nl = src.find("\n", i)
            i = n if nl < 0 else nl + 1
            continue
        if ch == "/" and nxt == "*":
            end = src.find("*/", i + 2)
            if end < 0:
                raise RuntimeError("JavaScript 註解沒有收尾")
            i = end + 2
            continue
        i += 1
    raise RuntimeError("JavaScript 函式大括號沒有收尾")


def _skip_js_template(src: str, i: int) -> int:
    n = len(src)
    i += 1
    while i < n:
        if src[i] == "\\":
            i += 2
            continue
        if src[i] == "`":
            return i + 1
        if src[i] == "$" and i + 1 < n and src[i + 1] == "{":
            i = _function_end(src, i + 1)
            continue
        i += 1
    raise RuntimeError("JavaScript template 沒有收尾")


def replace_js_function(html: str, signature: str, new_source: str) -> str:
    """用大括號配對替換函式。字串對不上時直接失敗，避免靜態 fallback 被靜默跳過。"""
    start = html.find(signature)
    if start < 0:
        raise RuntimeError(f"找不到 `{signature}`，靜態 fallback 沒有裝上。")
    if html.find(signature, start + len(signature)) >= 0:
        raise RuntimeError(f"`{signature}` 出現超過一次。")
    brace = html.find("{", start)
    if brace < 0:
        raise RuntimeError(f"`{signature}` 後面沒有函式本體。")
    end = _function_end(html, brace)
    return html[:start] + new_source.strip() + html[end:]


NEW_LOAD_ARTICLES = """async function loadArticles(){
 try{
  const response=await fetch('/api/aihr-articles',{cache:'no-store'});
  if(!response.ok) throw new Error('文章 API 回應失敗');
  aihrArticles=await response.json();
  renderHome();
 }catch{
  if(window.__PREBAKED_AIHR_ARTICLES__ && window.__PREBAKED_AIHR_ARTICLES__.length){
   aihrArticles=window.__PREBAKED_AIHR_ARTICLES__;
   renderHome();
   const zhCount=aihrArticles.filter(a=>a.has_zh).length;
   $('#librarySource').textContent=`發布版靜態資料 · ${aihrArticles.length} 篇 · ${zhCount} 篇有中文`;
  }else{
   aihrArticles=[];
   $('#latestArticles').innerHTML='<p class="empty-copy">讀不到文章。請在這個資料夾執行 python3 serve_blueprint.py，再開 http://127.0.0.1:8768/ 。</p>';
   $('#articleRows').innerHTML='<tr><td class="empty-row" colspan="6">尚未連上文章資料庫</td></tr>';
   $('#articleCount').textContent='尚未連上文章資料庫';
   $('#librarySource').textContent='需要本機服務或重新打包發布版';
  }
 }
}"""

NEW_OPEN_ARTICLE = """async function openArticle(slug){
 const known=aihrArticles.find(item=>item.slug===slug);
 articlePane=known&&known.has_zh?'summary':'en';
 $('#articleModal').dataset.slug=slug;
 $('#articleModal').hidden=false;
 document.body.style.overflow='hidden';
 $('#articleModalTitle').textContent=known?known.title:'讀取中';
 $('#articleModalZh').textContent='';
 $('#articleUsageNote').textContent='';
 $('#articleModalBody').innerHTML='<p>讀取全文…</p>';
 try{
  let article=articleCache.get(slug);
  if(!article){
   try{
    const response=await fetch('/api/aihr-articles/'+encodeURIComponent(slug),{cache:'no-store'});
    if(response.ok) article=await response.json();
   }catch(e){}
   if(!article && window.__PREBAKED_AIHR_DETAILS__ && window.__PREBAKED_AIHR_DETAILS__[slug]){
    article=window.__PREBAKED_AIHR_DETAILS__[slug];
   }
   if(!article) throw new Error('讀不到這篇');
   articleCache.set(slug, article);
  }
  showArticle(article);
 }catch(error){
  $('#articleModalBody').innerHTML=`<p class="empty-copy">${esc(error.message||'讀取失敗')}</p>`;
 }
}"""


def generate_self_contained_html(article_list: list[dict], article_details: dict[str, dict]) -> str:
    """將資料注入 HTML，建立兼具 API 模式與純靜態離線模式的發布版 index.html。"""
    raw_html = SOURCE_HTML.read_text(encoding="utf-8")

    list_json = embed_json(article_list)
    details_json = embed_json(article_details)

    # 注入預烘焙資料與無縫 Fallback 邏輯
    data_injection = f"""
<!-- ====== 發布版 預烘焙靜態資料庫 (GitHub Pages / 離線自給自足支援) ====== -->
<script>
window.__PREBAKED_AIHR_ARTICLES__ = {list_json};
window.__PREBAKED_AIHR_DETAILS__ = {details_json};
</script>
"""
    # 插入在 </head> 之前
    head_end_pos = raw_html.find("</head>")
    if head_end_pos > 0:
        html_with_data = raw_html[:head_end_pos] + data_injection + raw_html[head_end_pos:]
    else:
        html_with_data = data_injection + raw_html

    # 母版 fetch 曾加上 {cache:'no-store'}，整段字串比對會悄悄失敗。改用函式邊界替換。
    html_with_data = replace_js_function(html_with_data, "async function loadArticles(){", NEW_LOAD_ARTICLES)
    html_with_data = replace_js_function(html_with_data, "async function openArticle(slug){", NEW_OPEN_ARTICLE)
    required = (
        "window.__PREBAKED_AIHR_DETAILS__[slug]",
        "發布版靜態資料",
        "function renderArticlePagination(",
        "function closeArticleModal(",
    )
    missing = [marker for marker in required if marker not in html_with_data]
    if missing or html_with_data.count("async function loadArticles()") != 1:
        raise RuntimeError(f"靜態 fallback 沒有正確裝上：{missing}")
    if "讀不到 SQLite" in html_with_data:
        raise RuntimeError("舊的 SQLite 錯誤訊息還在，fallback 沒有換掉")

    return html_with_data


def export() -> None:
    print("==================================================")
    print("🚀 開始打包「AIHR文章學習_發布版」...")
    print("==================================================")

    PUBLISH_DIR.mkdir(parents=True, exist_ok=True)
    PUBLISH_EN_DIR.mkdir(parents=True, exist_ok=True)
    PUBLISH_ZH_DIR.mkdir(parents=True, exist_ok=True)

    # 1. 讀取資料庫
    print("📦 正在讀取 SQLite 資料庫...")
    article_list, article_details = collect_database_data()
    print(f"   總文章數: {len(article_list)} 篇 (有中文: {sum(1 for a in article_list if a['has_zh'])} 篇)")

    # 2. 產出自給自足發布版 index.html
    print("📄 正在產生發布版 index.html (注入靜態 fallback 支援)...")
    publish_html_content = generate_self_contained_html(article_list, article_details)
    PUBLISH_HTML.write_text(publish_html_content, encoding="utf-8")
    print(f"   已寫入: {PUBLISH_HTML}")

    # 3. 複製 SQLite 資料庫
    print("💾 正在備份 aihr_articles.db...")
    shutil.copy2(SOURCE_DB, PUBLISH_DB)
    print(f"   已寫入: {PUBLISH_DB}")

    # 4. 複製 articles 與 articles_zh 原檔
    print("📂 正在同步英文與中文 Markdown 文章...")
    if SOURCE_EN_DIR.exists():
        for f in SOURCE_EN_DIR.glob("*.md"):
            shutil.copy2(f, PUBLISH_EN_DIR / f.name)
    if SOURCE_ZH_DIR.exists():
        for f in SOURCE_ZH_DIR.glob("*.md"):
            shutil.copy2(f, PUBLISH_ZH_DIR / f.name)
    print(f"   英文檔案: {len(list(PUBLISH_EN_DIR.glob('*.md')))} 篇")
    print(f"   中文檔案: {len(list(PUBLISH_ZH_DIR.glob('*.md')))} 篇")

    # 5. 建立發布版本地伺服器 serve_blueprint.py
    publish_server_code = """#!/usr/bin/env python3
\"\"\"AIHR 文章學習發布版 本機 Web 伺服器。\"\"\"
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent
HTML_PATH = ROOT / "index.html"
DB_PATH = ROOT / "aihr_articles.db"
PORT = 8768  # 發布版專屬獨立 Port，避免與主專案衝突

class PublishHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path in {"/", "/index.html"}:
            self._bytes(HTML_PATH.read_bytes(), "text/html; charset=utf-8")
            return
        if path == "/api/aihr-articles":
            self._json(self.list_articles())
            return
        prefix = "/api/aihr-articles/"
        if path.startswith(prefix):
            slug = unquote(path[len(prefix):])
            article = self.get_article(slug)
            if article is None:
                self._json({"error": "找不到文章"}, status=404)
                return
            self._json(article)
            return
        self._json({"error": "找不到路徑"}, status=404)

    def list_articles(self) -> list[dict]:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            \"\"\"
            SELECT slug, source_url, title_en, title_zh, author, published, modified, category,
                   substr(summary_en, 1, 280) AS summary_en,
                   substr(summary_zh, 1, 280) AS summary_zh,
                   has_en, has_zh,
                   (SELECT COUNT(*) FROM article_images i WHERE i.slug = articles.slug) AS image_count
            FROM articles
            ORDER BY modified DESC, published DESC, slug
            \"\"\"
        ).fetchall()
        res = []
        for r in rows:
            res.append({
                "slug": r["slug"],
                "title": r["title_en"] or r["title_zh"] or r["slug"],
                "title_zh": r["title_zh"] or "",
                "url": r["source_url"],
                "date": (r["published"] or "")[:10],
                "updated": (r["modified"] or "")[:10] or (r["published"] or "")[:10],
                "author": r["author"] or "",
                "category": r["category"] or "其他",
                "summary_en": r["summary_en"] or "",
                "summary_zh": r["summary_zh"] or "",
                "has_en": bool(r["has_en"]),
                "has_zh": bool(r["has_zh"]),
                "image_count": r["image_count"],
            })
        conn.close()
        return res

    def get_article(self, slug: str) -> dict | None:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM articles WHERE slug = ?", (slug,)).fetchone()
        if not row:
            conn.close()
            return None
        imgs = conn.execute("SELECT lang, src, alt FROM article_images WHERE slug = ? ORDER BY id", (slug,)).fetchall()
        conn.close()
        return {
            "slug": row["slug"],
            "title": row["title_en"] or row["title_zh"] or row["slug"],
            "title_zh": row["title_zh"] or "",
            "url": row["source_url"],
            "date": (row["published"] or "")[:10],
            "updated": (row["modified"] or "")[:10] or (row["published"] or "")[:10],
            "author": row["author"] or "",
            "category": row["category"] or "其他",
            "summary_en": row["summary_en"] or "",
            "summary_zh": row["summary_zh"] or "",
            "body_en": row["body_en"] or "",
            "body_zh": row["body_zh"] or "",
            "has_en": bool(row["has_en"]),
            "has_zh": bool(row["has_zh"]),
            "images": [{"lang": im["lang"], "src": im["src"], "alt": im["alt"] or ""} for im in imgs],
        }

    def _json(self, payload: object, status: int = 200) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._bytes(data, "application/json; charset=utf-8", status)

    def _bytes(self, data: bytes, content_type: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt: str, *args: object) -> None:
        pass

def main():
    server = ThreadingHTTPServer(("127.0.0.1", PORT), PublishHandler)
    url = f"http://127.0.0.1:{PORT}/"
    print(f"🚀 AIHR 發布版服務已啟動: {url}")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\n已停止。")
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
"""
    (PUBLISH_DIR / "serve_blueprint.py").write_text(publish_server_code, encoding="utf-8")

    # 6. 建立發布版雙擊啟動腳本
    publish_command = """#!/bin/zsh
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
"""
    cmd_file = PUBLISH_DIR / "啟動發布版藍圖.command"
    cmd_file.write_text(publish_command, encoding="utf-8")
    cmd_file.chmod(0o755)

    # 7. 建立說明文件與 GitHub 私人同步指南
    readme_content = """# AIHR 文章學習與決策藍圖（獨立發布版）

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
"""
    (PUBLISH_DIR / "README.md").write_text(readme_content, encoding="utf-8")

    print("==================================================")
    print("🎉 打包完成！「AIHR文章學習_發布版」已就緒。")
    print(f"📂 路徑: {PUBLISH_DIR}")
    print("==================================================")


if __name__ == "__main__":
    export()
