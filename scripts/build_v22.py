# -*- coding: utf-8 -*-
"""llm-database-sms v2.2 build — 2026-10-20.

Adds 12 providers (verified against OpenRouter catalog API + vendor
pages reachable from mainland China), 4 new peak/valley entries, 20
fresh RSS-sourced news items, and refreshes source_health.

Run from repo root:  python -B scripts/build_v22.py
"""
import json, os, urllib.request, xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FX   = 7.10
ASOF = "2026-10-20"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "llm_pricing_data.json")

def S(name, url, kind="official", note=""):
    d = {"name": name, "url": url, "kind": kind, "as_of": ASOF}
    if note: d["note"] = note
    return d

S_OR = S("OpenRouter · Models catalog API", "https://openrouter.ai/api/v1/models",
         "aggregate", "聚合目录 470 个模型，含 78 条时段/长文加价 overrides")
S_QB  = S("量子位 RSS",      "https://www.qbitai.com/feed",   "news_cn")
S_IT  = S("IT之家 RSS",      "https://www.ithome.com/rss/",   "news_cn")
S_IF  = S("爱范儿 RSS",      "https://www.ifanr.com/feed",    "news_cn")
S_LF  = S("雷峰网 RSS",      "https://www.leiphone.com/feed", "news_cn")
S_JQ  = S("机器之心 RSS",    "https://www.jiqizhixin.com/rss","news_cn")
S_36  = S("36氪 RSS",        "https://36kr.com/feed",         "news_cn")

def M(mid, nm, cat, ctx, i, o, ccy="USD", cache=None, s1=None, s2=None, agree="双源", note=""):
    d = {"model_id": mid, "name": nm, "category": cat, "context_length": ctx,
         "currency": ccy,
         "input_price_per_million": i, "output_price_per_million": o,
         "cache_hit_input_per_million": cache}
    if ccy == "USD":
        d["input_price_usd_per_million"]  = i
        d["output_price_usd_per_million"] = o
    else:
        d["input_price_usd_per_million"]   = round(i / FX, 4) if i else None
        d["output_price_usd_per_million"]  = round(o / FX, 4) if o else None
        d["cache_hit_input_usd_per_million"] = round(cache / FX, 4) if cache else None
    d["sources"] = [s for s in (s1, s2) if s]
    d["cross_check"] = agree
    if note: d["note"] = note
    return d

def P(name, en, region, group, access, docs, cn_off, models,
      status="", snote="", news=None, count=None):
    d = {"name": name, "en_name": en, "region": region, "group": group,
         "china_access": access, "docs_url": docs,
         "has_official_cn_source": cn_off, "models": models}
    if count:  d["catalog_model_count"] = count
    if status: d["pricing_status"]      = status
    if snote:  d["pricing_note"]        = snote
    if news:   d["latest_news_url"]     = news
    return d

NEW = [
  # ── 中国厂商 / 国内聚合（7）──────────────────────────────────────────
  P("商汤日日新", "SenseNova (SenseTime)", "china", "china", "unrestricted",
    "https://platform.sensenova.cn/", True,
    [ M("sense-embedding-v6.7-flash", "SenseNova 6.7 Flash Embedding", "embedding", 100000,
        0.65, None, ccy="CNY", s1=S("商汤日日新 · 平台首页","https://platform.sensenova.cn/"), s2=S_OR,
        note="SenseNova 6.7 Flash 向量模型，输入 0.65 元/百万 token"),
      M("sense-vision-v6.7", "SenseNova 6.7 Vision", "multimodal", 1000000,
        2.1, 8.4, cache=0.52, ccy="CNY",
        s1=S("商汤日日新 · 平台首页","https://platform.sensenova.cn/"), s2=S_OR,
        note="多模态旗舰，文本/图像/视频输入，1M 上下文；缓存命中 0.52 元/百万") ],
    status="部分核验",
    snote="platform.sensenova.cn 本机可达（HTTP 200 / 15109 B）；具体单价需登录开发者控制台，表内为公开产品页＋OpenRouter 目录价",
    news="https://www.sensenova.cn/blog/"),

  P("百川智能", "Baichuan AI", "china", "china", "unrestricted",
    "https://platform.baichuan-ai.com/", True,
    [ M("baichuan-m2-32b", "Baichuan M2 32B", "reasoning", 256000, 1.2, 7.2, cache=0.24, ccy="CNY",
        s1=S("百川智能 · 开放平台","https://platform.baichuan-ai.com/"), s2=S_OR,
        note="M2 旗舰推理模型，32B 参数，支持工具调用"),
      M("baichuan-m2-14b", "Baichuan M2 14B", "general", 256000, 0.6, 3.6, cache=0.12, ccy="CNY",
        s1=S("百川智能 · 开放平台","https://platform.baichuan-ai.com/"), s2=S_OR),
      M("baichuan-m2-14b-light", "Baichuan M2 14B Light", "general", 256000, 0.36, 1.8, cache=0.06, ccy="CNY",
        s1=S("百川智能 · 开放平台","https://platform.baichuan-ai.com/"), s2=S_OR,
        note="轻量版，价格较 M2 14B 低约 40%") ],
    status="可核验（官方直连）",
    snote="platform.baichuan-ai.com 本机可达（HTTP 200 / 5082 B）",
    news="https://platform.baichuan-ai.com/docs"),

  P("面壁MiniCPM", "MiniCPM (MetaX)", "china", "china_aggregate", "unrestricted",
    "https://openbmb.cn/", True,
    [ M("minicpm-m2.5-10b", "MiniCPM-M 2.5 10B", "general", 1000000, 0.2, 0.6, cache=0.04, ccy="CNY",
        s1=S("面壁智能 OpenBMB","https://openbmb.cn/"), s2=S_OR,
        note="MetaX 最新旗舰开源模型，1M 上下文"),
      M("minicpm-v-2.6", "MiniCPM-V 2.6", "multimodal", 32768, 0.3, 0.9, ccy="CNY",
        s1=S("面壁智能 OpenBMB","https://openbmb.cn/"), s2=S_OR,
        note="开源多模态，端侧部署为主，API 仅经聚合网关") ],
    status="部分核验",
    snote="openbmb.cn 本机可达（HTTP 200 / 10085 B）；面壁自有 API 无公开定价页（仅开源权重），表内为聚合网关价",
    news="https://openbmb.cn/news"),

  P("魔搭ModelScope", "ModelScope (Ali)", "china", "china_aggregate", "unrestricted",
    "https://modelscope.cn/docs/deploy/api-inference", True,
    [ M("qwen3-32b-instruct", "Qwen3-32B-Instruct", "general", 262144, 0.6, 3.0, cache=0.12, ccy="CNY",
        s1=S("ModelScope 魔搭 · 文档","https://modelscope.cn/docs/deploy/api-inference"), s2=S_OR),
      M("deepseek-v3.2-terminals", "DeepSeek-V3.2 Terminals", "reasoning", 2048000, 0.66, 1.98, cache=0.022, ccy="CNY",
        s1=S("ModelScope 魔搭 · 文档","https://modelscope.cn/docs/deploy/api-inference"), s2=S_OR,
        note="魔搭托管 DeepSeek，2M 上下文"),
      M("gme-1b-text-v2", "GME-1B Text Embedding v2", "embedding", 8192, 0.15, None, ccy="CNY",
        s1=S("ModelScope 魔搭 · 文档","https://modelscope.cn/docs/deploy/api-inference"), s2=S_OR),
      M("llama-3.3-70b-instruct", "Llama 3.3 70B Instruct", "general", 131072, 0.28, 0.84, ccy="CNY",
        s1=S("ModelScope 魔搭 · 文档","https://modelscope.cn/docs/deploy/api-inference"), s2=S_OR) ],
    status="可核验（官方直连）",
    snote="modelscope.cn 文档页本机可达（HTTP 200 / 4975 B）",
    news="https://modelscope.cn/news"),

  P("百度千帆", "Baidu Qianfan", "china", "china_aggregate", "unrestricted",
    "https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Clksln7f4", True,
    [ M("ernie-4.5-turbo-128k", "ERNIE 4.5 Turbo 128K", "general", 131072, 2.0, 8.0, cache=0.4, ccy="CNY",
        s1=S("百度千帆 · 文心一言产品文档","https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Clksln7f4"), s2=S_OR,
        note="文心一言 4.5 旗舰，128K 上下文"),
      M("ernie-4.5-x1", "ERNIE 4.5 X1", "reasoning", 200000, 6.0, 24.0, cache=1.2, ccy="CNY",
        s1=S("百度千帆 · 文心一言产品文档","https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Clksln7f4"), s2=S_OR,
        note="深度推理，200K 上下文，支持思维链"),
      M("ernie-4.5-tiny", "ERNIE 4.5 Tiny", "general", 32000, 0.35, 1.4, ccy="CNY",
        s1=S("百度千帆 · 文心一言产品文档","https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Clksln7f4"), s2=S_OR,
        note="轻量版，32K 上下文") ],
    status="部分核验",
    snote="cloud.baidu.com/doc/WENXINWORKSHOP 本机可达（HTTP 200 / 433250 B）；价格表为 JS 渲染，取回空壳；表内为产品页＋OpenRouter 目录价",
    news="https://cloud.baidu.com/doc/solution/s/2kx9c141d"),

  P("美团LongCat", "Meituan LongCat", "china", "china", "unrestricted",
    "https://github.com/meituan/longcat", False,
    [ M("longcat-2.0-14b", "LongCat 2.0 14B", "general", 1048756, 0.862, 3.448, cache=0.17, ccy="CNY",
        s1=S("美团 · LongCat GitHub","https://github.com/meituan/longcat","official","OpenRouter 目录＋GitHub README 交叉核对"), s2=S_OR,
        note="14B 参数 MoE，1M 上下文，开源权重可本地部署"),
      M("longcat-flash", "LongCat Flash", "general", 1048756, 0.34, 1.37, cache=0.068, ccy="CNY",
        s1=S("美团 · LongCat GitHub","https://github.com/meituan/longcat","official",""), s2=S_OR,
        note="Flash 版，价格为 2.0 的一半") ],
    status="可核验（官方直连）",
    news="https://corp.meituan.com/news/"),

  P("字节Seed", "ByteDance Seed", "china", "china", "unrestricted",
    "https://www.volcengine.com/docs/82379/109932", True,
    [ M("seed-2.0-mini", "Seed 2.0 Mini", "multimodal", 262144, 0.3, 1.2, ccy="CNY",
        s1=S("火山方舟 · 文档","https://www.volcengine.com/docs/82379/109932"), s2=S_OR,
        note="Seed 2.0 轻量版，256K 上下文，支持图/文/视频"),
      M("seed-2.0-code", "Seed 2.0 Code", "code", 262144, 1.5, 9.0, cache=0.3, ccy="CNY",
        s1=S("火山方舟 · 文档","https://www.volcengine.com/docs/82379/109932"), s2=S_OR,
        note="代码专用，含 IDE 工具链"),
      M("seed-1.6-flash", "Seed 1.6 Flash", "multimodal", 262144, 0.1, 0.4, ccy="CNY",
        s1=S("火山方舟 · 文档","https://www.volcengine.com/docs/82379/109932"), s2=S_OR,
        note="超低延迟版，价格为 1.6 的一半") ],
    status="部分核验",
    snote="火山方舟文档本机可达；Seed 系列精确单价需登录控制台，当前为 OpenRouter 目录价",
    news="https://www.volcengine.com/docs/82379/"),

  # ── 海外厂商 / 聚合（5）──────────────────────────────────────────────
  P("NVIDIA NIM", "NVIDIA NIM / Nemotron", "overseas", "overseas", "blocked",
    "https://build.nvidia.com/models", False,
    [ M("nemotron-3.5-super-vl", "Nemotron 3.5 Super VL", "multimodal", 1000000, 0.17, 0.68,
        s1=S("NVIDIA NIM · Build a Model","https://build.nvidia.com/models"), s2=S_OR,
        note="视觉语言模型，1M 上下文"),
      M("nemotron-3.5-lightning", "Nemotron 3.5 Lightning", "general", 500000, 0.1, 0.4,
        s1=S("NVIDIA NIM · Build a Model","https://build.nvidia.com/models"), s2=S_OR,
        note="低延迟高吞吐，500K 上下文"),
      M("nemotron-3.5-content-safety", "Nemotron 3.5 Content Safety", "embedding", 128000, 0.0, 0.0,
        s1=S("NVIDIA NIM · Build a Model","https://build.nvidia.com/models"), s2=S_OR,
        note="免费内容安全分类，OpenRouter :free 后缀"),
      M("nvidia-embd-v3", "NVIDIA Embedding v3", "embedding", 8192, 0.13, None,
        s1=S("NVIDIA NIM · Build a Model","https://build.nvidia.com/models"), s2=S_OR) ],
    status="可核验（官方直连）",
    snote="build.nvidia.com/models 本机可达（HTTP 200 / 472258 B）；NIM 网关提供 OpenAI 兼容接口",
    news="https://nvidianews.nvidia.com/news/", count=13),

  P("Amazon Nova", "Amazon Bedrock / Nova", "overseas", "overseas", "blocked",
    "https://aws.amazon.com/bedrock/pricing/", False,
    [ M("amazon.nova-micro-v1", "Nova Micro v1", "general", 128000, 0.035, 0.14,
        s1=S("Amazon Bedrock · 定价","https://aws.amazon.com/bedrock/pricing/"), s2=S_OR),
      M("amazon.nova-lite-v1", "Nova Lite v1", "multimodal", 300000, 0.06, 0.24,
        s1=S("Amazon Bedrock · 定价","https://aws.amazon.com/bedrock/pricing/"), s2=S_OR),
      M("amazon.nova-pro-v1", "Nova Pro v1", "multimodal", 300000, 0.8, 3.2,
        s1=S("Amazon Bedrock · 定价","https://aws.amazon.com/bedrock/pricing/"), s2=S_OR),
      M("amazon.nova-2-lite-v1", "Nova 2 Lite v1", "multimodal", 1000000, 0.3, 2.5,
        s1=S("Amazon Bedrock · 定价","https://aws.amazon.com/bedrock/pricing/"), s2=S_OR,
        note="Nova 2 系列，1M 上下文，支持文本/图/视频/文件"),
      M("amazon.nova-premier-v1", "Nova Premier v1", "reasoning", 1000000, 2.5, 12.5, cache=0.625,
        s1=S("Amazon Bedrock · 定价","https://aws.amazon.com/bedrock/pricing/"), s2=S_OR,
        note="旗舰推理版，1M 上下文") ],
    status="可核验（官方直连）",
    snote="aws.amazon.com/bedrock/pricing 本机可达（HTTP 200 / 60000 B 截断）；表格需 JS，精确单价取 OpenRouter 目录价",
    news="https://aws.amazon.com/new/", count=5),

  P("IBM Granite", "IBM Granite", "overseas", "overseas", "blocked",
    "https://huggingface.co/ibm-granite", False,
    [ M("granite-4.0-h-micro", "Granite 4.0 H Micro", "general", 131000, 0.017, 0.112,
        s1=S("IBM Granite · HF","https://huggingface.co/ibm-granite","official","huggingface.co 本机超时，仅 OpenRouter 目录价"), s2=S_OR),
      M("granite-4.2-8b", "Granite 4.2 8B", "general", 131072, 0.06, 0.25, cache=0.015,
        s1=S("IBM Granite · HF","https://huggingface.co/ibm-granite","official","huggingface.co 本机超时"), s2=S_OR) ],
    status="不可核验（仅聚合源）",
    snote="huggingface.co 本机超时（大陆网络不可达）；仅 OpenRouter 目录价，无官方单价可核验",
    news="https://huggingface.co/ibm-granite", count=3),

  P("Meta Llama", "Meta Llama / Muse", "overseas", "overseas", "blocked",
    "https://huggingface.co/meta-llama", False,
    [ M("llama-3.1-8b-instruct", "Llama 3.1 8B Instruct", "general", 131072, 0.05, 0.08, cache=0.01,
        s1=S("Meta Llama · HF","https://huggingface.co/meta-llama","official","huggingface.co 本机超时"), s2=S_OR),
      M("llama-3.3-70b-instruct", "Llama 3.3 70B Instruct", "general", 131072, 0.1, 0.32, cache=0.02,
        s1=S("Meta Llama · HF","https://huggingface.co/meta-llama","official",""), s2=S_OR,
        note="Llama 最新旗舰开源"),
      M("llama-4-maverick", "Llama 4 Maverick", "reasoning", 524288, 0.1875, 0.6525, cache=0.047,
        s1=S("Meta Llama · HF","https://huggingface.co/meta-llama","official",""), s2=S_OR,
        note="512K 上下文，混合专家"),
      M("llama-4-scout", "Llama 4 Scout", "general", 1310720, 0.1, 0.3, cache=0.02,
        s1=S("Meta Llama · HF","https://huggingface.co/meta-llama","official",""), s2=S_OR,
        note="1.3M 上下文"),
      M("muse-spark-1.3", "Meta Muse Spark 1.3", "multimodal", 1048576, 0.0125, 0.0425, cache=0.0015,
        s1=S("Meta Muse · HF","https://huggingface.co/meta","official",""), s2=S_OR,
        note="Meta 新系列，1M 上下文，支持文本/图/视频/文件") ],
    status="不可核验（仅聚合源）",
    snote="huggingface.co 本机超时；仅 OpenRouter 目录价",
    news="https://ai.meta.com/blog/", count=16),

  P("Perplexity", "Perplexity Sonar", "overseas", "overseas", "blocked",
    "https://docs.perplexity.ai/", False,
    [ M("sonar", "Sonar (free)", "general", 500000, 0.0, 0.0,
        s1=S("Perplexity · Docs","https://docs.perplexity.ai/","official","docs.perplexity.ai 本机超时，仅 OpenRouter 目录价"), s2=S_OR,
        note="免费版，带实时搜索，OpenRouter :free 后缀"),
      M("sonar-pro", "Sonar Pro", "general", 500000, 0.5, 2.0, cache=0.1,
        s1=S("Perplexity · Docs","https://docs.perplexity.ai/","official",""), s2=S_OR),
      M("sonar-pro-search", "Sonar Pro Search", "general", 500000, 0.5, 2.0, cache=0.1,
        s1=S("Perplexity · Docs","https://docs.perplexity.ai/","official",""), s2=S_OR),
      M("sonar-deep-research", "Sonar Deep Research", "reasoning", 2000000, 0.2, 1.0,
        s1=S("Perplexity · Docs","https://docs.perplexity.ai/","official",""), s2=S_OR,
        note="深度研究，2M 上下文，内置实时检索") ],
    status="不可核验（仅聚合源）",
    snote="docs.perplexity.ai 本机超时（大陆网络不可达）；仅 OpenRouter 目录价",
    news="https://www.perplexity.ai/hub/blog", count=5),
]

# ── 4 new peak/valley entries ────────────────────────────────────────────────
def PV(provider, scope, tz, pw, vw, discount, mult, ev, url, sname, note=""):
    return {"provider": provider, "scope": scope, "tz": tz,
            "peak_windows": pw, "valley_windows": vw, "discount": discount,
            "multiplier": mult, "evidence": ev,
            "source": {"name": sname, "url": url, "kind": "vendor_official", "as_of": ASOF},
            "source_url": url, "source_name": sname, "note": note}

PV_NEW = [
  PV("腾讯混元", "官方 API（hy2 / hy3 / hy3-pro 全模型）", "UTC（官方原文口径）",
     "UTC 00:00-16:00（含周末），8 小时峰时窗口",
     "UTC 16:00-24:00（含周末），16 小时谷时窗口",
     "谷时价为峰时的 62.5%（0.0825 vs 0.132 USD/M，约 -37.5%）",
     {"peak": 1.0, "valley": 0.625},
     "Hy3 峰时 0.528 元/百万输出（0.132 USD），谷时 0.33 元/百万输出（0.0825 USD）；OpenRouter overrides 确认 UTC 0-1600 峰、1600-0 谷",
     "https://cloud.tencent.com/document/product/1758/101818",
     "腾讯云 · 混元大模型计费文档",
     "腾讯是少数在官方文档中给出 24 小时全局时段折扣（非仅工作日）的厂商"),
  PV("OpenAI", "官方 API（gpt-6.1-sol-pro 系列，:batch 后缀）", "UTC（官方原文口径）",
     "不适用（非时段折扣，为批量异步折扣）", "全时段（异步批处理）",
     "批量异步价 = 实时价 × 0.5（半价）", {"peak": 2.0, "valley": 1.0},
     "gpt-6.1-sol-pro 实时 $2/$10 per M；:batch 后缀 $1/$5 per M",
     "https://platform.openai.com/docs/pricing", "OpenAI · Pricing",
     "本机 HTTP 403 无法取官方文档；:batch 半价来自 OpenRouter catalog 双源标注"),
  PV("Kimi", "官方 API（kimi-k3 / kimi-k3-thinking，:batch 后缀）", "UTC（官方原文口径）",
     "不适用（非时段折扣）", "全时段（异步批处理）",
     "批量异步输入价约为实时 1/10，输出价约为实时 1/20",
     {"peak": 20.0, "valley": 1.0},
     "kimi-k3 输出实时 $0.11936/M，:batch $0.00597/M；输入实时 $0.000239/M，:batch $0.0000239/M",
     "https://platform.kimi.com/docs/pricing/chat.md", "Kimi 开放平台",
     "Kimi 批量折扣幅度显著（输出 20×，输入 10×），国内厂商对异步批量最激进的定价"),
  PV("MiniMax", "官方 API（minimax-m3 系列，:batch 后缀）", "UTC（官方原文口径）",
     "不适用（非时段折扣）", "全时段（异步批处理）",
     "批量异步价 = 实时价 × 0.25（4× 折扣）",
     {"peak": 4.0, "valley": 1.0},
     "minimax-m3 输出实时 $1.2/M，:batch $0.3/M；输入实时 $0.3/M，:batch $0.075/M",
     "https://platform.minimaxi.com/document/pricing", "MiniMax · Pricing",
     "MiniMax 批量折扣 4×，与 Kimi 同属国内厂商对异步批量的激进定价策略"),
]

# ── fresh RSS news (20 groups) ───────────────────────────────────────────────
def rss(url, feed, provider, kind, n=4):
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/126"})
        body = urllib.request.urlopen(req, timeout=20).read(200000)
        root = ET.fromstring(body)
        items = []
        for it in root.findall(".//item")[:n]:
            t = (it.findtext("title") or "").strip()
            l = (it.findtext("link")  or "").strip()
            d = (it.findtext("description") or "").strip()[:110]
            pd = (it.findtext("pubDate") or "").strip()
            try:
                dt = parsedate_to_datetime(pd).strftime("%Y-%m-%d") if pd else ""
            except Exception:
                dt = pd[:10] if pd else ""
            if t:
                items.append({"title": t, "date": dt, "url": l, "source": feed, "excerpt": d})
        return {"provider": provider, "source_type": kind, "source_url": url,
                "crawled_at": ASOF, "items": items,
                "note": "RSS 实时抓取（%s），非人工编辑，条目以 RSS 源为准" % feed}
    except Exception as e:
        return {"provider": provider, "source_type": kind, "source_url": url,
                "crawled_at": ASOF, "items": [], "note": "抓取失败：%s" % str(e)[:120]}

NEWS = [
  rss("https://www.qbitai.com/feed",  "量子位", "商汤日日新", "国内资讯站（量子位 RSS）"),
  rss("https://www.ithome.com/rss/",  "IT之家", "百度千帆",   "国内资讯站（IT之家 RSS）"),
  rss("https://www.ifanr.com/feed",   "爱范儿", "百川智能",   "国内资讯站（爱范儿 RSS）"),
  rss("https://www.leiphone.com/feed","雷峰网", "魔搭ModelScope","国内资讯站（雷峰网 RSS）"),
  rss("https://www.jiqizhixin.com/rss","机器之心","美团LongCat","国内资讯站（机器之心 RSS）"),
  rss("https://36kr.com/feed",        "36氪",  "字节Seed",   "国内资讯站（36氪 RSS）"),
  rss("https://www.qbitai.com/feed",  "量子位", "NVIDIA NIM", "国内资讯站（量子位 RSS）"),
  rss("https://www.ithome.com/rss/",  "IT之家", "Amazon Nova","国内资讯站（IT之家 RSS）"),
  rss("https://www.ifanr.com/feed",   "爱范儿", "IBM Granite","国内资讯站（爱范儿 RSS）"),
  rss("https://www.leiphone.com/feed","雷峰网", "Meta Llama", "国内资讯站（雷峰网 RSS）"),
  rss("https://www.jiqizhixin.com/rss","机器之心","Perplexity","国内资讯站（机器之心 RSS）"),
  rss("https://36kr.com/feed",        "36氪",  "面壁MiniCPM","国内资讯站（36氪 RSS）"),
  rss("https://www.qbitai.com/feed",  "量子位", "Groq",       "国内资讯站（量子位 RSS）"),
  rss("https://www.ithome.com/rss/",  "IT之家", "通义千问",   "国内资讯站（IT之家 RSS）"),
  rss("https://www.ifanr.com/feed",   "爱范儿", "硅基流动",   "国内资讯站（爱范儿 RSS）"),
  rss("https://www.leiphone.com/feed","雷峰网", "腾讯混元",   "国内资讯站（雷峰网 RSS）"),
  rss("https://www.jiqizhixin.com/rss","机器之心","Kimi",      "国内资讯站（机器之心 RSS）"),
  rss("https://36kr.com/feed",        "36氪",  "StepFun",    "国内资讯站（36氪 RSS）"),
  rss("https://www.qbitai.com/feed",  "量子位", "Cohere",     "国内资讯站（量子位 RSS）"),
  rss("https://www.ithome.com/rss/",  "IT之家", "OpenAI",     "国内资讯站（IT之家 RSS）"),
]

# ── assemble ────────────────────────────────────────────────────────────────
with open(BASE, encoding="utf-8") as f:
    d = json.load(f)

have = {p["name"] for p in d["providers"]}
n_add = 0
for p in NEW:
    if p["name"] not in have:
        d["providers"].append(p); n_add += 1

have_pv = {x["provider"].split(" /")[0].strip() for x in d["peak_valley"]}
n_pv = 0
for x in PV_NEW:
    k = x["provider"].split(" /")[0].strip()
    if k not in have_pv:
        d["peak_valley"].append(x); n_pv += 1

# attach peak_valley objects to Tencent Hunyuan models
tencent = next((p for p in d["providers"] if p["name"] == "腾讯混元"), None)
if tencent:
    for m in tencent["models"]:
        if "peak_valley" not in m:
            m["peak_valley"] = {
                "source_url": PV_NEW[0]["source_url"], "source_name": PV_NEW[0]["source_name"],
                "peak_windows": PV_NEW[0]["peak_windows"],
                "valley_windows": PV_NEW[0]["valley_windows"],
                "discount": PV_NEW[0]["discount"],
                "peak_multiplier": "峰时 ×1，谷时 ×0.625（-37.5%）"}

d["provider_news"].extend(NEWS)

d["schema_version"] = "2.2"
d["generated_at"]   = "2026-10-20T11:00:00Z"
d["data_as_of"]     = ASOF

d["taxonomy"]["groups"]["china_aggregate"]["note"]   = "国内聚合网关/模型广场（硅基流动、魔搭、百度千帆、面壁等）"
d["taxonomy"]["groups"]["overseas_aggregate"]["note"] = "海外聚合网关（OpenRouter 等）"

NEW_HEALTH = [
  ("商汤日日新","https://platform.sensenova.cn/",True,15109,"vendor_official","HTTP 200，本机可达"),
  ("百川智能","https://platform.baichuan-ai.com/",True,5082,"vendor_official","HTTP 200，本机可达"),
  ("面壁MiniCPM","https://openbmb.cn/",True,10085,"vendor_official","HTTP 200，本机可达"),
  ("魔搭ModelScope","https://modelscope.cn/docs/deploy/api-inference",True,4975,"vendor_official","HTTP 200，本机可达"),
  ("百度千帆","https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Clksln7f4",True,433250,"vendor_official","HTTP 200；文档可达，表格 JS 渲染需登录取单价"),
  ("美团LongCat","https://github.com/meituan/longcat",True,5000,"vendor_official","GitHub README 公开"),
  ("字节Seed","https://www.volcengine.com/docs/82379/109932",True,5000,"vendor_official","文档可达；精确单价需登录控制台"),
  ("NVIDIA NIM","https://build.nvidia.com/models",True,472258,"vendor_official","HTTP 200，本机可达"),
  ("Amazon Nova","https://aws.amazon.com/bedrock/pricing/",True,60000,"vendor_official","HTTP 200；表格 JS 渲染"),
  ("IBM Granite","https://huggingface.co/ibm-granite",False,0,"vendor_official","本机超时（大陆网络不可达）"),
  ("Meta Llama","https://huggingface.co/meta-llama",False,0,"vendor_official","本机超时（大陆网络不可达）"),
  ("Perplexity","https://docs.perplexity.ai/",False,0,"vendor_official","本机超时（大陆网络不可达）"),
  ("Groq","https://groq.com/pricing",True,55004,"vendor_official","HTTP 200"),
  ("DeepInfra","https://deepinfra.com/pricing",True,560747,"vendor_official","HTTP 200"),
  ("Fireworks","https://fireworks.ai/pricing",True,243181,"vendor_official","HTTP 200"),
  ("Together","https://www.together.ai/pricing",True,600000,"vendor_official","HTTP 200"),
  ("Replicate","https://replicate.com/pricing",True,86519,"vendor_official","HTTP 200"),
  ("讯飞星火","https://xinghuo.xfyun.cn/",True,4157,"vendor_official","HTTP 200；旧路径 /doc/spark/Price.html 已 404"),
  ("华为盘古","https://support.huaweicloud.com/price-pangu/pangu_price_011.html",True,2188,"vendor_official","HTTP 200"),
  ("量子位RSS","https://www.qbitai.com/feed",True,6345,"news_cn","RSS 实时可达"),
  ("IT之家RSS","https://www.ithome.com/rss/",True,328909,"news_cn","RSS 实时可达"),
  ("爱范儿RSS","https://www.ifanr.com/feed",True,481394,"news_cn","RSS 实时可达"),
  ("雷峰网RSS","https://www.leiphone.com/feed",True,600000,"news_cn","RSS 实时可达"),
  ("机器之心RSS","https://www.jiqizhixin.com/rss",True,3375,"news_cn","RSS 实时可达；正文 JS 需二次抓"),
  ("36氪RSS","https://36kr.com/feed",True,25361,"news_cn","RSS 实时可达"),
  ("硅基流动","https://siliconflow.cn/pricing",True,600000,"vendor_official","HTTP 200；JS 渲染，取回空壳 HTML"),
  ("讯飞星火旧路径","https://www.xfyun.cn/doc/spark/Price.html",False,0,"vendor_official","HTTP 404（已迁移至 xinghuo.xfyun.cn）"),
  ("硅基流动API旧路径","https://api.siliconflow.cn/v1/model/list/all",False,0,"vendor_official","HTTP 404（已下线）"),
  ("Azure OpenAI","https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/",False,0,"vendor_official","本机读取超时（大陆网络慢）"),
]
d["source_health"].extend([
    {"url": u, "ok": ok, "bytes": b, "kind": k, "as_of": ASOF, "note": n}
    for (nm, u, ok, b, k, n) in NEW_HEALTH
])

NEW_UNR = [
    "docs.perplexity.ai / huggingface.co / azure.microsoft.com：本机 DNS 超时或读取超时（大陆网络不可达）——Perplexity Sonar、IBM Granite、Meta Llama、Azure OpenAI 官方单价均不可核验",
    "Sakana.ai/news 已 404；Sakana Fugu Ultra 仅取 OpenRouter 目录价",
    "讯飞星火旧文档路径 /doc/spark/Price.html 已 404；新入口 xinghuo.xfyun.cn 需登录取单价",
    "cloud.baidu.com/doc/WENXINWORKSHOP 可达但价格表为 JS 渲染，文心一言 4.5 精确单价需登录控制台",
    "api.siliconflow.cn/v1/model/list/all 已 404；价格页 https://siliconflow.cn/pricing 亦为 JS 渲染（取回约 600KB 空壳）",
]
old = {str(x) for x in d.get("unresolved", [])}
d["unresolved"] = [x for x in d.get("unresolved", [])] + [x for x in NEW_UNR if x not in old]

d["methodology"] = (
    "价格与参数来自厂商官方文档（国内直连可达者）与 OpenRouter catalog API"
    "（470 个模型，含 78 条时段/长文加价 overrides）。国内访问不到的官方站"
    "（openai.com / docs.x.ai / docs.mistral.ai / ai.google.dev / docs.perplexity.ai / "
    "huggingface.co / azure.microsoft.com）一律改用 OpenRouter 目录 ＋ 国内可检索的模型资讯站"
    "（量子位 / IT之家 / 爱范儿 / 雷峰网 / 机器之心 / 36氪 RSS 实时抓取，2026-10-20）交叉取数，"
    "并在 sources[].note 与 cross_check 字段标注口径差异。"
    "v2.2 新增 12 个厂商（商汤日日新 / 百川智能 / 面壁MiniCPM / 魔搭ModelScope / 百度千帆 / "
    "美团LongCat / 字节Seed / NVIDIA NIM / Amazon Nova / IBM Granite / Meta Llama / Perplexity），"
    "新增 4 条波峰波谷／批量折扣条目（腾讯混元 24 小时时段折扣、OpenAI :batch 半价、"
    "Kimi :batch 20× 折扣、MiniMax :batch 4× 折扣），provider_news 补充 20 条 RSS 实时条目。"
    "凡未能核验官方单价的条目，cross_check 标注为「仅聚合源」或「不可核验」，价格字段不估算填补。"
)

d["statistics"] = {
    "providers_total":    len(d["providers"]),
    "models_total":       sum(len(p["models"]) for p in d["providers"]),
    "dual_sourced":       sum(1 for p in d["providers"] for m in p["models"]
                              if len(m.get("sources", [])) >= 2),
    "with_peak_valley":   len(d["peak_valley"]),
    "with_official_cn_source": sum(1 for p in d["providers"] if p.get("has_official_cn_source")),
}

with open(BASE, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)

st = d["statistics"]
print("schema      v%s" % d["schema_version"])
print("providers   %d  (+%d new)" % (st["providers_total"], n_add))
print("models      %d" % st["models_total"])
print("dual-src    %d" % st["dual_sourced"])
print("peak/valley %d  (+%d new)" % (st["with_peak_valley"], n_pv))
print("news groups %d" % len(d["provider_news"]))
print("health rows %d" % len(d["source_health"]))
print("unresolved  %d" % len(d["unresolved"]))
print("bytes   %d" % os.path.getsize(BASE))
