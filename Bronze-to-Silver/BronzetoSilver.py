# -----------------------------------------------------------------------------
# Medallion Pipeline: Bronze -> Silver (Sales)
# This script reads the raw parquet files for each Sales table from the Bronze
# layer, standardizes all date columns (casts to timestamp, converts to UTC,
# and formats as yyyy-MM-dd), then writes the cleaned data to the Silver layer
# as Delta tables (one per source table).
# -----------------------------------------------------------------------------

# List to hold the names of the Sales tables found in the Bronze layer
table_name = []

# Iterate over the folders in the Bronze mount and collect the table names
# (the folder name is used as the table name)
for i in dbutils.fs.ls("mnt/bronze/Sales/"):
    table_name.append(i.name.split('/')[0])


# Import the functions needed to standardize date columns
from pyspark.sql.functions import from_utc_timestamp, date_format
from pyspark.sql.types import TimestampType

# Process each Sales table one by one
for i in table_name:
    # Build the path to the parquet file for the current table in Bronze
    path = "/mnt/bronze/Sales/" + i + "/" + i + ".parquet"

    # Load the parquet file into a Spark DataFrame
    df = spark.read.format('parquet').load(path)

    # Get the list of columns to inspect for date columns
    columns = df.columns

    # Standardize any column whose name contains "Date" or "date":
    # cast to timestamp, align to UTC, and format as yyyy-MM-dd
    for col in columns:
        if "Date" in col or "date" in col:
            df = df.withColumn(col, 
                        date_format(
                            from_utc_timestamp(
                                df[col].cast(TimestampType()), "UTC"
                                ), "yyyy-MM-dd"
                            )
                        )
    
    # Build the output path for the Silver layer (one folder per table)
    output_path = "/mnt/silver/Sales/" + i + "/"

    # Write the transformed DataFrame as a Delta table in Silver,
    # overwriting any previous version
    df.write.format("delta").mode("overwrite").save(output_path)

    # Display the transformed DataFrame for a quick visual check
    display(df)
