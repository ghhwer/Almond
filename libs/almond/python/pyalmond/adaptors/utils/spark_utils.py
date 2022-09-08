from pyspark.sql.functions import col

def get_df_repartition_options(df, no_repartition, num_partitions):
    if (no_repartition):
        return df
    else:
        if (num_partitions is None):
            raise ValueError('no_repartition cannot be false while num_partitions is null')
        return df.coalesce(num_partitions)

def save_as_table_parquet_hive_metastore(
    spark, df, target_database, target_table, partition_col, metadata, write_mode,
    no_repartition=True, num_partitions=0
):
    if ((write_mode != 'overwrite') and (write_mode != 'append')):
        raise ValueError('Invalid write_mode passed, must be either overwrite or append')
   
    print("SPARK - SAVING INTO:", target_database, target_table)
    table_exists = metadata.table_exists(target_database, target_table)
    if table_exists == 0:
        print(
            "WARNING: table {} does not exists. Is this the first run?".format(
                target_table
            )
        )
        if partition_col is not None:
            print(f"Partitioning by {partition_col}")
            df = get_df_repartition_options(df, no_repartition, num_partitions)
            df.write.option(
                "compression", "snappy"
            ).partitionBy(partition_col).saveAsTable(
                target_database + "." + target_table,
                format="parquet",
                mode="overwrite"
            )
        else:
            print("Atention: no partition column specified.")
            df = get_df_repartition_options(df, no_repartition, num_partitions)
            df.write.option(
                "compression", "snappy"
            ).saveAsTable(
                target_database + "." + target_table,
                format="parquet",
                mode="overwrite"
            )
    else:
        kw_insert = "INSERT OVERWRITE" if write_mode == 'overwrite' else "INSERT INTO"
        if partition_col is not None:
            print(
                "INFO: table {} already exists. Data in the current partition is going to be overwritten.".format(
                    target_table
                )
            )
            df = get_df_repartition_options(df, no_repartition, num_partitions)
            df2 = (
                df.withColumn(partition_col + "_tmp", col(partition_col))
                .drop(partition_col)
                .withColumnRenamed(partition_col + "_tmp", partition_col)
            )
            df2.createOrReplaceTempView("df2")
            spark.sql(
                "{} TABLE {}.{} PARTITION({}) (SELECT * FROM {})".format(
                    kw_insert, target_database, target_table, partition_col, "df2"
                )
            )
        else:
            print("Atention: no partition column specified.")
            print(
                "INFO: table {} already exists and all its data is going to be overwritten.".format(
                    target_table
                )
            )
            df = get_df_repartition_options(df, no_repartition, num_partitions)
            df.createOrReplaceTempView("df")
            spark.sql(
                "{} TABLE {}.{} (SELECT * FROM {})".format(
                    kw_insert, target_database, target_table, "df"
                )
            )
