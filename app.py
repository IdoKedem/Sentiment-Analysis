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
        return render_template('analyze_text.html', message='')

    # METHOD = POST

    message = request.form['text']

    groq_client = get_groq_client()
    instructions: str = (
        "You are a sentiment analysis assistant. Analyze the sentiment and emotion of the given message and "
            "respond with the following sections: \n"
        "1. **Sentiment Analysis:** Provide an in-depth analysis of the sentiment (positive, neutral, or negative)"
            " and the emotion (e.g., joy, sadness, anger) in the message. Include a detailed explanation. \n"
        "2. **Contrasting Sentiments:** If there are contrasting sentiments within the same message,"
            " explain the dynamics between them. \n"
        "3. **Confidence Level:** Provide your Confidence Level in percentages."
            " For example: 'CONFIDENCE LEVEL: 85% positive, 10% neutral, and 5% negative.'"
            " This section should only appear once, and no explanation is needed for the confidence breakdown. \n"
        "4. **Summary:** Conclude with a brief summary of your analysis in 1-2 sentences."
    )

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