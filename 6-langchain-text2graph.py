import os
import pickle

from langchain_community.document_loaders import TextLoader
from langchain_community.graphs import Neo4jGraph
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_experimental.graph_transformers.llm import LLMGraphTransformer
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain_text_splitters.character import RecursiveCharacterTextSplitter


# Deepseek
API_KEY = "sk-axxxxx"
ENDPOINT = "https://api.deepseek.com/beta"
MODEL_NAME = "deepseek-chat"


llm = ChatOpenAI(
    base_url=ENDPOINT,
    model=MODEL_NAME,
    api_key=API_KEY,
    temperature=0,
    max_tokens=8000,
)

# Load the document
loaded_documents = TextLoader(file_path="imdbtop15.txt").load()

# Split the document into chunks
documents_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=300)
splitted_documents = documents_splitter.split_documents(documents=loaded_documents)


# Transform documents into graph-based documents using a LLM
llm_graph_transformer = LLMGraphTransformer(
    llm=llm,
    allowed_nodes=["Person", "Movie", "Character", "Genre", "Year"],
    allowed_relationships=[
        "RELEASED_IN",
        "GENRE",
        "ACTED_IN",
        "DIRECTED_BY",
        "PERFORMED_AS",
    ],
)
graph_documents = llm_graph_transformer.convert_to_graph_documents(splitted_documents)
local_file = "graph_documents.pkl"

with open(local_file, "wb") as f:
    pickle.dump(graph_documents, f)

with open(local_file, "rb") as f:
    graph_documents = pickle.load(f)
print(graph_documents)

# NEO4J connection
neo4j_uri = "bolt://neo4j:7687"
neo4j_user = "neo4j"
neo4j_password = "langchain"

graph = Neo4jGraph(url=neo4j_uri, username=neo4j_user, password=neo4j_password)
graph.add_graph_documents(graph_documents, baseEntityLabel=False, include_source=False)

# MATCH (n) DETACH DELETE n;
# MATCH (n)-[r]->(m) RETURN n, r, m;
