
# Load and configure the geo-boundaries module
with open(workflow.source_path("../../config/modules/geo_boundaries.yaml"), "r") as file:
    config_geo_boundaries = yaml.safe_load(file.read())

module module_geo_boundaries:
    config: config_geo_boundaries
    snakefile: github("modelblocks-org/module_geo_boundaries", path="workflow/Snakefile", tag="v1.0.0")
    pathvars:
        logs="resources/geo_boundaries/logs",
        resources="resources/geo_boundaries/resources",
        results="resources/geo_boundaries/results",
        shapes="results/shapes/{scenario}.parquet"
use rule * from module_geo_boundaries as module_geo_boundaries_*
