from etl.clients import connect_bigquery, run_sql_file
from etl.settings import load_config, PROJECT_ROOT
from etl.tables import SOURCE_TABLES
from etl.sql_builder import build_create_params


def run():
    config = load_config()
    client = connect_bigquery(config)

    sql_dir = PROJECT_ROOT / "sql"

    run_sql_file(
        client,
        sql_dir / "01_create_datasets.sql",
        project_id=config["bigquery"]["project_id"],
        location=config["bigquery"]["location"]
    )

    for table in SOURCE_TABLES:
        params = build_create_params(config, table)

        run_sql_file(
            client,
            sql_dir / "02_create_bronze.sql",
            **params
        )

        run_sql_file(
            client,
            sql_dir / "03_create_staging.sql",
            **params
        )


if __name__ == "__main__":
    run()