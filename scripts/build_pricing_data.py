# -*- coding: utf-8 -*-
"""Build llm_pricing_data.json v2 (schema v2) — harvested live 2026-10-20."""
import io, json, datetime

FX = 7.10          # approx USD->CNY, display aid only (labelled in JSON)
ASOF = "2026-10-20"
def usd(cny): return round(cny / FX, 4)
def src(name, url, note=""): return {"name": name, "url": url, "as_of": ASOF, "note": note}

S_DS=src("DeepSeek API Docs · Models & Pricing","https://api-docs.deepseek.com/quick_start/pricing")
S_DS_N=src("DeepSeek API Docs · News/Change Log","https://api-docs.deepseek.com/news")
S_KIMI=src("Kimi 开放平台 · 模型推理价格说明","https://platform.kimi.com/docs/pricing/chat.md")
S_MOON=src("Kimi 开放平台 · 定价文档","https://platform.moonshot.cn/docs/pricing")
S_MOON_N=src("Kimi 开放平台 · News","https://platform.moonshot.cn/docs/news")
S_STEP=src("阶跃星辰 · API 定价","https://platform.stepfun.com/docs/zh/guides/pricing/details.md")
S_STEP_A=src("阶跃星辰 · Step 5 Preview 调价公告","https://platform.stepfun.com/docs/zh/announcements/step-5-preview-price-adjustment.md")
S_SF=src("硅基流动 · 模型价格中心","https://siliconflow.cn/pricing")
S_SF_N=src("硅基流动 · 企业动态","https://siliconflow.cn/news")
S_ALI=src("阿里云百炼 · 模型大全功能规格与计费","https://help.aliyun.com/zh/model-studio/models")
S_ALI_N=src("阿里云百炼 · 发布记录","https://help.aliyun.com/zh/model-studio/release-notes")
S_QWEN=src("Qwen Blog","https://qwenlm.github.io/blog/")
S_VOLC=src("火山方舟 · 文档中心（模型列表/价格入口）","https://www.volcengine.com/docs/82379/109932")
S_VOLC_P=src("火山方舟 · 模型价格","https://www.volcengine.com/docs/82379/1544106","页面需登录/前端渲染，未取到官方单价")
S_HY=src("腾讯云 · 混元大模型计费文档","https://cloud.tencent.com/document/product/1758/101818")
S_GLM=src("智谱 BigModel · 定价页","https://open.bigmodel.cn/pricing","前端渲染（需 JS/登录），本机仅取回空壳页，改用可检索镜像源交叉核对")
S_ZP=src("智谱 Z.ai 官网 · 新闻/模型页","https://www.zhipuai.cn/zh")
S_ANTH=src("Anthropic · Plans & pricing","https://www.anthropic.com/pricing","可取回 200，但仅订阅价（Free/Pro/Max），无 API 单价表")
S_ANTH_N=src("Anthropic · News","https://www.anthropic.com/news")
S_OR=src("OpenRouter · Models catalog API","https://openrouter.ai/api/v1/models","聚合目录 470 个模型；为目录价（含平台费），非厂商原价")
S_OR_B=src("OpenRouter · Announcements","https://openrouter.ai/announcements")
S_MM=src("MiniMax · 产品定价/发布说明","https://platform.minimaxi.com/document/pricing")
S_COH=src("Cohere · Docs / Models","https://docs.cohere.com/docs/models","docs.cohere.com/docs/pricing 已 404")
S_OAI=src("OpenAI · 定价页","https://platform.openai.com/docs/pricing","本机返回 HTTP 403（地区/反爬限制），未能核验官方单价")
S_XAI=src("xAI · Models docs","https://docs.x.ai/developers/models","本机连接超时")
S_MIS=src("Mistral · Models overview","https://docs.mistral.ai/getting-started/models/models_overview/","本机连接超时")
S_JQ=src("机器之心 · 资讯站","https://www.jiqizhixin.com/","正文需 JS 渲染，本站仅作资讯入口")
S_QB=src("量子位 RSS","https://www.qbitai.com/feed")
S_IT=src("IT之家 RSS","https://www.ithome.com/rss/")
S_IF=src("爱范儿 RSS","https://www.ifanr.com/feed")
S_LF=src("雷峰网 RSS","https://m.leiphone.com/feed")

def M(mid, name, cat, ctx, i, o, ccy="USD", cache=None, s1=None, s2=None, agree="一致", note="", off=None):
    d = {"model_id": mid, "name": name, "category": cat, "context_length": ctx, "currency": ccy,
         "input_price_per_million": i, "output_price_per_million": o,
         "cache_hit_input_per_million": cache,
         "input_price_usd_per_million": (i if ccy=="USD" else (usd(i) if i is not None else None)),
         "output_price_usd_per_million": (o if ccy=="USD" else (usd(o) if o is not None else None)),
         "sources": [x for x in (s1, s2) if x], "cross_check": agree}
    if note: d["note"] = note
    if off: d["peak_valley"] = off
    return d

def P(name, en, region, group, cn, docs, official_cn, models, status="", snote="", news=None, note="", count=None):
    d = {"name": name, "en_name": en, "region": region, "group": group, "china_access": cn,
         "docs_url": docs, "has_official_cn_source": official_cn, "models": models}
    if count is not None: d["catalog_model_count"] = count
    if status: d["pricing_status"] = status
    if snote: d["pricing_note"] = snote
    if news: d["latest_news_url"] = news
    if note: d["note"] = note
    return d

providers = []

# ============================ 海外厂商 ============================
providers.append(P("OpenAI","OpenAI","overseas","overseas","blocked","https://platform.openai.com/docs/pricing",False,[
 M("gpt-6.1-sol","GPT-6.1 Sol","general",1050000,2.0,10.0,s1=S_OR,s2=S_OAI,agree="仅聚合源（官方 403）",note="官方定价页本机 HTTP 403，价格取自 OpenRouter 目录价"),
 M("gpt-6.1-sol-pro","GPT-6.1 Sol Pro","reasoning",1050000,2.0,10.0,s1=S_OR,agree="仅聚合源"),
 M("gpt-6-astra","GPT-6 Astra","reasoning",1050000,10.0,50.0,s1=S_OR,agree="仅聚合源"),
 M("gpt-6-luna","GPT-6 Luna","general",1050000,0.1,0.5,s1=S_OR,agree="仅聚合源"),
 M("gpt-5.6-luna","GPT-5.6 Luna","general",1050000,0.2,1.2,s1=S_OR,agree="仅聚合源"),
],"不可核验（403）",
 "platform.openai.com/docs/pricing 与 /api/pricing/ 均返回 HTTP 403，官方单价无法核验；表内为 OpenRouter 目录价（含平台费）",
 news="https://openai.com/news/", count=65))

providers.append(P("Anthropic","Anthropic (Claude)","overseas","overseas","blocked","https://www.anthropic.com/pricing",False,[
 M("claude-opus-5.5","Claude Opus 5.5","reasoning",1000000,4.0,20.0,s1=S_OR,s2=S_ANTH,agree="仅聚合源",note="官方页可访问但只给订阅价：Pro $17/月（年付）或 $20/月、Max 自 $100/月起"),
 M("claude-sonnet-5.5","Claude Sonnet 5.5","general",1000000,2.0,10.0,s1=S_OR,s2=S_ANTH,agree="仅聚合源"),
 M("claude-haiku-5.5","Claude Haiku 5.5","general",1000000,0.1,0.5,s1=S_OR,agree="仅聚合源"),
 M("claude-fable-5.1","Claude Fable 5.1","reasoning",1000000,10.0,50.0,s1=S_OR,agree="仅聚合源"),
 M("claude-sonnet-4.6","Claude Sonnet 4.6","general",1000000,3.0,15.0,s1=S_OR,agree="仅聚合源"),
],"部分核验",
 "anthropic.com/pricing 取回 200，含 Claude 订阅计划价（Free / Pro / Max，Max 附 $100–$200/月 API credits），API 每百万 tokens 单价仍需 platform 控制台核验",
 news="https://www.anthropic.com/news", count=15))

providers.append(P("Google Gemini","Google (Gemini)","overseas","overseas","blocked","https://ai.google.dev/gemini-api/docs/pricing",False,[
 M("gemini-4-argon","Gemini 4 Argon","general",1048576,2.0,10.0,s1=S_OR,agree="仅聚合源"),
 M("gemini-3.8-flash","Gemini 3.8 Flash","multimodal",1048576,0.825,4.125,s1=S_OR,agree="仅聚合源"),
 M("gemini-3.5-flash-lite","Gemini 3.5 Flash-Lite","multimodal",1048576,0.3,2.5,s1=S_OR,agree="仅聚合源"),
 M("gemini-3-pro-image","Gemini 3 Pro Image","multimodal",131072,2.0,12.0,s1=S_OR,agree="仅聚合源"),
 M("gemini-nano-banana-2.1","Nano Banana 2.1（图像）","multimodal",65536,1.5,7.5,s1=S_OR,agree="仅聚合源"),
],"不可核验（超时）","ai.google.dev 本机连接超时（大陆不可直连）；数值取自 OpenRouter 目录价",
 news="https://blog.google/technology/ai/", count=30))

providers.append(P("Mistral","Mistral AI","overseas","overseas","blocked","https://docs.mistral.ai/getting-started/models/pricing",False,[
 M("mistral-large-4","Mistral Large 4","general",1048576,0.68,2.09,s1=S_OR,agree="仅聚合源"),
 M("mistral-large-2512","Mistral Large 2512","general",262144,0.5,1.5,s1=S_OR,agree="仅聚合源"),
 M("mistral-medium-3.5","Mistral Medium 3.5","general",262144,1.5,7.5,s1=S_OR,agree="仅聚合源"),
 M("mistral-small-2603","Mistral Small 2603","general",262144,0.15,0.6,s1=S_OR,agree="仅聚合源"),
 M("devstral-2512","Devstral 2512（代码）","code",262144,0.4,2.0,s1=S_OR,agree="仅聚合源"),
],"不可核验（超时）","docs.mistral.ai / mistral.ai 本机连接超时；数值取自 OpenRouter 目录价",
 news="https://mistral.ai/news", count=20))

providers.append(P("Cohere","Cohere","overseas","overseas","blocked","https://docs.cohere.com/docs/models",False,[
 M("command-a-plus-05-2026","Command A+","general",192000,0.3,1.5,s1=S_OR,s2=S_COH,agree="双源（官方文档给型号与上下文，OpenRouter 给单价）"),
 M("command-a-03-2026","Command A","general",256000,2.5,10.0,s1=S_OR,s2=S_COH,agree="双源"),
 M("command-r-plus-08-2024","Command R+","general",128000,2.5,10.0,s1=S_OR,agree="仅聚合源"),
 M("command-r7b-12-2024","Command R7B","general",128000,0.0375,0.15,s1=S_OR,agree="仅聚合源"),
],"部分核验","docs.cohere.com/docs/models 可访问（模型/上下文/端点表），docs.cohere.com/docs/pricing 已 404，单价仅 OpenRouter 源",
 news="https://cohere.com/blog", count=5))

providers.append(P("xAI","xAI (Grok)","overseas","overseas","blocked","https://docs.x.ai/developers/models",False,[
 M("grok-4.7","Grok 4.7","general",500000,2.0,6.0,s1=S_OR,agree="仅聚合源"),
 M("grok-4.5","Grok 4.5","general",500000,2.0,6.0,s1=S_OR,agree="仅聚合源"),
 M("grok-4.3","Grok 4.3","general",1000000,1.25,2.5,s1=S_OR,agree="仅聚合源"),
 M("grok-build-0.1","Grok Build 0.1（代码）","code",256000,1.0,2.0,s1=S_OR,agree="仅聚合源"),
],"不可核验（超时）","docs.x.ai / x.ai 本机连接超时；数值取自 OpenRouter 目录价",
 news="https://x.ai/news", count=7))

providers.append(P("Groq","Groq","overseas","overseas","blocked","https://console.groq.com/docs/pricing",False,[
 M("openai/gpt-oss-120b","GPT-OSS 120B（Groq 托管）","general",131072,0.15,0.6,s1=S_OR,agree="仅聚合源"),
],"不可核验","docs.x.ai 类站外源超时；本行以 OpenRouter 目录价为唯一可取源", news="https://groq.com/newsroom/", count=6))

# ============================ 国内厂商 ============================
providers.append(P("DeepSeek","DeepSeek（深度求索）","china","china","unrestricted","https://api-docs.deepseek.com/quick_start/pricing",True,[
 M("deepseek-flash","DeepSeek-V4.1-Flash-1017","general",1048576,0.3,1.2,ccy="CNY",cache=0.15,s1=S_DS,s2=S_OR,agree="双源一致（目录价 0.3/1.2 USD 档为峰时折算）",
   off={"peak":"北京时间 09:00-12:00 与 14:00-18:00（UTC 01:00-04:00、06:00-10:00，周一至周五，中国法定节假日除外）","valley":"其余时段（含周末与法定节假日全天）","off_peak_discount":"谷时段价格为峰时的 50%（半价）","peak_multiplier":"峰时 ×2","source":S_DS["url"],
        "peak_prices":{"input_cache_miss":0.6,"input_cache_hit":0.3,"output":2.4},"valley_prices":{"input_cache_miss":0.3,"input_cache_hit":0.15,"output":1.2}}),
 M("deepseek-v4-pro","DeepSeek-V4-Pro-0813","reasoning",1048576,0.66,1.98,ccy="CNY",cache=0.022,s1=S_DS,s2=S_SF,agree="双源",
   off={"peak":"同 DeepSeek 官方峰时（UTC 01-04、06-10 工作日）","valley":"其余时段","off_peak_discount":"谷时 = 峰时 × 50%","source":S_DS["url"],
        "peak_prices":{"input_cache_miss":1.32,"input_cache_hit":0.044,"output":3.96},"valley_prices":{"input_cache_miss":0.66,"input_cache_hit":0.022,"output":1.98}}),
 M("deepseek-v3.2","DeepSeek-V3.2（上一代）","general",163840,0.28,0.42,ccy="USD",s1=S_OR,agree="仅聚合源",
   note="官方说明：legacy 名称 deepseek-v4-flash / -vision-exp 仍接受但模型已退役，请求由 V4.1-Flash-1017 承接并按 Flash 价计费"),
],"可核验（官方直连）","官方定价页本机可直连取回（HTTP 200），价格与峰谷规则均取自官方原文",
 news="https://api-docs.deepseek.com/news", count=3,
 note="另有 Search / Fetch 独立 API：$0.75 每 1000 次成功请求；DeepSeek Harness 内测中，2026-11-01 00:00（北京时间）起服务端工具调用开始计费"))

providers.append(P("Kimi","Kimi（月之暗面 Moonshot AI）","china","aggregate" if False else "china","unrestricted","https://platform.kimi.com/docs/pricing/chat.md",True,[
 M("kimi-k3","Kimi K3","reasoning",1048576,20.0,100.0,ccy="CNY",cache=2.0,s1=S_KIMI,s2=S_MOON,agree="双源一致（官方文档，两域名同表）",
   note="K3 缓存写入另计：TTL 5min ¥20／TTL 1h ¥40（每百万 tokens）；OpenRouter 目录价 0.239/11.936 疑为批量或促销档，口径差异大",
   off={"peak":"官方未设峰谷计价","valley":"全天统一价；可用批量推理（Batch）替代谷时段省钱","off_peak_discount":"Batch API = 标准价 60%","source":S_KIMI["url"],
        "batch":{"kimi-k2.7-code":{"input_cache_miss":3.90,"input_cache_hit":0.78,"output":16.20},"kimi-k2.6":{"input_cache_miss":3.90,"input_cache_hit":0.66,"output":16.20}}}),
 M("kimi-k2.7-code","Kimi K2.7 Code","code",262144,6.5,27.0,ccy="CNY",cache=1.3,s1=S_KIMI,s2=S_SF,agree="双源一致（硅基流动镜像 ¥6.5/¥27）"),
 M("kimi-k2.7-code-highspeed","Kimi K2.7 Code Highspeed","code",262144,13.0,54.0,ccy="CNY",cache=2.6,s1=S_KIMI,agree="仅官方源"),
 M("kimi-k2.6","Kimi K2.6","general",262144,6.5,27.0,ccy="CNY",cache=1.1,s1=S_KIMI,s2=S_SF,agree="双源一致"),
],"可核验（官方直连）","platform.kimi.com / platform.moonshot.cn 本机均可直连取回 Markdown 定价表",
 news="https://platform.moonshot.cn/docs/news", count=4,
 note="批量推理（Batch）不受实时并发限制，费用为标准价 60%，需 completion_window 内完成"))

providers.append(P("GLM","GLM（智谱 Z.ai）","china","china","unrestricted","https://open.bigmodel.cn/pricing",True,[
 M("glm-5.3","GLM-5.3","general",1048576,8.0,28.0,ccy="CNY",cache=2.0,s1=S_SF,s2=S_GLM,agree="镜像价（官方页需 JS 渲染无法直取）",
   note="智谱官网描述：GLM-5.3 前沿编程能力与涌现的网络安全能力，面向复杂软件工程与长程 Agent 任务，支持 1M 上下文"),
 M("glm-5.3-flash","GLM-5.3 Flash","general",1048576,0.8,2.8,ccy="CNY",cache=0.23,s1=S_SF,s2=S_GLM,agree="镜像价",
   note="硅基流动 2026-10-15 上线 GLM-5.3-Flash 高速版（GLM-5 系列首款原生多模态）"),
 M("glm-5.2","GLM-5.2","general",1048576,8.0,28.0,ccy="CNY",cache=2.0,s1=S_SF,s2=S_ALI,agree="镜像价（阿里云百炼模型列表亦上架 GLM-5.2）"),
 M("glm-5.1-pro","GLM-5.1 Pro（分段计价）","reasoning",204800,6.0,24.0,ccy="CNY",cache=1.3,s1=S_SF,agree="仅镜像源",
   note="输入 [0,32k) ¥6/¥24/缓存¥1.3；输入 [32k,+∞) ¥8/¥28/缓存¥2.0"),
 M("glm-5v-turbo","GLM-5V-Turbo（多模态）","multimodal",202752,1.2,4.0,ccy="USD",s1=S_OR,s2=S_ZP,agree="仅聚合源",
   note="OpenRouter 标注上下文 202752，与官网「1M 上下文」口径存在差异"),
],"需 JS/登录","open.bigmodel.cn/pricing 本机取回 200 但为前端空壳（需 JS + 登录），按约定改用国内可检索的硅基流动价格中心与阿里云百炼上架信息交叉核对",
 news="https://www.zhipuai.cn/news", count=16))

providers.append(P("通义千问","Qwen（阿里云百炼 Model Studio）","china","china","unrestricted","https://help.aliyun.com/zh/model-studio/models",True,[
 M("qwen3.8-max-0902","Qwen3.8 Max","general",1000000,2.0,6.0,ccy="USD",s1=S_OR,s2=S_ALI,agree="聚合价 + 官方上架确认（官方文档未直出单价）",
   note="阿里云百炼文档列出 qwen3.8-max / qwen3.7-plus / qwen3.8-flash 等文本生成矩阵，覆盖图像、音频、视频与向量重排序"),
 M("qwen3.8-max-prime","Qwen3.8 Max Prime","reasoning",1000000,4.0,12.0,ccy="USD",s1=S_OR,agree="仅聚合源"),
 M("qwen3.8-flash","Qwen3.8 Flash","general",1000000,0.15,0.47,ccy="USD",s1=S_OR,s2=S_ALI,agree="聚合价 + 官方上架确认"),
 M("qwen3.8-omni-flash","Qwen3.8 Omni Flash（全模态）","multimodal",1000000,0.15,0.47,ccy="USD",s1=S_OR,s2=S_ALI,agree="聚合价 + 官方上架确认",
   note="官方：音视频分析与文本生成用 qwen3.8-omni-flash（Chat Completions / Responses）；实时音视频对话用 qwen3.8-omni-flash-realtime；离线语音输出用 qwen3.5-omni-plus"),
 M("qwen3.7-plus","Qwen3.7 Plus","general",1000000,0.32,1.28,ccy="USD",s1=S_OR,s2=S_ALI,agree="聚合价 + 官方上架确认"),
 M("Qwen/Qwen3.8-27B","Qwen3.8-27B（开源权重）","general",262144,3.0,12.0,ccy="CNY",s1=S_SF,s2=S_ALI,agree="镜像价",
   note="同一开源权重模型在硅基流动为 ¥3/¥12，与官方按量目录价口径不同（自建 vs 托管）"),
],"部分核验","help.aliyun.com 与 alibabacloud.com 文档本机可直连（200），取到模型矩阵与能力说明；每百万 tokens 单价表位于控制台定价页，未匿名取回",
 news="https://help.aliyun.com/zh/model-studio/release-notes", count=42,
 note="百炼同时上架第三方模型：deepseek-v4-pro-0813、deepseek-v4.1-flash、kimi-k3、glm-5.2、ZHIPU/GLM-5.3、MiniMax-M3、mimo-v2.5-pro"))

providers.append(P("豆包","Doubao / Seed（火山方舟 VeRL-Ark）","china","china","unrestricted","https://www.volcengine.com/docs/82379/109932",True,[
 M("doubao-seed-2-5","Doubao Seed 2.5","general",1048576,0.8,2.0,ccy="CNY",s1=S_OR,s2=S_VOLC_P,agree="仅聚合源（方舟价格页需登录）",
   note="方舟文档中心可取回模型列表（Seed-Evolving、DeepSeek-V4.1-Flash 上架 1017 版本），model-pricing 页返回占位内容"),
 M("doubao-seedance-2-5","Doubao Seedance 2.5（视频生成）","video",0,None,None,ccy="CNY",s1=S_VOLC,agree="按秒/条计费，不适用 tokens 单价"),
 M("doubao-seedream-5.0-pro","Doubao Seedream 5.0 Pro / flash（图像生成）","image",0,None,None,ccy="CNY",s1=S_VOLC,agree="按张计费，不适用 tokens 单价"),
 M("ByteDance-Seed/Seed-OSS-36B-Instruct","Seed-OSS 36B Instruct（开源）","general",131072,1.5,4.0,ccy="CNY",s1=S_SF,s2=S_OR,agree="镜像价"),
],"文档可达、价格需登录","www.volcengine.com 文档中心本机可直连（200，189 KB），但 82379/1544106 模型价格页与 pricing 页仅返回渲染占位（需登录控制台）",
 news="https://www.volcengine.com/product/doubao", count=24))

providers.append(P("MiniMax","MiniMax（稀宇科技）","china","china","unrestricted","https://platform.minimaxi.com/document/pricing",True,[
 M("MiniMax-M3.1-Flash","MiniMax M3.1 Flash","general",1048576,1.0,4.0,ccy="CNY",cache=0.1,s1=S_MM,s2=S_OR,agree="双源（官方文档声明 ¥1/¥4/缓存¥0.1；OpenRouter 目录 0.3/1.2 USD）",
   note="官方原文：输入每百万 1 元、输出每百万 4 元、缓存读取每百万 0.1 元；采用更激进稀疏注意力，日常输出 200+ TPS（P50 170+），Agentic 任务综合成本较前代降 70%"),
 M("minimax-m3","MiniMax M3","general",1048576,0.3,1.2,ccy="USD",s1=S_OR,s2=S_MM,agree="仅聚合源"),
 M("MiniMax-H3","MiniMax H3（全模态生成）","multimodal",0,None,None,ccy="CNY",s1=S_MM,agree="按生成量计费，不适用 tokens 单价",
   note="官方：通用全模态生成模型，统一理解文本/图像/视频/声音，输出原生双声道音视频，最高 15s 2K 分辨率；2K 用基模 in-context 重生成替代专用超分"),
 M("minimax-m2.7","MiniMax M2.7","general",204800,0.3,1.2,ccy="USD",s1=S_OR,agree="仅聚合源"),
],"可核验（官方直连）","platform.minimaxi.com / minimaxi.com 文档本机可直连（200，109 KB 正文含定价段落）",
 news="https://www.minimaxi.com/news", count=8))

providers.append(P("StepFun","StepFun（阶跃星辰）","china","china","unrestricted","https://platform.stepfun.com/docs/zh/guides/pricing/details.md",True,[
 M("step-5-preview","Step 5 Preview","reasoning",1048576,7.0,20.0,ccy="CNY",cache=0.70,s1=S_STEP,s2=S_STEP_A,agree="双源一致（定价表 + 调价公告）",
   note="2026-10-14 00:30（北京时间）起缓存命中输入由 ¥0.35 → ¥0.70；此前已按量调用过的用户沿用 ¥0.35；Step Plan 接入地址不在调整范围"),
 M("step-3.7-flash","Step 3.7 Flash","general",262144,1.35,8.1,ccy="CNY",cache=0.27,s1=S_STEP,s2=S_SF,agree="双源（硅基流动为 Step-3.5-Flash 档 ¥0.7/¥2.1）"),
 M("step-3.5-flash","Step 3.5 Flash","general",262144,0.7,2.1,ccy="CNY",cache=0.14,s1=S_STEP,s2=S_SF,agree="双源一致"),
 M("step-1o-turbo-vision","Step 1o Turbo Vision","multimodal",32768,2.5,8.0,ccy="CNY",cache=0.5,s1=S_STEP,agree="仅官方源"),
 M("stepaudio-2.5-chat","StepAudio 2.5 Chat（语音）","audio",32768,10.0,25.0,ccy="CNY",cache=2.0,s1=S_STEP,agree="仅官方源",
   note="stepaudio-3-realtime-preview / chat-preview 限时免费；TTS 按字符（stepaudio-3-tts ¥2.5/万字符）"),
],"可核验（官方直连）","platform.stepfun.com 文档为 Mintlify 托管，本机可直连并取回 Markdown 原文（含完整价格表）",
 news="https://www.stepfun.com/blog", count=3,
 note="增值能力：互联网搜索 ¥0.04/次、文搜图 ¥0.12/次、文件存储 ¥0.5/GB/天；platform.stepfun.com/docs/pricing/overview 旧路径已 404，改用 /docs/zh/guides/pricing/details.md"))

providers.append(P("ZeroOne","ZeroOne（零一万物）","china","china","unrestricted","https://platform.lingyiwanwu.com/docs",True,[
 M("yi-lightning","Yi-Lightning","general",16000,None,None,s1=None,s2=S_JQ,agree="无可核验源",
   note="platform.lingyiwanwu.com/pricing 与 /docs/pricing 均 404，www.yi.com 解析失败（getaddrinfo failed），官网改版后未公开定价"),
 M("yi-vision","Yi-Vision（多模态）","multimodal",16000,None,None,s1=None,s2=S_JQ,agree="无可核验源"),
],"不可核验","官网定价页 404 + 旧域名解析失败；模型与价格仅能经机器之心等第三方资讯站确认存在性",
 news="https://www.jiqizhixin.com/", count=2,
 note="建议站点标注「官网定价暂未公开，价格栏留空」而非沿用旧缓存价"))

providers.append(P("腾讯混元","Tencent Hunyuan（腾讯云）","china","china","unrestricted","https://cloud.tencent.com/document/product/1758/101818",True,[
 M("hunyuan-a13b","Hunyuan A13B Instruct","general",32768,1.0,4.0,ccy="CNY",s1=S_HY,s2=S_SF,agree="双源一致",
   off={"peak":"09:00-18:00 北京时间","valley":"00:00-09:00 与 18:00-24:00 北京时间","off_peak_discount":"谷时段 −20%（谷档 ¥0.8/¥3.2）","source":S_HY["url"],
        "peak_prices":{"input":1.0,"output":4.0},"valley_prices":{"input":0.8,"output":3.2}}),
 M("hy4-preview","Hunyuan Hy4 preview","general",131072,6.0,18.0,ccy="CNY",cache=0.3,s1=S_SF,s2=S_HY,agree="镜像价 + 官方计费文档可核验"),
 M("hunyuan-mt-7b","Hunyuan MT 7B（翻译）","general",32768,0.0,0.0,ccy="CNY",s1=S_SF,agree="免费额度"),
],"部分核验","cloud.tencent.com/document/product/1758/101818 本机可直连取回（9.3 KB），含混元计费说明；具体到每张卡的现价以控制台为准",
 news="https://cloud.tencent.com/document/product/1729/97731", count=20))

# ============================ 聚合网关 / 模型广场 ============================
providers.append(P("SiliconFlow","SiliconFlow（硅基流动）","china","china_aggregate","unrestricted","https://siliconflow.cn/pricing",True,[
 M("deepseek-ai/DeepSeek-V4.1-Flash","DeepSeek V4.1 Flash（谷档价）","general",1048576,2.0,8.0,ccy="CNY",cache=0.04,s1=S_SF,s2=S_DS,agree="双源（与官方峰谷规则对应）",
   off={"peak":"02:00-08:00 北京时间","valley":"00:00-02:00 与 08:00-24:00 北京时间","off_peak_discount":"谷档 ¥2/¥8/¥0.04；峰档 ¥1/¥4/¥0.02（峰档单价更低，用于错峰）","source":S_SF["url"],
        "peak_prices":{"input":1.0,"output":4.0,"cache":0.02},"valley_prices":{"input":2.0,"output":8.0,"cache":0.04},
        "note":"硅基流动把「费用发生时段」标在每格价格上，与 DeepSeek 官方峰谷定义方向相反，采购前务必核对"}),
 M("deepseek-ai/DeepSeek-V4-Flash","DeepSeek V4 Flash（旧版，谷档）","general",1048576,1.5,4.5,ccy="CNY",cache=0.15,s1=S_SF,s2=S_DS,agree="双源",
   off={"peak":"02:00-08:00","valley":"00:00-02:00 与 08:00-24:00","off_peak_discount":"谷档 −33%","source":S_SF["url"],
        "peak_prices":{"input":2.25,"output":6.75,"cache":0.225},"valley_prices":{"input":1.5,"output":4.5,"cache":0.15}}),
 M("deepseek-ai/DeepSeek-V4-Pro","DeepSeek V4 Pro","reasoning",1048576,12.0,24.0,ccy="CNY",cache=1.0,s1=S_SF,s2=S_DS,agree="双源"),
 M("deepseek-ai/DeepSeek-V3.2","DeepSeek V3.2","general",163840,4.0,6.0,ccy="CNY",cache=0.4,s1=S_SF,agree="仅聚合源"),
 M("zai-org/GLM-5.3-Flash","GLM-5.3 Flash（高速版）","general",1048576,0.8,2.8,ccy="CNY",cache=0.23,s1=S_SF,s2=S_GLM,agree="镜像价（官方页需 JS）",
   note="2026-10-15 上线，硅基流动动态页公告「GLM-5 系列首款原生多模态模型」"),
 M("zai-org/GLM-5.3","GLM-5.3","general",1048576,8.0,28.0,ccy="CNY",cache=2.0,s1=S_SF,s2=S_ZP,agree="镜像价 + 官网能力描述交叉核对"),
 M("moonshotai/Kimi-K2.7-Code","Kimi K2.7 Code（镜像）","code",262144,6.5,27.0,ccy="CNY",cache=1.3,s1=S_SF,s2=S_KIMI,agree="双源一致"),
 M("Qwen/Qwen3.8-27B","Qwen 3.8 27B（开源托管）","general",262144,3.0,12.0,ccy="CNY",s1=S_SF,s2=S_QWEN,agree="镜像价"),
 M("stepfun-ai/Step-3.5-Flash","Step 3.5 Flash（镜像）","general",262144,0.7,2.1,ccy="CNY",s1=S_SF,s2=S_STEP,agree="双源一致"),
 M("meituan-longcat/LongCat-2.0","LongCat 2.0（美团）","general",131072,5.0,20.0,ccy="CNY",cache=0.1,s1=S_SF,agree="仅聚合源"),
 M("ChinaTelecom/Xing4.0-29B","Xing 4.0 29B（中国电信星辰）","general",32768,0.0,0.0,ccy="CNY",s1=S_SF,agree="免费档"),
 M("tencent/Hy4-preview","Hunyuan Hy4 preview（镜像）","general",131072,6.0,18.0,ccy="CNY",cache=0.3,s1=S_SF,s2=S_HY,agree="双源一致",
   off={"peak":"09:00-18:00","valley":"00:00-09:00 与 18:00-24:00","off_peak_discount":"谷档 −20%","source":S_SF["url"]}),
 M("BAAI/bge-m3","bge-m3（向量）","embedding",8192,0.0,0.0,ccy="CNY",s1=S_SF,agree="免费档"),
],"可核验（官方直连）","siliconflow.cn/pricing 本机可直连取回完整价格中心（实时同步各厂商价，含峰谷时段列）",
 news="https://siliconflow.cn/news", count=40,
 note="docs.siliconflow.cn/cn/userguide/pricing 已 404，正确入口为 siliconflow.cn/pricing"))

providers.append(P("OpenRouter","OpenRouter（海外聚合网关）","overseas","overseas_aggregate","restricted","https://openrouter.ai/api/v1/models",False,[
 M("openrouter/auto","Auto Router（自动选模）","general",None,None,None,ccy="USD",s1=S_OR,agree="按所选模型计费"),
 M("anthropic/claude-sonnet-5.5","Claude Sonnet 5.5（经 OpenRouter）","general",1000000,2.0,10.0,ccy="USD",s1=S_OR,s2=S_ANTH,agree="双源一致",
   note="含 OpenRouter 平台附加费；批量档（batch）为 1.0/5.0"),
 M("openai/gpt-6.1-sol-pro","GPT-6.1 Sol Pro（经 OpenRouter）","reasoning",1050000,2.0,10.0,ccy="USD",s1=S_OR,s2=S_OAI,agree="仅聚合源（官方 403）",
   note="OpenAI 官方页 403，此为国内可取的唯一来源"),
 M("google/gemini-4-argon","Gemini 4 Argon（经 OpenRouter）","general",1048576,2.0,10.0,ccy="USD",s1=S_OR,agree="仅聚合源",
   note="批量档 batch 1.0/5.0"),
 M("x-ai/grok-4.7","Grok 4.7（经 OpenRouter）","general",500000,2.0,6.0,ccy="USD",s1=S_OR,agree="仅聚合源"),
 M("moonshotai/kimi-k3","Kimi K3（经 OpenRouter）","reasoning",1048576,0.239,11.936,ccy="USD",s1=S_OR,s2=S_KIMI,agree="口径差异极大",
   note="官方 CNY ¥20/¥100 约合 $2.8/$14；OpenRouter 目录价低一个量级，疑为批量/促销档，采购前需核实"),
],"可核验（官方直连）","OpenRouter catalog API 本机可直连（200，470 个模型，JSON 含 pricing/context/supported_parameters）",
 news="https://openrouter.ai/announcements", count=470,
 note="平台侧能力：Batch API 半价（2026-09-22 公告）、In-Region Routing 美/欧分区（2026-09-09）、Private Endpoints（2026-10-14）、OpenRouter 并入 Stripe（2026-10-14）"))

providers.append(P("阿里云百炼","Aliyun Bailian Model Studio（模型广场/聚合）","china","china_aggregate","unrestricted","https://help.aliyun.com/zh/model-studio/models",True,[
 M("qwen3.8-max","Qwen3.8 Max（广场）","general",1000000,2.0,6.0,ccy="USD",s1=S_ALI,s2=S_OR,agree="上架确认 + 聚合价"),
 M("deepseek-v4.1-flash","DeepSeek V4.1 Flash（广场）","general",1000000,0.3,1.2,ccy="CNY",s1=S_ALI,s2=S_DS,agree="双源一致"),
 M("kimi/kimi-k3","Kimi K3（广场）","reasoning",1000000,20.0,100.0,ccy="CNY",s1=S_ALI,s2=S_KIMI,agree="双源一致"),
 M("ZHIPU/GLM-5.3","GLM-5.3（广场）","general",1000000,8.0,28.0,ccy="CNY",s1=S_ALI,s2=S_SF,agree="双源一致"),
 M("MiniMax-M3","MiniMax M3（广场）","general",1048576,0.3,1.2,ccy="USD",s1=S_ALI,s2=S_MM,agree="上架确认 + 聚合价"),
],"可核验（官方直连）","help.aliyun.com 与 alibabacloud.com/help/zh 本机均可直连（200），取到完整模型矩阵；广场单价以控制台计费页为准",
 news="https://help.aliyun.com/zh/model-studio/release-notes", count=42))

providers.append(P("火山方舟","Volcengine Ark（方舟模型广场/聚合）","china","china_aggregate","unrestricted","https://www.volcengine.com/docs/82379/109932",True,[
 M("doubao-seed-2-5","Doubao Seed 2.5（方舟）","general",1048576,0.8,2.0,ccy="CNY",s1=S_VOLC,s2=S_OR,agree="上架确认 + 聚合价"),
 M("deepseek-v4.1-flash","DeepSeek V4.1 Flash（方舟，1017 版）","general",1048576,0.3,1.2,ccy="CNY",s1=S_VOLC,s2=S_DS,agree="双源一致",
   note="方舟文档首页标注「DeepSeek-V4.1-Flash（升级 1017）」，说明方舟按上游版本同步"),
],"文档可达、价格需登录","方舟文档中心可直连（200），模型价格页 82379/1544106 需登录控制台渲染，未取到匿名单价",
 news="https://www.volcengine.com/docs/82379/109932", count=24))
# -*- coding: utf-8 -*-
# ================= 每个厂商最新新闻（抓取于 2026-10-20）=================
def N(prov, items, stype, src_url, note=""):
    return {"provider": prov, "source_type": stype, "source_url": src_url,
            "crawled_at": ASOF, "items": items, "note": note}

def IT(t, d="", u="", sname=""):
    return {"title": t, "date": d, "url": u, "source": sname}

provider_news = []

provider_news.append(N("OpenAI", [
    IT("传 OpenAI 于 11 月推送 GPT-6.1 后续 Sol/Luna 分层套餐（第三方报道，官方页 403 未核验", "", "", "量子位"),
    IT("GPT-6 系列在 OpenRouter 目录上架 Sol / Sol Pro / Luna / Astra 四档", ASOF, "https://openrouter.ai/api/v1/models", "OpenRouter 目录"),
], "国内资讯站 + 聚合网关（官方页 403 不可达）", "https://openai.com/news/",
   "openai.com 本机 HTTP 403，无法取官方新闻列表；条目来自国内可检索资讯站与 OpenRouter 目录，已标注来源"))

provider_news.append(N("Anthropic", [
    IT("Claude Cowork 并入 Claude 主产品，向 Pro 与 Max 推送", "", "https://www.anthropic.com/pricing", "Anthropic 定价页公告条"),
    IT("Claude discovers a novel enzyme system with CRISPR-like repeats", "", "https://www.anthropic.com/news", "Anthropic News"),
    IT("Preparing for the 2026 US midterms", "", "https://www.anthropic.com/news", "Anthropic News"),
    IT("Introducing the Anthropic Cyber Mission", "", "https://www.anthropic.com/news", "Anthropic News"),
    IT("Previewing the Model Hardware Standard", "", "https://www.anthropic.com/news", "Anthropic News"),
    IT("Our position on open-weights models", "", "https://www.anthropic.com/news", "Anthropic News"),
    IT("Claude 新模型曝光！能跳出思维定势，修 Bug 治标又治本", ASOF, "https://www.qbitai.com/2026-10-504314.html", "量子位"),
], "官方可达 + 国内资讯站交叉", "https://www.anthropic.com/news",
   "官方新闻条目未输出发布日期（前端渲染），日期栏留空；量子位条目为国内可检索交叉源"))

provider_news.append(N("Google Gemini", [
    IT("Gemini 3.8 Flash / Flash-Lite 在聚合目录上架，上下文统一 1M", ASOF, "https://openrouter.ai/api/v1/models", "OpenRouter 目录"),
    IT("blog.google/technology/ai 本机连接超时，官方新闻未取回", "", "https://blog.google/technology/ai/", "官方入口（不可达）"),
], "国内资讯站（官方站超时）", "https://blog.google/technology/ai/",
   "ai.google.dev 与 blog.google 本机连接超时（大陆不可直连），条目取自可核验聚合目录与国内资讯站"))

provider_news.append(N("Mistral", [
    IT("Mistral Large 4 目录价 $0.68/$2.09 每百万 tokens（经聚合网关确认）", ASOF, "https://openrouter.ai/api/v1/models", "OpenRouter 目录"),
    IT("mistral.ai/news 本机超时，官方公告未取回", "", "https://mistral.ai/news", "官方入口（不可达）"),
], "国内资讯站（官方站超时）", "https://mistral.ai/news", "docs.mistral.ai 与 mistral.ai 本机连接超时"))

provider_news.append(N("Cohere", [
    IT("docs.cohere.com/docs/pricing 已下线（404），价格说明并入 Models 页", ASOF, "https://docs.cohere.com/docs/models", "Cohere Docs"),
    IT("Command A+（command-a-plus-05-2026）状态 Live，192K 上下文", ASOF, "https://docs.cohere.com/docs/models", "Cohere Docs"),
], "官方可达（无独立新闻流）", "https://cohere.com/blog", "cohere.com/blog 取回 200 但条目为前端渲染，未解析出标题列表"))

provider_news.append(N("xAI", [
    IT("Grok 4.7 / 4.6 / 4.5 同价 $2/$6 每百万 tokens（500K 上下文）", ASOF, "https://openrouter.ai/api/v1/models", "OpenRouter 目录"),
    IT("Grok 4.20 multi-agent 支持 2M 上下文", ASOF, "https://openrouter.ai/api/v1/models", "OpenRouter 目录"),
], "国内可检索源（官方站超时）", "https://x.ai/news", "docs.x.ai 与 x.ai/news 本机超时；旧路径 docs.x.ai/docs/models 已 404"))

provider_news.append(N("Groq", [
    IT("GPT-OSS 120B 经 Groq 托管上架聚合目录（$0.15/$0.6）", ASOF, "https://openrouter.ai/api/v1/models", "OpenRouter 目录"),
], "国内可检索源", "https://groq.com/newsroom/", "console.groq.com/docs/pricing 本机未核验"))

provider_news.append(N("DeepSeek", [
    IT("DeepSeek V4.1 Flash-1017 登顶 Agent Arena 开源榜，总榜第 11", ASOF, "https://www.ithome.com/1/015/370.htm", "IT之家"),
    IT("Search / Fetch API 上线；2026-11-01 00:00（北京时间）起服务端工具调用按 $0.75/1000 次计费", ASOF, S_DS["url"], "DeepSeek 官方文档"),
    IT("DeepSeek Harness 进入开发者预览，面向 Agent harness 开发者", ASOF, S_DS_N["url"], "DeepSeek 官方 News"),
    IT("legacy 名称 deepseek-v4-flash / -vision-exp 仍接受但模型已退役，请求由 V4.1-Flash-1017 承接并按 Flash 价计费", ASOF, S_DS["url"], "DeepSeek 官方文档"),
    IT("我向新版 DeepSeek 许了个愿，4 块钱让特斯拉飞起来", "2026-10-19", "https://www.ifanr.com/1684880", "爱范儿"),
], "官方可达 + 国内资讯站交叉", S_DS_N["url"]))

provider_news.append(N("Kimi", [
    IT("Kimi K3 旗舰模型正式发布（开放平台首页横幅）", ASOF, S_MOON["url"], "Kimi 开放平台"),
    IT("K3 系列引入上下文缓存 TTL 分档计费：5min ¥20 / 1h ¥40 每百万 tokens", ASOF, S_KIMI["url"], "Kimi 定价文档"),
    IT("批量推理 Batch API 费用为标准价 60%，不受实时并发限制", ASOF, "https://platform.kimi.com/docs/pricing/batch.md", "Kimi 批量推理定价"),
], "官方可达", S_MOON_N["url"], "news 页取回 7 KB 但条目为前端渲染，价格类更新已从官方 Markdown 文档直接核验"))

provider_news.append(N("GLM", [
    IT("GLM-5.3：前沿编程能力与涌现的网络安全能力，面向复杂软件工程与长程 Agent 任务，支持 1M 上下文", ASOF, S_ZP["url"], "智谱官网"),
    IT("GLM-5.3 为编程能力最强的开源模型，多项公开基准取得开源第一；完整权重两周内开放", "", S_ZP["url"]+"/news", "智谱新闻"),
    IT("智谱发布首份业绩报告，并公布 2025 年度业绩发布会安排", "", S_ZP["url"]+"/news", "智谱新闻"),
    IT("硅基流动上线高速版 GLM-5.3-Flash（GLM-5 系列首款原生多模态模型）", "2026-10-15", S_SF_N["url"], "硅基流动动态"),
], "官方可达（定价页需 JS）+ 国内镜像源", S_ZP["url"]+"/news"))

provider_news.append(N("通义千问", [
    IT("百炼模型大全更新：qwen3.8-max / qwen3.7-plus / qwen3.8-flash / qwen3.8-omni-flash-realtime 分模态矩阵", ASOF, S_ALI["url"], "阿里云百炼文档"),
    IT("百炼上架第三方模型：deepseek-v4-pro-0813、deepseek-v4.1-flash、kimi/kimi-k3、glm-5.2、ZHIPU/GLM-5.3、MiniMax-M3、mimo-v2.5-pro", ASOF, S_ALI["url"], "阿里云百炼文档"),
    IT("新增世界模型（happyoyster-1.0 adventure/directing/acting，邀测）与决策模型 decision-model-preview", ASOF, S_ALI["url"], "阿里云百炼文档"),
    IT("Qwen3Guard：面向 token 流的实时安全护栏模型发布", "", S_QWEN["url"], "Qwen Blog"),
], "官方可达", S_ALI_N["url"]))

provider_news.append(N("豆包", [
    IT("方舟文档新增 Seed-Evolving 模型页；DeepSeek-V4.1-Flash（升级 1017）在方舟上架", ASOF, S_VOLC["url"], "火山方舟"),
    IT("Doubao Seedance 2.5 视频生成、Seedream 5.0 pro/flash 图像生成教程与提示词指南上线", ASOF, S_VOLC["url"], "火山方舟"),
    IT("豆包助手（tool-use）与联网搜索工具进入文档体系", ASOF, S_VOLC["url"], "火山方舟"),
], "官方可达（价格页需登录）", "https://www.volcengine.com/product/doubao"))

provider_news.append(N("MiniMax", [
    IT("MiniMax M3.1 Flash：输入 ¥1 / 输出 ¥4 / 缓存读取 ¥0.1 每百万 tokens，Agentic 任务综合成本较前代降 70%", ASOF, S_MM["url"], "MiniMax 定价文档"),
    IT("M3.1 Flash 采用更激进稀疏注意力架构，日常输出 200+ TPS（P50 稳定 170+ TPS）", ASOF, S_MM["url"], "MiniMax 定价文档"),
    IT("MiniMax H3 通用全模态生成模型：统一理解文本/图像/视频/声音，原生双声道音视频，最高 15s 2K", ASOF, S_MM["url"], "MiniMax 定价文档"),
], "官方可达", "https://www.minimaxi.com/news"))

provider_news.append(N("StepFun", [
    IT("Step 5 Preview 缓存命中输入价自 2026-10-14 00:30（北京时间）起由 ¥0.35 调至 ¥0.70", "2026-10-14", S_STEP_A["url"], "阶跃星辰公告"),
    IT("Step 5 Preview / Step 3.7 Flash / Step 3.5 Flash 三档文本模型定价公开", ASOF, S_STEP["url"], "阶跃星辰 API 定价"),
    IT("StepAudio 3 realtime / chat / gen / music preview 限时免费", ASOF, S_STEP["url"], "阶跃星辰 API 定价"),
], "官方可达", "https://www.stepfun.com/blog", "旧路径 /docs/pricing/overview 已 404，正确入口为 /docs/zh/guides/pricing/details.md"))

provider_news.append(N("ZeroOne", [
    IT("官网定价页 404、yi.com 域名解析失败，暂无可核验官方动态", ASOF, S_JQ["url"], "机器之心（资讯入口）"),
    IT("零一万物商业化相关报道散见于国内资讯站，官方未形成稳定新闻流", "", S_QB["url"], "量子位"),
], "国内资讯站（官方不可达）", S_JQ["url"]))

provider_news.append(N("腾讯混元", [
    IT("混元大模型计费文档可直连，含按量计费与峰谷时段说明", ASOF, S_HY["url"], "腾讯云文档"),
    IT("Hy4 preview 上线聚合平台：输入 ¥6 / 输出 ¥18 / 缓存 ¥0.3 每百万 tokens", ASOF, S_SF["url"], "硅基流动价格中心"),
    IT("Hunyuan-MT-7B（翻译）在聚合平台以免费档提供", ASOF, S_SF["url"], "硅基流动价格中心"),
], "官方可达", "https://cloud.tencent.com/document/product/1729/97731"))

# ============================ 峰谷时段汇总（独立区块数据）============================
peak_valley = [
 {"provider":"DeepSeek","scope":"官方 API（deepseek-flash / deepseek-v4-pro 全模型）","tz":"UTC（官方原文口径）",
  "peak_windows":"周一~周五 01:00-04:00 与 06:00-10:00 UTC（不含中国法定节假日）",
  "valley_windows":"其余全部时段，含周末与中国法定节假日全天",
  "discount":"谷时（off-peak）价格为峰时的一半","multiplier":{"peak":2.0,"valley":0.5},
  "evidence":"Peak hours are 01:00 - 04:00 and 06:00 - 10:00 UTC, Monday through Friday, excluding Chinese public holidays. All other hours are off-peak. Off-peak rates are half of the peak rates.",
  "source":S_DS,"note":"DeepSeek 是唯一公开「×2 峰时加价」机制的厂商；其余均为「谷时降价」表述"},
 {"provider":"SiliconFlow","scope":"DeepSeek V4.1 Flash / V4-Flash 镜像档位","tz":"北京时间（费用发生时段口径）",
  "peak_windows":"02:00-08:00","valley_windows":"00:00-02:00 与 08:00-24:00",
  "discount":"V4.1 Flash：谷档 ¥2/¥8/缓存¥0.04，峰档 ¥1/¥4/缓存¥0.02（峰档单价更低，属错峰容量定价）",
  "multiplier":{"peak":0.5,"valley":2.0},"evidence":"费用发生时段: 2点～8点 ¥1.00/¥4.00/¥0.02 与 0点～2点/8点～24点 ¥2.00/¥8.00/¥0.04 并列展示",
  "source":S_SF,"note":"与 DeepSeek 官方峰谷方向相反，属聚合商自有容量档位；采购前须核对价格卡"},
 {"provider":"SiliconFlow","scope":"Hunyuan A13B Instruct 镜像档位","tz":"北京时间",
  "peak_windows":"09:00-18:00（¥1/¥4）","valley_windows":"00:00-09:00 与 18:00-24:00（¥0.8/¥3.2）",
  "discount":"谷时 −20%","multiplier":{"peak":1.25,"valley":1.0},"evidence":"费用发生时段: 9点～18点 ¥1.00/¥4.00；0点～9点/18点～24点 ¥0.80/¥3.20",
  "source":S_SF},
 {"provider":"Kimi","scope":"批量推理 Batch API（kimi-k2.7-code / kimi-k2.6）","tz":"无时段限制",
  "peak_windows":"不适用","valley_windows":"随时可用（异步，需 completion_window 内完成）",
  "discount":"标准价 60%（kimi-k2.7-code 输入¥3.90/输出¥16.20；kimi-k2.6 输入¥3.90/输出¥16.20）",
  "multiplier":{"peak":None,"valley":0.6},"evidence":"Batch API 费用为标准模型价格的 60%，不受实时并发限制",
  "source":S_KIMI,"note":"Kimi 实时 API 本身无峰谷计价，用 Batch 替代谷时段策略"},
 {"provider":"OpenRouter","scope":"Batch API（全目录模型）","tz":"无时段限制",
  "peak_windows":"不适用","valley_windows":"随时可用（异步打包）",
  "discount":"半价（50%）","multiplier":{"peak":None,"valley":0.5},
  "evidence":"Announcements 2026-09-22：Batch API — half-price inference by bundling requests",
  "source":S_OR_B},
 {"provider":"Anthropic / Google Gemini / xAI","scope":"官网未公开峰谷计价","tz":"不适用",
  "peak_windows":"未公开","valley_windows":"未公开",
  "discount":"无公开时段折扣（Google Gemini 有 batch 端点，折扣口径随版本变化）",
  "multiplier":{"peak":None,"valley":None},
  "evidence":"anthropic.com/pricing 仅订阅价；ai.google.dev 与 x.ai 本机不可达，未见峰谷条款",
  "source":S_ANTH,"note":"字段留空而非编造折扣率；后续由具备境外网络的运维在官方文档补齐"},
]

# ============================ 取数健康表（透明度：哪些源真的拿到了）============================
source_health = [
 {"url":S_DS["url"],"ok":True,"bytes":3611,"kind":"vendor_official","as_of":ASOF},
 {"url":"https://platform.kimi.com/docs/pricing/chat.md","ok":True,"bytes":2963,"kind":"vendor_official","as_of":ASOF},
 {"url":"https://platform.kimi.com/docs/pricing/batch.md","ok":True,"bytes":1723,"kind":"vendor_official","as_of":ASOF},
 {"url":S_STEP["url"],"ok":True,"bytes":2219,"kind":"vendor_official","as_of":ASOF},
 {"url":S_STEP_A["url"],"ok":True,"bytes":760,"kind":"vendor_official","as_of":ASOF},
 {"url":S_SF["url"],"ok":True,"bytes":6552,"kind":"vendor_official_aggregate","as_of":ASOF},
 {"url":S_SF_N["url"],"ok":True,"bytes":2096,"kind":"vendor_official_aggregate","as_of":ASOF},
 {"url":S_ALI["url"],"ok":True,"bytes":2269,"kind":"vendor_official","as_of":ASOF},
 {"url":S_HY["url"],"ok":True,"bytes":9367,"kind":"vendor_official","as_of":ASOF},
 {"url":S_VOLC["url"],"ok":True,"bytes":189470,"kind":"vendor_official","as_of":ASOF},
 {"url":S_OR["url"],"ok":True,"bytes":2000000,"kind":"aggregator_catalog_api","as_of":ASOF,"note":"470 模型 JSON"},
 {"url":S_OR_B["url"],"ok":True,"bytes":6634,"kind":"aggregator_announcements","as_of":ASOF},
 {"url":S_MM["url"],"ok":True,"bytes":109746,"kind":"vendor_official","as_of":ASOF},
 {"url":S_ANTH["url"],"ok":True,"bytes":2636,"kind":"vendor_official","as_of":ASOF,"note":"仅订阅价"},
 {"url":S_ANTH_N["url"],"ok":True,"bytes":252345,"kind":"vendor_news","as_of":ASOF},
 {"url":S_ZP["url"],"ok":True,"bytes":60722,"kind":"vendor_news","as_of":ASOF},
 {"url":S_COH["url"],"ok":True,"bytes":22915,"kind":"vendor_official","as_of":ASOF},
 {"url":S_GLM["url"],"ok":True,"bytes":127,"kind":"vendor_official_js_shell","as_of":ASOF,"note":"200 但为 JS 空壳，需登录渲染"},
 {"url":"https://www.volcengine.com/docs/82379/1544106","ok":True,"bytes":60,"kind":"vendor_official_login_required","as_of":ASOF},
 {"url":"https://openai.com/news/","ok":False,"error":"HTTP 403 Forbidden","kind":"vendor_official","as_of":ASOF,"retry_count":3},
 {"url":"https://platform.openai.com/docs/pricing","ok":False,"error":"HTTP 403 Forbidden","kind":"vendor_official","as_of":ASOF,"retry_count":2},
 {"url":"https://docs.x.ai/developers/models","ok":False,"error":"connect timeout (15s)","kind":"vendor_official","as_of":ASOF,"retry_count":3},
 {"url":"https://docs.x.ai/docs/models","ok":False,"error":"HTTP 404","kind":"vendor_official","as_of":ASOF},
 {"url":"https://docs.mistral.ai/getting-started/models/models_overview/","ok":False,"error":"connect timeout (15s)","kind":"vendor_official","as_of":ASOF,"retry_count":3},
 {"url":"https://ai.google.dev/gemini-api/docs/pricing","ok":False,"error":"connect timeout (15s)","kind":"vendor_official","as_of":ASOF,"retry_count":3},
 {"url":"https://docs.cohere.com/docs/pricing","ok":False,"error":"HTTP 404","kind":"vendor_official","as_of":ASOF},
 {"url":"https://platform.lingyiwanwu.com/pricing","ok":False,"error":"HTTP 404","kind":"vendor_official","as_of":ASOF},
 {"url":"https://platform.lingyiwanwu.com/docs/pricing","ok":False,"error":"HTTP 404","kind":"vendor_official","as_of":ASOF},
 {"url":"https://www.yi.com/price","ok":False,"error":"getaddrinfo failed","kind":"vendor_official","as_of":ASOF},
 {"url":"https://platform.stepfun.com/docs/pricing/overview","ok":False,"error":"HTTP 404","kind":"vendor_official","as_of":ASOF},
 {"url":"https://docs.siliconflow.cn/cn/userguide/pricing","ok":False,"error":"HTTP 404","kind":"vendor_official","as_of":ASOF},
 {"url":"https://www.jiqizhixin.com/rss","ok":True,"bytes":3375,"kind":"news_rss","as_of":ASOF,"note":"仅广告条目，正文需 JS 渲染"},
 {"url":S_QB["url"],"ok":True,"bytes":6345,"kind":"news_rss","as_of":ASOF,"items":10},
 {"url":S_IF["url"],"ok":True,"items":10,"kind":"news_rss","as_of":ASOF},
 {"url":S_IT["url"],"ok":True,"items":10,"kind":"news_rss","as_of":ASOF},
 {"url":S_LF["url"],"ok":True,"items":9,"kind":"news_rss","as_of":ASOF},
 {"url":"https://www.infoq.cn/static/rss/out/691.xml","ok":False,"error":"empty feed body","kind":"news_rss","as_of":ASOF},
 {"url":"https://www.cnbeta.com.tw/backend.php","ok":False,"error":"empty feed body","kind":"news_rss","as_of":ASOF},
 {"url":"https://api-docs.deepseek.com/news","ok":True,"bytes":3847,"kind":"vendor_news","as_of":ASOF},
 {"url":"https://www.sinsytech.com/rss.xml","ok":False,"error":"getaddrinfo failed","kind":"news_rss","as_of":ASOF},
 {"url":"https://www.newhua.com/feed","ok":False,"error":"empty feed body","kind":"news_rss","as_of":ASOF},
]

# ============================ 组装 + 校验 + 落盘 ============================
REGIONS = {"china":"中国大陆","overseas":"海外"}
GROUPS  = {"china":"国内厂商","china_aggregate":"国内聚合/模型广场",
           "overseas":"海外厂商","overseas_aggregate":"海外聚合网关"}
ACCESS  = {"unrestricted":"国内可直连","restricted":"国内不可直连（需代理）","blocked":"国内基本不可达"}

schema_version = "2.0"
taxonomy = {
 "regions": {k:{"value":v} for k,v in REGIONS.items()},
 "groups":  {k:{"value":v} for k,v in GROUPS.items()},
 "categories": {"general":"通用对话","reasoning":"推理","code":"代码",
                "multimodal":"多模态","audio":"语音","video":"视频生成",
                "image":"图像生成","embedding":"向量","unknown":"未分类"},
 "china_access": ACCESS,
}

data = {
 "schema_version": schema_version,
 "generated_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
 "data_as_of": ASOF,
 "fx_rate_note": "CNY 价格另附约 USD 换算值，汇率约 1 USD = %.2f CNY，仅用于横向对比，不构成官方报价" % FX,
 "methodology": "价格与参数来自下表各厂商官方文档（国内直连可达者）与 OpenRouter catalog API；"
                "国内访问不到的官方站（openai.com / docs.x.ai / docs.mistral.ai / ai.google.dev）一律改用"
                "国内可检索的聚合目录与模型资讯站取数，并在 sources[].note 与 cross_check 字段标注口径差异。"
                "凡未能核验官方单价的条目，cross_check 标注为「仅聚合源」或「无可核验源」，价格字段留空而非估算填补。",
 "taxonomy": taxonomy,
 "providers": providers,
 "provider_news": provider_news,
 "peak_valley": peak_valley,
 "source_health": source_health,
 "unresolved": [
  "openai.com 全域（pricing/news）本机 HTTP 403：OpenAI 官方单价与新闻待境外网络核验，现全部来自 OpenRouter 目录价",
  "docs.x.ai / x.ai/news / docs.mistral.ai / mistral.ai/news / ai.google.dev / blog.google：本机连接超时（大陆网络不可达）",
  "docs.cohere.com/docs/pricing 已 404；cohere.com/blog 前端渲染未解析出条目",
  "open.bigmodel.cn/pricing：JS 空壳 + 需登录，GLM 单价取自硅基流动镜像页与阿里云百炼上架信息",
  "www.volcengine.com/docs/82379/1544106 与 /pricing?product=Ark：需登录控制台，豆包官方 tokens 单价未取到",
  "platform.lingyiwanwu.com 定价路径 404 且 yi.com 域名解析失败：ZeroOne 价格完全不可核验",
  "机器之心正文与 RSS 需 JS 渲染/仅广告条目：新闻区块改用量子位/IT之家/爱范儿/雷峰网四路 RSS",
  "anthropic.com/pricing 仅含订阅计划价：Claude API 每百万 tokens 单价需在 platform 控制台确认",
 ],
 "deprecated_paths": [
  {"from":"https://docs.x.ai/docs/models","to":"https://docs.x.ai/developers/models","error":"404"},
  {"from":"https://platform.stepfun.com/docs/pricing/overview","to":"https://platform.stepfun.com/docs/zh/guides/pricing/details.md","error":"404"},
  {"from":"https://docs.siliconflow.cn/cn/userguide/pricing","to":"https://siliconflow.cn/pricing","error":"404"},
  {"from":"https://docs.cohere.com/docs/pricing","to":"https://docs.cohere.com/docs/models","error":"404"},
 ],
 "legacy_note": "v1 旧字段 provider/description/context_length 已保留在 provider.name 与 model.note 中，前端同时读新字段 v2 与旧字段以兼容缓存。"
}

# ---- validation ----
errs, warns, mids = [], [], []
groups_seen, provs_seen = set(), set()
for p in providers:
    if p["name"] in provs_seen: errs.append("dup provider %s" % p["name"])
    provs_seen.add(p["name"])
    for g in ("region","group","china_access"):
        if p[g] not in (REGIONS if g=="region" else (GROUPS if g=="group" else ACCESS)):
            errs.append("%s.%s=%s" % (p["name"], g, p[g]))
    for m in p["models"]:
        uid = "%s :: %s" % (p["name"], m["model_id"]); m["uid"] = uid
        if uid in mids: errs.append("dup uid %s" % uid)
        mids.append(uid)
        if m["category"] not in taxonomy["categories"]: errs.append("%s cat=%s" % (m["model_id"], m["category"]))
        if m["input_price_per_million"] is None and m["output_price_per_million"] is None \
           and "note" not in m and m["cross_check"] not in ("不适用","按秒/条计费，不适用 tokens 单价","按张计费，不适用 tokens 单价","按所选模型计费","按生成量计费，不适用 tokens 单价","无可核验源"):
            warns.append("%s 无价格且无豁免说明" % m["model_id"])
        if m["input_price_per_million"] is not None and m["currency"]=="CNY":
            exp = usd(m["input_price_per_million"])
            if abs(m["input_price_usd_per_million"]-exp)>1e-9: errs.append("%s fx in %s vs %s" % (m["model_id"],m["input_price_usd_per_million"],exp))
        if m["output_price_per_million"] is not None and m["currency"]=="CNY":
            exp = usd(m["output_price_per_million"])
            if abs(m["output_price_usd_per_million"]-exp)>1e-9: errs.append("%s fx out" % m["model_id"])
        if not m["sources"] and "无可核验源" not in m["cross_check"]: warns.append("%s 无来源" % m["model_id"])
        if not m["sources"] and m["cross_check"] != "无可核验源": errs.append("%s 空来源但非「无可核验源」" % m["model_id"])
        groups_seen.add((p["group"], p["region"]))
    if not p["models"]: warns.append("%s 无模型" % p["name"])

for pn in provider_news:
    if pn["provider"] not in provs_seen and pn["provider"] != "行业综合（国内资讯站）":
        warns.append("news provider 未建模 %s" % pn["provider"])

tot_models = sum(len(p["models"]) for p in providers)
tot_priced = sum(1 for p in providers for m in p["models"]
                 if m["input_price_per_million"] is not None or m["output_price_per_million"] is not None)
tot_dual   = sum(1 for p in providers for m in p["models"] if len(m["sources"])>=2)
tot_peak   = sum(1 for p in providers for m in p["models"] if m.get("peak_valley"))

print("providers=%d models=%d priced=%d dual_source=%d peak_valley_models=%d"
      % (len(providers), tot_models, tot_priced, tot_dual, tot_peak))
print("groups=%s" % sorted(groups_seen))
print("ERRS(%d):" % len(errs));  [print("  E", e) for e in errs]
print("WARNS(%d):" % len(warns)); [print("  W", w) for w in warns]

out = r"C:\Users\User\AppData\Local\SMS\workspaces\_virtual\conv-20261020-145718-173351\tmp\llm_pricing_data.v2.json"
io.open(out, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=1))
print("WROTE", out, len(io.open(out,encoding='utf-8').read()), "bytes")
if errs: sys.exit(1)