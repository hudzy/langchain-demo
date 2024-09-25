import os

from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from neo4j import GraphDatabase

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

llm = ChatOpenAI(
    base_url=ENDPOINT,
    model=MODEL_NAME,
    api_key=API_KEY,
    temperature=0,
)

# NEO4J connection
neo4j_uri = "bolt://neo4j:7687"
neo4j_user = "neo4j"
neo4j_password = "langchain"

graph = Neo4jGraph(
    url=neo4j_uri, username=neo4j_user, password=neo4j_password, enhanced_schema=False
)

graph.refresh_schema()
#  print(graph.schema)

neo4j_query = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    allow_dangerous_requests=True,
)
#  neo4j_query.get_prompts()[0].pretty_print()

#  Who acted in The Shawshank Redemption, and the according role
#  List movies released in 1994
#  List all drama movies
#  List movies that has same director, also list director name

#  user_question = input("Enter your question: ")
#  neo4j_result = neo4j_query.invoke({"query": user_question})
#  neo4j_result = neo4j_query.invoke(
#      {"query": "Who acted in The Shawshank Redemption, and the according role"}
#  )
#  print(f"Result: {neo4j_result["result"]}")

while True:
    user_question = input("Enter your question (or type 'exit' to quit): ")

    if user_question.lower() == "exit":
        print("Goodbye!")
        break

    neo4j_result = neo4j_query.invoke({"query": user_question})

    print(f"Result: {neo4j_result['result']}")
