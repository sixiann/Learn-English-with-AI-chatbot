from flask import Flask
from flask import render_template
from flask import Response, request, jsonify, send_file
app = Flask(__name__)
import tempfile
import subprocess
import shutil


#for gpt
import os
import openai

import secrets2
openai.api_key = secrets2.SECRET_KEY



#for dalle
import json
from base64 import b64decode
from pathlib import Path

@app.route('/transcribe_audio', methods=['POST'])
def transcribe_audio():
    try:
        audio_file = request.files['audio_file']
        if audio_file:
            # Save the uploaded audio file to a temporary directory
            temp_dir = tempfile.mkdtemp()
            audio_path = f"{temp_dir}/uploaded_audio.{audio_file.filename.split('.')[-1]}"
            audio_file.save(audio_path)

            # Use Whisper AI or any other speech-to-text service to transcribe the audio
            # Replace the following code with your Whisper AI integration
            transcription = transcribe_audio_with_whisper(audio_path)

            # Clean up the temporary directory
            shutil.rmtree(temp_dir)

            # Return the transcription result as JSON
            return jsonify({'text': transcription.text})
        else:
            return jsonify({'error': 'No audio file uploaded.'})
    except Exception as e:
        return jsonify({'error': str(e)})


def transcribe_audio_with_whisper(audio_path):
    # Implement the Whisper AI integration here to transcribe the audio
    # Replace this dummy implementation with the actual integration
    # Example using subprocess to call a hypothetical Whisper AI executable:
    try:
        audio_file = open(audio_path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        print(transcript)
        return transcript


    except Exception as e:
        print(f"Error transcribing audio: {str(e)}")
        return "Transcription failed"


@app.route('/')
def home():
    # you can pass in an existing article or a blank one.
    return render_template('home.html')   


if __name__ == '__main__':
    # app.run(debug = True, port = 4000)    
    app.run(debug = True)




