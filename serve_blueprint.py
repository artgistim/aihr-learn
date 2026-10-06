#!/usr/bin/env python3
"""AIHR 文章學習發布版 本機 Web 伺服器。"""
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
        print("\n已停止。")
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
