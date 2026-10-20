# -*- coding: utf-8 -*-
"""Repair RSS news groups that failed due to truncated XML. Re-fetches each
feed with a full body read and a regex-based tolerant item extractor."""
import json, os, re, urllib.request
from email.utils import parsedate_to_datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "llm_pricing_data.json")
ASOF = "2026-10-20"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/126",
      "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}

ITEM_RE = re.compile(r"<item\b[^>]*>(.*?)</item>", re.S)

def tag(item, name):
    m = re.search(r"<%s[^>]*>(.*?)</%s>" % (name, name), item, re.S)
    return m.group(1).strip() if m else ""

def clean(s):
    s = re.sub(r"<!\[CDATA\[(.*?)\]\]?>?", lambda m: m.group(1), s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    for a, b in [("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'),
                 ("&apos;", "'"), ("&amp;", "&"), ("&#39;", "'"), ("&nbsp;", " ")]:
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()

def fetch(url, feed, provider, kind, n=4):
    try:
        req = urllib.request.Request(url, headers=UA)
        body = urllib.request.urlopen(req, timeout=25).read()
        items = []
        for it in ITEM_RE.findall(body.decode("utf-8", "ignore"))[:n]:
            t = clean(tag(it, "title"))
            l = clean(tag(it, "link"))
            de = clean(tag(it, "description"))[:110]
            pd = clean(tag(it, "pubDate"))
            try:
                dt = parsedate_to_datetime(pd).strftime("%Y-%m-%d") if pd else ""
            except Exception:
                dt = pd[:10] if pd else ""
            if t:
                items.append({"title": t, "date": dt, "url": l,
                              "source": feed, "excerpt": de})
        return ({"provider": provider, "source_type": kind, "source_url": url,
                 "crawled_at": ASOF, "items": items,
                 "note": "RSS 实时抓取（%s），条目以源为准，未经人工编辑" % feed}, len(body))
    except Exception as e:
        return ({"provider": provider, "source_type": kind, "source_url": url,
                 "crawled_at": ASOF, "items": [],
                 "note": "抓取失败：%s" % str(e)[:120]}, 0)

with open(BASE, encoding="utf-8") as f:
    d = json.load(f)

FIXED = FAILED = 0
for idx, g in enumerate(d["provider_news"]):
    if g["items"]:
        continue
    feed = g["items"][0]["source"] if g["items"] else (
        g["source_type"].split("（")[-1].rstrip("）") if "（" in g["source_type"] else g["source_type"])
    rec, n = fetch(g["source_url"], feed, g["provider"], g["source_type"], n=4)
    if rec["items"]:
        d["provider_news"][idx] = rec
        FIXED += 1
        print("FIXED  %-12s %-34s %d items (%dB)" % (
            g["provider"][:12], g["source_url"][:34], len(rec["items"]), n))
    else:
        d["provider_news"][idx] = rec
        FAILED += 1
        print("STILL  %-12s %-34s %s" % (g["provider"][:12], g["source_url"][:34], rec["note"][:60]))

still = [g for g in d["provider_news"] if not g["items"]]
print("\nfixed=%d still-fail=%d total-groups=%d total-items=%d"
      % (FIXED, FAILED, len(d["provider_news"]), sum(len(g["items"]) for g in d["provider_news"])))

with open(BASE, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
print("wrote %d bytes" % os.path.getsize(BASE))
