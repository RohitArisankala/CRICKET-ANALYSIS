import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace 'YOUR_GEMINI_API_KEY' with your actual Gemini API key
GEMINI_API_KEY = 'AIzaSyCIvK9ehOk_MTam_emDp_sAzlXL5xE2Bgc'
GEMINI_API_URL = 'https://api.gemini.com/v1/chat'

def query_wikipedia(query):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('extract', 'No summary available.')
    else:
        return 'Error fetching data from Wikipedia.'

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    # Query Wikipedia
    wiki_response = query_wikipedia(user_input)

    # Create the payload for the Gemini API
    payload = {
        'model': 'gemini',
        'prompt': f"User asked about: {user_input}\nWikipedia summary: {wiki_response}",
        'max_tokens': 150
    }

    headers = {
        'Authorization': f'Bearer {GEMINI_API_KEY}',
        'Content-Type': 'application/json'
    }

    # Make the request to the Gemini API
    response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        gemini_response = response.json()
        return jsonify({'response': gemini_response['choices'][0]['text']})
    else:
        return jsonify({'error': 'Error communicating with Gemini API'}), 500

if __name__ == '__main__':
    app.run(debug=True)
