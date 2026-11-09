"""Buoc khoi tao: tao dataset/table BigQuery can dung (raw + clean + ops)."""

from etl.clients import connect_bigquery, create_dataset
from etl.schema import create_raw_table
from etl.settings import PROJECT_ROOT, load_config
from etl.tables import SOURCE_TABLES

def run():
    config = load_config()
    client = connect_bigquery(config)
    bq = config["bigquery"]

    print("Creating BigQuery datasets...")
    create_dataset(client, config, bq["raw_dataset"])
    
    print("Creating raw tables...")
    for table in SOURCE_TABLES:
        create_raw_table(client, config, table)
        print(f"  ready: raw.{table['name']}")

    print("BigQuery initialization complete.")


if __name__ == "__main__":
    run()
