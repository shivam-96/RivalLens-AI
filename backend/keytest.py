import os
from openai import OpenAI

# Use the OPENAI_API_KEY environment variable (e.g., from your .env file)
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say 'API key works!'"}]
    )
    print("SUCCESS: API key is working!")
    print(response.choices[0].message.content)

except Exception as e:
    print("FAILURE: API key is NOT working")
    print("Error:", str(e))