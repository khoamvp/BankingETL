def build_create_params(config, table):
    name = table["name"]

    columns = ", ".join(
        f"`{col}` {dtype}"
        for col, dtype in table["columns"].items()
    )

    project = config["bigquery"]["project_id"]

    return {
        "bronze_table": f"`{project}.bronze.{name}`",
        "staging_table": f"`{project}.staging.{name}`",
        "column_definitions": columns
    }




def build_merge_params(config, table):
    params = build_create_params(config, table)

    cols = list(table["columns"].keys())
    key = table["primary_key"]

    params.update({
        "join_condition": f"target.`{key}` = source.`{key}`",
        "update_assignments": ", ".join(
            f"`{c}` = source.`{c}`"
            for c in cols if c != key
        ),
        "column_names": ", ".join(
            f"`{c}`" for c in cols
        ),
        "source_columns": ", ".join(
            f"source.`{c}`" for c in cols
        )
    })

    return params