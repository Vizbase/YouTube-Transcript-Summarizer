from youtube_transcript_api import YouTubeTranscriptApi  
import streamlit as st  
import openai  
from dotenv import load_dotenv  
import os  
 

# Load OpenAI API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to extract video ID and transcript
def extract_transcript(video_url):
    """Fetch the transcript and video ID of a YouTube video."""
    try:
        # Extract video ID from various YouTube URL formats
        if "v=" in video_url:
            video_id = video_url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in video_url:
            video_id = video_url.split("youtu.be/")[1].split("?")[0]
        else:
            return None, "Invalid YouTube URL format."

        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([item['text'] for item in transcript])
        return video_id, full_text
    except Exception as e:
        return None, f"Error: {str(e)}"

# Function to truncate transcript
def truncate_transcript(transcript, max_length=10000):
    """Truncate the transcript to fit within the token limit."""
    return transcript[:max_length]

# Function to summarize transcript
# Function to summarize transcript
def summarize_text(transcript, format="Bullet Points", length=200, difficulty="Beginner-Friendly"):
    """Summarize the transcript using OpenAI's ChatCompletion API."""
    try:
        # Customize the prompt based on difficulty level
        difficulty_prompts = {
            "Beginner-Friendly": """Imagine you are a teacher summarizing a YouTube video for a younger audience. Your goal is to provide a simple and clear summary that even a high school student can easily understand. Focus on:
            1. **Main Ideas**: Highlight the most important points discussed in an easy-to-digest way.      
            2. **Key Takeaways**: Share any conclusions or suggestions made, avoiding technical jargon.
            3. **Interesting Details**: Include notable facts or examples that make the content engaging and relatable.

            Use simple sentences and explain in a way that feels approachable. For bullet points, keep them short and to the point. For paragraphs, write clearly with a natural flow.

            Here's the content to summarize:
            """,
            "Intermediate": """
            Imagine you are preparing a concise and moderately detailed summary of a YouTube video for a university-level audience. Your objective is to present a balanced explanation. Focus on:

            1. **Main Themes**: Identify and summarize the critical ideas with sufficient detail.
            2. **Key Insights**: Highlight conclusions, including context and reasoning where relevant.
            3. **Relevant Examples**: Mention notable facts or supporting examples, adding clarity without overloading details.

            Aim for clarity and logical structure. Bullet points should be precise and informative. Paragraphs should present ideas smoothly, connecting them logically.

            Here's the content to summarize:
            """,
            "Advanced/Technical": """
            You are tasked with preparing a highly detailed and precise summary of a YouTube video for a professional audience. The summary should focus on technical accuracy and in-depth insights. Emphasize:

            1. **Core Concepts**: Break down the most significant ideas using technical terminology where appropriate.
            2. **Conclusions and Implications**: Highlight important conclusions with detailed analysis or reasoning.
            3. **Supporting Data**: Include facts, figures, or insights that showcase technical depth and relevance.

            Ensure the summary is thorough and professional. Bullet points should be compact but rich in information. Paragraphs should flow logically while emphasizing depth and clarity.

            Here's the content to summarize:
            """
        }
        # Adjust the length to include buffer for completion
        adjusted_length = length + 100  # Add buffer for smoother completion
        prompt = f"{difficulty_prompts[difficulty]}\n\nSummarize the following text in {format} format within {length} words:\n\n{transcript}"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=min(adjusted_length, 4096),  # Adjusted length for smooth completions
            temperature=0.7
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Function to translate text with the same format
def translate_text(text, target_language, format="Bullet Points"):
    """Translate the text into the selected language using OpenAI, preserving the original format."""
    try:
        language_map = {
            "English": "English",
            "German": "German",
            "Dutch": "Dutch"
        }
        # Adjust the prompt to preserve the format
        if format == "Bullet Points":
            prompt = f"Translate the following text into {language_map[target_language]} while keeping the bullet point format. Ensure the translation is fluent and professional:\n\n{text}"
        else:
            prompt = f"Translate the following text into {language_map[target_language]} in a paragraph format. Ensure the translation reads naturally and fluently:\n\n{text}"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that translates text while preserving its original structure."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096,
            temperature=0.7
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit App
st.title("YouTube Transcript Summarizer")

# Sidebar for Summary Settings
st.sidebar.header("Summary Settings")
summary_length = st.sidebar.slider("Length Summary", min_value=50, max_value=2500, value=200, step=50)
summary_format = st.sidebar.radio("Format", ["Bullet Points", "Paragraph"])
difficulty_level = st.sidebar.selectbox("Difficulty Level", ["Beginner-Friendly", "Intermediate", "Advanced/Technical"])
target_language = st.sidebar.selectbox("Translate Summary to:", ["None", "English", "German", "Dutch"])


# Initialize session state
if "video_id" not in st.session_state:
    st.session_state.video_id = None
if "transcript" not in st.session_state:
    st.session_state.transcript = None



# Input for YouTube Video Link
youtube_link = st.text_input("Enter YouTube Video Link:")

# Fetch and store transcript and thumbnail only once
if youtube_link and st.session_state.video_id is None:
    video_id, transcript_or_error = extract_transcript(youtube_link)
    if video_id:
        st.session_state.video_id = video_id
        st.session_state.transcript = transcript_or_error
    else:
        st.error(transcript_or_error)

# Display thumbnail if video_id is set
if st.session_state.video_id:
    st.image(f"http://img.youtube.com/vi/{st.session_state.video_id}/0.jpg", caption="Video Thumbnail")

# Generate Summary
if st.button("Generate Summary") and st.session_state.transcript:
    transcript = st.session_state.transcript
    if "Error" in transcript:
        st.error(transcript)
    else:
        # Truncate if necessary
        if len(transcript) > 100000:
            st.warning("The transcript is too long and has been truncated for summarization.")
            transcript = truncate_transcript(transcript)
        
        st.success("Transcript extracted successfully!")
        summary = summarize_text(transcript, summary_format, summary_length, difficulty_level)
        if "Error" in summary:
            st.error(summary)
        else:
            st.write("### Summary:")
            st.write(summary)

            # Translate summary if requested
            if target_language != "None":
                translated_summary = translate_text(summary, target_language, summary_format)
                if "Error" in translated_summary:
                    st.error(translated_summary)
                else:
                    st.write(f"### Translated Summary ({target_language}):")
                    st.write(translated_summary)
