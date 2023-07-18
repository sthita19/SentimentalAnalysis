import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import streamlit as st
import tqdm
from tqdm import tqdm
# Cleaning data
def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    return text

# Tokenizing
# def tokenize_text(text):
#     tokens = word_tokenize(text)
#     return tokens

# # Normalizing
# def normalize_text(tokens):
#     stop_words = set(stopwords.words('english'))
#     # lemmatizer = WordNetLemmatizer()
#     # normalized_tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
#     return normalized_tokens

# Driver function
def execute(transcripts):
    cleaned_transcripts = []
    progress_bar = st.progress(0)

    with tqdm(total=len(transcripts), bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
        for i, transcript in enumerate(transcripts):
            cleaned_transcript = clean_text(transcript)
            cleaned_transcripts.append(cleaned_transcript)
            progress = (i + 1) / len(transcripts)
            progress_bar.progress(progress)
            pbar.update(1)

        progress_message = f"Text Cleaning Progress: {round(progress * 100)}%"
        st.text(progress_message)

    return cleaned_transcripts