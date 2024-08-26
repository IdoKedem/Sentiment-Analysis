import os

from groq import Groq

with open('api key.txt', 'r') as f:
    key = f.read()

client = Groq(
    api_key=key
)

prompt = 'Analyze the sentiment of the following sentence:'
message = "I am usually happy but i have been feeling sad lately"

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt + message,
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)