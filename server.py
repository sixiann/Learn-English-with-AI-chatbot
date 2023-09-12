from flask import Flask
from flask import render_template
from flask import request, jsonify
app = Flask(__name__)
import tempfile
import shutil


#for gpt
import openai

import secrets2
openai.api_key = secrets2.SECRET_KEY


@app.route('/transcribe_audio', methods=['POST'])
def transcribe_audio():
    try:
        audio_file = request.files['audio_file']
        if audio_file:
            # Save the uploaded audio file to a temporary directory
            temp_dir = tempfile.mkdtemp()
            audio_path = f"{temp_dir}/uploaded_audio.{audio_file.filename.split('.')[-1]}"
            audio_file.save(audio_path)

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
    try:
        audio_file = open(audio_path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        print(transcript)
        return transcript


    except Exception as e:
        print(f"Error transcribing audio: {str(e)}")
        return "Transcription failed"


@app.route('/generate_response', methods=['POST'])
def generate_response():
    try:
        data = request.get_json()
        transcription = data.get('transcription', '')
        feedback_type = data.get('feedback_type', '')  

        if feedback_type == "grammar": 
            prompt = "Tell me if this speech is grammatical: " + transcription + ". Format the response as \
                This speech is grammatical, or this speech is not grammatical. \
                    if it not grammatical, include how to fix the grammar error."
        elif feedback_type == "vocab":
            prompt = "Give me feedback about the vocabulary of this speech: " + transcription + ". \
            Do not mention anything about grammar. " 

        else:
            prompt = transcription + ". Continue this conversation as if you were talking to a friend. \
                Limit your response to 2 sentences."
            
        response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=256)["choices"][0]["text"]
        print(response)
        
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)})
    

@app.route('/')
def home():
    return render_template('home.html')   


if __name__ == '__main__':
    # app.run(debug = True, port = 4000)    
    app.run(debug = True)




