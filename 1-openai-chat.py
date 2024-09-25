import os

from openai import OpenAI

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
