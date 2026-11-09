import pandas as pd
from google.cloud import bigquery

from .clients import connect_bigquery, connect_postgres, table_id
from .schema import raw_schema
from .settings import load_config
from .tables import SOURCE_TABLES


def build_extract_query(table):
    columns = ", ".join(table["columns"].keys())
    return f"SELECT {columns} FROM {table['name']}"

# dùng table trong source_table để đúng column_names
def to_dataframe(table, rows):
    column_names = list(table["columns"].keys())
    return pd.DataFrame(rows, columns=column_names)

def load_to_bigquery_raw(client, config, table, dataframe):
    if dataframe.empty:
        return
    schema = raw_schema(table)
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        schema=schema,
    )
    load_job = client.load_table_from_dataframe(
        dataframe,
        table_id(config, config["bigquery"]["raw_dataset"], table["name"]),
        job_config=job_config,
    )
    load_job.result()


def run():
    config = load_config()
    client = connect_bigquery(config)

    print("Starting raw load.")

    with connect_postgres(config) as source_conn:
        for table in SOURCE_TABLES:
            sql = build_extract_query(table)

            with source_conn.cursor() as cursor:
                cursor.execute(sql)       # Thực thi SQL
                rows = cursor.fetchall()  # Lấy toàn bộ kết quả còn lại thành list(full load)

            dataframe = to_dataframe(table, rows)
            load_to_bigquery_raw(client, config, table, dataframe)

    print("Raw load complete.")


if __name__ == "__main__":
    run()
