from flask import Flask, request, jsonify
from llmprocess import final_summary
from youtube_transcript_api import YouTubeTranscriptApi
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# Define a simple route for the home page
@app.route('/', methods=['GET'])
def home():
    return {"message": "Hello from Flask API"}

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Extract the YouTube URL from the request
        data = request.json
        youtube_url = data.get('youtube_url')

        summary = final_summary(youtube_url)
        
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
    app.run(debug=True)
