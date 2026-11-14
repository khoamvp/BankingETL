import pandas as pd
from psycopg import sql


def build_extract_query(table):
    columns = sql.SQL(", ").join( sql.Identifier(col) for col in table["columns"].keys())
    table_name = sql.Identifier("public",table["name"])
    return sql.SQL("SELECT {} FROM {}").format( columns, table_name)


def to_dataframe(table, rows):
    column_names = list(table["columns"].keys())
    return pd.DataFrame(rows, columns=column_names)


def extract_table(source_conn, table):
    query = build_extract_query(table)

    with source_conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    dataframe = to_dataframe(table, rows)

    return dataframe