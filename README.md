# LLM Database Explorer

一个纯静态的 **大模型厂商 / 服务提供商数据库**：把各家 LLM 的价格、上下文、峰谷时段、
最新动态整理成一张可筛选、可排序、可交叉核验的数据表，并附「取数健康表」如实记录
哪些官方源本机可达、哪些需要走聚合目录与模型资讯站取数。

> 站点托管于 GitHub Pages：`xiandb69.github.io/llm-database-site`
> 由 GitHub Actions 自动部署（`.github/workflows/deploy.yml`，push 到 `master` 触发）。

## 数据内容（`llm_pricing_data.json` · schema v2.0）

- **提供商分组信息架构**：海外 / 国内两大区域 × 厂商 / 聚合网关（含国内可直连的海外模型
  镜像分组），每个 provider 带 `region` / `group` / `china_access` 字段，前端按分组标签页 +
  区域、可达性、分类、取数核验方式多维筛选。
- **国内可直连取数**：DeepSeek、Kimi、GLM、通义（百炼）、豆包（方舟）、MiniMax、StepFun、
  腾讯混元、SiliconFlow 等官方文档/价格页本机可达；
  **国内访问不到的官方站**（OpenAI / Google / Mistral / Cohere / xAI）一律改由
  OpenRouter 目录 API + 国内模型资讯站交叉取数，并在 `sources[].kind` 与 `cross_check` 字段
  双源标注口径，无法核验的字段留空而不是估算填补。
- **每个厂商最新新闻**：`provider_news[]`，国内厂商取官方 News/公告，国内不可达的厂商
  取量子位 / IT之家 / 爱范儿 / 雷峰网等可检索资讯站，每条带抓取日期与来源。
- **波峰波谷时段**：`peak_valley[]` 与每个模型可选的 `peak_valley` 对象——DeepSeek 官方
  峰谷价（工作日 UTC 01-04 / 06-10 为峰，谷时半价）、SiliconFlow 镜像的时段定价、
  Kimi 与 OpenRouter 的 Batch 折扣；**厂商未公开的标注为「未公开」，不做推算**。
- **取数健康表**：`source_health[]` 记录每个来源的可达性实测结果（HTTP 状态、取回字节数、
  重试次数），`unresolved` / `deprecated_paths` 记录待补与已失效路径。

## 目录结构

```
index.html            # 单页：筛选区 + 模型卡片 + 峰谷时段 + 厂商新闻 + 取数健康
app.js                # 前端逻辑（只读 llm_pricing_data.json）
styles.css            # 样式
llm_pricing_data.json # 数据（schema v2.0，含全部来源标注）
scripts/build_pricing_data.py  # 数据生成脚本（可重跑）
.github/workflows/deploy.yml   # GitHub Pages 自动部署
```

## 本地开发

纯静态站，直接把仓库根目录指向任意静态服务器即可：

```
npx serve .        # 或 python -m http.server
```
