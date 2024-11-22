import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import AutoTokenizer

GOOGLE_API_KEY='AIzaSyBeTHnFgFm-ZX1V7ETvPAAWMd8Oe0QnuAg'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
tokenizer = AutoTokenizer.from_pretrained("gpt2")


def get_transcripts(youtube_url):
    # Extract the video ID from the YouTube URL
    video_id = youtube_url.split("=")[1]
    print(video_id)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'hi', 'gu'])
    except Exception as e:
        print(f"Error fetching transcript for video ID {video_id}: {str(e)}")
        raise Exception(f"Error fetching transcript: {e}")

    full_transcript = " ".join([entry['text'] for entry in transcript])
    return full_transcript

def chunk_text(text, max_token_length=4000):
    # Tokenize the text
    tokens = tokenizer.encode(text, add_special_tokens=False)

    # Chunk tokens into max_token_length chunks
    chunks = [tokens[i:i + max_token_length] for i in range(0, len(tokens), max_token_length)]

    # Decode token chunks back into text
    chunked_texts = [tokenizer.decode(chunk) for chunk in chunks]

    return chunked_texts

def generate_summary(text):
    prompt = f"Summarize the following text with cover all context:\n\n{text}\n\nSummary:"
    response = model.generate_content(prompt)
    return response.text

def final_summary(youtube_url):
    full_transcript = get_transcripts(youtube_url)
    chunks = chunk_text(full_transcript)
    summaries = [generate_summary(chunk) for chunk in chunks]
    return  " ".join(summaries)

def summary_pdf(text):
    chunks = chunk_text(text)
    summaries = [generate_summary(chunk) for chunk in chunks]
    return  " ".join(summaries)