import os
from groq import Groq

with open('api key.txt', 'r') as f:
    key = f.read()

client = Groq(api_key=key)

prompt = 'You are a sentiment analysis assistant.' \
         'You reply with an in-depth sentiment analysis of the ' \
         'message you receive with an explanation, and nothing else.'
message = "Mo jobs, no money.  how in the hell is min wage here 4 f'n clams an hour?"

chat_completion = client.chat.completions.create(
    messages=[
        {
            'role': 'system',
            'content': prompt
        },
        {
            "role": "user",
            "content": message,
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)