Use web search to produce a “Crypto Daily Brief: Market Review and Near-Term Outlook.”

You are a prudent, evidence-focused market researcher. Using observed prices, market participation, macroeconomic developments, spot and derivatives evidence, and important protocol or token events, explain what crypto markets have just repriced and what deserves attention next.

The central questions are:
What changed over the past 24 hours, and what actually drove the move?
Do price, market breadth, demand, and leverage support the same interpretation?
Which earlier assessments should be maintained or revised?
What could matter over the next 24–72 hours, and what observable evidence would confirm or overturn the assessment?

Produce one integrated daily report, not separate Brief and Review outputs. Combine retrospective attribution with a substantive, conditional forward outlook without repeating the same analysis twice. Crypto trades continuously: do not impose a universal opening, closing, premarket, or after-hours session.

[I. Timing and Information Boundaries]

1. Use UTC as the primary timestamp convention and Beijing time, Asia/Shanghai (UTC+8), as the secondary reference. Respect an explicitly requested cutoff and time zone, then show the UTC equivalent.
   Unless otherwise specified, use the actual research cutoff T as the report's as-of time. This is an analytical snapshot, not an exchange closing time.

2. The default review window is the 24 hours ending at T. The primary forward window is the next 24 hours after T, with a separate 24–72-hour outlook and material catalysts over the next 7 calendar days.
   State the exact backward-looking and forward-looking intervals. A report generated late in a UTC day still looks ahead from T; do not reduce the outlook to the few hours before midnight or treat elapsed hours as forecasts.

3. Record the news cutoff and the actual market-data endpoint separately. Use synchronized observations for the main 24-hour return comparison; disclose a material delay or mismatch and label the actual measured interval when it differs from the intended window.
   Use the past 7 and 30 calendar days for context. Keep rolling returns, UTC calendar-day returns, and changes since a previous report distinct. Do not combine dashboard observations taken at different times into an apparently synchronized snapshot.

4. Prioritize material news first made public during the review window. Retain earlier developments only when their unresolved implications still matter, and label their original dates.
   Where a previous Daily Brief is actually available, evaluate developments since its publication against its original conditions. If reporting intervals overlap or leave a gap, identify the actual evaluation window rather than treating the reports as disjoint calendar days.

5. If a historical date D is specified without a time, review that UTC calendar day, using D+1 at 00:00 UTC as both its endpoint and the default historical information cutoff. An explicit as-of timestamp instead uses the 24 hours ending at that timestamp.
   Use only expectations and data vintages publicly available by the historical cutoff, and form the outlook from that perspective. Do not use later prices, revised wallet labels, or subsequently known outcomes. For an explicitly future date, label the output an early edition based on currently available evidence; do not fabricate a completed review of that future day.

6. Distinguish events first public before the price-data endpoint, news released between that endpoint and T, and disclosures measuring an earlier period. Later news may update the outlook but cannot explain a price move that preceded its release.
   State the reference period, publication time, and provisional status of material fund-flow and on-chain observations. Missing or delayed figures are not zero activity.

7. Include weekends and holidays in the crypto window. Verify the actual calendar and live/stale status of each traditional-market, fund, derivatives, and settlement observation.
   For important future events, give UTC and Beijing times and scheduling certainty. Check daylight saving time for local schedules and distinguish confirmed clock times from estimated block- or epoch-based milestones.

[II. Research Methods and Crypto Data Standards]

1. Prioritize original evidence: official economic releases and central-bank communication; regulators, court records, and fund filings; exchange market data and contract specifications; protocol documentation, governance records, status pages, and verifiable on-chain transactions.
   Use established market and on-chain data providers with disclosed methodology for aggregation. Specialist reporting can identify leads and add context, but duplicated reporting is not independent confirmation. Verify current product availability, trading hours, and rules rather than relying on remembered arrangements.

2. Follow this analytical chain:
   New fact → difference from prior expectations → effect on demand, available supply, liquidity, economic activity, token value capture, or risk premia → observed price response → confirmation and invalidation conditions.
   Separate facts, interpretations, and forward hypotheses. Compare actual releases with sourced pre-release expectations, previous readings, and revisions. A prior reading or a project's own target is not market consensus. Search for counterevidence to the main explanation; do not use “profit taking,” “whale buying,” or “short covering” as unsupported default explanations.

3. Use consistent providers, instruments, quote currencies, and timestamps for comparisons. Distinguish spot, index, mark, perpetual-futures, dated-futures, and fund prices. USD, USDT, and USDC quotes are not automatically interchangeable, especially during a depeg.
   Calculate period returns from consistent boundary observations or completed candles: ending price / starting price - 1. Compound subperiod returns rather than adding them. Do not mix price returns with staking-inclusive returns, funding P&L, or airdrop proceeds. Treat rolling 24-hour dashboard statistics as rolling observations, not calendar-day results. A series of overlapping 24-hour volume snapshots cannot be summed into period volume.

4. Use BTC and ETH as core reference assets, not as substitutes for the whole market. Include other liquid assets when their market role or new evidence warrants it. State the source, sample size, eligibility, and weighting of any breadth or sector statistic.
   Exclude stablecoins, duplicate wrapped or bridged representations, leveraged tokens, and tokenized non-crypto assets from the default risk-token breadth universe; analyze them separately when relevant. Handle new listings, migrations, redenominations, delistings, and missing histories explicitly. Use point-in-time constituents for historical comparisons when available; otherwise label survivor-biased or illustrative samples.
   Define the denominator of BTC dominance and any “ex-BTC/ex-ETH” aggregate, including whether stablecoins are included. Market-cap changes also reflect supply and constituent changes: they are neither net capital flows nor automatically an investable portfolio return. Overlapping theme labels must not be added as independent market shares.

5. Separate spot demand, exchange transfers, investment-product flows, corporate treasury purchases, and stablecoin supply changes. For each, state the measurement window, coverage, publication time, and whether the figure is final, provisional, or inferred.
   Fund trading volume and AUM changes are not subscriptions. Announced purchases are not executed purchases. Stablecoin minting is not proof of deployment into risk assets. An exchange deposit is not proof of a sale; an outflow is not proof of accumulation. Wallet labels and entity classifications can be incomplete or revised. Do not combine overlapping flow measures into an invented total of “new money.”

6. For open interest, funding, basis, options, and liquidations, verify the venue, instrument, units, timestamp, and aggregation method. Distinguish contract or coin quantities from USD notional; price changes alone can alter USD open interest. Check whether a provider counts one or both sides before combining datasets.
   Distinguish predicted funding from settled payments; verify each contract's current settlement interval and normalize only on a stated basis. Funding and open interest alone do not identify net directional conviction. Separate perpetual funding from dated-futures basis, and options premium from underlying notional. State tenor and conventions for implied volatility or skew. Reported liquidation notional is not traders' cash losses, and liquidation heatmaps are estimates rather than observed future orders. Do not invent dealer gamma, hidden positions, or a compulsory “max-pain” price outcome.

7. Distinguish network or application usage, user fees, provider-defined revenue, and economic benefits actually accruing to the token. Identify the active mechanism and its beneficiaries; a proposal, a tokenless application, or revenue accruing to an operating company does not automatically benefit a related token.
   Check incentives, activity quality, double counting, and the effect of token prices on USD-denominated operating metrics. Treat total value locked (TVL) as a stock, not revenue or net inflow. Addresses are not unique people; transfers are not necessarily payments. Use comparable definitions across protocols and explain material methodology differences.

8. Separate circulating supply, total supply, maximum supply, free float, issuance, vesting releases, burns, and unlocks. Verify token units, recipients, restrictions, and schedule certainty. Scheduled availability, actual distribution, transfer to an exchange, and executed selling are different stages.
   When material, assess supply pressure relative to circulating supply and credible executable liquidity, not merely headline dollar value or inflated reported turnover. Avoid double counting emissions and unlocks. Fully diluted valuation depends on the supply definition and is not a universal measure of fair value.

9. Align crypto observations with the actual timestamps and current trading calendars of cross-asset instruments, funds, and settlement channels. Do not treat stale traditional-market quotes or unreported fund flows as contemporaneous confirmation, zero flow, or a live divergence. Verify daylight saving time for U.S. events; do not assume all derivatives or funding channels share one schedule.
   Distinguish policy proposals, filings, approvals, effective rules, and operational launches. For a security incident, distinguish a reported allegation, verified exploit, estimated loss, recovery, and unresolved exposure. Do not amplify unverified wallet identities or rumors as facts.

10. Use only data actually retrieved or reproducibly calculated from retrieved inputs. Ground technical levels in a named instrument, timestamp, timeframe, and method; distinguish completed candles from an unfinished candle. Do not invent indicators, targets, causal contribution percentages, calibrated probabilities, or universal signal thresholds.
    Disclose a material data gap once, near the affected conclusion, and reduce the strength of that conclusion. Omit nonessential unavailable metrics rather than filling the report with “not found,” “to be determined,” or empty sections. An inaccessible paid dataset is not permission to fabricate a proxy. Research priorities are not automatic orders, leverage recommendations, or fixed portfolio allocations.

[III. Use the Following Output Structure]

# Crypto Daily Brief | As-of Date and Time (UTC)
State the 24-hour review window, market-data endpoint, news cutoff, and forward horizon in UTC and Beijing time, together with only the limitations that materially affect the assessment.

## 1. Today's Core Conclusions
In approximately 200 Chinese characters, answer:
What primarily drove repricing: macro conditions, spot demand, leverage, supply, protocol developments, or a few asset-specific events?
What were the 3–5 most consequential changes?
Did BTC/ETH performance agree with broader participation?
Did the risk environment improve, deteriorate, remain broadly unchanged, or become more fragmented?
Which change matters most over the next 24–72 hours?

Give the main supporting evidence and strongest counterevidence. If there is no coherent market-wide driver, identify dispersion rather than inventing a dominant narrative.

## 2. Performance, Market Breadth, and the Shape of the Move
Compare BTC, ETH, ETH/BTC, and a disclosed liquid non-stablecoin sample over the review window, with 7- and 30-day context. Add relevant major assets or sector benchmarks only when they clarify the market structure.
Where reliable, examine median returns, advancing/declining participation, the fraction outperforming BTC, concentration, spot activity, and volatility. Distinguish absolute gains from merely outperforming a falling market.

Identify broad demand, BTC-led concentration, selective rotation, high-beta rebounds, liquidation-driven dislocation, or widespread de-risking. Do not declare broad altcoin expansion from a falling BTC-dominance reading or a few large gainers.
Explain the few decisive event windows rather than narrating every hour. Use completed 1-day and 4-hour structure for context, and 1-hour observations only for useful near-term validation. Any technical level must have a retrieved basis, named instrument, timeframe, and method; one venue's wick is not automatically a market-wide break.

## 3. Key Events, Expectation Gaps, and Price Reactions
Select approximately 3–5 material developments, fewer when warranted. For each, explain:
First-public timestamp → sourced prior expectation or prior state → actual new information → demand/supply/liquidity/economic transmission → initial reaction → persistence, reversal, or broader participation by the snapshot → unresolved implication.

Potential developments include macro releases, policy decisions, verified fund or treasury disclosures, exchange changes, upgrades, governance execution, supply events, and security incidents.
Pay particular attention to favorable news with a weak response, resilience after adverse news, and strong benchmark performance with deteriorating participation. Separate an event's initial trigger from the mechanism amplifying its impact. Give a plausible alternative explanation and confidence assessment for the leading attribution.
Do not rank importance by social-media popularity or the size of a thinly traded token's move. Future releases belong in the event calendar, not among actual results.

## 4. Spot Demand, Derivatives, Supply, and Liquidity
Use the few observations that best distinguish competing explanations rather than displaying every available metric.
Assess material changes in spot participation and executable liquidity; the latest verified investment-product flows, treasury transactions, and stablecoin developments; open interest, settled funding, basis, liquidations, and options pricing; and relevant token-supply events.

Ask whether the evidence is more consistent with persistent spot participation, leveraged extension, position unwinding, or a temporary liquidity shock. Price and open interest alone do not establish how many new longs, shorts, or institutional purchases occurred.
Distinguish leverage added or removed from USD-notional revaluation. For depth, give the venue, price band, and timestamp. For a supply release, distinguish scheduled availability, actual distribution, and observed selling.
Explain what the remaining position and liquidity structure implies for the next 24–72 hours. Do not assume a reset in funding or a liquidation episode has eliminated risk.

## 5. Macro and Cross-Asset Checks
Assess the relevant policy-rate expectations, U.S. yields and real yields, the dollar, equities, credit, gold, and other assets only when they have a plausible connection to the current crypto thesis.
Explain whether matched-window reactions support a shared macro driver or point toward a crypto-specific catalyst. Label stale readings and reporting lags; a closed or delayed market cannot provide live confirmation.

Distinguish changes in growth, inflation, policy, liquidity, and risk appetite. Do not mechanically treat lower yields or easier policy as bullish, or assume crypto has a permanent safe-haven or fixed-beta relationship with another asset.
Identify the cross-asset evidence that would strengthen or weaken the next-period thesis. Shorten this section when there is no material independent confirmation or contradiction.

## 6. Theme Rotation and Priority Assets
Scan the market broadly, but discuss only approximately 3–5 areas with meaningful changes in relative strength, participation, economic evidence, catalysts, or risk. Include deterioration and failed responses as well as leaders; do not force daily coverage of every sector.

Present one compact table:
Area / representative token | 24-hour and recent relative performance | Main catalyst and actual token exposure | Change in participation or phase | Next confirmation condition and horizon | Invalidation condition / main risk.

Distinguish trend continuation from a one-day bounce and token-holder benefits from success at the network, application, or operating-company level. A thematic label is not evidence of direct economic exposure.
Use representatives to explain the thesis, not as a shopping list. Clarify which areas deserve continued attention, which are improving but unconfirmed, and which should receive lower priority. Do not let an intraday move settle a multiweek adoption or valuation thesis.

## 7. Review of Previous Assessments
Include this section only when an actual earlier Daily Brief is available. Evaluate its 2–3 most material hypotheses against their original evidence, trigger conditions, publication time, and validity horizons.
Use a compact comparison where useful:
Original hypothesis and horizon | Original trigger | Observed post-publication outcome | Evaluation | Required revision.

Use these categories: supported, partially supported, invalidated, not triggered, and still awaiting validation.
Assess direction, mechanism, timing, and risk warnings separately. Do not rewrite a trigger after the fact, score pre-publication price action, treat an untriggered condition as a win or loss, or terminate a longer horizon merely because 24 hours have passed.
If no earlier report is available, omit forecast scoring without asking for one. The report's retrospective market analysis and forward outlook must still be complete.

## 8. Next 24–72 Hours: Event Calendar and Conditional Scenarios
List the most important events over the next 24–72 hours, plus consequential events within the next 7 calendar days. State exact UTC/Beijing times where verified, scheduling certainty, the sourced expectation or prior state, and the hypothesis each event tests.
Include macro and policy releases, product milestones, protocol implementations, governance execution, token releases, derivatives expiries/settlements, and operational interruptions only when material. Do not assign invented clock times to uncertain milestones.

Provide three scenarios: base case, stronger case, and weaker case.
For each specify:
Observable trigger → confirming price/participation/flow response → expected market structure and theme effects → research priority → invalidation condition → validity window.

Explain which scenario is best supported by current evidence without assigning uncalibrated numerical probabilities. A stronger scenario needs positive confirmation, not just an absence of bad news.
Conclude this section with 2–3 testable hypotheses for the next daily edition, each using a named asset or metric, observable condition, and explicit event window or horizon. Preserve them for later evaluation if that edition has access to this report.
Use event reactions and the next completed 1-hour or 4-hour observation where useful; there is no universal opening auction or closing-session test. An untriggered scenario is not an instruction to enter a trade.

## 9. Risks and Final Watch Items
Explain the leading risk through a specific trigger and transmission mechanism: weak depth, unstable leverage, token supply, stablecoin or counterparty stress, protocol incidents, correlated exposure, or event timing, according to the evidence.

Conclude with:
The most valuable new evidence and the assessment it changes;
Three confirmation signals for the next phase;
The principal invalidation condition;
One materially unresolved question or reason to wait rather than extrapolate the move.

Do not repeat the event descriptions or scenario table. Research priorities are conditional observations, not immediate orders, leverage recommendations, or fixed position allocations.

[IV. Writing Requirements]

Write in Chinese, retaining necessary English tickers and identifiers. Target approximately 2,000–3,000 Chinese characters for the main text.
Integrate review and outlook into one report: use recent evidence to explain the current state, then provide meaningful forward scenarios and validation conditions. Do not concatenate two reports or reduce the outlook to a token closing sentence.
Keep background brief. Daily research should privilege material new information and immediate validation over exhaustive sector catalogues or slow-moving valuation essays.
End with one sentence answering: “What did the past 24 hours change, and what most needs confirmation over the next 24–72 hours?”

Lead with conclusions. Prioritize changes, evidence, disagreements, and validation rather than a long news digest or indicator inventory.
If web access is unavailable, say so and do not simulate current research from training memory. Complete only the verifiable portions and distinguish any non-current framework from live findings.
Do not ask me to supply a token universe, market data files, or earlier reports. Use an available user watchlist as additional context, not as a replacement for market-wide coverage; otherwise select a disclosed liquid-market reference universe.
Review earlier hypotheses only when the actual prior report is available in the conversation or accessible authorized context. Never invent earlier views or a forecasting record. Each edition includes both review and outlook; it does not require a separate companion report. Do not imply that alerts, monitoring, trades, or future reports have been scheduled by writing this report.

[Markdown and Formatting Rules]

1. Use standard Markdown for the report body. Use one # title and ## main sections, translating section names naturally into Chinese. Prefer ordinary paragraphs; avoid unnecessary deeper headings, decorative separators, bold, italics, code blocks, HTML, and nested lists.

2. Use tables where explicitly requested or where they materially improve comparison. Keep cells short, with one record per row and no embedded line breaks or lists. Leave a blank line before and after a table. Do not put the vertical-bar character inside cell text. Put dense sourcing in the corresponding paragraph after the table rather than breaking the table layout.

3. Cite sources close to key figures, news facts, and evidence-based assessments. Use the platform's supported citations; when these are unavailable, provide readable source names and working source links. Never print raw internal reference IDs, tool fields, unfinished citation syntax, search placeholders, or empty “Sources” sections.

4. Each paragraph should usually contain 2–5 sentences and develop one idea. Use short lists only for scenarios, event calendars, and final watch items. Explain a fact fully once; later sections should develop its implication rather than repeat the same news.

5. The section order is a research framework, not a requirement to pad the report. Shorten or omit explicitly conditional sections when there is no material evidence. Do not omit core conclusions, period definitions, main supporting and opposing evidence, or the final validation conditions. Prioritize substantive completeness over mechanical word counts while keeping the simplest readable format.
