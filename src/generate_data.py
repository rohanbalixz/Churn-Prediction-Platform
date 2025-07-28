import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Number of rows to generate
n_rows = 1000

# Define possible event types
event_types = ["login", "click", "logout", "view", "purchase"]

# Generate data
data = []
start_date = datetime(2025, 1, 1)
for user_id in range(1, n_rows + 1):
    # Random timestamp within first 6 months of 2025
    random_seconds = random.randint(0, 6 * 30 * 24 * 3600)
    event_timestamp = (start_date + timedelta(seconds=random_seconds)).isoformat()
    event_type = random.choice(event_types)
    feature1 = round(np.random.rand(), 3)
    feature2 = random.randint(0, 1)
    # Simulate churn with 20% probability
    churned = int(random.random() < 0.2)
    data.append({
        "user_id": user_id,
        "event_timestamp": event_timestamp,
        "event_type": event_type,
        "feature1": feature1,
        "feature2": feature2,
        "churned": churned
    })

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv("data/sample_events.csv", index=False)

print(f"Generated {len(df)} rows in data/sample_events.csv")

