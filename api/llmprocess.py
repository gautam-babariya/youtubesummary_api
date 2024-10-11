import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

GOOGLE_API_KEY='AIzaSyACKz-i5GfZF3hbbtwV_ZvqaCnaokhnbUg'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


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

def chunk_text_by_char(text, max_char_length=18500):
    # Initialize a list to hold the chunks
    chunks = []
    
    # Split the text into chunks of the specified maximum length
    for i in range(0, len(text), max_char_length):
        chunks.append(text[i:i + max_char_length])
    
    return chunks

def generate_summary(text):
    prompt = f"Summarize the following text with cover all context:\n\n{text}\n\nSummary:"
    response = model.generate_content(prompt)
    return response.text

def final_summary(youtube_url):
    full_transcript = get_transcripts(youtube_url)
    chunks = chunk_text_by_char(full_transcript)
    summaries = [generate_summary(chunk) for chunk in chunks]
    return  " ".join(summaries)
