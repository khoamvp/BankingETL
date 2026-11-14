from google.cloud import bigquery


def raw_schema(table):
    schema = []
    all_columns = {**table["columns"]}
    for column_name, column_type in all_columns.items():
        schema.append(bigquery.SchemaField(column_name, column_type, mode="NULLABLE"))
    return schema
