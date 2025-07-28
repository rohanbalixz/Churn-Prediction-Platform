#!/usr/bin/env bash
set -euo pipefail

# ─── 1) Extract the first feature vector using PySpark ────────────────────────
FEATURES_JSON=$(python3 - <<'PYCODE'
from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession
import json

# Build SparkSession with Delta support
builder = SparkSession.builder \
    .appName("FetchFeatureVector") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# Read one row and extract features array
row = spark.read.parquet("data/train").limit(1).collect()[0]
lst = row.features.toArray().tolist()

# Print as JSON
print(json.dumps(lst))

spark.stop()
PYCODE
)

echo "Using features: $FEATURES_JSON"

# ─── 2) Call the /predict endpoint ────────────────────────────────────────────
HTTP_RESPONSE=$(curl -s -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d "{\"features\": $FEATURES_JSON}")

echo "API response: $HTTP_RESPONSE"
