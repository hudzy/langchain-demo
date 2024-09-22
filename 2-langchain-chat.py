import os

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import AzureChatOpenAI, ChatOpenAI


# Deepseek
API_KEY = "sk-axxxxx"
ENDPOINT = "https://api.deepseek.com"
MODEL_NAME = "deepseek-chat"


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're a helpful assistant. Respond in plain text, less than 30 words.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)

llm = ChatOpenAI(
    base_url=ENDPOINT,
    model=MODEL_NAME,
    api_key=API_KEY,
    temperature=0,
)

chain = prompt | llm

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)

ai_msg = with_message_history.invoke(
    {"question": "What is the name of imdb top 1 movie?"},
    config={"configurable": {"session_id": "abc123"}},
)
print(ai_msg.content)

ai_msg = with_message_history.invoke(
    {"question": "which org created you?"},
    config={"configurable": {"session_id": "abc123"}},
)
print(ai_msg.content)

ai_msg = with_message_history.invoke(
    {"question": "repeat my first question"},
    config={"configurable": {"session_id": "abc123"}},
)
print(ai_msg.content)
#  print(ai_msg)
print(store)