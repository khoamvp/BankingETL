from etl.clients import (
    connect_postgres,
    connect_bigquery,
    run_sql_file
)
from etl.settings import load_config, PROJECT_ROOT
from etl.tables import SOURCE_TABLES
from etl.extract import extract_table
from etl.load import load_to_staging
from etl.sql_builder import build_merge_params


def run():
    config = load_config()
    client = connect_bigquery(config)

    with connect_postgres(config) as source_conn:
        for table in SOURCE_TABLES:

            # 1. Extract
            df = extract_table(source_conn, table)

            # 2. Load Staging
            load_to_staging(client, config, table, df)

            # 3. MERGE Bronze
            params = build_merge_params(config, table)

            run_sql_file(
                client,
                PROJECT_ROOT / "sql" / "04_merge_bronze.sql",
                **params
            )
    print("ETL process completed successfully.")

if __name__ == "__main__":
    run()