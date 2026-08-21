<<<<<<< Updated upstream
from app.config import settings

=======
from google import genai
from app.config import settings

# 1. Prompt 模板
>>>>>>> Stashed changes
SYSTEM_PROMPT_TEMPLATE = (
    "You are an expert Accounting Knowledge Assistant for Alfa Focus. "
    "Provide accurate, professional, and clear responses to all queries."
)

USER_PROMPT_TEMPLATE = """Context: {context}

Query: {query}
Answer:"""


def get_formatted_prompt(query: str, context: str = "No additional context provided.") -> str:
    return USER_PROMPT_TEMPLATE.format(query=query, context=context)


<<<<<<< Updated upstream
def generate_response_gemini(prompt: str, system_prompt: str = SYSTEM_PROMPT_TEMPLATE) -> str:
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured.")

    from google import genai
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
=======
# 2. 调用 Key 1
def generate_response_key1(prompt: str, system_prompt: str = SYSTEM_PROMPT_TEMPLATE) -> str:
    if not settings.GEMINI_API_KEY_1:
        raise ValueError("GEMINI_API_KEY_1 is not set.")

    client = genai.Client(api_key=settings.GEMINI_API_KEY_1)
>>>>>>> Stashed changes
    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=f"{system_prompt}\n\n{prompt}",
    )
    return response.text or ""

<<<<<<< Updated upstream
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


=======

# 3. 调用 Key 2（备用/测试）
def generate_response_key2(prompt: str, system_prompt: str = SYSTEM_PROMPT_TEMPLATE) -> str:
    if not settings.GEMINI_API_KEY_2:
        raise ValueError("GEMINI_API_KEY_2 is not set.")

    client = genai.Client(api_key=settings.GEMINI_API_KEY_2)
    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=f"{system_prompt}\n\n{prompt}",
    )
    return response.text or ""


# 默认聊天调用入口
def generate_response(query: str) -> str:
    prompt = get_formatted_prompt(query=query)
    return generate_response_key1(prompt)


# 4. 占位测试脚本
>>>>>>> Stashed changes
if __name__ == "__main__":
    test_query = "What is the primary function of this accounting assistant?"
    prompt = get_formatted_prompt(test_query)

    print("=== Testing Prompt Template ===")
    print(prompt)
    print("\n" + "="*40 + "\n")

<<<<<<< Updated upstream
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
=======
    print("=== Testing Key 1 (Gemini) ===")
    try:
        res1 = generate_response_key1(prompt)
        print("Gemini Key 1 Response:\n", res1)
    except Exception as e:
        print(f"Key 1 Error: {e}")

    print("\n" + "="*40 + "\n")

    print("=== Testing Key 2 (Gemini) ===")
    try:
        res2 = generate_response_key2(prompt)
        print("Gemini Key 2 Response:\n", res2)
    except Exception as e:
        print(f"Key 2 Error: {e}")
>>>>>>> Stashed changes
