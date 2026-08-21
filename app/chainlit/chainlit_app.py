import chainlit as cl
from app.rag.generator import generate_response

@cl.on_chat_start
async def start():
    await cl.Message(
<<<<<<< Updated upstream
        content="# Alfa Focus Knowledge Assistant\nWelcome! Ask me any accounting or business question."
=======
        content="# Alfa Focus Knowledge Assistant\nWelcome! Ask me any question."
>>>>>>> Stashed changes
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
<<<<<<< Updated upstream
    
    msg = cl.Message(content="")
    await msg.send()

    try:
        
        reply_text = await cl.make_async(generate_response)(message.content)
        msg.content = reply_text
    except Exception as e:
        msg.content = f"⚠️ 生成回答时出错: {str(e)}"

    
    await msg.update()
=======
   
    try:
        reply_text = generate_response(message.content)
    except Exception as e:
        reply_text = f"Error generating response: {str(e)}"

    await cl.Message(content=reply_text).send()
>>>>>>> Stashed changes
