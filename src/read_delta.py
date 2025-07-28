from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession

# Build SparkSession with Delta Lake support
builder = SparkSession.builder \
    .appName("ReadDelta") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# Path to Delta table
delta_path = "data/delta/events"

# Read and show
df = spark.read.format("delta").load(delta_path)
df.show()

spark.stop()

