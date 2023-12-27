import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
AUTH_SESSION_NAME = "auth_token"

MONTH_NAMES = {
    "01": "Jan",
    "02": "Feb",
    "03": "Mar",
    "04": "Apr",
    "05": "May",
    "06": "Jun",
    "07": "Jul",
    "08": "Aug",
    "09": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec",
}

EMBEDDING_MODEL = os.environ.get(
    "EMBEDDING_MODEL",
    "sentence-transformers/paraphrase-xlm-r-multilingual-v1")   
QDRANT_URL = os.environ.get("QDRANT_URL", "http://localhost:6333")
QDRANT_TOKEN = os.environ.get("QDRANT_TOKEN", None)
QDRANT_COLLECTION_NAME = os.environ.get("QDRANT_COLLECTION_NAME", "source_code")
CODE_LLAMA2 = os.environ.get("CODE_LLAMA2", "microsoft/CodeGPT-small-py")
