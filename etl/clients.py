import psycopg
from google.cloud import bigquery
from psycopg.rows import dict_row


def connect_bigquery(config):
    bq = config["bigquery"]
    return bigquery.Client(project=bq["project_id"], location=bq["location"])

8
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

# Lấy tên table 
def table_id(config, dataset_name, table_name):
    return f"{config['bigquery']['project_id']}.{dataset_name}.{table_name}"

def create_dataset(client, config, dataset_name):
    dataset=bigquery.Dataset(f"{config['bigquery']['project_id']}.{dataset_name}")
    dataset.location=config['bigquery']['location']
    client.create_dataset(dataset, exists_ok=True)
