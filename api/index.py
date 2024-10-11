from flask import Flask, request, jsonify
# from .llmprocess import final_summary
# from .llmprocess import get_transcripts
from youtube_transcript_api import YouTubeTranscriptApi


def get_transcripts(youtube_url):
    # Extract the video ID from the YouTube URL
    video_id = youtube_url.split("=")[1]

    print(video_id)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'hi', 'gu'])
    except Exception as e:
        raise Exception(f"Error fetching transcript: {e}")

    full_transcript = " ".join([entry['text'] for entry in transcript])
    return full_transcript

# Initialize the Flask application
app = Flask(__name__)

# Define a simple route for the home page
@app.route('/', methods=['GET'])
def home():
    return "Flask app is working!"

@app.route('/generate', methods=['POST'])
def generate():
    

    try:
        # Extract the YouTube URL from the request
        data = request.json
        youtube_url = data.get('youtube_url')

        summary = get_transcripts(youtube_url)
        
        # Return the summary
        return jsonify({
            'status': 'success',
            'summary': summary
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    # Run the Flask app on localhost:5000
    app.run()
