# Medallion Architecture: Silver -> Gold transformation
# Iterates over all Delta tables in the Silver layer (SalesLT schema),
# renames columns to snake_case, and writes the result to the Gold layer.

# Step 1: List all table folders in the Silver layer mount point
table_name = []

for i in dbutils.fs.ls("/mnt/silver/SalesLT"):
    # Extract the table name (last part of the path) from each directory entry
    table_name.append(i.name.split("/")[0])

table_name

# Step 2: Process each Silver table and write it to Gold
for name in table_name:
    # Build the full path to the Silver Delta table
    path = "/mnt/silver/SalesLT/" + name
    print(path)

    # Load the Silver table as a Delta DataFrame
    df = spark.read.format("delta").load(path)

    # Get the list of column names

    column_names = df.columns

    # Step 3: Rename columns from CamelCase to snake_case
    # e.g. "SalesOrderID" -> "sales_order_id" (snake_case naming convention for Gold)
    for old_col_name in column_names:
        # Insert an underscore before each uppercase letter (except consecutive capitals)
        # and strip any leading underscore
        new_col_name = "".join(["_" + char if char.isupper() and not old_col_name[i-1].isupper() else char for i, char in enumerate(old_col_name)]).lstrip("_")

        # Apply the rename to the DataFrame
        df = df.withColumnRenamed(old_col_name, new_col_name)
    
    # Step 4: Write the transformed DataFrame to the Gold layer as a Delta table
    # mode='overwrite' replaces any existing Gold table with the same name
    output_path = "/mnt/gold/SalesLT/" + name + "/"
    df.write.format('delta').mode('overwrite').save(output_path)


    # Preview the transformed DataFrame
    display(df)