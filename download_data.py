import os
from datasets import load_dataset
import pandas as pd

print("Downloading dataset...")
ds = load_dataset("ManikaSaini/zomato-restaurant-recommendation")
os.makedirs("data", exist_ok=True)
csv_path = os.path.join("data", "zomato.csv")
ds["train"].to_csv(csv_path, index=False)
print(f"Dataset saved to {csv_path}")

df = pd.read_csv(csv_path)
print("\n--- Columns ---")
print(df.columns.tolist())
print("\n--- First 3 rows ---")
print(df.head(3).to_dict(orient="records"))
