from llama_index.core.llms import ChatMessage,MessageRole
from llm_factory.get_llm import get_ollama

def get_answer(model_name,chat_history):
    llm = get_ollama(model_name)
    messages = [
        ChatMessage(
        role = MessageRole.SYSTEM,content = "You are a helpful assistant."
        )
    ]

    messages.extend(
        ChatMessage(role = MessageRole[msg["role"].upper()],content = msg["content"])
        for msg in chat_history
    )
# Message.USER = MessageRole["USER"]
    response = llm.chat(messages = messages)
    return response.message.content