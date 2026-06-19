
rule summarize_shape_datasets:
    input:
        shapes=expand(
            "results/shapes/{scenario}.parquet",
            scenario=config_geo_boundaries["scenarios"],
        ),
    output:
        "results/shape_summary.md",
    log:
        "<logs>/summarize_shape_datasets.log",
    params:
        scenarios=config_geo_boundaries["scenarios"],
        default_crs=config_geo_boundaries["crs"],
    message:
        "Summarize geo-political boundary test datasets."
    script:
        "../scripts/summarize_shape_datasets.py"
