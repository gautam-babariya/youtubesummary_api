from flask import Flask, request, jsonify
from llmprocess import final_summary,summary_pdf
from youtube_transcript_api import YouTubeTranscriptApi
from flask_cors import CORS
from PyPDF2 import PdfReader
from io import BytesIO


# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# Define a simple route for the home page
@app.route('/', methods=['GET'])
def home():
    return {"message": "Hello from Flask API"}

@app.route('/generateyoutube', methods=['POST'])
def generate():
    try:
        # Extract the YouTube URL from the request
        data = request.json
        youtube_url = data.get('youtube_url')

        summary = final_summary(youtube_url)
        return jsonify({
            'status': 'success',
            'summary': summary
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file was uploaded
    if 'pdf' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    uploaded_file = request.files['pdf']
    
    # Validate file type
    if uploaded_file.filename.split('.')[-1].lower() != 'pdf':
        return jsonify({"error": "Uploaded file is not a PDF"}), 400

    try:
        # Read file in memory
        pdf_reader = PdfReader(BytesIO(uploaded_file.read()))
        extracted_text = ""

        # Extract text from each page
        for page in pdf_reader.pages:
            extracted_text += page.extract_text()
        cleaned_text = " ".join(extracted_text.splitlines())

        summary = summary_pdf(cleaned_text)
        return jsonify({
            'status': 'success',
            'summary': summary
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

    except Exception as e:
        return jsonify({"error": f"Failed to process file: {str(e)}"}), 500    

if __name__ == '__main__':
    # Run the Flask app on localhost:5000
    app.run()
