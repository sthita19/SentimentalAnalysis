from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import  RobertaForSequenceClassification, RobertaTokenizer
import torch
import streamlit as st
import tqdm
from tqdm import tqdm

# Sentiment analysis and classification functions
# def get_sentiment_score(text):
#     analyzer = SentimentIntensityAnalyzer()
#     sentiment_score = analyzer.polarity_scores(text)
#     compound_score = sentiment_score['compound']
#     return compound_score

# def classify_sentiment(score):
#     if score >= 0.2:
#         return 'positive'
#     elif score >= 0.05 and score < 0.2:
#         return 'slightly_positive'
#     elif score > -0.05 and score < 0.05:
#         return 'neutral'
#     elif score > -0.2 and score <= -0.05:
#         return 'slightly_negative'
#     else:
#         return 'negative'


# # Perform sentiment analysis and classification
# def sentiment_analysis(normalized_transcripts):
#     transcript_sentiments = []
#     word_counts = {
#         'positive': 0,
#         'slightly_positive': 0,
#         'neutral': 0,
#         'slightly_negative': 0,
#         'negative': 0
#     }
#     total_words = 0
#     for transcript in normalized_transcripts:
#         text = ' '.join(transcript)
#         sentiment_score = get_sentiment_score(text)
#         sentiment = classify_sentiment(sentiment_score)
#         transcript_sentiments.append(sentiment)
#         word_count = len(text.split())
#         word_counts[sentiment] += word_count
#         total_words += word_count

#     transcript_sentiment_counts = {
#         'positive': transcript_sentiments.count('positive'),
#         'slightly_positive': transcript_sentiments.count('slightly_positive'),
#         'neutral': transcript_sentiments.count('neutral'),
#         'slightly_negative': transcript_sentiments.count('slightly_negative'),
#         'negative': transcript_sentiments.count('negative')
#     }

#     overall_sentiment = max(transcript_sentiment_counts, key=transcript_sentiment_counts.get)
#     total_sentiment_count = sum(abs(value) for value in transcript_sentiment_counts.values())
    
#     non_zero_word_count = {
#         sentiment: count
#         for sentiment, count in word_counts.items() if count > 0
#     }

#     sentiment_percentages = {
#         sentiment: abs(score) / total_sentiment_count * 100
#         for sentiment, score in transcript_sentiment_counts.items() if abs(score) > 0
#     }

#     return overall_sentiment, sentiment_percentages, non_zero_word_count

def analyse(cleaned_transcripts):
    model = RobertaForSequenceClassification.from_pretrained('roberta-base')
    tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    sentiment_scores = []
    progress_bar = st.progress(0)  # Create the progress bar

    with tqdm(total=len(cleaned_transcripts), bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
        for i, text in enumerate(cleaned_transcripts):
            text_chunks = [text[i:i + 512] for i in range(0, len(text), 512)]
            chunk_scores = []

            for chunk in text_chunks:
                inputs = tokenizer(chunk, truncation=True, padding=True, return_tensors="pt").to(device)
                with torch.inference_mode():
                    model_output = model(**inputs)
            logits = model_output.logits
            probabilities = torch.softmax(logits, dim=1)
            sentiment_score = probabilities[:, 1].item()  # positive sentiment
            chunk_scores.append(sentiment_score)

            average_score = sum(chunk_scores) / len(chunk_scores)
            sentiment_scores.append(average_score)

            # Update the progress bar
            progress = (i + 1) / len(cleaned_transcripts)
            progress_bar.progress(progress)

            # Update the tqdm progress bar
            pbar.update(1)

            # Update the progress text
            progress_text = f"Sentiment Analysis Progress: {round(progress * 100, 2)}%"
            st.text(progress_text)


        # Update the progress bar
        # progress = (i + 1) / len(cleaned_transcripts)
        # progress_bar.progress(progress)

        # # Update the progress text
        # progress_percent = int(progress * 100)
        # progress_text.text(f"Sentimental Analysis Progress: {progress_percent}%")
        # pbar.update(1)
    # st.text("Sentimental Analysis Done")
    # st.markdown("<h3 style='text-align: center;'>Sentimental Analysis Completed</h3>", unsafe_allow_html=True)

    
    for i, text in enumerate(cleaned_transcripts):
        sentiment_score = sentiment_scores[i]
        sentiment_label = "Positive" if sentiment_score >= 0.5 else "Negative"

    mean_sentiment_score = torch.mean(torch.tensor(sentiment_scores))
    overall_sentiment = ''
    if mean_sentiment_score >= 0.5:
        overall_sentiment = 'POSITIVE'
    else:
        overall_sentiment = 'NEGATIVE'
    
    return sentiment_scores

# Driver function
# def execute(normalized_transcripts):
def execute(cleaned_transcripts):
    # overall_sentiment, sentiment_percentages, non_zero_word_count = sentiment_analysis(normalized_transcripts)
    # return overall_sentiment, sentiment_percentages, non_zero_word_count
    sentiment_scores = analyse(cleaned_transcripts)
    return sentiment_scores

    