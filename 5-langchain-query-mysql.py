import os
from operator import itemgetter

from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
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

llm = ChatOpenAI(
    base_url=ENDPOINT,
    model=MODEL_NAME,
    api_key=API_KEY,
    temperature=0,
)

query_template = """You are a MySQL expert. Given an input question, create a syntactically correct MySQL query.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURDATE() function to get the current date, if the question involves "today".

Only use the following tables:
{table_info}

Question: {input}

return the query in text format only"""

query_prompt = PromptTemplate(
    input_variables=["input", "table_info"],
    input_types={},
    partial_variables={"top_k": "5"},
    template=query_template,
)

answer_template = """Given the following user question, corresponding SQL query, and SQL result, you will: return the executed SQL query, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Executed query and Answer: """
answer_prompt = PromptTemplate(template=answer_template)

# MySQL connection
mysql_uri = "mysql"
mysql_user = "langchain"
mysql_password = "langchain"
mysql_db = "langchain"

db = SQLDatabase.from_uri(
    f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_uri}/{mysql_db}"
)

#  print(db.get_usable_table_names())
#  print(db.run("SELECT * FROM students LIMIT 5;"))


compose_query = create_sql_query_chain(llm=llm, db=db, prompt=query_prompt)
strip_query = RunnableLambda(lambda x: "\n".join(x.splitlines()[1:-1]))
execute_query = QuerySQLDataBaseTool(db=db, verbose=False)
#  query_chain = compose_query | strip_query | execute_query
#  mysql_result = query_chain.invoke({"question": "Who got the lowest grade and why?"})
#  print(mysql_result)

query_chain = (
    RunnablePassthrough.assign(query=compose_query).assign(
        result=itemgetter("query") | strip_query | execute_query
    )
    | answer_prompt
    | llm
)
#  query_chain.get_prompts()[0].pretty_print()
#  query_chain.get_prompts()[1].pretty_print()

# Who got the lowest grade and why?
# calculate the average score
# calculate the average score except 0 scores
# get the parents info of the student with the lowest score

#  user_question = input("Enter your question: ")
#  question_result = query_chain.invoke({"question": user_question})
#  question_result = query_chain.invoke({"question": "Who got the lowest grade and why?"})
#  print(question_result.content)

while True:
    user_question = input("Enter your question (or type 'exit' to quit): ")

    if user_question.lower() == "exit":
        print("Goodbye!")
        break

    question_result = query_chain.invoke({"question": user_question})

    print(question_result.content)
