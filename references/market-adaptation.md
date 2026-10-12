# Market adaptation

Read this guide when the requested equity market has no matching Asset prompt,
or when the user explicitly asks to add a market to the library. Use the existing
prompt as the research assignment; adapt its local assumptions in the current
agent. The selection table in `SKILL.md` remains the library's only route list.

## Choose the base

Identify the target listing market or exchanges, instrument universe, and cadence.
An issuer's home country, listing venue, quote currency, and report language can
differ. A thematic focus retains broad market coverage unless the user restricts it.
For a regional brief, define the covered exchanges and benchmark universe; keep
different session endpoints explicit rather than inventing a single regional close.

Use a user-selected base when it fits the assignment. Otherwise choose the same
cadence and closest research structure: the U.S. equity prompts are the default
base for other equity markets; the A-share prompts may fit a specifically requested
policy/industry emphasis. Read the selected file completely. Name the target and
base in a brief adaptation note outside an exported prompt, or beside the report's
scope statement. The deliverable remains a report or a full prompt, as requested.

Preserve the cadence. Do not turn a Crypto Daily Brief into an equity premarket
brief, infer that an equity "daily" means postmarket without clear context, or
invent a premarket session for a continuous market. Resolve an ambiguous window
with one short question. For a different asset class, explain whether an existing
prompt covers its economics; if it does not, agree the new research assignment
instead of presenting a renamed equity prompt as full support.

## Preserve the research, replace the local assumptions

Keep the base's analytical depth, materiality-based selection, source hierarchy,
expectation comparisons, breadth and sector scan, company economics, substantive
outlook, counterevidence, and confirmation/invalidation conditions. Preserve explicit
user dates, cutoffs, coverage, language, and accessible prior reports. Do not shorten
the assignment to a generic news summary during adaptation.

Resolve these dimensions throughout the prompt or execution:

| Dimension | Target-market adaptation |
| --- | --- |
| Time and sessions | Verify the exchange calendar, local time zone, opening/closing auctions, breaks, holidays and early closes. Derive review and forward windows from actual sessions; keep historical cutoffs and any requested secondary time zone. |
| Universe and benchmarks | Use target listings and relevant broad, sector and style benchmarks with disclosed samples, classifications and weighting. Identify cross-listings and depositary receipts; do not double count them. |
| Quotes and returns | Label quote currency, units, session, timestamp, delay, price/total-return basis and corporate-action adjustments. Separate cash indices, futures, ETFs and extended-session observations; retain FX effects for cross-currency comparisons. |
| Primary sources | Find the target exchange, regulator, central bank, statistical agencies and issuer disclosure channels. Verify their remit. Retain foreign sources where the cross-market mechanism warrants them. |
| Company economics | Localize financial reporting, fiscal periods, accounting basis and expectations sources. Preserve operating/earnings evidence separately from valuation and embedded expectations. |
| Structure and flows | Verify local trading, settlement, short-sale and price-limit rules only where material. Verify fund/flow channels and disclosure coverage; turnover, assets and inferred positioning are not net purchases. |
| Events and transmission | Use relevant policy releases, company disclosures and supply/demand catalysts. Explain how foreign developments affect target earnings, costs, discount rates or risk premia. |

Replace source-market headings, dates, session rules, mandatory domestic indicators,
representative securities, agencies and flow mechanisms wherever they define the
target market. Keep U.S., Chinese or Crypto evidence when it is explicitly a relevant
cross-market observation. Do not remove a genuine transmission channel merely to
eliminate a country name. Other equity markets default to English; explicit language
requests override this without changing the market or sources.

Verify current local facts with official sources at research time; do not encode
remembered trading rules as permanent defaults. For historical work, use calendars,
rules, expectations and data versions applicable by the requested cutoff. If a
material local assumption cannot be verified, disclose it and limit the affected
conclusion. If the session or universe cannot be determined, resolve it before
claiming a current market brief. Missing optional data need not stop useful research.

## Deliver a one-off adaptation

For a brief, execute the adapted assignment directly and deliver the complete
source-backed report with its actual research window and cutoff. No intermediate
prompt file is required. For an export, deliver a complete standalone prompt with
local clauses resolved in its body; an override header that leaves contradictory
source-market instructions underneath is insufficient. Keep date-dependent rules
as verification tasks unless a sourced, explicitly dated rule is requested.

Check the result for inherited market assumptions, session/cutoff consistency,
benchmark and instrument comparability, primary-source coverage, and preservation
of the base's outlook and counterevidence. Review Markdown formatting as well.
Keep both workflows outside `assets/prompts/`; save only when a destination is
requested. With no browsing, export verification instructions or deliver clearly
labeled non-current analysis, without claiming local rules were verified.

## Add permanent library support

Only an explicit request to add, maintain, or permanently support a market authorizes
a new library entry. Choose a descriptive filename such as `hk-premarket-prompt.md`
and write the complete adapted prompt in `assets/prompts/`. It must work when copied
alone, without loading this guide or its base. Add one market/cadence route in
`SKILL.md` and a corresponding README link. Do not add a second route for an alias.

Review the new scenario and the unchanged base. Run `python scripts/check.py`, the
package tests, and build/extract the package to confirm the added asset travels with
the skill. Keep private comparison reports and experiments in ignored directories.
Report text review, source verification, executed-report evidence and package checks
separately; packaging alone does not establish research quality in the new market.
