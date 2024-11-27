# YouTube Transcript Summarizer

This application uses OpenAI’s GPT API and YouTube Transcript API to convert YouTube video transcripts into concise, insightful summaries. Designed to help users quickly understand the key points of a video, this Streamlit-based app generates summarized notes with flexible customization options.

---

## Features

- **Transcript Extraction**: Automatically extracts transcripts from YouTube videos using the video URL.
- **Summarization**: Utilizes OpenAI’s GPT API to generate summaries in bullet-point or paragraph format, with options for difficulty levels.
- **Customizable Settings**: Users can choose summary length, format, difficulty level, and language for translation.
- **Translations**: Supports translating summaries into English, German, or Dutch while retaining the original format.
- **Dynamic UI**: Displays a video thumbnail for verification before processing.

---

## Requirements

- **Python 3.10+**
- **Streamlit**
- **dotenv**
- **OpenAI API**
- **YouTube Transcript API**

---

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/youtube-transcript-summarizer.git
cd youtube-transcript-summarizer
```

### Step 2: Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate       # On Windows
```

### Step 3: Install Required Packages
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
1. Create a `.env` file in the project directory.
2. Add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

---

## Usage

### Step 1: Run the Streamlit App
```bash
streamlit run app.py
```

### Step 2: Open in Browser
Once the app is running, open your browser and go to:
```
http://localhost:8501
```

### Step 3: Generate Summaries
1. Enter a YouTube video link.
2. Adjust the settings in the sidebar:
   - **Summary Length**: Choose the word count.
   - **Format**: Select bullet points or paragraph.
   - **Difficulty Level**: Choose between beginner, intermediate, or technical.
   - **Language**: Optionally translate the summary.
3. Click **Generate Summary** to process the video transcript.

### Step 4: View and Translate Summaries
- View the original summary.
- Translate it into the selected language while retaining the format.

---

## Contribution

We welcome contributions! Feel free to open issues or submit pull requests to improve this app.

---


