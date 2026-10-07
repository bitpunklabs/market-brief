# Market Brief Prompt

Turn a market research request into a complete, ready-to-copy prompt.

A lightweight agent skill for CN equities, U.S. equities, and Crypto. It designs
research assignments from shared capabilities, market mechanisms, and cadence
requirements, then reviews them against hand-written controls. Each prompt gives
the receiving model one integrated task: research, verify, analyze, develop an
outlook, write, and self-review.

<p align="center">
  <img src="assets/demo-placeholder.svg" alt="Demo placeholder: a research request becomes a reviewed, ready-to-copy prompt." width="960">
</p>

*Request → design and review → complete research prompt.*

<!-- DEMO PLACEHOLDER
Replace the image source above with assets/demo.gif when the recording is ready.
Storyboard: a 12-second loop, 1200 × 600, readable at 960 px, with a still opening frame.
0–3s: enter "$market-brief-prompt Generate a U.S. monthly research prompt."
3–8s: show the generated assignment's time boundaries, earnings, and valuation tasks.
8–12s: scroll to the issue-driven outlook and copy the complete Markdown prompt.
Use a real generation recording; the demo ends at prompt delivery.
-->

## Quick start

Use an agent that can load skills and read local Markdown files. For Codex, copy
the entire skill folder from this repository's root into your personal skills
directory:

```sh
mkdir -p "$HOME/.agents/skills"
cp -R skills/market-brief-prompt "$HOME/.agents/skills/"
```

For a project-specific installation, use that project's `.agents/skills/`
directory instead. See the [official Codex skills guide](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)
for discovery details.

Ask the agent to generate or upgrade a prompt:

```text
$market-brief-prompt Generate a CN premarket research prompt.
$market-brief-prompt Generate a U.S. weekly prompt focused on earnings and interest rates.
$market-brief-prompt Generate a September 2026 Crypto monthly prompt using only information public before 2026-10-01 00:00 UTC.
$market-brief-prompt Upgrade the prompt below, preserving its research depth and simplifying repeated instructions.
```

Specify a date or period, information cutoff, focus, coverage restriction, language,
or Markdown destination when needed. A focus adds depth; a restriction changes
the research universe. Unspecified dates are resolved when the prompt is executed.

The output is a self-contained prompt. Run it with a model that has web research
and source-verification tools to produce a current market report. Model and effort
settings belong in the execution environment.

## Supported markets

| Market | Cadences | Default prompt and report language |
| --- | --- | --- |
| CN equities | Premarket, postmarket, weekly, monthly | Chinese |
| U.S. equities | Premarket, postmarket, weekly, monthly | English |
| Crypto | Daily, weekly, monthly | English |

Explicit language requests override these defaults. Other markets require an
institutional profile grounded in official sources before prompt generation.

## How it works

1. Resolve the request and read the relevant research, cadence, and market resources.
2. Design a complete assignment with visible analytical priorities and evidence requirements.
3. Review the draft against semantic acceptance criteria and the matching hand-written control; repair material losses before delivery.

The outlook follows the research's unresolved questions: the best-supported view,
its mechanism, priced expectations, and evidence that would advance or revise it.
Time, calendars, current rules, and market data are verified during execution.

The package contains one [skill entry point](skills/market-brief-prompt/SKILL.md),
[shared research capabilities](skills/market-brief-prompt/references/research.md),
[cadence requirements](skills/market-brief-prompt/references/cadences.md),
[market profiles](skills/market-brief-prompt/references/markets/), and
[11 hand-written controls](skills/market-brief-prompt/assets/prompts/).
All runtime resources live inside the skill folder; the project has no client,
database, or scheduler dependency.

## Status and evaluation

Early preview. Local evaluation records cover 11 market/cadence combinations,
two parameter cases, and two fresh-context generations, with revisions against
the controls. These are prompt-text evaluations; report quality remains to be
tested with matched market, date, cutoff, source access, and model settings.

Evaluation artifacts currently live in the ignored `temp/` directory and are
not included in a fresh checkout. See the
[evaluation criteria](skills/market-brief-prompt/references/evaluation.md) for the
acceptance method. A published evaluation sample and a license are pending.

## Contributing

Keep shared research responsibilities, cadence rules, and market semantics in
their respective resources. Preserve coverage, depth, evidence selection, and
deliverable clarity when simplifying instructions. Compare affected prompts with
the controls and record limitations alongside evaluation results.
