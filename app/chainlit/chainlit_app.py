import logging
from typing import Dict, List, Optional
import chainlit as cl
import anyio
from typing import Optional
from chainlit.input_widget import Select

from app.auth.chainlit_bridge import user_from_request_headers
from app.rag.generator import generate_response

logger = logging.getLogger(__name__)

# Key for storing user chat history in the isolated session state
CHAT_HISTORY_KEY = "chat_history"


@cl.header_auth_callback
async def header_auth_callback(headers) -> Optional[cl.User]:
    """Accept the FastAPI aka_session cookie — Chainlit does not check passwords (AU-84).

    Chainlit calls POST /chat/auth/header before the WebSocket connects.
    That request carries the browser's aka_session cookie in its headers.
    user_from_request_headers decodes it and returns the corresponding cl.User.
    Returning None causes Chainlit to reject the connection with 401.
    """
    try:
        user = await anyio.to_thread.run_sync(user_from_request_headers, headers)
        if user:
            return user
        logger.warning("chainlit_header_auth_no_session_cookie")
    except Exception as e:
        logger.warning("user_from_request_headers error: %s", e)
    return None

@cl.on_chat_start
async def start():
    print("=== CHAT START FIRED ===")
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="AI Model",
                values=[
                    "gemini-3-8-flash",
                    "groq-gpt-oss-120b",
                    "openrouter-free",
                    "free-fallback",
                ],
                initial_index=0,
            ),
        ]
    ).send()
    print(f"=== INITIAL SETTINGS: {settings} ===")
    cl.user_session.set("settings", settings)


@cl.on_message
async def on_message(message: cl.Message):
    logger.info("on_message fired: %s", message.content)

    try:
        metadata = message.metadata or {}
        selected_model = metadata.get("model", "gemini-3-8-flash")

        logger.info("Selected model: %s", selected_model)
        print(f"=== REQUESTED MODEL: {selected_model} ===")
        print(f"=== ACTUAL LITELLM MODEL: {selected_model} ===")

        reply_text = await cl.make_async(generate_response)(
            message.content,
            model=selected_model,
        )

        logger.info(
            "generate_response returned: %s",
            reply_text[:200] if reply_text else "",
        )

    except Exception as e:
        logger.exception("generate_response error: %s", e)
        reply_text = f"⚠️ error message: {str(e)}"

    await cl.Message(content=reply_text).send()