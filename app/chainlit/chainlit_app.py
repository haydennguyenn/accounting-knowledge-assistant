import chainlit as cl

@cl.on_chat_start
async def start():
    await cl.Message(content="# Alfa Focus Knowledge Assistant").send()

@cl.on_message
async def on_message(message: cl.Message):
    await cl.Message(content=f"Placeholder response — received: {message.content}").send()