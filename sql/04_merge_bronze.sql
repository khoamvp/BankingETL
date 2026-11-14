MERGE {bronze_table} AS target
USING {staging_table} AS source
ON {join_condition}

WHEN MATCHED THEN
    UPDATE SET {update_assignments}

WHEN NOT MATCHED THEN
    INSERT ({column_names})
    VALUES ({source_columns})

WHEN NOT MATCHED BY SOURCE THEN
    DELETE;