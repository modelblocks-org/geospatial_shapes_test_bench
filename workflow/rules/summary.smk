
rule summarize_shape_datasets:
    input:
        shapes=expand(
            "results/shapes/{scenario}.parquet",
            scenario=config_geo_boundaries["scenarios"],
        ),
    output:
        "results/summary.md",
    log:
        "<logs>/summarize_shape_datasets.log",
    params:
        scenarios=config_geo_boundaries["scenarios"],
        default_crs=config_geo_boundaries["crs"],
    conda:
        "../envs/conda-spec.yaml"
    message:
        "Summarize geo-political boundary test datasets."
    script:
        "../scripts/summarize_shape_datasets.py"


rule compress_figures:
    input:
        expand(
            "resources/geo_boundaries/results/{scenario}/shapes.png",
            scenario=config_geo_boundaries["scenarios"],
        ),
    output:
        "results/figures.zip",
    log:
        "<logs>/compress_figures.log",
    threads: 1
    params:
        format_name="zip",
        internal_paths=[
            f"{scenario}.png" for scenario in config_geo_boundaries["scenarios"]
        ],
    wrapper:
        "v9.8.0/utils/libarchive/compress"
