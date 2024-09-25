import os

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import AzureChatOpenAI, ChatOpenAI

# Deepseek
# API_KEY = os.getenv("DEEPSEEK_API_KEY")
# ENDPOINT = "https://api.deepseek.com"
# MODEL_NAME = "deepseek-chat"

# Github marketplace
# API_KEY = os.getenv("GITHUB_MARKETPLACE_API_KEY")
# ENDPOINT = "https://models.inference.ai.azure.com"
# MODEL_NAME = "gpt-4o"

# Cloudflare Worker AI
API_KEY = os.getenv("CLOUDFLARE_WORKER_AI_API_KEY")
ACCOUNT_ID = os.getenv("CLOUDFLARE_WORKER_AI_ACCOUNT_ID")
ENDPOINT = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/v1"
MODEL_NAME = "@cf/meta/llama-3.1-8b-instruct"

os.environ["SSL_CERT_FILE"] = os.getenv("REQUESTS_CA_BUNDLE")

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
