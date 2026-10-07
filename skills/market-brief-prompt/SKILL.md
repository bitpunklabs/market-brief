---
name: market-brief-prompt
description: Design, generate, or upgrade a complete market-brief research prompt from reusable research capabilities, market mechanisms, and cadence requirements. Use for CN, US, Crypto, or adapting this methodology to another specified market.
---

# Market Brief Prompt

Deliver a self-contained research prompt that a receiving model can execute as
one integrated research task. This skill delivers the prompt; market research
and the resulting report happen at execution time.

## Understand the request

Resolve market, cadence, and any explicit date/period, cutoff, focus, restricted
coverage, language, prior-report material, or destination. Ask for a missing or
conflicting essential choice; preserve supplied values exactly. Apply the resolved
language to both prompt and report: default to Chinese (`zh`) for CN and English
(`en`) for every other market. Explicit language requests override this default.
A focus adds depth; restricted coverage changes the universe.
Unspecified dates retain execution-time resolution rules.

For an upgrade, read the supplied prompt and identify its research obligations
before redesigning it. User requirements take precedence over defaults.

## Read the relevant capabilities

Read [research capabilities](references/research.md) and the selected sections of
[cadence requirements](references/cadences.md), then the relevant market profile:

| Market | Profile | Default cadences |
| --- | --- | --- |
| CN / A股 | [CN](references/markets/cn.md) | premarket, postmarket, weekly, monthly |
| US / 美股 | [US](references/markets/us.md) | premarket, postmarket, weekly, monthly |
| Crypto | [Crypto](references/markets/crypto.md) | daily, weekly, monthly |

These resources define research responsibilities and correctness conditions,
not prose fragments or a fixed report outline. Select, integrate, and express
them for the actual task. Keep the substantive obligations of the chosen market
and cadence even when changing the organization or wording.

For another specified market, follow the adaptation procedure in
[evaluation and evolution](references/evaluation.md). Ground exchange, calendar,
currency, benchmarks, disclosures, policy transmission, and market rules in
institutional sources before generating a tailored prompt.

## Design and write

Choose a coherent research objective, information boundary, and report structure.
Build sections around what the receiving model must determine and the evidence
needed to do so. Integrate shared requirements once, then deepen the selected
market and cadence. Define required outcomes while giving the model discretion
over research tools, ordering, and effort allocation.

Write a complete new prompt rather than returning module names or concatenating
reference text. Use affirmative instructions: state the desired analysis,
eligible data, correct calculation, or treatment of uncertainty. Preserve data
distinctions and information boundaries through precise positive requirements.

Develop the outlook from material unresolved questions in the preceding research:
the best-supported view, mechanism, priced expectations, and evidence that could
advance or revise it. Express observations and horizons naturally for each issue.
Maintain an unchanged thesis through updates to evidence and unresolved questions.

Use execution-time instructions for actual time, calendars, current rules, data,
and sources. Prompt preparation supplies the research design; current findings
are established by the receiving model. Capability-specific guidance is useful
when the user supplies execution constraints. Keep model names, effort settings,
and configuration handoffs in the execution environment.

## Review and deliver

Check the draft against the semantic acceptance criteria in
[evaluation and evolution](references/evaluation.md). Revise lost obligations,
parameter conflicts, ambiguous endpoints, repetitive instructions, and unsupported
assumptions. Keep essential research depth ahead of brevity.
Express material data distinctions operationally: what the observation measures,
which additional evidence a stronger inference needs, and how periods or units align.

`assets/prompts/` contains the eleven hand-written controls. For a supported
combination with a control, read it after drafting to audit substantive
responsibilities before delivery. Repair material losses while preserving the
new prompt's coherent design. Compare meaning rather than headings or wording.
Generation starts from capability references; controls enter during review.

Output the complete ready-to-copy prompt, or save UTF-8 Markdown at the requested
destination. Evaluation notes are separate artifacts when requested.

For requested skill/model upgrades, use the evidence-driven revision procedure
in the evaluation reference. The current host model performs prompt design;
changes are accepted on observed results, with limitations stated explicitly.
