import os
import sys
import pandas as pd

DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "zomato.csv")

def download_with_datasets():
    """Primary method: use HuggingFace datasets library."""
    from datasets import load_dataset
    print("Downloading dataset via HuggingFace datasets library...")
    ds = load_dataset("ManikaSaini/zomato-restaurant-recommendation")
    ds["train"].to_csv(CSV_PATH, index=False)
    print(f"Dataset saved to {CSV_PATH}")

def download_with_urllib():
    """Fallback method: download parquet directly from HuggingFace Hub."""
    import urllib.request
    import tempfile
    
    parquet_url = "https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation/resolve/main/data/train-00000-of-00001.parquet"
    print(f"Fallback: Downloading parquet from {parquet_url}...")
    
    tmp_path = os.path.join(DATA_DIR, "temp.parquet")
    urllib.request.urlretrieve(parquet_url, tmp_path)
    
    df = pd.read_parquet(tmp_path)
    df.to_csv(CSV_PATH, index=False)
    os.remove(tmp_path)
    print(f"Dataset saved to {CSV_PATH} ({len(df)} rows)")

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if os.path.exists(CSV_PATH):
        print(f"Dataset already exists at {CSV_PATH}, skipping download.")
        sys.exit(0)

    # Try primary method, fallback to direct download
    try:
        download_with_datasets()
    except Exception as e:
        print(f"Primary download failed: {e}")
        print("Trying fallback method...")
        try:
            download_with_urllib()
        except Exception as e2:
            print(f"Fallback download also failed: {e2}")
            sys.exit(1)
    
    # Verify
    df = pd.read_csv(CSV_PATH)
    print(f"Verification: {len(df)} rows, columns: {df.columns.tolist()}")
