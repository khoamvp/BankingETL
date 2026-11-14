from google.cloud import bigquery
from .schema import raw_schema


def load_to_staging(client, config, table, dataframe):
    # 1. Xác định bảng Staging
    destination = f"{config["bigquery"]["project_id"]}.{"staging"}.{table["name"]}"
    # 2. Xử lý bảng nguồn rỗng
    if dataframe.empty:
        client.query( f"TRUNCATE TABLE `{destination}`").result()
        return 0
    # 3. Lấy schema
    schema = raw_schema(table)
    # 4. Cấu hình Load Job
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        create_disposition=bigquery.CreateDisposition.CREATE_NEVER,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )
    # 5. Load dữ liệu vào Staging
    load_job = client.load_table_from_dataframe(
        dataframe[[field.name for field in schema]],
        destination,
        job_config=job_config
    )

    # 6. Đợi load hoàn thành
    load_job.result()

    return len(dataframe)