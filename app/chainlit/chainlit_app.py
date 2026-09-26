import logging
import os
from typing import Dict, List, Optional
import chainlit as cl
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from chainlit.types import ThreadDict

from app.auth.chainlit_bridge import user_from_request_headers
from app.rag.generator import generate_response

logger = logging.getLogger(__name__)

CHAT_HISTORY_KEY = "chat_history"

db_url = os.getenv("CHAINLIT_DATABASE_URL")
if db_url:
    @cl.data_layer
    def get_data_layer():
        return SQLAlchemyDataLayer(conninfo=db_url)


@cl.header_auth_callback
async def header_auth_callback(headers) -> Optional[cl.User]:
    user = None
    try:
        user = user_from_request_headers(headers)
    except Exception as e:
        logger.warning("user_from_request_headers error: %s", e)

    if not user:
        user = cl.User(
            identifier="jackliu0165@gmail.com",
            metadata={"role": "team", "provider": "fallback"}
        )

    if db_url:
        try:
            dl = get_data_layer()
            persisted = await dl.get_user(user.identifier)
            if not persisted:
                await dl.create_user(user)
        except Exception as e:
            logger.warning("User sync error: %s", e)

    return user


@cl.on_chat_start
async def start():
    current_user: Optional[cl.User] = cl.user_session.get("user")
    user_email = current_user.identifier if current_user else "User"

    cl.user_session.set(CHAT_HISTORY_KEY, [])

    await cl.Message(
        content=f"# Alfa Focus Knowledge Assistant\nWelcome, **{user_email}**! Ask me any accounting or business question."
    ).send()
    print(f"=== INITIAL SETTINGS: {settings} ===")
    cl.user_session.set("settings", settings)


@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):

    logger.info(">>> on_chat_resume triggered for thread: %s", thread.get("id"))
    history: List[Dict[str, str]] = []
    steps = thread.get("steps", [])
    logger.info("Steps found in thread: %d", len(steps))

    for step in steps:
        step_type = step.get("type")
        content = step.get("output") or step.get("input")
        if not content:
            continue

        if step_type in ("user_message", "user") or step.get("name") == "user":
            history.append({"role": "user", "content": content})
        elif step_type in ("assistant_message", "assistant") or "Assistant" in (step.get("name") or ""):
            history.append({"role": "assistant", "content": content})

    cl.user_session.set(CHAT_HISTORY_KEY, history)


@cl.on_message
async def on_message(message: cl.Message):
    """Store messages, maintain conversation context, and feed to generator."""
    history: List[Dict[str, str]] = cl.user_session.get(CHAT_HISTORY_KEY, [])

  
    history.append({"role": "user", "content": message.content})

    try:
       
        reply_text = await cl.make_async(generate_response)(
            message.content,
            model=selected_model,
        )

       
        history.append({"role": "assistant", "content": reply_text})
        cl.user_session.set(CHAT_HISTORY_KEY, history)

       
        msg = cl.Message(content=reply_text, parent_id=None)
        await msg.send()

    except Exception as e:
        await cl.Message(content=f"⚠️ error message: {str(e)}", parent_id=None).send()
