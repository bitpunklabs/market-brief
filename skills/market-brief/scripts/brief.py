#!/usr/bin/env python3
"""Deterministic input-only helpers. No network, model client or research verdict."""

import argparse
import hashlib
import json
import re
import sys
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal, InvalidOperation
from itertools import pairwise
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import tomllib

ROOT = Path(__file__).resolve().parents[1]
UTC = timezone.utc
VERSION = 1


def require(condition, message):
    if not condition:
        raise ValueError(message)


def timestamp(value, label="timestamp"):
    require(isinstance(value, str), f"{label}: expected ISO timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None and parsed.utcoffset() is not None,
            f"{label}: timezone offset required")
    return parsed.astimezone(UTC)


def iso(value):
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def number(value, label):
    require(not isinstance(value, bool), f"{label}: boolean is not a number")
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"{label}: invalid number") from exc
    require(result.is_finite(), f"{label}: finite number required")
    return result


def public_url(value):
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def registry():
    with (ROOT / "registry.toml").open("rb") as handle:
        return tomllib.load(handle)


def canonical_request(raw, config):
    require(isinstance(raw, dict), "request must be an object")
    requested_market = raw.get("market", "")
    require(isinstance(requested_market, str), "market must be a string")
    candidates = [key for key, value in config["markets"].items()
                  if requested_market.casefold() in
                  [alias.casefold() for alias in [key, *value["aliases"]]]]
    require(len(candidates) == 1, "market is missing, ambiguous or unsupported")
    market_id = candidates[0]
    market = config["markets"][market_id]
    require(raw.get("cadence") in market["cadences"], "unsupported market/cadence")
    language = raw.get("language") or ("zh-CN" if market_id == "cn_equity" else "en")
    require(isinstance(language, str) and language.strip(), "invalid language")
    allow_updates = raw.get("allow_post_period", False)
    require(isinstance(allow_updates, bool), "allow_post_period must be boolean")
    result = {**raw, "market": market_id, "language": language,
              "scope": raw.get("scope") or market["scope"],
              "allow_post_period": allow_updates}
    require(isinstance(result["scope"], str), "scope must be a string")
    return result, market


def midnight(day, tz):
    return datetime.combine(day, time.min, tz).astimezone(UTC)


def month_start_before(day):
    return (day.replace(day=1) - timedelta(days=1)).replace(day=1)


def next_month(day):
    return (day.replace(day=28) + timedelta(days=4)).replace(day=1)


def period_dates(cadence, target, anchor, week_start):
    if cadence == "monthly":
        if target is not None:
            require(isinstance(target, str) and re.fullmatch(r"\d{4}-\d{2}", target),
                    "monthly target must be YYYY-MM")
            start = date.fromisoformat(target + "-01")
        else:
            start = month_start_before(anchor)
        return start, next_month(start)
    require(cadence == "weekly", "invalid period cadence")
    if target is not None:
        start = date.fromisoformat(target)
        start -= timedelta(days=(start.weekday() - week_start) % 7)
    else:
        start = anchor - timedelta(days=(anchor.weekday() - week_start) % 7 + 7)
    return start, start + timedelta(days=7)


def calendar_sessions(raw, market, now):
    require(isinstance(raw, dict), "calendar must be an object")
    require(public_url(raw.get("source_url")), "calendar needs public source_url")
    require(isinstance(raw.get("support"), str) and raw["support"].strip(),
            "calendar needs source support/locator")
    require(raw.get("timezone") == market["timezone"], "calendar timezone mismatch")
    require(timestamp(raw.get("retrieved_at"), "calendar.retrieved_at") <= now,
            "calendar retrieval is in the future")
    start, end = date.fromisoformat(raw["start_date"]), date.fromisoformat(raw["end_date"])
    require(start <= end, "calendar coverage inverted")
    tz = ZoneInfo(market["timezone"])
    sessions = []
    require(isinstance(raw.get("sessions"), list), "calendar.sessions must be a list")
    for item in raw["sessions"]:
        day = date.fromisoformat(item["date"])
        opening, closing = timestamp(item["open"]), timestamp(item["close"])
        require(start <= day <= end, "session outside calendar coverage")
        require(opening < closing, "session open must precede close")
        require(opening.astimezone(tz).date() == day and closing.astimezone(tz).date() == day,
                "session date does not match local timezone")
        for key in ("open", "close"):
            given = datetime.fromisoformat(item[key].replace("Z", "+00:00"))
            # UTC timestamps are valid; local timestamps must have the actual DST offset.
            require(given.utcoffset() == timedelta(0) or
                    given.utcoffset() == given.astimezone(tz).utcoffset(),
                    "session offset inconsistent with market timezone/DST")
        sessions.append({"date": day, "open": opening, "close": closing})
    sessions.sort(key=lambda item: item["date"])
    require(len({s["date"] for s in sessions}) == len(sessions), "duplicate calendar session")
    require(all(a["close"] < b["open"] for a, b in pairwise(sessions)),
            "calendar sessions overlap")
    return sessions, start, end


def resolve(payload):
    """Resolve only from supplied actual clock and calendar inputs."""
    config = registry()
    request, market = canonical_request(payload.get("request"), config)
    now = timestamp(payload.get("now"), "now")
    explicit_cutoff = timestamp(request["as_of"], "as_of") if request.get("as_of") else None
    require(explicit_cutoff is None or explicit_cutoff <= now, "as_of is in the future")
    cutoff = explicit_cutoff or now
    target = request.get("target")
    tz = ZoneInfo(market["timezone"])
    cadence = request["cadence"]
    inclusive = True
    origin = "explicit" if explicit_cutoff else "current"
    session = None
    calendar_info = None
    calendar_period = None
    price_start = None
    primary_end = None

    def pending(reason):
        return {"schema_version": VERSION, "status": "pending", "reason": reason,
                "request": request, "generated_at": iso(now)}

    sessions = []
    if market["session_type"] == "exchange_calendar":
        if not payload.get("calendar"):
            return pending("sourced session calendar required; no weekday/holiday assumptions made")
        sessions, coverage_start, coverage_end = calendar_sessions(payload["calendar"], market, now)
        calendar_info = dict(payload["calendar"])
        calendar_info["verification"] = "input_validated"

    if cadence == "daily":
        if target is not None:
            start_day = date.fromisoformat(target)
            start = midnight(start_day, tz)
            end = midnight(start_day + timedelta(days=1), tz)
            if end > now:
                return pending("target day is incomplete/future; an explicitly labeled early edition is required")
            if not explicit_cutoff:
                cutoff, origin = end, "period_default"
            require(cutoff >= end, "as_of conflicts with target day")
            require(cutoff == end or request["allow_post_period"],
                    "later as_of needs allow_post_period for a fixed target")
            inclusive = cutoff > end
            primary_end = end
        else:
            start, end = cutoff - timedelta(hours=24), cutoff
        price_start, price_end = start, end
    elif cadence in {"premarket", "postmarket"}:
        if target is not None:
            day = date.fromisoformat(target)
            if not coverage_start <= day <= coverage_end:
                return pending("target date outside calendar coverage")
            candidates = [s for s in sessions if s["date"] == day]
        elif cadence == "premarket":
            if not coverage_start <= cutoff.astimezone(tz).date() <= coverage_end:
                return pending("current date outside calendar coverage")
            candidates = [s for s in sessions if s["open"] > cutoff]
        else:
            if not coverage_start <= cutoff.astimezone(tz).date() <= coverage_end:
                return pending("current date outside calendar coverage")
            candidates = [s for s in reversed(sessions) if s["close"] <= cutoff]
        if not candidates:
            return pending("no matching actual session in supplied calendar")
        session = candidates[0]
        previous = [s for s in sessions if s["date"] < session["date"]]
        if not previous:
            return pending("previous session required to resolve holiday/overnight window")
        previous = previous[-1]
        start = previous["close"]
        if cadence == "premarket":
            if target is not None and not explicit_cutoff and session["open"] <= now:
                cutoff, origin = session["open"], "period_default"
            require(cutoff <= session["open"], "premarket as_of cannot include the target session")
            inclusive = cutoff < session["open"]
            end, price_end = cutoff, previous["close"]
        else:
            if session["close"] > now:
                return pending("target regular session has not completed")
            if target is not None and not explicit_cutoff:
                cutoff, origin = session["close"], "period_default"
            require(cutoff >= session["close"], "postmarket as_of precedes target close")
            if target is not None:
                require(cutoff == session["close"] or request["allow_post_period"],
                        "later as_of needs allow_post_period for a fixed target")
            end, primary_end = session["close"], session["close"]
            price_start, price_end = previous["close"], session["close"]
        require(start < end, "as_of precedes previous close")
    else:
        start_day, end_day = period_dates(cadence, target, cutoff.astimezone(tz).date(), market["week_start"])
        if cadence == "weekly" and market["asset_type"] == "equity" and target is None:
            # Select the newest actual week with every regular session complete,
            # including a holiday-shortened week before the weekend begins.
            start_day += timedelta(days=7)
            end_day += timedelta(days=7)
            if coverage_end < end_day - timedelta(days=1):
                return pending("calendar must cover the current week to determine whether all sessions completed")
            while start_day >= coverage_start:
                week_sessions = [s for s in sessions if start_day <= s["date"] < end_day]
                if week_sessions and week_sessions[-1]["close"] <= cutoff:
                    break
                start_day -= timedelta(days=7)
                end_day -= timedelta(days=7)
        start, end = midnight(start_day, tz), midnight(end_day, tz)
        if end > now and not (cadence == "weekly" and market["asset_type"] == "equity"):
            return pending("target period is incomplete/future; full-period results are unavailable")
        primary_end = end
        if market["session_type"] == "exchange_calendar":
            if coverage_start > start_day or coverage_end < end_day - timedelta(days=1):
                return pending("calendar must cover the entire target period including closed dates")
            in_period = [s for s in sessions if start_day <= s["date"] < end_day]
            if not in_period:
                return pending("target period has no trading sessions; not a completed trading period")
            previous = [s for s in sessions if s["date"] < start_day]
            if not previous:
                return pending("previous regular close required for period price return")
            price_start, price_end = previous[-1]["close"], in_period[-1]["close"]
            primary_end = price_end
            calendar_period = {"start_date": start_day.isoformat(), "end_date_exclusive": end_day.isoformat(),
                               "session_count": len(in_period)}
            if cadence == "weekly":
                start, end = price_start, price_end
                if end > now:
                    return pending("target trading week has regular sessions still to complete")
        else:
            price_start, price_end = start, end
        if target is not None and not explicit_cutoff:
            cutoff, origin = end, "period_default"
        require(cutoff >= end, "as_of precedes the completed target period")
        if target is not None:
            require(cutoff == end or request["allow_post_period"],
                    "later as_of needs allow_post_period for a fixed target")
        inclusive = cutoff > end or (cadence == "weekly" and market["asset_type"] == "equity")

    end_inclusive = cadence == "postmarket" or (cadence in {"daily", "premarket"} and inclusive)
    if cadence == "weekly" and market["asset_type"] == "equity":
        end_inclusive = True
    if cadence == "daily" and target is not None:
        end_inclusive = False
    primary_end = primary_end or end
    primary_inclusive = end_inclusive or (market["asset_type"] == "equity" and cadence == "monthly")
    context = {
        "task_id": f"{request['market']}.{cadence}", "market": request["market"],
        "cadence": cadence, "scope": request["scope"], "language": request["language"],
        "timezone": market["timezone"], "target": target,
        "as_of": iso(cutoff), "as_of_inclusive": inclusive, "cutoff_origin": origin,
        "generated_at": iso(now), "allow_post_period": request["allow_post_period"],
        "period": {"start": iso(start), "end": iso(end),
                   "start_inclusive": cadence not in {"premarket", "postmarket"},
                   "end_inclusive": end_inclusive},
        "primary_cutoff": {"at": iso(primary_end), "inclusive": primary_inclusive},
        "price_window": {"start": iso(price_start) if price_start else None, "end": iso(price_end)},
        "target_session": {key: iso(session[key]) for key in ("open", "close")} if session else None,
        "calendar": calendar_info,
        "calendar_period": calendar_period,
        "historical_reconstruction": origin == "period_default" or bool(target and explicit_cutoff and cutoff < now),
    }
    if cadence == "daily":
        context["forward_window"] = {"start": iso(cutoff), "end_24h": iso(cutoff + timedelta(hours=24)),
                                     "end_72h": iso(cutoff + timedelta(hours=72))}
    return {"schema_version": VERSION, "status": "resolved", "request": request, "context": context}


def calculate(payload):
    operation = payload.get("operation")
    if operation == "return":
        start, end = number(payload.get("start"), "start"), number(payload.get("end"), "end")
        require(start > 0 and end >= 0, "return requires start > 0 and end >= 0")
        result = end / start - 1
    elif operation == "compound":
        returns = payload.get("returns")
        require(isinstance(returns, list) and returns, "nonempty decimal returns required")
        result = Decimal(1)
        for value in returns:
            value = number(value, "return")
            require(value >= -1, "return cannot be less than -1")
            result *= 1 + value
        result -= 1
    elif operation == "daily_average":
        require(payload.get("measure_type") == "flow", "daily average requires a flow, not a stock")
        days = number(payload.get("days"), "days")
        require(days > 0, "days must be positive")
        result = number(payload.get("total"), "total") / days
    else:
        raise ValueError("unsupported operation; use return, compound or daily_average")
    return {"operation": operation, "value": str(result),
            "unit": "decimal_return" if operation != "daily_average" else payload.get("unit"),
            "inputs": payload}


def canonical_hash(payload):
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def check(run, brief_bytes):
    """Check recorded inputs; accumulate failures without creating a quality verdict."""
    errors, warnings = [], []

    def record_error(path, message):
        errors.append({"path": path, "message": message})

    def expect(condition, path, message):
        if not condition:
            record_error(path, message)

    def parsed(value, path):
        try:
            return timestamp(value, path)
        except (ValueError, TypeError) as exc:
            record_error(path, str(exc))
            return None

    expect(run.get("schema_version") == VERSION, "schema_version", "unsupported version")
    expect(run.get("research_quality") in {"complete", "partial", "unavailable"},
           "research_quality", "semantic quality declaration required")
    context = run.get("context", {})
    expect(isinstance(context, dict), "context", "object required")
    if not isinstance(context, dict):
        context = {}
    cutoff = parsed(context.get("as_of"), "context.as_of")
    generated = parsed(context.get("generated_at"), "context.generated_at")
    expect(cutoff is None or generated is None or cutoff <= generated,
           "context", "as_of cannot follow generation")
    for key in ("as_of_inclusive", "allow_post_period"):
        expect(isinstance(context.get(key), bool), f"context.{key}", "boolean required")
    primary = context.get("primary_cutoff", {})
    expect(isinstance(primary, dict), "context.primary_cutoff", "object required")
    primary = primary if isinstance(primary, dict) else {}
    primary_time = parsed(primary.get("at"), "context.primary_cutoff.at")
    expect(isinstance(primary.get("inclusive"), bool), "context.primary_cutoff.inclusive", "boolean required")
    expect(cutoff is None or primary_time is None or primary_time <= cutoff,
           "context.primary_cutoff", "primary cutoff exceeds global cutoff")
    period = context.get("period", {})
    if not isinstance(period, dict):
        record_error("context.period", "object required")
        period = {}
    period_start = parsed(period.get("start"), "context.period.start")
    period_end = parsed(period.get("end"), "context.period.end")
    expect(period_start is None or period_end is None or period_start < period_end,
           "context.period", "period must be increasing")
    expect(period_end is None or cutoff is None or period_end <= cutoff,
           "context.period", "period exceeds cutoff")
    for key in ("start_inclusive", "end_inclusive"):
        expect(isinstance(period.get(key), bool), "context.period." + key, "boolean required")
    price_window = context.get("price_window", {})
    if not isinstance(price_window, dict):
        record_error("context.price_window", "object required")
        price_window = {}
    price_end = parsed(price_window.get("end"), "context.price_window.end")
    price_start = parsed(price_window["start"], "context.price_window.start") if price_window.get("start") else None
    expect(price_start is None or price_end is None or price_start < price_end,
           "context.price_window", "price endpoints inverted")
    expect(price_end is None or cutoff is None or price_end <= cutoff,
           "context.price_window", "price endpoint exceeds cutoff")
    try:
        request, market = canonical_request(run.get("request"), registry())
        for key in ("market", "cadence", "scope", "language", "allow_post_period"):
            expect(context.get(key) == request.get(key), f"context.{key}", "request/context mismatch")
        expect(context.get("task_id") == f"{request['market']}.{request['cadence']}",
               "context.task_id", "task ID mismatch")
        expect(context.get("timezone") == market["timezone"], "context.timezone", "market timezone mismatch")
        if market["asset_type"] == "equity":
            expect(isinstance(context.get("calendar"), dict), "context.calendar", "equity calendar record required")
    except (ValueError, KeyError, TypeError) as exc:
        record_error("request", str(exc))

    def collection(name):
        values = run.get(name)
        expect(isinstance(values, list), name, "list required")
        result = {}
        for index, item in enumerate(values if isinstance(values, list) else []):
            path = f"{name}[{index}]"
            if not isinstance(item, dict):
                record_error(path, "object required")
                continue
            identifier = item.get("id")
            if not isinstance(identifier, str) or not identifier:
                record_error(path + ".id", "nonempty ID required")
                continue
            if identifier in result:
                record_error(path + ".id", "duplicate ID")
            result[identifier] = item
        return result

    evidence = collection("evidence")
    observations = collection("observations")
    claims = collection("claims")
    availability = {}
    for eid, item in evidence.items():
        path = f"evidence.{eid}"
        expect(public_url(item.get("url")), path + ".url", "public http(s) URL required")
        for key in ("publisher", "support", "reference_period"):
            expect(isinstance(item.get(key), str) and bool(item[key].strip()), path + "." + key,
                   "nonempty source field required")
        publication = parsed(item.get("published_at"), path + ".published_at") if item.get("published_at") else None
        version = parsed(item.get("version_at"), path + ".version_at") if item.get("version_at") else None
        retrieved = parsed(item.get("retrieved_at"), path + ".retrieved_at")
        precision = item.get("time_precision")
        expect(precision in {"instant", "date", "unknown"}, path + ".time_precision", "invalid precision")
        if precision != "instant" or publication is None or version is None:
            expect(bool(item.get("time_reason")), path + ".time_reason", "missing/imprecise time needs a reason")
            warnings.append({"path": path, "message": "historical availability needs semantic review"})
        if publication and version:
            expect(version >= publication, path + ".version_at", "version cannot precede first publication")
        if retrieved:
            expect(generated is None or retrieved <= generated, path + ".retrieved_at", "retrieval exceeds generation")
            expect(publication is None or publication <= retrieved, path, "publication follows retrieval")
            expect(version is None or version <= retrieved, path, "version follows retrieval")
        latest = max([v for v in (publication, version) if v is not None], default=None)
        availability[eid] = latest
        if latest and cutoff:
            expect(latest < cutoff or (context.get("as_of_inclusive") is True and latest == cutoff),
                   path, "source became available after/excluded at cutoff")

    def references(item, key, known, path, nonempty=False):
        ids = item.get(key)
        expect(isinstance(ids, list), path + "." + key, "reference list required")
        ids = ids if isinstance(ids, list) else []
        if nonempty:
            expect(bool(ids), path + "." + key, "support reference required")
        for identifier in ids:
            expect(isinstance(identifier, str) and identifier in known, path + "." + key,
                   f"unknown reference {identifier!r}")
        return [identifier for identifier in ids if isinstance(identifier, str) and identifier in known]

    observation_sources = {}
    for oid, item in observations.items():
        path = f"observations.{oid}"
        observation_sources[oid] = references(item, "evidence_ids", evidence, path, True)
        for key in ("entity", "market", "sample", "unit", "basis"):
            expect(isinstance(item.get(key), str) and bool(item[key].strip()), path + "." + key,
                   "nonempty observation field required")
        expect("currency" in item, path + ".currency", "currency field required (null when not applicable)")
        start = parsed(item.get("period_start"), path + ".period_start")
        end = parsed(item.get("period_end"), path + ".period_end")
        expect(start is None or end is None or start <= end, path, "measurement period inverted")
        expect(end is None or cutoff is None or end <= cutoff, path, "measurement period exceeds cutoff")
        if item.get("value") is None:
            expect(bool(item.get("missing_reason")), path + ".missing_reason", "null needs missing reason")
        else:
            try:
                number(item["value"], path + ".value")
            except ValueError as exc:
                record_error(path + ".value", str(exc))
        if item.get("calculation") is not None:
            try:
                expected = number(calculate(item["calculation"])["value"], "calculated value")
                actual = number(item.get("value"), "recorded value")
                tolerance = number(item.get("tolerance", "0.00000001"), "tolerance")
                expect(0 <= tolerance <= Decimal("0.0001"), path + ".tolerance", "tolerance outside [0, 0.0001]")
                expect(abs(expected - actual) <= tolerance, path + ".value", "recomputed value mismatch")
            except (ValueError, AttributeError, TypeError) as exc:
                record_error(path + ".calculation", str(exc))

    for cid, item in claims.items():
        path = f"claims.{cid}"
        expect(item.get("kind") in {"fact", "inference", "hypothesis"}, path + ".kind", "invalid claim kind")
        for key in ("text", "reason"):
            expect(isinstance(item.get(key), str) and bool(item[key].strip()), path + "." + key, "nonempty field required")
        eids = references(item, "evidence_ids", evidence, path)
        oids = references(item, "observation_ids", observations, path)
        counter_ids = references(item, "counterevidence_ids", evidence, path)
        expect(bool(eids or oids), path, "claim needs evidence or observation support")
        expect(bool(item.get("counterevidence_ids") or item.get("counterevidence_reason")),
               path, "counterevidence or explicit search limitation required")
        if item.get("kind") in {"inference", "hypothesis"}:
            expect(bool(item.get("mechanism")), path + ".mechanism", "mechanism required")
        if item.get("kind") == "hypothesis":
            for key in ("trigger", "confirmation", "invalidation", "horizon"):
                expect(bool(item.get(key)), path + "." + key, "conditional outlook field required")
        section = item.get("section")
        expect(section in {"period", "update", "outlook"}, path + ".section", "invalid claim section")
        if section == "update":
            expect(context.get("allow_post_period") is True, path, "post-period updates not allowed")
        sources = set(eids)
        for oid in oids:
            sources.update(observation_sources[oid])
        support_sources = set(sources)
        sources.update(counter_ids)
        boundary = primary_time if section == "period" else cutoff
        allowed_equal = primary.get("inclusive") if section == "period" else context.get("as_of_inclusive")
        for eid in sources:
            available = availability[eid]
            if available and boundary:
                expect(available < boundary or (allowed_equal is True and available == boundary),
                       path, f"{eid} became available outside this claim's information boundary")
        if section == "period":
            for oid in oids:
                observed_end = parsed(observations[oid].get("period_end"), path + ".observation_period_end")
                expect(observed_end is None or boundary is None or observed_end <= boundary,
                       path, "observation exceeds this claim's period boundary")
        if item.get("kind") == "inference" and item.get("reaction_end"):
            reaction_end = parsed(item["reaction_end"], path + ".reaction_end")
            expect(reaction_end is None or cutoff is None or reaction_end <= cutoff,
                   path + ".reaction_end", "reaction exceeds cutoff")
            for eid in support_sources:
                expect(evidence[eid].get("time_precision") == "instant" and
                       evidence[eid].get("published_at") is not None and evidence[eid].get("version_at") is not None,
                       path, "intraday attribution needs precise publication/version times")
                if availability[eid] and reaction_end:
                    expect(availability[eid] <= reaction_end, path, "later source cannot explain earlier reaction")

    coverage = run.get("coverage")
    expect(isinstance(coverage, list) and bool(coverage), "coverage", "nonempty coverage plan required")
    coverage_ids = set()
    for index, item in enumerate(coverage if isinstance(coverage, list) else []):
        path = f"coverage[{index}]"
        if not isinstance(item, dict):
            record_error(path, "object required")
            continue
        identifier = item.get("area")
        expect(isinstance(identifier, str) and bool(identifier), path + ".area", "area required")
        if isinstance(identifier, str):
            expect(identifier not in coverage_ids, path + ".area", "duplicate coverage area")
            coverage_ids.add(identifier)
        status = item.get("status")
        expect(status in {"checked", "checked_no_change", "not_checked", "failed"}, path + ".status", "invalid status")
        if status in {"not_checked", "failed"}:
            expect(bool(item.get("reason")), path + ".reason", "gap reason required")
            expect(run.get("research_quality") != "complete", path, "complete quality conflicts with coverage gap")
        else:
            references(item, "evidence_ids", evidence, path, True)

    execution = run.get("execution")
    if not isinstance(execution, dict):
        record_error("execution", "execution record required")
        execution = {}
    capability = execution.get("capabilities", {})
    expect(isinstance(capability, dict), "execution.capabilities", "object required")
    capability = capability if isinstance(capability, dict) else {}
    expect(capability.get("scope") in {"complete", "partial", "current_session"},
           "execution.capabilities.scope", "observable capability scope required")
    expect(bool(capability.get("source")), "execution.capabilities.source", "source required")
    if capability.get("retrieved_at"):
        observed_at = parsed(capability["retrieved_at"], "execution.capabilities.retrieved_at")
        expect(observed_at is None or generated is None or observed_at <= generated,
               "execution.capabilities.retrieved_at", "capability retrieval exceeds generation")
    else:
        record_error("execution.capabilities.retrieved_at", "timestamp required")
    expect(isinstance(capability.get("tools"), list), "execution.capabilities.tools", "visible tools list required")
    bindings = execution.get("bindings", {})
    if not isinstance(bindings, dict):
        record_error("execution.bindings", "object required")
        bindings = {}
    for tier in registry()["tiers"]:
        binding = bindings.get(tier)
        expect(isinstance(binding, dict) and bool(binding.get("reason")), f"execution.bindings.{tier}", "binding and reason required")
    tasks = execution.get("tasks")
    expect(isinstance(tasks, list), "execution.tasks", "task records list required")
    tier_for = {task: tier for tier, names in registry()["tiers"].items() for task in names}
    ranks = {"light": 0, "medium": 1, "heavy": 2}
    for index, task in enumerate(tasks if isinstance(tasks, list) else []):
        path = f"execution.tasks[{index}]"
        if not isinstance(task, dict):
            record_error(path, "object required")
            continue
        required_tier = tier_for.get(task.get("task_id"))
        expect(required_tier is not None, path + ".task_id", "unknown research task")
        expect(task.get("required_tier") == required_tier, path, "tier differs from registry")
        applied = task.get("applied_tier")
        expect(applied in ranks and required_tier in ranks and ranks.get(applied, -1) >= ranks.get(required_tier, 3),
               path + ".applied_tier", "task requirement cannot be downgraded")
        expect(task.get("control") in {"inherited", "uncontrolled", "host_applied"}, path + ".control", "invalid control")
        for key in ("requested", "accepted", "actual"):
            expect(key in task, path + "." + key, "configuration result required (null if unknown)")
        if task.get("actual") is None:
            expect(bool(task.get("unknown_reason")), path + ".unknown_reason", "unobservable execution needs a reason")

    semantic = run.get("semantic_review", {})
    expect(isinstance(semantic, dict), "semantic_review", "object required")
    semantic = semantic if isinstance(semantic, dict) else {}
    expect(semantic.get("status") in {"passed", "failed", "not_performed"}, "semantic_review.status", "separate semantic review declaration required")
    if run.get("research_quality") == "complete":
        expect(semantic.get("status") == "passed", "semantic_review", "complete research needs a recorded semantic review")
        expect(bool(evidence and claims), "research_quality", "complete research needs evidence and claims")
    expect(bool(semantic.get("notes")), "semantic_review.notes", "review findings/limitations required")
    expected_hash = run.get("hashes", {}).get("brief_sha256") if isinstance(run.get("hashes"), dict) else None
    actual_hash = hashlib.sha256(brief_bytes).hexdigest()
    expect(expected_hash == actual_hash, "hashes.brief_sha256", "missing or mismatched body hash")
    body = brief_bytes.decode("utf-8")
    expect(bool(body.strip()), "brief.md", "empty report")
    expect(not re.search(r"(?:turn\d+(?:search|view|fetch)\d+|navlist||)", body),
           "brief.md", "internal citation syntax must be exported to public Markdown links")
    for link in re.findall(r"\]\((https?://[^\s)]+)\)", body):
        expect(link in {e.get("url") for e in evidence.values()}, "brief.md", "source link missing from evidence record")
    input_hash = canonical_hash({key: value for key, value in run.items() if key not in {"checks", "hashes"}})
    stored_input_hash = run.get("hashes", {}).get("run_input_sha256") if isinstance(run.get("hashes"), dict) else None
    if stored_input_hash is not None:
        expect(stored_input_hash == input_hash, "hashes.run_input_sha256", "research input hash mismatch")
    return {"status": "passed" if not errors else "failed", "errors": errors, "warnings": warnings,
            "hashes": {"brief_sha256": actual_hash, "run_input_sha256": input_hash},
            "scope": "structure, recorded time boundaries, calculations and body hash only; semantic review is a host declaration"}


def read_json(path):
    text = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
    result = json.loads(text, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"nonfinite JSON: {value}")))
    require(isinstance(result, dict), "input JSON must be an object")
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    for command in ("resolve", "calculate", "check"):
        sub = subs.add_parser(command)
        sub.add_argument("input", help="JSON file or - for stdin")
        if command == "check":
            sub.add_argument("--brief", required=True, help="saved Markdown report")
    args = parser.parse_args(argv)
    try:
        payload = read_json(args.input)
        if args.command == "resolve":
            result = resolve(payload)
        elif args.command == "calculate":
            result = calculate(payload)
        else:
            result = check(payload, Path(args.brief).read_bytes())
        print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
        return 2 if result.get("status") == "pending" else int(result.get("status") == "failed")
    except (ValueError, KeyError, TypeError, AttributeError, OSError, OverflowError) as exc:
        print(json.dumps({"status": "invalid", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
