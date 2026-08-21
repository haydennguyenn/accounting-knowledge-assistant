from app.config import settings

SYSTEM_PROMPT_TEMPLATE = (
    "You are an expert Accounting Knowledge Assistant for Alfa Focus. "
    "Provide accurate, professional, and clear responses to all queries."
)

USER_PROMPT_TEMPLATE = """Context: {context}

Query: {query}
Answer:"""


def get_formatted_prompt(query: str, context: str = "No additional context provided.") -> str:
    return USER_PROMPT_TEMPLATE.format(query=query, context=context)


def generate_response_gemini(prompt: str, system_prompt: str = SYSTEM_PROMPT_TEMPLATE) -> str:
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured.")

    from google import genai
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=f"{system_prompt}\n\n{prompt}",
    )
    return response.text or ""

def generate_response_groq(prompt: str, system_prompt: str = SYSTEM_PROMPT_TEMPLATE) -> str:
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not configured.")

    from groq import Groq
    client = Groq(api_key=settings.GROQ_API_KEY)
    completion = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    return completion.choices[0].message.content or ""

def generate_response(query: str) -> str:
    prompt = get_formatted_prompt(query=query)
    if settings.GROQ_API_KEY:
        return generate_response_groq(prompt)
    return generate_response_gemini(prompt)


if __name__ == "__main__":
    test_query = "What is the primary function of this accounting assistant?"
    prompt = get_formatted_prompt(test_query)

    print("=== Testing Prompt Template ===")
    print(prompt)
    print("\n" + "="*40 + "\n")

    print("=== Testing LLM 1: Groq ===")
    try:
        res_groq = generate_response_groq(prompt)
        print("Groq Response:\n", res_groq)
    except Exception as e:
        print(f"Groq Error: {e}")

    print("\n" + "="*40 + "\n")

    print("=== Testing LLM 2: Google Gemini ===")
    try:
        res_gemini = generate_response_gemini(prompt)
        print("Gemini Response:\n", res_gemini)
    except Exception as e:
        print(f"Gemini Error: {e}")