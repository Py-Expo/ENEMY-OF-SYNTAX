from flask import Flask, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import spacy

app = Flask(__name__)

# Initialize ChatBot with a specific storage adapter for persistent storage
chatbot = ChatBot(
    'CustomerSupportBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3'
)

# Optionally, train the chatbot on additional data
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')  # Train on English corpus

# Load spaCy model for advanced NLP
nlp = spacy.load('en_core_web_sm')

def process_message(user_message):
    # Perform advanced NLP tasks like named entity recognition, sentiment analysis, etc.
    doc = nlp(user_message)
    # Implement your custom logic for processing the message, extracting entities, etc.
    return doc

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if user_message:
        # Process the user message using advanced NLP techniques
        processed_message = process_message(user_message)
        # Get a response from the chatbot based on the processed message
        response = chatbot.get_response(processed_message.text)
        return jsonify({"message": str(response)})
    else:
        return jsonify({"message": "No message received."}), 400

if __name__ == '__main__':
    app.run(debug=True)