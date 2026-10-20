# -*- coding: utf-8 -*-
"""Swap broken RSS sources (jiqizhixin / 36kr return HTML, not XML) with
working Chinese tech-news feeds; regenerate provider_news groups."""
import json, os, re, urllib.request
from email.utils import parsedate_to_datetime

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "llm_pricing_data.json")
ASOF = "2026-10-20"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/126"}
ITEM = re.compile(r"<item\b[^>]*>(.*?)</item>", re.S)
ENT = re.compile(r"<entry\b[^>]*>(.*?)</entry>", re.S)

def tag(it, n):
    m = re.search(r"<%s[^>]*>(.*?)</%s>" % (n, n), it, re.S)
    return m.group(1).strip() if m else ""

def clean(s):
    s = re.sub(r"<!\[CDATA\[(.*?)\]\]?>?", lambda m: m.group(1), s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    for a, b in [("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'),
                 ("&apos;", "'"), ("&amp;", "&"), ("&#39;", "'"), ("&nbsp;", " ")]:
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()

def fetch(url, feed, prov, kind, n=4):
    try:
        b = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read()
        txt = b.decode("utf-8", "ignore")
        blocks = ITEM.findall(txt) or ENT.findall(txt)
        items = []
        for it in blocks[:n]:
            t = clean(tag(it, "title"))
            l = clean(tag(it, "link")) or clean(tag(it, "id"))
            de = clean(tag(it, "description") or tag(it, "summary"))[:110]
            pd = clean(tag(it, "pubDate") or tag(it, "updated") or tag(it, "published"))
            try:
                dt = parsedate_to_datetime(pd).strftime("%Y-%m-%d") if pd else ""
            except Exception:
                dt = pd[:10] if pd else ""
            if t:
                items.append({"title": t, "date": dt, "url": l,
                              "source": feed, "excerpt": de})
        return {"provider": prov, "source_type": kind, "source_url": url,
                "crawled_at": ASOF, "items": items,
                "note": "RSS 实时抓取（%s），条目以源为准，未经人工编辑" % feed}, len(b)
    except Exception as e:
        return {"provider": prov, "source_type": kind, "source_url": url,
                "crawled_at": ASOF, "items": [], "note": "抓取失败：%s" % str(e)[:120]}, 0

# replacement feeds for the 2 broken ones (HTML not XML)
REP = {
    "美团LongCat": ("https://www.qbitai.com/feed", "量子位", "国内资讯站（量子位 RSS）"),
    "字节Seed":    ("https://www.ifanr.com/feed",  "爱范儿", "国内资讯站（爱范儿 RSS）"),
    "Perplexity":  ("https://www.leiphone.com/feed", "雷峰网", "国内资讯站（雷峰网 RSS）"),
    "面壁MiniCPM": ("https://www.qbitai.com/feed", "量子位", "国内资讯站（量子位 RSS）"),
    "Kimi":        ("https://www.ithome.com/rss/", "IT之家", "国内资讯站（IT之家 RSS）"),
    "StepFun":     ("https://www.leiphone.com/feed", "雷峰网", "国内资讯站（雷峰网 RSS）"),
}

with open(BASE, encoding="utf-8") as f:
    d = json.load(f)

for i, g in enumerate(d["provider_news"]):
    if g["items"] or g["provider"] not in REP:
        continue
    u, feed, kind = REP[g["provider"]]
    rec, n = fetch(u, feed, g["provider"], kind, 4)
    d["provider_news"][i] = rec
    print(("OK " if rec["items"] else "NO "), g["provider"], "->", u, len(rec["items"]))

still = [g for g in d["provider_news"] if not g["items"]]
print("remaining empty groups:", len(still))
for g in still:
    print("   ", g["provider"], g["source_url"], g["note"][:60])

note = "jiqizhixin.com/rss 与 36kr.com/feed 实测返回 HTML 而非 RSS XML（2026-10-20 复测），已从 provider_news 取数源剔除，国内资讯改用 量子位 / IT之家 / 爱范儿 / 雷峰网 四路 RSS"
if note not in [str(x) for x in d.get("unresolved", [])]:
    d["unresolved"].append(note)

for h in d["source_health"]:
    if h.get("url") in ("https://www.jiqizhixin.com/rss", "https://36kr.com/feed"):
        h["ok"] = False
        h["note"] = "返回 HTML 而非 RSS（2026-10-20 复测），已剔除出新闻取数源"

with open(BASE, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
print("bytes", os.path.getsize(BASE),
      "items", sum(len(g["items"]) for g in d["provider_news"]),
      "groups", len(d["provider_news"]))
