#!/usr/bin/env python3
"""
bench-aggregate: Scan bench/**/results/*.json and update recipes.lock.json
with the most recent metrics per (bench_id, provider, model, variant).
Stdlib only; best-effort git SHA detection.
"""
from __future__ import annotations
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from glob import glob
from typing import Any, Dict, List, Optional, Tuple
import subprocess

LOCK_PATH = "recipes.lock.json"
RESULTS_GLOB = os.path.join("bench", "**", "results", "*.json")


def read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def try_git_sha() -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], encoding="utf-8").strip()
        if out:
            return out
    except Exception:
        pass
    return "UNSET"


def parse_ts(s: str) -> float:
    try:
        # ISO 8601 with timezone; fallback if naive
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.timestamp()
    except Exception:
        return 0.0


@dataclass
class Metric:
    accuracy: float
    avg_latency_ms: float
    tool_calls: int
    ended_at: float


def variant_key(variants: Optional[List[str]]) -> str:
    if not variants:
        return "default"
    return "+".join(variants)


def aggregate_latest(results_paths: List[str]) -> Dict[str, Any]:
    # metrics[bench_id][provider][model][variant] = Metric (latest)
    metrics: Dict[str, Dict[str, Dict[str, Dict[str, Metric]]]] = {}

    for p in results_paths:
        try:
            data = read_json(p)
        except Exception:
            continue
        bench_id = data.get("bench_id") or "unknown"
        provider = data.get("provider") or "unknown"
        model = data.get("model") or "unknown"
        variants = data.get("variants")
        vkey = variant_key(variants if isinstance(variants, list) else None)
        totals = data.get("totals", {})
        m = Metric(
            accuracy=float(totals.get("accuracy", 0.0)),
            avg_latency_ms=float(totals.get("avg_latency_ms", 0.0)),
            tool_calls=int(totals.get("tool_calls", 0)),
            ended_at=parse_ts(data.get("ended_at") or ""),
        )

        metrics.setdefault(bench_id, {}).setdefault(provider, {}).setdefault(model, {})
        cur = metrics[bench_id][provider][model].get(vkey)
        if cur is None or m.ended_at >= cur.ended_at:
            metrics[bench_id][provider][model][vkey] = m

    # build serializable dict
    out: Dict[str, Any] = {}
    for bench_id, providers in metrics.items():
        out.setdefault(bench_id, {})
        for provider, models in providers.items():
            out[bench_id].setdefault(provider, {})
            for model, variants in models.items():
                out[bench_id][provider].setdefault(model, {"variants": {}})
                for vkey, metric in variants.items():
                    out[bench_id][provider][model]["variants"][vkey] = {
                        "accuracy": round(metric.accuracy, 4),
                        "avg_latency_ms": round(metric.avg_latency_ms, 2),
                        "tool_calls": metric.tool_calls,
                    }
    return out


def main() -> int:
    paths = sorted(glob(RESULTS_GLOB, recursive=True))
    if not paths:
        print("No results found; nothing to aggregate", file=sys.stderr)
        return 0

    agg = aggregate_latest(paths)

    lock = {
        "version": "0.1.0",
        "release": {
            "sha": try_git_sha(),
            "date": datetime.now(timezone.utc).date().isoformat(),
        },
        "metrics": agg,
    }

    write_json(LOCK_PATH, lock)
    print(json.dumps({"lockfile": LOCK_PATH, "bench_count": len(agg)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
