"""Create a markdown table for Zenodo."""

import sys
from typing import TYPE_CHECKING, Any

import geopandas as gpd
import pandas as pd

if TYPE_CHECKING:
    snakemake: Any

SCENARIO_TYPES = {"L": "Large scale", "V": "Voronoi EEZ", "S": "Small scale"}


def scenario_type(scenario):
    """Return the scenario type encoded in names like EUROPE_S_C1_ADM1."""
    parts = scenario.split("_")
    if len(parts) < 2:
        return "unknown"
    return SCENARIO_TYPES.get(parts[1], parts[1])


def region(scenario):
    """Return the region encoded in names like EUROPE_S_C1_ADM1."""
    return scenario.split("_", maxsplit=1)[0]


def main() -> None:
    """Main snakemake process."""
    scenarios = snakemake.params.scenarios
    default_crs = snakemake.params.default_crs

    rows = []
    shape_paths = dict(zip(scenarios, snakemake.input.shapes))
    for scenario, scenario_config in scenarios.items():
        shape_path = shape_paths[scenario]
        shapes = gpd.read_parquet(shape_path)
        projected_crs = scenario_config.get("crs", {}).get(
            "projected", default_crs["projected"]
        )
        projected_shapes = shapes.to_crs(projected_crs)
        area_km2 = projected_shapes.geometry.area.sum() / 1_000_000
        country_codes = sorted(shapes["country_id"].dropna().astype(str).unique())
        configured_country_count = len(scenario_config.get("countries", {}))
        shape_class = shapes["shape_class"].astype(str).str.lower()
        data_sources = sorted(shapes["parent"].dropna().astype(str).unique())
        rows.append(
            {
                "Scenario": scenario,
                "Region": region(scenario),
                "Scenario type": scenario_type(scenario),
                "Countries": ", ".join(country_codes),
                "Total countries": configured_country_count,
                "Estimated total area": round(area_km2),
                "Land shapes": int((shape_class == "land").sum()),
                "Maritime shapes": int((shape_class == "maritime").sum()),
                "Data sources": ", ".join(data_sources),
            }
        )

    pd.DataFrame(rows).to_markdown(snakemake.output[0], index=False)


if __name__ == "__main__":
    sys.stderr = open(snakemake.log[0], "w", buffering=1)
    main()
