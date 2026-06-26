#!/usr/bin/env python3
"""
validate_protocol.py — consistency self-check for the Kitso Handshake repo.

Enforces that protocol.json (the SSOT) agrees with everything that states a
version: the JSON Schemas, the well-known protocol_version const, the README
header table, and the CHANGELOG. Run locally or in CI; exits non-zero on any
mismatch.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def load_json(p: Path):
    try:
        return json.loads(p.read_text())
    except Exception as e:  # noqa: BLE001
        errors.append(f"{p}: invalid JSON ({e})")
        return None


def main() -> int:
    manifest = load_json(ROOT / "protocol.json")
    if manifest is None:
        print("FATAL: protocol.json unreadable")
        return 1

    spec_version = manifest["spec_version"]
    wire_version = manifest["wire_version"]
    spec_published = manifest["spec_published"]
    wire_dir = ROOT / "schemas" / wire_version

    # 1) wire dir for the declared wire_version must exist
    if not wire_dir.is_dir():
        errors.append(f"protocol.json wire_version={wire_version} but {wire_dir} is missing")

    # 2) every schema is valid JSON, draft 2020-12, and its $id matches its path
    schema_base = f"https://kitsuno.ai/handshake/{wire_version}/"
    if wire_dir.is_dir():
        for f in sorted(wire_dir.glob("*.json")):
            doc = load_json(f)
            if doc is None:
                continue
            if doc.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
                errors.append(f"{f.name}: $schema is not draft 2020-12")
            expected_id = schema_base + f.name
            if doc.get("$id") != expected_id:
                errors.append(f"{f.name}: $id={doc.get('$id')!r} != {expected_id!r}")

    # 3) well-known.json must pin protocol_version const == wire_version
    wk = load_json(wire_dir / "well-known.json") if wire_dir.is_dir() else None
    if wk:
        const = wk.get("properties", {}).get("protocol_version", {}).get("const")
        if const != wire_version:
            errors.append(
                f"well-known.json protocol_version const={const!r} != wire_version {wire_version!r}"
            )

    # 4) README header table must match spec_version + spec_published
    readme = (ROOT / "README.md").read_text()
    m = re.search(r"\*\*Current draft\*\*\s*\|\s*([^\s|]+)\s*—\s*published\s*([0-9-]+)", readme)
    if not m:
        errors.append("README: could not find 'Current draft | <ver> — published <date>' row")
    else:
        if m.group(1) != spec_version:
            errors.append(f"README current draft={m.group(1)!r} != spec_version {spec_version!r}")
        if m.group(2) != spec_published:
            errors.append(
                f"README published={m.group(2)!r} != spec_published {spec_published!r}"
            )

    # 5) CHANGELOG must have a top entry for spec_version
    changelog = (ROOT / "CHANGELOG.md").read_text()
    if not re.search(rf"^##\s*\[?{re.escape(spec_version)}\]?", changelog, re.MULTILINE):
        errors.append(f"CHANGELOG: no '## {spec_version}' entry")

    if errors:
        print("PROTOCOL CONSISTENCY: FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"PROTOCOL CONSISTENCY: OK  (spec {spec_version}, wire {wire_version})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
