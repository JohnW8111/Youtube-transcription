


import re
import os  # Add this line at the top of main.py
from youtube_transcript_api import YouTubeTranscriptApi
from flask import Flask, request, render_template, Response, redirect, url_for
from flask import Response

app = Flask(__name__)


def extract_youtube_id(url):
    # This pattern looks for '?v=' followed by exactly 11 characters (alphanumeric and underscore)
    pattern = r'(?<=v=)[\w-]{11}'
    match = re.search(pattern, url)
    if match:
        return match.group()
    else:
        return None

def get_transcription(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    full_transcript = ''
    with open('transcript.txt', 'w') as file:
      for line in transcript:
        full_line = line['text'] + '\n'
        file.write(full_line)
        full_transcript += full_line
    return full_transcript  # return the full transcript text

def generate_transcription(video_id):
  transcript = YouTubeTranscriptApi.get_transcript(video_id)
  for line in transcript:
      yield line['text'] + '\n'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        video_id = extract_youtube_id(url)
        if video_id:
            transcription = get_transcription(video_id)
            return Response(
                transcription,
                mimetype="text/plain",
                headers={"Content-Disposition": "attachment;filename=transcription.txt"}
            )
        else:
            return 'Invalid YouTube URL', 400

    return render_template('index.html')
  
@app.route('/clear', methods=['GET'])
def clear():
    if os.path.exists('transcript.txt'):
        os.remove('transcript.txt')
    return redirect(url_for('index'))

# Modify the get_transcription function to be a generator

@app.route('/api/transcribe', methods=['POST'])
def api_transcribe():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return {'error': 'No URL provided'}, 400

    video_id = extract_youtube_id(url)
    if video_id:
        transcription_generator = generate_transcription(video_id)
        return Response(transcription_generator, mimetype="text/plain",
                        headers={"Content-Disposition": "attachment;filename=transcription.txt"})
    else:
        return 'Invalid YouTube URL', 400
      
      
  


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)






