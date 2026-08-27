from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from app.config import settings

load_dotenv()

client = InferenceClient(
    provider="hf-inference",
    api_key=settings.HF_TOKEN,
)

text = "Employees may claim reasonable travel expenses."

embedding = client.feature_extraction(
    text,
    model="BAAI/bge-m3",
)

print("Text:", text)
print("Embedding dimensions:", len(embedding))
print("First 5 values:", embedding[:5])