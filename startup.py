import subprocess
import sys
import os

print("=== Startup: Downloading dataset ===")
subprocess.run([sys.executable, "download_data.py"], check=True)

print("=== Startup: Launching Uvicorn ===")
port = os.environ.get("PORT", "8000")
os.execvp("uvicorn", ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", port])
