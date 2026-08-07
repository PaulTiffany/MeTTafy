from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analysis import analyze_source
from .emit import emit_strategy_metta


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="mettafy",
        description="Recover computational strategies from Python and emit MeTTa semantic artifacts.",
    )
    parser.add_argument("source", type=Path, help="Python source file to analyze")
    parser.add_argument(
        "--format",
        choices=("metta", "json"),
        default="metta",
        help="output format (default: metta)",
    )
    args = parser.parse_args()

    source = args.source.read_text(encoding="utf-8")
    strategies = analyze_source(source, filename=str(args.source))

    if args.format == "json":
        print(json.dumps([strategy.to_dict() for strategy in strategies], indent=2))
    else:
        print(emit_strategy_metta(strategies), end="")


if __name__ == "__main__":
    main()
