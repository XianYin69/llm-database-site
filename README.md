# LLM Database Explorer

一个纯静态的 **大模型厂商 / 服务提供商数据库**：把各家 LLM 的价格、上下文、峰谷时段、
最新动态整理成一张可筛选、可排序、可交叉核验的数据表，并附「取数健康表」如实记录
哪些官方源本机可达、哪些需要走聚合目录与模型资讯站取数。

> 站点托管于 GitHub Pages：`xianyin69.github.io/llm-database-site`
> 由 GitHub Actions 自动部署（`.github/workflows/deploy.yml`，push 到 `master` 触发）。

## 数据内容（`llm_pricing_data.json` · schema v2.2 · 32 厂商 / 130 模型）

- **提供商分组信息架构**：海外 / 国内两大区域 × 厂商 / 聚合网关（含国内可直连的海外模型
  镜像分组），每个 provider 带 `region` / `group` / `china_access` 字段，前端按分组标签页 +
  区域、可达性、分类、取数核验方式多维筛选。
- **v2.2 新增 12 家厂商**：
  国内 —— 商汤日日新、百川智能、面壁 MiniCPM、魔搭 ModelScope、百度千帆、美团 LongCat、字节 Seed；
  海外 —— NVIDIA NIM / Nemotron、Amazon Nova、IBM Granite、Meta Llama / Muse、Perplexity Sonar。
- **国内可直连取数**：DeepSeek、Kimi、GLM、通义（百炼）、豆包（方舟）、MiniMax、StepFun、
  腾讯混元、SiliconFlow、商汤、百川、面壁、魔搭、百度千帆、美团、火山方舟等官方文档/价格页本机可达；
  **国内访问不到的官方站**（OpenAI / Google / Mistral / Cohere / xAI / Perplexity / HuggingFace /
  Azure）一律改由 OpenRouter 目录 API + 国内可检索模型资讯站交叉取数，并在 `sources[].kind` 与
  `cross_check` 字段双源标注口径，无法核验的字段留空而不是估算填补。
- **每个大模型厂商最新新闻**：`provider_news[]` 36 组 / 128 条，**全部为 2026-10-20 实时 RSS 抓取**
  （量子位 / IT之家 / 爱范儿 / 雷峰网 + 各厂商官方 News）；机器之心与 36氪的 RSS 地址实测返回
  HTML 而非 XML，已剔除并在 `unresolved` 中登记。每条带标题、日期、链接、来源与摘要。
- **波峰波谷时段信息**：`peak_valley[]` 9 组 + 每个模型可选的 `peak_valley` 对象——
  ① DeepSeek 官方峰谷价（工作日 UTC 01-04 / 06-10 为峰，谷时半价）；
  ② 腾讯混元 24 小时全局时段折扣（UTC 00-16 峰、16-24 谷，谷时 62.5%）；
  ③ SiliconFlow 镜像档位定价；④ Kimi / MiniMax / OpenRouter / OpenAI 的 `:batch` 异步折扣；
  ⑤ Anthropic / Google / xAI 明确标注「未公开时段定价，不做推算」。
  OpenRouter catalog 实测 470 个模型中有 78 条 `pricing.overrides`（时段或长上下文加价），
  已按时段折扣与长文加价两类分别标注。
- **取数健康表**：`source_health[]` 70 条记录每个来源的可达性实测（HTTP 状态、取回字节数、备注），
  `unresolved` 14 条 / `deprecated_paths` 记录待补与已失效路径。

## 目录结构

```
index.html                    # 单页：筛选区 + 模型卡片 + 峰谷时段 + 厂商新闻 + 取数健康
app.js                        # 前端逻辑（只读 llm_pricing_data.json）
styles.css                    # 样式
llm_pricing_data.json         # 数据（schema v2.2，含全部来源标注）
scripts/build_pricing_data.py # 数据生成脚本（v2.0 基线，可重跑）
scripts/build_v22.py          # v2.2 扩充脚本（新增 12 厂商 / 峰谷 / 健康表）
scripts/fix_news.py           # RSS 截断修复（完整读取 + 容错解析）
scripts/fix_news2.py          # 失效 RSS 源替换（机器之心/36氪 → 量子位等四路）
.github/workflows/deploy.yml  # GitHub Pages 自动部署
```

## 数据重跑

```bash
python -B scripts/build_pricing_data.py   # 生成 v2.0 基线
python -B scripts/build_v22.py            # 扩充为 v2.2
python -B scripts/fix_news.py             # 修复被截断的 RSS 组
python -B scripts/fix_news2.py            # 替换失效 RSS 源
```

## 本地开发

纯静态站，直接把仓库根目录指向任意静态服务器即可：

```
npx serve .        # 或 python -m http.server
```
