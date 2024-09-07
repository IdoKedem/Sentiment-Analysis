from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)

def get_groq_client():
    with open('api key.txt') as f:
        api_key = f.read()
    return Groq(api_key=api_key)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analyze-text', methods=['GET', 'POST'])
def analyze_text():
    if request.method == 'GET':
        return render_template('analyze_text.html')

    # METHOD = POST

    message = request.form['text']

    groq_client = get_groq_client()
    instructions: str = \
        'You are a sentiment analysis assistant.' \
        'You reply with an in-depth sentiment analysis and ' \
        'the emotion in the message you receive, with an explanation.' \
        'You recognize contrasting sentiments in the same text and ' \
        'explain the dynamics between them.' \
        'Additionally, you provide your Confidence Level (in percentages), how confident you are' \
        'the message is positive, neutral or negative. For example:' \
        'CONFIDENCE LEVEL: 85% positive, 10% neutral and 5% negative. no explanation needed ' \
        'Lastly, you add a summary of your analysis.'

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

    return render_template('analyze_text.html', sentiment=sentiment,
                           message=message)


@app.route('/compare-texts', methods=['GET', 'POST'])
def compare_texts():
    if request.method == 'GET':
        return render_template('compare_texts.html')

    #METHOD = POST

    text1 = request.form['text1']
    text2 = request.form['text2']

    groq_client = get_groq_client()
    instructions: str = \
        'You are a sentiment analysis assistant.' \
        'You receive two texts, the first text and the second text and analyze their sentiments.' \
        'After doing so, you reply with a comparison between the sentiments of the two texts.' \
        'In your comparison, refer to the meaning of the text, as well as ' \
        'capital letters and punctuation marks, as they often ' \
        'change the sentiment of a text.' \
        'For example, the text "YES!" shows more excitement than a simple "yes", ' \
        'Lastly, you summarize your comparison to a few lines at the end of your reply'
    groq_response = \
        groq_client.chat.completions.create(
            messages=[
                {
                    'role': 'system',
                    'content': instructions
                },
                {
                    'role': 'user',
                    'content': f'the first text: {text1}, the second text: {text2}'
                }
            ],
            model='llama3-8b-8192'
        )
    comparison = groq_response.choices[0].message.content
    return render_template('compare_texts.html', comparison=comparison,
                           text1=text1, text2=text2)

if __name__ == '__main__':
    app.run(debug=True)