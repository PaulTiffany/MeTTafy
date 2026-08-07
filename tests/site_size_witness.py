from __future__ import annotations

import json
from pathlib import Path

SITE = Path("_site")
OUT = Path("artifacts/witnesses/site-size.json")
FIRST_PARTY_LIMIT = 512 * 1024
SINGLE_VENDOR_FILE_LIMIT = 1024 * 1024


def main() -> int:
    if not SITE.is_dir():
        raise SystemExit("missing _site; build the Pages artifact before running size witness")

    files = sorted(path for path in SITE.rglob("*") if path.is_file())
    records = [
        {
            "path": path.relative_to(SITE).as_posix(),
            "bytes": path.stat().st_size,
            "vendor": path.relative_to(SITE).as_posix().startswith("assets/vendor/"),
        }
        for path in files
    ]
    first_party = [item for item in records if not item["vendor"]]
    vendor = [item for item in records if item["vendor"]]

    first_party_bytes = sum(item["bytes"] for item in first_party)
    total_bytes = sum(item["bytes"] for item in records)
    largest_vendor = max((item["bytes"] for item in vendor), default=0)
    largest_vendor_path = next(
        (item["path"] for item in vendor if item["bytes"] == largest_vendor), None
    )

    metrics = {
        "first_party_static_bytes": first_party_bytes,
        "single_vendor_bundle_bytes": largest_vendor,
        "total_site_bytes": total_bytes,
        "file_count": len(records),
    }
    thresholds = {
        "first_party_static_bytes": FIRST_PARTY_LIMIT,
        "single_vendor_bundle_bytes": SINGLE_VENDOR_FILE_LIMIT,
    }
    failures = []
    if first_party_bytes > FIRST_PARTY_LIMIT:
        failures.append(
            f"first-party site bytes {first_party_bytes} exceed {FIRST_PARTY_LIMIT}"
        )
    if largest_vendor > SINGLE_VENDOR_FILE_LIMIT:
        failures.append(
            f"vendor file {largest_vendor_path} is {largest_vendor} bytes, "
            f"exceeding {SINGLE_VENDOR_FILE_LIMIT}"
        )

    payload = {
        "witness": "WIT-WEB-SIZE",
        "claim_boundary": (
            "The generated static site remains within the versioned byte budgets; "
            "this does not establish runtime latency or memory performance."
        ),
        "metrics": metrics,
        "thresholds": thresholds,
        "largest_vendor_path": largest_vendor_path,
        "files": records,
        "result": "pass" if not failures else "fail",
        "failures": failures,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(
        "Site size witness: "
        f"first-party={first_party_bytes}/{FIRST_PARTY_LIMIT} bytes; "
        f"largest-vendor={largest_vendor}/{SINGLE_VENDOR_FILE_LIMIT} bytes; "
        f"total={total_bytes} bytes."
    )
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
