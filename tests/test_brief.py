"""Synthetic boundary cases; these do not validate live calendars or research."""

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills/market-brief/scripts/brief.py"
SPEC = importlib.util.spec_from_file_location("brief", SCRIPT)
brief = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(brief)


def crypto_request(cadence="daily", **kwargs):
    return {"now": "2026-10-07T15:40:00Z", "request": {"market": "crypto", "cadence": cadence, **kwargs}}


def calendar(market, sessions, start="2026-09-25", end="2026-10-12"):
    return {"source_url": "https://example.org/calendar", "support": "Synthetic test schedule, not a live exchange calendar",
            "retrieved_at": "2026-10-07T00:00:00Z", "start_date": start, "end_date": end,
            "timezone": brief.registry()["markets"][market]["timezone"], "sessions": sessions}


def cn_session(day):
    return {"date": day, "open": day + "T09:30:00+08:00", "close": day + "T15:00:00+08:00"}


def fixture():
    resolved = brief.resolve(crypto_request(target="2026-10-05"))
    body = b"# Synthetic report\n\nObserved price change. [Test source](https://example.org/price)\n"
    source = {"id": "price", "url": "https://example.org/price", "publisher": "Test fixture",
              "support": "Synthetic prices 100 at start and 110 at endpoint", "reference_period": "2026-10-05",
              "published_at": "2026-10-05T23:59:00Z", "version_at": "2026-10-05T23:59:00Z",
              "retrieved_at": "2026-10-07T00:00:00Z", "time_precision": "instant"}
    observation = {"id": "return", "evidence_ids": ["price"], "entity": "Synthetic BTC spot",
                   "market": "crypto", "sample": "one synthetic instrument", "value": "0.1",
                   "unit": "decimal_return", "currency": "USD", "basis": "price return, synthetic endpoints",
                   "period_start": "2026-10-05T00:00:00Z", "period_end": "2026-10-06T00:00:00Z",
                   "calculation": {"operation": "return", "start": "100", "end": "110"}}
    claim = {"id": "observed", "kind": "fact", "section": "period", "text": "Synthetic price rose 10%.",
             "reason": "Return recomputed from fixture inputs", "evidence_ids": [], "observation_ids": ["return"],
             "counterevidence_ids": [], "counterevidence_reason": "Arithmetic fixture; no market interpretation asserted"}
    run = {"schema_version": 1, "request": resolved["request"], "context": resolved["context"],
           "research_quality": "partial", "evidence": [source], "observations": [observation], "claims": [claim],
           "coverage": [{"area": "benchmark fixture", "status": "checked", "evidence_ids": ["price"]},
                        {"area": "macro", "status": "not_checked", "reason": "Synthetic test only"}],
           "execution": {"capabilities": {"source": "test harness", "scope": "current_session",
                                          "retrieved_at": "2026-10-07T00:00:00Z", "tools": []},
                         "bindings": {tier: {"model": None, "effort": None, "reason": "Synthetic test, no model execution"}
                                      for tier in ("light", "medium", "heavy")}, "tasks": []},
           "semantic_review": {"status": "not_performed", "notes": "No real market research in fixture"},
           "hashes": {"brief_sha256": hashlib.sha256(body).hexdigest()}}
    return run, body


class ResolutionTests(unittest.TestCase):
    def test_registry_preserves_eleven_task_combinations(self):
        config = brief.registry()
        self.assertEqual(sum(len(m["cadences"]) for m in config["markets"].values()), 11)
        self.assertEqual({t for tasks in config["tiers"].values() for t in tasks},
                         {"resolve", "coverage", "discover", "extract", "verify", "analyze", "review_previous", "outlook", "write", "format", "review"})

    def test_late_crypto_snapshot_looks_ahead_from_actual_cutoff(self):
        payload = crypto_request(as_of="2026-10-06T23:40:00Z")
        ctx = brief.resolve(payload)["context"]
        self.assertEqual(ctx["period"]["start"], "2026-10-05T23:40:00Z")
        self.assertEqual(ctx["forward_window"]["end_24h"], "2026-10-07T23:40:00Z")
        self.assertEqual(ctx["forward_window"]["end_72h"], "2026-10-09T23:40:00Z")

    def test_crypto_historical_day_is_end_exclusive(self):
        ctx = brief.resolve(crypto_request(target="2026-10-05"))["context"]
        self.assertEqual(ctx["as_of"], "2026-10-06T00:00:00Z")
        self.assertEqual(ctx["cutoff_origin"], "period_default")
        self.assertFalse(ctx["period"]["end_inclusive"])
        self.assertTrue(ctx["historical_reconstruction"])

    def test_crypto_week_includes_weekend(self):
        ctx = brief.resolve(crypto_request("weekly"))["context"]
        self.assertEqual(ctx["period"]["start"], "2026-09-28T00:00:00Z")
        self.assertEqual(ctx["period"]["end"], "2026-10-05T00:00:00Z")
        self.assertFalse(ctx["period"]["end_inclusive"])

    def test_month_end_and_leap_day(self):
        for target, end in [("2024-02", "2024-03-01T00:00:00Z"), ("2025-12", "2026-01-01T00:00:00Z")]:
            with self.subTest(target=target):
                self.assertEqual(brief.resolve(crypto_request("monthly", target=target))["context"]["as_of"], end)

    def test_language_override_does_not_change_window(self):
        a = brief.resolve(crypto_request())["context"]
        b = brief.resolve(crypto_request(language="zh-CN"))["context"]
        self.assertEqual(a["period"], b["period"])
        self.assertEqual(a["language"], "en")
        self.assertEqual(b["language"], "zh-CN")

    def test_missing_equity_calendar_is_pending(self):
        result = brief.resolve({"now": "2026-10-07T00:00:00Z", "request": {"market": "A股", "cadence": "premarket"}})
        self.assertEqual(result["status"], "pending")
        self.assertEqual(result["request"]["language"], "zh-CN")

    def test_cn_long_holiday_window(self):
        payload = {"now": "2026-10-07T15:40:00Z", "request": {"market": "cn", "cadence": "premarket"},
                   "calendar": calendar("cn_equity", [cn_session("2026-09-30"), cn_session("2026-10-08")])}
        ctx = brief.resolve(payload)["context"]
        self.assertEqual(ctx["period"]["start"], "2026-09-30T07:00:00Z")
        self.assertEqual(ctx["target_session"]["open"], "2026-10-08T01:30:00Z")
        self.assertEqual(ctx["calendar"]["verification"], "input_validated")

    def test_explicit_premarket_after_open_stays_on_requested_day(self):
        payload = {"now": "2026-10-07T15:40:00Z", "request": {"market": "cn", "cadence": "premarket", "target": "2026-09-30"},
                   "calendar": calendar("cn_equity", [cn_session("2026-09-29"), cn_session("2026-09-30"), cn_session("2026-10-08")])}
        ctx = brief.resolve(payload)["context"]
        self.assertEqual(ctx["as_of"], "2026-09-30T01:30:00Z")
        self.assertFalse(ctx["as_of_inclusive"])
        payload["request"]["as_of"] = "2026-09-30T02:00:00Z"
        with self.assertRaisesRegex(ValueError, "premarket as_of"):
            brief.resolve(payload)

    def test_us_dst_and_early_close(self):
        sessions = [{"date": "2026-03-06", "open": "2026-03-06T09:30:00-05:00", "close": "2026-03-06T16:00:00-05:00"},
                    {"date": "2026-03-09", "open": "2026-03-09T09:30:00-04:00", "close": "2026-03-09T13:00:00-04:00"}]
        payload = {"now": "2026-10-07T15:40:00Z", "request": {"market": "us", "cadence": "postmarket", "target": "2026-03-09"},
                   "calendar": calendar("us_equity", sessions, "2026-03-01", "2026-03-10")}
        ctx = brief.resolve(payload)["context"]
        self.assertEqual(ctx["target_session"]["open"], "2026-03-09T13:30:00Z")
        self.assertEqual(ctx["price_window"]["end"], "2026-03-09T17:00:00Z")
        payload["calendar"]["sessions"][1]["open"] = "2026-03-09T09:30:00-05:00"
        with self.assertRaisesRegex(ValueError, "DST"):
            brief.resolve(payload)

    def test_fully_closed_equity_week_is_not_trading_week(self):
        payload = {"now": "2026-10-07T15:40:00Z", "request": {"market": "cn", "cadence": "weekly", "target": "2026-09-28"},
                   "calendar": calendar("cn_equity", [cn_session("2026-09-25"), cn_session("2026-10-08")])}
        self.assertIn("no trading sessions", brief.resolve(payload)["reason"])

    def test_short_equity_week_keeps_full_news_interval(self):
        payload = {"now": "2026-10-07T15:40:00Z", "request": {"market": "cn", "cadence": "weekly", "target": "2026-09-28"},
                   "calendar": calendar("cn_equity", [cn_session("2026-09-25"), cn_session("2026-09-28"), cn_session("2026-09-30")])}
        ctx = brief.resolve(payload)["context"]
        self.assertEqual(ctx["price_window"], {"start": "2026-09-25T07:00:00Z", "end": "2026-09-30T07:00:00Z"})
        self.assertEqual(ctx["period"]["end"], "2026-09-30T07:00:00Z")
        self.assertEqual(ctx["as_of"], "2026-09-30T07:00:00Z")
        self.assertTrue(ctx["as_of_inclusive"])
        self.assertEqual(ctx["calendar_period"]["session_count"], 2)

    def test_latest_equity_week_is_ready_at_last_actual_close(self):
        payload = {"now": "2026-10-07T15:40:00Z", "request": {"market": "cn", "cadence": "weekly"},
                   "calendar": calendar("cn_equity", [cn_session("2026-09-25"), cn_session("2026-09-30"), cn_session("2026-10-07")])}
        ctx = brief.resolve(payload)["context"]
        self.assertEqual(ctx["price_window"]["end"], "2026-10-07T07:00:00Z")
        self.assertEqual(ctx["calendar_period"]["start_date"], "2026-10-05")

    def test_unfinished_and_closed_default_weeks_select_last_actual_complete_week(self):
        payload = {"now": "2026-10-07T15:40:00Z", "request": {"market": "cn", "cadence": "weekly"},
                   "calendar": calendar("cn_equity", [cn_session("2026-09-25"), cn_session("2026-09-30"), cn_session("2026-10-08")])}
        self.assertEqual(brief.resolve(payload)["context"]["price_window"]["end"], "2026-09-30T07:00:00Z")
        payload["calendar"]["sessions"].pop()
        self.assertEqual(brief.resolve(payload)["context"]["price_window"]["end"], "2026-09-30T07:00:00Z")

    def test_month_news_cutoff_and_price_attribution_boundary_are_separate(self):
        payload = {"now": "2026-10-07T15:40:00Z", "request": {"market": "cn", "cadence": "monthly", "target": "2026-09"},
                   "calendar": calendar("cn_equity", [cn_session("2026-08-31"), cn_session("2026-09-30")], "2026-08-28", "2026-10-12")}
        ctx = brief.resolve(payload)["context"]
        self.assertEqual(ctx["as_of"], "2026-09-30T16:00:00Z")
        self.assertEqual(ctx["primary_cutoff"], {"at": "2026-09-30T07:00:00Z", "inclusive": True})

    def test_calendar_coverage_and_previous_session_required(self):
        payload = {"now": "2026-10-07T15:40:00Z", "request": {"market": "cn", "cadence": "weekly", "target": "2026-09-28"},
                   "calendar": calendar("cn_equity", [cn_session("2026-09-30")], "2026-09-30", "2026-10-12")}
        self.assertEqual(brief.resolve(payload)["status"], "pending")
        payload["request"] = {"market": "cn", "cadence": "premarket", "target": "2026-09-30"}
        self.assertIn("previous session", brief.resolve(payload)["reason"])

    def test_duplicate_calendar_date_rejected(self):
        payload = {"now": "2026-10-07T15:40:00Z", "request": {"market": "cn", "cadence": "premarket"},
                   "calendar": calendar("cn_equity", [cn_session("2026-09-30")] * 2)}
        with self.assertRaisesRegex(ValueError, "duplicate"):
            brief.resolve(payload)

    def test_invalid_inputs_do_not_silently_substitute(self):
        for request in [{"market": "crypto", "cadence": "premarket"}, {"market": "hk", "cadence": "weekly"},
                        {"market": "crypto", "cadence": "daily", "as_of": "2026-10-06T00:00:00"},
                        {"market": "crypto", "cadence": "daily", "as_of": "2026-10-08T00:00:00Z"}]:
            with self.subTest(request=request), self.assertRaises(ValueError):
                brief.resolve({"now": "2026-10-07T15:40:00Z", "request": request})

    def test_future_completed_period_pending(self):
        self.assertEqual(brief.resolve(crypto_request("monthly", target="2026-10"))["status"], "pending")
        self.assertEqual(brief.resolve(crypto_request(target="2026-10-08"))["status"], "pending")

    def test_explicit_period_updates_need_permission_and_keep_exclusive_end(self):
        payload = crypto_request(target="2026-10-05", as_of="2026-10-06T01:00:00Z")
        with self.assertRaisesRegex(ValueError, "allow_post_period"):
            brief.resolve(payload)
        payload["request"]["allow_post_period"] = True
        ctx = brief.resolve(payload)["context"]
        self.assertFalse(ctx["primary_cutoff"]["inclusive"])
        self.assertTrue(ctx["as_of_inclusive"])


class CalculationTests(unittest.TestCase):
    def test_compounds_gap_and_intraday_returns(self):
        self.assertEqual(brief.calculate({"operation": "compound", "returns": ["0.1", "-0.1"]})["value"], "-0.01")

    def test_return_from_endpoints(self):
        self.assertEqual(brief.calculate({"operation": "return", "start": "100", "end": "110"})["value"], "0.1")

    def test_daily_average_flow_not_stock(self):
        self.assertEqual(brief.calculate({"operation": "daily_average", "total": 310, "days": 31, "measure_type": "flow"})["value"], "10")
        with self.assertRaisesRegex(ValueError, "not a stock"):
            brief.calculate({"operation": "daily_average", "total": 310, "days": 31, "measure_type": "stock"})

    def test_nonfinite_boolean_zero_base_invalid(self):
        for value in ["NaN", "Infinity", True, None, 0]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                brief.calculate({"operation": "return", "start": value, "end": 10})


class RecordTests(unittest.TestCase):
    def assert_failure(self, run, body, message):
        result = brief.check(run, body)
        self.assertEqual(result["status"], "failed")
        self.assertTrue(any(message in e["message"] for e in result["errors"]), result)

    def test_valid_synthetic_record_and_hash_stability(self):
        run, body = fixture()
        result = brief.check(run, body)
        self.assertEqual(result["status"], "passed", result)
        run["hashes"].update(result["hashes"])
        run["checks"] = result
        self.assertEqual(brief.check(run, body)["hashes"]["run_input_sha256"], result["hashes"]["run_input_sha256"])

    def test_hash_detects_changed_body_and_inputs(self):
        run, body = fixture()
        self.assert_failure(run, body + b"changed", "body hash")
        run["hashes"].update(brief.check(run, body)["hashes"])
        run["claims"][0]["text"] = "changed"
        self.assert_failure(run, body, "input hash")

    def test_revised_page_and_excluded_boundary_rejected(self):
        for version in ["2026-10-06T00:00:00Z", "2026-10-06T01:00:00Z"]:
            with self.subTest(version=version):
                run, body = fixture()
                run["evidence"][0]["version_at"] = version
                self.assert_failure(run, body, "cutoff")

    def test_post_period_source_cannot_enter_period_claim_via_observation(self):
        run, body = fixture()
        resolved = brief.resolve(crypto_request(target="2026-10-05", as_of="2026-10-06T01:00:00Z", allow_post_period=True))
        run.update({"request": resolved["request"], "context": resolved["context"]})
        run["evidence"][0].update({"published_at": "2026-10-06T00:30:00Z", "version_at": "2026-10-06T00:30:00Z"})
        self.assert_failure(run, body, "claim's information boundary")
        run["claims"][0]["section"] = "update"
        self.assertEqual(brief.check(run, body)["status"], "passed")

    def test_later_news_cannot_explain_earlier_reaction(self):
        run, body = fixture()
        run["claims"][0].update({"kind": "inference", "mechanism": "Synthetic mechanism", "reaction_end": "2026-10-05T20:00:00Z"})
        self.assert_failure(run, body, "earlier reaction")

    def test_counterevidence_obeys_the_same_period_boundary(self):
        run, body = fixture()
        resolved = brief.resolve(crypto_request(target="2026-10-05", as_of="2026-10-06T01:00:00Z", allow_post_period=True))
        run.update({"request": resolved["request"], "context": resolved["context"]})
        later = copy.deepcopy(run["evidence"][0])
        later.update({"id": "later", "published_at": "2026-10-06T00:30:00Z", "version_at": "2026-10-06T00:30:00Z"})
        run["evidence"].append(later)
        run["claims"][0]["counterevidence_ids"] = ["later"]
        self.assert_failure(run, body, "claim's information boundary")

    def test_later_measurement_cannot_enter_period_claim(self):
        run, body = fixture()
        resolved = brief.resolve(crypto_request(target="2026-10-05", as_of="2026-10-06T01:00:00Z", allow_post_period=True))
        run.update({"request": resolved["request"], "context": resolved["context"]})
        run["observations"][0]["period_end"] = "2026-10-06T00:30:00Z"
        self.assert_failure(run, body, "claim's period boundary")

    def test_unknown_and_date_precision_cannot_certify_intraday_causality(self):
        run, body = fixture()
        run["evidence"][0].update({"time_precision": "date", "time_reason": "Only calendar date available"})
        run["claims"][0].update({"kind": "inference", "mechanism": "Synthetic", "reaction_end": "2026-10-05T23:59:59Z"})
        self.assert_failure(run, body, "precise publication")

    def test_missing_support_duplicate_and_unknown_reference(self):
        for change in ("duplicate", "unknown", "support"):
            with self.subTest(change=change):
                run, body = fixture()
                if change == "duplicate":
                    run["evidence"].append(copy.deepcopy(run["evidence"][0]))
                elif change == "unknown":
                    run["claims"][0]["observation_ids"] = ["missing"]
                else:
                    run["evidence"][0]["support"] = ""
                self.assertEqual(brief.check(run, body)["status"], "failed")

    def test_recompute_rejects_wrong_return(self):
        run, body = fixture()
        run["observations"][0]["value"] = "0.2"
        self.assert_failure(run, body, "recomputed value")

    def test_null_observation_needs_reason(self):
        run, body = fixture()
        run["observations"][0].update({"value": None, "calculation": None})
        self.assert_failure(run, body, "null needs missing reason")

    def test_partial_does_not_excuse_unknown_reference(self):
        run, body = fixture()
        run["observations"][0]["evidence_ids"] = ["missing"]
        self.assert_failure(run, body, "unknown reference")

    def test_complete_cannot_have_coverage_gaps_or_unreviewed_semantics(self):
        run, body = fixture()
        run["research_quality"] = "complete"
        self.assert_failure(run, body, "coverage gap")
        self.assert_failure(run, body, "semantic review")

    def test_structural_success_does_not_certify_semantic_support(self):
        run, body = fixture()
        run["claims"][0]["text"] = "An unsupported economic interpretation is still a host review responsibility."
        self.assertEqual(brief.check(run, body)["status"], "passed")
        self.assertEqual(run["semantic_review"]["status"], "not_performed")

    def test_inherited_and_unobservable_model_is_recorded_honestly(self):
        run, body = fixture()
        run["execution"]["tasks"] = [{"task_id": "verify", "required_tier": "heavy", "applied_tier": "heavy",
                                       "control": "inherited", "requested": None, "accepted": None, "actual": None,
                                       "unknown_reason": "Synthetic fixture; no model called"}]
        self.assertEqual(brief.check(run, body)["status"], "passed")
        run["execution"]["tasks"][0]["applied_tier"] = "light"
        self.assert_failure(run, body, "downgraded")

    def test_outlook_needs_trigger_confirmation_invalidation_and_horizon(self):
        run, body = fixture()
        run["claims"][0].update({"kind": "hypothesis", "section": "outlook", "mechanism": "Synthetic mechanism"})
        self.assert_failure(run, body, "conditional outlook")

    def test_internal_citations_rejected(self):
        run, body = fixture()
        body += b"turn0search3"
        run["hashes"]["brief_sha256"] = hashlib.sha256(body).hexdigest()
        self.assert_failure(run, body, "internal citation")

    def test_context_and_measurement_time_mismatches_rejected(self):
        run, body = fixture()
        run["context"]["language"] = "zh-CN"
        self.assert_failure(run, body, "request/context mismatch")
        run["observations"][0]["period_end"] = "2026-10-07T00:00:00Z"
        self.assert_failure(run, body, "measurement period exceeds")


class CliTests(unittest.TestCase):
    def test_stdin_output_and_exit_codes(self):
        for payload, expected in [(crypto_request(), 0),
                                  ({"now": "2026-10-07T00:00:00Z", "request": {"market": "cn", "cadence": "premarket"}}, 2),
                                  ({"request": {}}, 1)]:
            with self.subTest(expected=expected):
                result = subprocess.run([sys.executable, str(SCRIPT), "resolve", "-"],
                                        input=json.dumps(payload), capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, expected, result.stderr)
                self.assertIsInstance(json.loads(result.stderr if expected == 1 else result.stdout), dict)

    def test_saved_package_is_inspectable_and_checkable(self):
        folder = SCRIPT.parents[3] / "tests/fixtures/crypto-daily"
        result = subprocess.run([sys.executable, str(SCRIPT), "check", str(folder / "run.json"),
                                 "--brief", str(folder / "brief.md")], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(json.loads(result.stdout)["status"], "passed")


if __name__ == "__main__":
    unittest.main()
