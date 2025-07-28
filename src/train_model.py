from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense
from sklearn.metrics import roc_auc_score, precision_score
import xgboost as xgb

# ──────────────────────────────────────────────────────────────────────────────
# 1) Start Spark with Delta Lake support
builder = SparkSession.builder \
    .appName("ChurnModel") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
spark = configure_spark_with_delta_pip(builder).getOrCreate()

# 2) Read the train/test splits from disk
train_sdf = spark.read.parquet("data/train")
test_sdf  = spark.read.parquet("data/test")

# 3) Collect to driver and extract numpy arrays
#    Each row.features is a pyspark.ml.linalg.DenseVector
train_rows = train_sdf.collect()
test_rows  = test_sdf.collect()

X_train = np.vstack([row.features.toArray() for row in train_rows]).astype(float)
y_train = np.array([row.label for row in train_rows], dtype=int)

X_test  = np.vstack([row.features.toArray() for row in test_rows]).astype(float)
y_test  = np.array([row.label for row in test_rows], dtype=int)

# Done with Spark
spark.stop()

# ──────────────────────────────────────────────────────────────────────────────
# 4) Reshape for LSTM
X_train_seq = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
X_test_seq  = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

# ──────────────────────────────────────────────────────────────────────────────
# 5) Build, train & save LSTM
model = Sequential([
    Input(shape=(1, X_train.shape[1])),
    LSTM(32),
    Dense(1, activation="sigmoid")
])
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["AUC"])
model.fit(X_train_seq, y_train.astype(float),
          epochs=5, batch_size=8, validation_split=0.2)

model.save("models/lstm.h5")
print("Saved LSTM model to models/lstm.h5")

# ──────────────────────────────────────────────────────────────────────────────
# 6) Get LSTM predictions
train_preds = model.predict(X_train_seq).flatten()
test_preds  = model.predict(X_test_seq).flatten()

# ──────────────────────────────────────────────────────────────────────────────
# 7) Prepare XGBoost DMatrix and train
dtrain = xgb.DMatrix(np.column_stack([train_preds, X_train]), label=y_train)
dtest  = xgb.DMatrix(np.column_stack([test_preds,  X_test]),  label=y_test)

params = {
    "objective": "binary:logistic",
    "eval_metric": "auc"
}
bst = xgb.train(params, dtrain, num_boost_round=50)

bst.save_model("models/xgb.model")
print("Saved XGBoost model to models/xgb.model")

# ──────────────────────────────────────────────────────────────────────────────
# 8) Evaluate ensemble
xgb_preds = bst.predict(dtest)
print("Final ROC‑AUC:", roc_auc_score(y_test, xgb_preds))
print("Final Precision:", precision_score(y_test, xgb_preds > 0.5))

