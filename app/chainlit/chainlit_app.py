import logging
from typing import Dict, List, Optional
import chainlit as cl

from app.auth.chainlit_bridge import user_from_request_headers
from app.rag.generator import generate_response

logger = logging.getLogger(__name__)

# Key for storing user chat history in the isolated session state
CHAT_HISTORY_KEY = "chat_history"


@cl.header_auth_callback
def header_auth_callback(headers) -> Optional[cl.User]:
    """Accept the FastAPI aka_session cookie — Chainlit does not check passwords (AU-84)."""
    try:
        user = user_from_request_headers(headers)
        if user:
            return user
    except Exception as e:
        logger.warning("user_from_request_headers error: %s", e)

    # Fallback identity for local dev/testing if cookie headers are absent during handshake
    return cl.User(identifier="jackliu0165@gmail.com", metadata={"role": "team", "provider": "fallback"})


@cl.on_chat_start
async def start():
    """Triggered when a user opens a new chat session (Implement session state & reset)."""
    current_user: Optional[cl.User] = cl.user_session.get("user")
    user_email = current_user.identifier if current_user else "User"

    # Initialize isolated message history for the active session state
    cl.user_session.set(CHAT_HISTORY_KEY, [])

    await cl.Message(
        content=f"# Alfa Focus Knowledge Assistant\nWelcome, **{user_email}**! Ask me any accounting or business question."
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    """Store conversation messages, maintain conversation context, and feed to generator."""
    # Retrieve current user's isolated session history
    history: List[Dict[str, str]] = cl.user_session.get(CHAT_HISTORY_KEY, [])

    # Record the user's latest query into the active history
    history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    try:
        # Pass user query and full conversation history buffer into the generator
        reply_text = await cl.make_async(generate_response)(
            query=message.content,
            history=history,
        )

        # Append assistant's response to the conversation context
        history.append({"role": "assistant", "content": reply_text})
        cl.user_session.set(CHAT_HISTORY_KEY, history)

        msg.content = reply_text
    except Exception as e:
        msg.content = f"error message: {str(e)}"

    await msg.update()