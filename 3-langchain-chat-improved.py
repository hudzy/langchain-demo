import os
import random
import string

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

SYSTEM_MESSAGE = (
    "You're a helpful assistant. Respond in plain text, less than 30 words."
)

# Store to hold chat histories for different sessions
session_store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Retrieve or initialize chat history for a session."""
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]


def setup_llm() -> ChatOpenAI:
    """Set up and return an ChatOpenAI instance."""
    return ChatOpenAI(
        base_url=ENDPOINT,
        model=MODEL_NAME,
        api_key=API_KEY,
        temperature=0,
    )


def create_prompt(system_message: str) -> ChatPromptTemplate:
    """Create and return a prompt template with a configurable system message."""
    return ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )


def setup_runnable(prompt, llm) -> RunnableWithMessageHistory:
    """Set up and return a RunnableWithMessageHistory instance."""
    return RunnableWithMessageHistory(
        prompt | llm,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )


def generate_session_id(length=8) -> str:
    """Generate a random session ID of lowercase letters and numbers."""
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def main():
    # Set up prompt and LLM
    prompt = create_prompt(SYSTEM_MESSAGE)
    llm = setup_llm()
    with_message_history = setup_runnable(prompt, llm)

    # Generate a random session ID
    session_id = generate_session_id()
    print(f"Generated Session ID: {session_id}")

    # Start a conversation loop
    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Conversation ended.")
            break

        try:
            # Invoke the LLM with user input and session history
            ai_msg = with_message_history.invoke(
                {"question": user_input},
                config={"configurable": {"session_id": session_id}},
            )

            # Print the AI's response
            print(f"AI: {ai_msg.content}")
            #  print(f"token_usage: {ai_msg.response_metadata}")

            # Extract and print token usage from response metadata
            #  if (
            #      "response_metadata" in ai_msg
            #      and "token_usage" in ai_msg["response_metadata"]
            #  ):
            #      token_usage = ai_msg["response_metadata"]["token_usage"]
            #      print(f"Token Usage: {token_usage}")

        except Exception as e:
            print(f"Error during invocation: {e}")


if __name__ == "__main__":
    main()
