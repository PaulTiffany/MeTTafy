from __future__ import annotations

import json

from mettafy.four_color_staging_fixtures import red_team_staging_fixtures
from mettafy.strategy_staging import NormalizationPolicy, build_staging_report


def main() -> None:
    fixtures = red_team_staging_fixtures()
    report = build_staging_report(
        fixtures,
        NormalizationPolicy(
            mirror_equivalent=True,
            periodic_cycles=(("B", "C"),),
        ),
    )
    print(
        json.dumps(
            {
                "raw_traces": report.raw_traces,
                "raw_operations": report.raw_operations,
                "normal_forms": report.normal_forms,
                "max_remaining_degrees": report.max_remaining_degrees,
                "max_normalized_operations": report.max_normalized_operations,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
