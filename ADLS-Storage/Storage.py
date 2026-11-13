# =============================================================
# Mount Azure Data Lake Storage Gen2 containers to DBFS
# (bronze, silver, gold) using Azure AD credential passthrough.
# =============================================================

# BRONZE CONTAINER

# Configure authentication for the ADLS Gen2 mount using
# credential passthrough (the current user's Azure AD credentials).
configs = {
  "fs.azure.account.auth.type": "CustomAccessToken",
  "fs.azure.account.custom.token.provider.class": spark.conf.get("spark.databricks.passthrough.adls.gen2.tokenProviderClassName")
}

# Mount the bronze container of the storage account.
# Optionally, you can add <directory-name> to the source URI of your mount point.
dbutils.fs.mount(
  source = "abfss://bronze@deprojdatalakegen2.dfs.core.windows.net/",
  mount_point = "/mnt/bronze",
  extra_configs = configs)

# Verify the bronze mount by listing files in the Sales directory.
dbutils.fs.ls("/mnt/bronze/Sales")


  # SILVER CONTAINER

# Reuse the same passthrough auth configuration for the silver mount.
configs = {
  "fs.azure.account.auth.type": "CustomAccessToken",
  "fs.azure.account.custom.token.provider.class": spark.conf.get("spark.databricks.passthrough.adls.gen2.tokenProviderClassName")
}

# Mount the silver container of the storage account.
# Optionally, you can add <directory-name> to the source URI of your mount point.
dbutils.fs.mount(
  source = "abfss://silver@deprojdatalakegen2.dfs.core.windows.net/",
  mount_point = "/mnt/silver",
  extra_configs = configs)



  # GOLD CONTAINER

# Reuse the same passthrough auth configuration for the gold mount.
configs = {
  "fs.azure.account.auth.type": "CustomAccessToken",
  "fs.azure.account.custom.token.provider.class": spark.conf.get("spark.databricks.passthrough.adls.gen2.tokenProviderClassName")
}

# Mount the gold container of the storage account.
# Optionally, you can add <directory-name> to the source URI of your mount point.
dbutils.fs.mount(
  source = "abfss://gold@deprojdatalakegen2.dfs.core.windows.net/",
  mount_point = "/mnt/gold",
  extra_configs = configs)