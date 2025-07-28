from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, dayofweek
from pyspark.ml.feature import VectorAssembler

# 1. Spark session with Delta support
builder = SparkSession.builder \
    .appName("ChurnPreprocess") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
spark = configure_spark_with_delta_pip(builder).getOrCreate()

# 2. Load Delta table and cast columns
df = spark.read.format("delta").load("data/delta/events")
df = df.withColumn("feature1", col("feature1").cast("double")) \
       .withColumn("feature2", col("feature2").cast("double")) \
       .withColumn("churned", col("churned").cast("integer"))

# 3. Basic feature engineering
df = df.withColumn("event_time", to_timestamp(col("event_timestamp")))
df = df.withColumn("day_of_week", dayofweek(col("event_time")))

# 4. Aggregate event_type counts per user
pivoted = (
    df.groupBy("user_id")
      .pivot("event_type")
      .count()
      .na.fill(0)
)

# 5. Combine churn label, numeric features, and pivots
features_df = (
    df.select("user_id", "churned", "feature1", "feature2", "day_of_week")
      .dropDuplicates(["user_id"])
      .join(pivoted, on="user_id", how="left")
)

# 6. Assemble feature vector
input_cols = ["feature1", "feature2", "day_of_week"] + pivoted.columns[1:]
assembler = VectorAssembler(inputCols=input_cols, outputCol="features")
ml_df = assembler.transform(features_df)

# 7. Rename churned to label and select
ml_df = ml_df.withColumnRenamed("churned", "label").select("user_id", "features", "label")

# 8. Train/test split
train_df, test_df = ml_df.randomSplit([0.8, 0.2], seed=42)

# 9. Save splits for modeling
train_df.write.mode("overwrite").parquet("data/train")
test_df.write.mode("overwrite").parquet("data/test")

spark.stop()

