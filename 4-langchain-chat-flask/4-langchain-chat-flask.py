import os
import random
import string

from flask import Flask, jsonify, render_template, request
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import AzureChatOpenAI, ChatOpenAI


# Configuration variables
# Deepseek
API_KEY = "sk-axxxxx"
ENDPOINT = "https://api.deepseek.com"
MODEL_NAME = "deepseek-chat"


SYSTEM_MESSAGE = (
    #  "You're a helpful assistant. Respond in plain text, less than 30 words."
    "You're a helpful assistant."
)

app = Flask(__name__)


# Serve the HTML file from the static folder
@app.route("/")
def index():
    return render_template("index.html")


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


#  def setup_llm() -> AzureChatOpenAI:
#      """Set up and return an AzureChatOpenAI instance."""
#      return AzureChatOpenAI(
#          api_version="2024-06-01",
#          azure_endpoint=ENDPOINT,
#          model_name=MODEL_NAME,
#          api_key=API_KEY,
#          temperature=0,
#      )


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


# Route for handling the conversation
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("question")
    session_id = request.json.get("session_id")

    # If no session ID is provided, generate one
    if not session_id:
        session_id = generate_session_id()

    try:
        # Set up prompt and LLM with system message
        prompt = create_prompt(SYSTEM_MESSAGE)
        llm = setup_llm()
        with_message_history = setup_runnable(prompt, llm)

        # Invoke the LLM with user input and session history
        ai_msg = with_message_history.invoke(
            {"question": user_input},
            config={"configurable": {"session_id": session_id}},
        )

        # Extract token usage and send response back to frontend
        response_data = {"response": ai_msg.content, "session_id": session_id}

        if (
            "response_metadata" in ai_msg
            and "token_usage" in ai_msg["response_metadata"]
        ):
            token_usage = ai_msg["response_metadata"]["token_usage"]
            response_data["token_usage"] = token_usage

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
