---
name: market-brief-prompt
description: Generate a complete, ready-to-run market research prompt for CN equities, U.S. equities, or Crypto using the original premarket, postmarket, daily, weekly, and monthly templates. Use when the user wants a market-brief prompt to hand to a high-capability model.
---

# Market Brief Prompt

Produce the complete research prompt. The receiving model performs the whole
research task, including browsing, verification, analysis, outlook, writing and
self-review. This skill generates instructions; it does not research the market
or generate the report during prompt preparation.

## Select the original template

Resolve the market and cadence from the request or clear conversation context.
Ask only when either is missing or conflicting. Read only the selected file:

| Market | Cadence | Template |
| --- | --- | --- |
| CN / A股 | premarket / 盘前 | [A股盘前](assets/prompts/A股盘前prompt.md) |
| CN / A股 | postmarket / 盘后 | [A股盘后](assets/prompts/A股盘后prompt.md) |
| CN / A股 | weekly / 周度 | [A股周度](assets/prompts/A股周度复盘prompt.md) |
| CN / A股 | monthly / 月度 | [A股月度](assets/prompts/A股月度复盘prompt.md) |
| US / 美股 | premarket / 盘前 | [美股盘前](assets/prompts/us-premarket-prompt.md) |
| US / 美股 | postmarket / 盘后 | [美股盘后](assets/prompts/us-postmarket-prompt.md) |
| US / 美股 | weekly / 周度 | [美股周度](assets/prompts/us-weekly-review-prompt.md) |
| US / 美股 | monthly / 月度 | [美股月度](assets/prompts/us-monthly-review-prompt.md) |
| Crypto / 加密资产 | daily / 日报 | [Crypto日报](assets/prompts/crypto-daily-brief-prompt.md) |
| Crypto / 加密资产 | weekly / 周度 | [Crypto周度](assets/prompts/crypto-weekly-review-prompt.md) |
| Crypto / 加密资产 | monthly / 月度 | [Crypto月度](assets/prompts/crypto-monthly-review-prompt.md) |

These are the eleven supported combinations. Do not silently map unsupported
markets or cadences to one of them. All original templates request Chinese
reports, including templates whose instructions are written in English.

## Prepare the complete prompt

Preserve the selected template's research depth, output structure, source rules,
time boundaries, counterevidence and conditional outlook. Return its full body,
not a summary, a link to the template, a plan or empty section headings.

Add a short request-specific preamble only for the supplied date/period, cutoff,
focus, restricted scope, language, prior-report materials or output destination.
Keep supplied values exact. A focus adds emphasis; an explicit restricted scope
changes coverage. Do not invent prior reports, current facts or market data.
If a requested language differs, update the template's language/length rules
consistently rather than leaving conflicting instructions in the preamble.

When date or cutoff is unspecified, retain the template's execution-time defaults.
The receiving model must verify actual time, exchange calendars and daylight
saving time when it runs. Do not bake the prompt-generation timestamp or an
assumed trading date into a reusable prompt. Preserve historical-information
boundaries when a historical period is requested.

Output only the complete research prompt. Do not prepend model-selection,
reasoning-effort or execution-configuration handoff instructions.

Check the prompt for conflicting parameters, omitted template sections,
unresolved placeholders and accidental shortening before delivery. Output the
ready-to-copy prompt directly; save it as UTF-8 Markdown when a destination is
requested. Generating a prompt does not authorize running it, scheduling it or
publishing its future report.
