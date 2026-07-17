import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "zomato.csv")
TOP_N_CANDIDATES = 20
CACHE_TTL_SECONDS = 3600
