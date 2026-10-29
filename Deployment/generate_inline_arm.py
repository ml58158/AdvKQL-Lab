#!/usr/bin/env python3
"""Generate a self-contained ARM template from the repository's KQL schema file.

Run at repo root: python Deployment/generate_inline_arm.py
No Azure credentials or network access required.
"""
import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "Scripts" / "advanced_kql_v2.kql"
BASE = REPO_ROOT / "Deployment" / "azuredeploy.base.json"
OUTPUT = REPO_ROOT / "Deployment" / "azuredeploy-inline.json"

def main():
    raw = SOURCE.read_bytes()
    if len(raw) >= 1_000_000:
        raise SystemExit("KQL is approaching the ARM per-resource limit; use external deployment instead.")
    content = raw.decode("utf-8-sig")
    git_blob_sha = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
    template = json.loads(BASE.read_text(encoding="utf-8"))
    script_resources = [r for r in template["resources"] if r["type"].lower() == "microsoft.kusto/clusters/databases/scripts"]
    if len(script_resources) != 1:
        raise SystemExit("Expected exactly one ADX script resource.")
    script = script_resources[0]["properties"]
    if script.get("scriptContent") != "__INLINE_KQL_SCRIPT__":
        raise SystemExit("Unexpected base script placeholder.")
    if template["parameters"]["scriptForceUpdateTag"]["defaultValue"] != "__GIT_BLOB_SHA__":
        raise SystemExit("Unexpected base source SHA placeholder.")
    script["scriptContent"] = content
    template["parameters"]["scriptForceUpdateTag"]["defaultValue"] = git_blob_sha
    output = json.dumps(template, indent=2, ensure_ascii=False) + "\n"
    if len(output.encode("utf-8")) >= 1_000_000:
        raise SystemExit("Generated template exceeds the 1 MB conservative guardrail.")
    OUTPUT.write_text(output, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(REPO_ROOT)} ({len(output.encode('utf-8')):,} bytes)")
    print(f"KQL source Git blob SHA: {git_blob_sha}")
    print(f"Table definitions: {sum(1 for line in content.splitlines() if line.lstrip().startswith('.create table '))}")

if __name__ == "__main__":
    main()
