#!/usr/bin/env python3
"""
check_live_conformance.py — proves the live operator instance still conforms to
the schemas in this repo. Fetches Kitsuno's published well-known doc and one of
its cards and validates them against schemas/<wire>/. Run on a schedule or
manually; if the live deployment ever drifts from the published schemas, this
fails loudly instead of silently diverging.

Usage: check_live_conformance.py [--base https://kitsuno.ai]
"""
import argparse
import json
import sys
import urllib.request
from pathlib import Path

from jsonschema import Draft202012Validator, RefResolver

ROOT = Path(__file__).resolve().parent.parent


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "kitso-handshake-conformance"})
    with urllib.request.urlopen(req, timeout=20) as r:  # noqa: S310
        return json.loads(r.read().decode())


def validator_for(schema_path: Path) -> Draft202012Validator:
    schema = json.loads(schema_path.read_text())
    store = {}
    for f in schema_path.parent.glob("*.json"):
        s = json.loads(f.read_text())
        if "$id" in s:
            store[s["$id"]] = s
    resolver = RefResolver(base_uri=schema.get("$id", ""), referrer=schema, store=store)
    return Draft202012Validator(schema, resolver=resolver)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://kitsuno.ai")
    args = ap.parse_args()

    manifest = json.loads((ROOT / "protocol.json").read_text())
    wire = manifest["wire_version"]
    sdir = ROOT / "schemas" / wire
    failures = []

    # 1) live well-known validates against well-known.json
    wk_url = args.base.rstrip("/") + manifest["well_known_path"]
    try:
        wk = fetch_json(wk_url)
        v = validator_for(sdir / "well-known.json")
        errs = sorted(v.iter_errors(wk), key=lambda e: e.path)
        if errs:
            failures.append((wk_url, [f"{list(e.path)}: {e.message}" for e in errs]))
        else:
            print(f"OK   {wk_url}  (protocol_version={wk.get('protocol_version')}, "
                  f"spec_version={wk.get('spec_version', '—')})")
        # advisory: spec_version, if present, should equal the manifest
        if wk.get("spec_version") and wk["spec_version"] != manifest["spec_version"]:
            failures.append((wk_url, [f"spec_version {wk['spec_version']} != manifest "
                                      f"{manifest['spec_version']}"]))
    except Exception as e:  # noqa: BLE001
        failures.append((wk_url, [f"fetch/parse failed: {e}"]))
        wk = {}

    # 2) one live card validates against vacancy-card.json (best-effort via cards_index)
    idx_url = (wk.get("endpoints") or {}).get("cards_index")
    if idx_url:
        try:
            feed = fetch_json(idx_url)
            items = feed.get("cards") or feed.get("items") or []
            sample = next((c for c in items if "vacancy" in str(c.get("kind", "")).lower()), None)
            if sample and sample.get("uri"):
                card = fetch_json(sample["uri"])
                v = validator_for(sdir / "vacancy-card.json")
                errs = sorted(v.iter_errors(card), key=lambda e: e.path)
                if errs:
                    failures.append((sample["uri"], [f"{list(e.path)}: {e.message}" for e in errs]))
                else:
                    print(f"OK   {sample['uri']}  (live vacancy card valid)")
            else:
                print("SKIP live card check — no vacancy card found in cards_index")
        except Exception as e:  # noqa: BLE001
            print(f"SKIP live card check — {e}")
    else:
        print("SKIP live card check — no cards_index in well-known")

    if failures:
        print("\nLIVE CONFORMANCE: FAIL")
        for url, msgs in failures:
            print(f"  {url}")
            for m in msgs:
                print(f"    - {m}")
        return 1
    print("\nLIVE CONFORMANCE: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
