from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('index.html')

    # METHOD = POST
    with open('api key.txt') as f:
        api_key = f.read()
    groq_client = Groq(api_key=api_key)

    instructions: str = \
        'You are a sentiment analysis assistant.' \
        'You reply with an in-depth sentiment analysis of the ' \
        'message you receive with an explanation.' \
        'You recognize contrasting sentiments in the same text and ' \
        'explain the dynamics between them.' \
        'Lastly, you add a summary of your analysis in a new line.'
    message = request.form['text']

    groq_response = \
        groq_client.chat.completions.create(
            messages=[
                {
                    'role': 'system',
                    'content': instructions
                },
                {
                    'role': 'user',
                    'content': message
                }
            ],
            model='llama3-8b-8192'
        )
    sentiment = groq_response.choices[0].message.content

    return render_template('index.html',
                           sentiment=sentiment, message=message)



if __name__ == '__main__':
    app.run(debug=True)