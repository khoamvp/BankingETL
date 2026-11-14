import psycopg
from google.cloud import bigquery
from psycopg.rows import dict_row
from pathlib import Path

def connect_bigquery(config):
    bq = config["bigquery"]
    return bigquery.Client(project=bq["project_id"], location=bq["location"])


def connect_postgres(config):
    db = config["source_db"]
  
    return psycopg.connect(        
        host= db['host'],
        port=db['port'],
        dbname= db['database'],
        user= db['user'],
        password=db['password'],
        connect_timeout=15,
        row_factory=dict_row    # dùng dict_row để postgres trả về data dạng json
    )



def run_sql_file(client, file_path, **params):
    with open(file_path, encoding="utf-8") as f:
        sql = f.read()

    sql = sql.format(**params)
    client.query(sql).result()