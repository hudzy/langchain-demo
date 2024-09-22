import os

from openai import OpenAI

# Deepseek
token = "sk-axxxxx"
endpoint = "https://api.deepseek.com"
model_name = "deepseek-chat"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            #  "content": "What is the capital of France?",
            "content": "write a short description for IMDB top 3 movies, including the name, genre, release date, director and cast",
        },
    ],
    model=model_name,
    temperature=0,
    max_tokens=1000,
    top_p=1.0,
)

print(response.choices[0].message.content)
#  print(response)