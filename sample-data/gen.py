import pandas as pd
import json

# Generate sample data
data = {
    "id": range(1, 21),
    "name": [f"Name_{i}" for i in range(1, 21)],
    "age": [25 + (i % 5) for i in range(1, 21)],
    "email": [f"user{i}@example.com" for i in range(1, 21)],
    "signup_date": pd.date_range(start="2023-01-01", periods=20, freq="D").astype(str)
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV
csv_file_path = "./sample.csv"
df.to_csv(csv_file_path, index=False)

# Save to JSONL
jsonl_file_path = "./sample.jsonl"
with open(jsonl_file_path, 'w') as f:
    for row in df.to_dict(orient="records"):
        f.write(json.dumps(row) + "\n")

csv_file_path, jsonl_file_path
