from app.config import settings


def test_environment_configuration():
    "Verify that required environment variables are loaded."

    assert settings.GEMINI_API_KEY, "GEMINI_API_KEY is missing"
    assert settings.GROQ_API_KEY, "GROQ_API_KEY is missing"
    assert settings.HF_TOKEN, "HF_TOKEN is missing"
    assert settings.SUPABASE_DB_URL, "SUPABASE_DB_URL is missing"

    assert settings.GEMINI_MODEL, "GEMINI_MODEL is missing"
    assert settings.GROQ_MODEL, "GROQ_MODEL is missing"

    print("✓ Environment configuration loaded successfully")