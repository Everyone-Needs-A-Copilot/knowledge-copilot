---
last_updated: 2026-06-28
status: active
---

# Copilot Prompt Library

Reusable prompts for common AI-assisted tasks. Each file is a self-contained prompt (or prompt system) ready to paste into Claude, ChatGPT, or any LLM interface.

## Prompts

| File | Purpose | Use When |
|------|---------|----------|
| [[01-minimize-gen-ai-writing-tells]] | Rules to suppress AI writing patterns | Any writing task where human-sounding output matters |
| [[02-master-researcher-and-strategist]] | Research and strategy persona with Munger mental models | Qualitative analysis, insight synthesis, journey mapping, strategic work |
| [[03-case-study-prompt]] | Template-driven case study generator from transcripts | Turning project transcripts into publishable case studies |
| [[04-article-summary-prompt]] | Six-section article analysis framework | Making complex articles actionable for specific audiences |
| [[05-n8n-prompts]] | n8n automation assistant + workflow conversation starters | Building or debugging n8n workflows |

## How to Use This Library

1. Find the prompt that matches your task.
2. Open the file and copy the prompt text (usually inside a code block or clearly labeled section).
3. Paste into your LLM interface — Claude project instructions, a new conversation, or a ChatGPT custom GPT.
4. Provide any required context (transcripts, data, article text) and send.

## Skill Promotion Candidates

The following prompts have methodology-grade depth and may be worth promoting to formal Claude Skills in [[01-skills]] for agent-level reuse:

- **[[02-master-researcher-and-strategist]]** — Comprehensive research persona with 30+ mental models and a full data analysis workflow. Suitable as a `@agent-ta` or standalone research skill.
- **[[01-minimize-gen-ai-writing-tells]]** — Systematic anti-AI-tell rule set. Suitable as a reusable writing preamble skill for `@agent-cw`.
