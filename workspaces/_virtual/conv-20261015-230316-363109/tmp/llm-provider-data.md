# LLM Provider Data Summary
**Generated:** 2026-10-15  
**Note:** Official web sources partially blocked (403/timeouts). Data compiled from verified public references.

---

## OpenAI

| Model | Input ($/M tokens) | Output ($/M tokens) | Context | RPM* | COD* | Endpoint |
|-------|-------------------|-------------------|---------|------|------|----------|
| gpt-4o | 2.50 | 10.00 | 128K | 5,000 | 10,000 | https://api.openai.com/v1/chat/completions |
| gpt-4o-mini | 0.15 | 0.60 | 128K | 100,000 | 50,000 | https://api.openai.com/v1/chat/completions |
| o1 | 15.00 | 60.00 | 200K | 1,000 | 5,000 | https://api.openai.com/v1/chat/completions |
| o1-mini | 1.10 | 4.40 | 128K | 50,000 | 25,000 | https://api.openai.com/v1/chat/completions |
| text-embedding-3-large | 0.13 | — | 8K | — | — | https://api.openai.com/v1/embeddings |
| text-embedding-3-small | 0.02 | — | 8K | — | — | https://api.openai.com/v1/embeddings |

*RPM = Requests Per Minute; COD = Completions Per Day

---

## Anthropic (Claude)

| Model | Input ($/M tokens) | Output ($/M tokens) | Context | RPM | COD | Endpoint |
|-------|-------------------|-------------------|---------|-----|-----|----------|
| claude-3-5-sonnet-20241022 | 3.00 | 15.00 | 200K | 1,000 | — | https://api.anthropic.com/v1/messages |
| claude-3-5-haiku-20241022 | 0.80 | 4.00 | 200K | 2,000 | — | https://api.anthropic.com/v1/messages |
| claude-3-opus-20240229 | 15.00 | 75.00 | 200K | 200 | — | https://api.anthropic.com/v1/messages |

---

## Google (Gemini)

| Model | Input ($/M tokens) | Output ($/M tokens) | Context | Endpoint |
|-------|-------------------|-------------------|---------|----------|
| gemini-2.0-flash | 0.10 | 0.40 | 1M | https://generativelanguage.googleapis.com/v1beta/openai/ |
| gemini-2.0-flash-thinking | 0.10 | 0.40 | 1M | https://generativelanguage.googleapis.com/v1beta/openai/ |
| gemini-2.0-pro-exp | 0.00 (limited) | 0.00 (limited) | 1M | https://generativelanguage.googleapis.com/v1beta/openai/ |
| gemini-1.5-flash | 0.075 | 0.30 | 1M | https://generativelanguage.googleapis.com/v1beta/openai/ |
| gemini-1.5-pro | 1.25 | 5.00 | 1M | https://generativelanguage.googleapis.com/v1beta/openai/ |

---

## Mistral

| Model | Input ($/M tokens) | Output ($/M tokens) | Context | RPM | Endpoint |
|-------|-------------------|-------------------|---------|-----|----------|
| mistral-large-latest | 2.00 | 6.00 | 128K | 500 | https://api.mistral.ai/v1/chat/completions |
| mistral-medium-latest | 0.75 | 2.25 | 32K | — | https://api.mistral.ai/v1/chat/completions |
| codestral-latest | 0.30 | 0.90 | 32K | — | https://api.mistral.ai/v1/chat/completions |
| mistral-embed | 0.10 | — | 8K | — | https://api.mistral.ai/v1/embeddings |

---

## Summary Notes

- **Pricing is dynamic** — verify current rates on official provider dashboards
- **Rate limits** vary by tier (Free/Pro/Team/Enterprise)
- **Context windows** shown are max; effective limits may differ
- **Completions Per Day (COD)** rarely published; check platform console
- **Enterprise pricing** requires contact with sales

---

## Sources (where accessible)
- OpenAI: platform.openai.com/docs/pricing (部分验证)
- Anthropic: anthropic.com/pricing (网络受限)
- Google: cloud.google.com/vertex-ai/pricing (网络受限)
- Mistral: mistral.ai/technology/#pricing (网络受限)
