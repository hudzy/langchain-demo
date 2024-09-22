import os

from langchain.chains import LLMChain, SimpleSequentialChain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import AzureChatOpenAI, ChatOpenAI


# Deepseek
API_KEY = "sk-axxxxx"
ENDPOINT = "https://api.deepseek.com"
MODEL_NAME = "deepseek-chat"


article_template = "You're a professional in movies. Write an article about top {number} IMDb movie, covering the cast, director, genre, release year, keep it short but still covers the required fields."
article_prompt = PromptTemplate(template=article_template)

summary_template = """Summary each movie in the article about IDMb movies strictly following below format:
1. **It's a Wonderful Life**
   - *Year*: 1946
   - *Director*: Frank Capra
   - *Genre*: Drama, Family, Fantasy
   - *Cast*: James Stewart (as George Bailey)
   - *Cast*: Donna Reed (as Mary Hatch)
   - *Cast*: Lionel Barrymore (as Mr. Potter)
Here's the article:
{article}
"""
summary_prompt = PromptTemplate(template=summary_template)

llm = ChatOpenAI(
    base_url=ENDPOINT,
    model=MODEL_NAME,
    api_key=API_KEY,
    temperature=0,
)


article_chain = article_prompt | llm
summary_chain = summary_prompt | llm

sequential_chain = article_chain | summary_chain

imdb_result = sequential_chain.invoke("3")

print(imdb_result.content)
