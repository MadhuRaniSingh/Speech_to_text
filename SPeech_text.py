from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from googletrans import Translator

app = Flask(__name__)

# Initialize recognizer
recognizer = sr.Recognizer()
translator = Translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize_speech():
    # Capture audio from the microphone
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    # Perform speech recognition
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand audio.")
        return "Sorry, I could not understand audio."
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return "Could not request results; {0}".format(e)

@app.route('/translate', methods=['POST'])
def translate_text():
    request_data = request.get_json()
    text = request_data['text']
    language = request_data['language']

    translated_text = translator.translate(text, dest=language).text
    return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)
