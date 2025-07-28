from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession

# Build SparkSession with Delta Lake support
builder = SparkSession.builder \
    .appName("ChurnIngestion") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# Paths
input_path = "data/sample_events.csv"    # your sample CSV file
delta_path = "data/delta/events"         # target Delta Lake folder

# Ingest CSV into Delta Lake, inferring schema so numeric and label columns are typed
df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(input_path)

df.write.format("delta").mode("overwrite").save(delta_path)

spark.stop()

