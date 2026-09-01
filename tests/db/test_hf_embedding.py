from huggingface_hub import InferenceClient
from app.config import settings


def test_hf_embedding():
    """Verify that the Hugging Face inference client can generate embeddings."""
    assert settings.HF_TOKEN, "HF_TOKEN is missing or not set in configuration"

    client = InferenceClient(
        provider="hf-inference",
        api_key=settings.HF_TOKEN,
    )

    sample_text = "Employees may claim reasonable travel expenses."

    embedding = client.feature_extraction(
        sample_text,
        model="BAAI/bge-m3",
    )

    assert embedding is not None, "Failed to retrieve embedding (got None)"
    assert len(embedding) > 0, "Embedding vector is empty"
    # BAAI/bge-m3 typically outputs a 1024-dimension vector
    print(f"\n✓ Embedding generated successfully with dimension: {len(embedding)}")
