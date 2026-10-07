# Record and helper contract (schema version 1)

Requires Python 3.11+ with standard-library `tomllib` and IANA timezone data. No
package install, network or model call is performed by the helper. Commands read
a JSON object from a file or `-` (stdin), and emit JSON without modifying inputs.
Exit codes: 0 resolved/calculated/passed, 1 invalid/failed, 2 pending.

## Resolve

```json
{
  "now": "2026-10-07T08:00:00Z",
  "request": {
    "market": "crypto",
    "cadence": "daily",
    "target": "2026-10-05",
    "language": "en",
    "allow_post_period": false
  }
}
```

```sh
python3 scripts/brief.py resolve request.json
```

The host obtains actual `now` before calling; all timestamps require explicit
UTC offsets. `market` accepts registry aliases, `cadence` an exact supported ID.
Optional `scope` is a text description, not an implied full-universe guarantee.
Omit `target` for default selection. Daily/session targets are YYYY-MM-DD,
weekly targets are any YYYY-MM-DD within the requested market week, monthly
targets YYYY-MM. Explicit language overrides registry-derived defaults.

Optional `as_of` freezes an explicit timestamp, never later than `now`. Fixed
historical targets without as_of use period_default: before open (exclusive),
regular close (inclusive, also for an equity trading week), or next-period
boundary (exclusive, for natural months and continuous-market weeks). A later explicit
as_of for a fixed completed target requires `allow_post_period: true`; it never
changes primary-period attribution. Latest full week/month can have a current
global cutoff while their primary cutoff stays at period end. Later facts may
enter outlook, and update claims require explicit allow_post_period.

Equities require `calendar` alongside request/now:

```json
{
  "source_url": "https://example.org/exchange-calendar",
  "support": "Actual read excerpt or exact schedule locator; example URL is not evidence",
  "retrieved_at": "2026-10-07T08:00:00Z",
  "timezone": "Asia/Shanghai",
  "start_date": "2026-09-28",
  "end_date": "2026-10-09",
  "sessions": [
    {"date": "2026-09-30", "open": "2026-09-30T09:30:00+08:00", "close": "2026-09-30T15:00:00+08:00"},
    {"date": "2026-10-08", "open": "2026-10-08T09:30:00+08:00", "close": "2026-10-08T15:00:00+08:00"}
  ]
}
```

This is a shape example, not a verified exchange schedule. The host must confirm
every actual session/closure within inclusive coverage dates. Include the
previous actual session for price/news boundaries. Full-period requests require
the entire period's coverage, including the current equity week for default
weekly selection. An actual short week completes at its final regular close;
default selection skips fully closed weeks. Helper status `resolved`/`input_validated` checks
these recorded inputs; it cannot prove the source schedule is complete or correct.
UTC or actual local-offset session timestamps are accepted; stale DST offsets,
duplicate sessions and inverted coverage are rejected.

The result contains canonical request and context: task ID, language/scope,
timezone, frozen as_of, generation time, cutoff origin/inclusivity, information
period with explicit endpoints, primary attribution cutoff, intended price
window, actual target session, calendar provenance and historical-reconstruction
label. Equity weeks' primary cutoff is their final regular close, not next
Monday; equity months retain a natural-month news cutoff and a separate final
regular-close attribution boundary. Calendar-period labels retain actual session
count. Price observations retain their actual measured endpoints separately.
Continuous daily context adds forward endpoints at 24/72 hours after cutoff.

Missing calendar/previous session, closed periods and future/incomplete completed
requests return pending. First helper version does not resolve wtd/mtd, custom
intervals or future completed-period early editions; handle their boundary
definition explicitly in the host rather than coercing them into full periods.

## Calculate

```sh
python3 scripts/brief.py calculate calculation.json
```

Supported shapes:

- `{"operation":"return","start":"100","end":"110"}` → decimal price return.
- `{"operation":"compound","returns":["0.1","-0.1"]}` → compounded decimal return.
- `{"operation":"daily_average","total":"310","days":31,"measure_type":"flow","unit":"USD/day"}` → flow per day.

Use decimal strings for exact numeric inputs. Returns are decimal fractions,
not percentage points. Stocks cannot be divided by day counts. Currency, units,
instrument comparability and genuine data provenance still need host review.

## Check a saved research package

Save the actual report and one run record outside the skill installation:

```text
runs/<run_id>/brief.md
runs/<run_id>/run.json
runs/<run_id>/inputs/   # only when actual raw inputs need preservation
```

```sh
python3 scripts/brief.py check runs/<run_id>/run.json --brief runs/<run_id>/brief.md
```

`run.json` fields:

| Field | Contract |
| --- | --- |
| schema_version | 1 |
| request/context | canonical resolve result, supplemented with actual data limitations |
| research_quality | host judgment: complete, partial or unavailable |
| evidence | unique id, public url, publisher, support excerpt/locator, reference_period, published_at, version_at, retrieved_at, time_precision (instant/date/unknown); null/imprecise publication/version needs time_reason |
| observations | unique id, evidence_ids, entity, market, sample, numeric value or null+missing_reason, unit, currency (null if not applicable), basis, period_start/end; optional calculation and tolerance |
| claims | unique id, kind (fact/inference/hypothesis), section (period/update/outlook), text, reason, evidence_ids, observation_ids, counterevidence_ids or explicit counterevidence_reason; inference/hypothesis needs mechanism; hypothesis also needs trigger, confirmation, invalidation and horizon |
| coverage | area, status (checked/checked_no_change/not_checked/failed); checked states need evidence_ids, missing/failed needs reason |
| execution | capabilities, three bindings and task records as below |
| semantic_review | host declaration status (passed/failed/not_performed) and notes explaining actual review/limits |
| hashes | brief_sha256; helper returns run_input_sha256 excluding hashes/checks |
| checks | optional saved helper result, separate from semantic review |

Optional inference `reaction_end` enables a necessary timing test: the causal
source must have precise publication/version times no later than reaction_end.
It does not prove causality. Support and counterevidence follow the claim's
section boundary, and period claims cannot use later observation endpoints. Date/unknown
source timing emits a semantic-review warning. Out-of-window source versions,
dangling IDs and wrong recomputations fail even when research_quality is partial.

Execution capabilities record source, retrieved_at, scope
(complete/partial/current_session), tools and any actually known candidates and
limitations. Bindings have light/medium/heavy objects with a reason and known
model/effort or null. Task records contain task_id, required_tier, applied_tier,
control (inherited/uncontrolled/host_applied), requested, accepted, actual and
unknown_reason when actual is null. Omitted optional review_previous work does
not imply a prior report exists. Never fabricate execution logs to fill fields.

Compute the body SHA-256 over saved UTF-8 bytes. `check` returns computed hashes
without writing files; the host may save them and checks into run.json and rerun.
The input hash ignores only `hashes` and `checks`, avoiding self-reference. A
stored input hash, when present, must match. Decimal recomputation tolerance
defaults to 1e-8 and cannot exceed 1e-4; rescale the observation correctly rather
than expanding tolerance to hide disagreement.

Successful checks mean structure, recorded time relationships, recomputation and
body hash passed. A semantic review marked passed is an agent declaration,
not a helper finding. Source existence cannot prove textual support, exhaustive
coverage, market interpretation, live routing, delivery or predictive performance.
