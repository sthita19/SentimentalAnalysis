from nltk.sentiment import SentimentIntensityAnalyzer

# Sentiment analysis and classification functions
def get_sentiment_score(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)
    compound_score = sentiment_score['compound']
    return compound_score

def classify_sentiment(score):
    if score >= 0.2:
        return 'positive'
    elif score >= 0.05 and score < 0.2:
        return 'slightly_positive'
    elif score > -0.05 and score < 0.05:
        return 'neutral'
    elif score > -0.2 and score <= -0.05:
        return 'slightly_negative'
    else:
        return 'negative'


# Perform sentiment analysis and classification
def sentiment_analysis(normalized_transcripts):
    transcript_sentiments = []
    word_counts = {
        'positive': 0,
        'slightly_positive': 0,
        'neutral': 0,
        'slightly_negative': 0,
        'negative': 0
    }
    total_words = 0
    for transcript in normalized_transcripts:
        text = ' '.join(transcript)
        sentiment_score = get_sentiment_score(text)
        sentiment = classify_sentiment(sentiment_score)
        transcript_sentiments.append(sentiment)
        word_count = len(text.split())
        word_counts[sentiment] += word_count
        total_words += word_count

    transcript_sentiment_counts = {
        'positive': transcript_sentiments.count('positive'),
        'slightly_positive': transcript_sentiments.count('slightly_positive'),
        'neutral': transcript_sentiments.count('neutral'),
        'slightly_negative': transcript_sentiments.count('slightly_negative'),
        'negative': transcript_sentiments.count('negative')
    }

    overall_sentiment = max(transcript_sentiment_counts, key=transcript_sentiment_counts.get)
    total_sentiment_count = sum(abs(value) for value in transcript_sentiment_counts.values())
    
    non_zero_word_count = {
        sentiment: count
        for sentiment, count in word_counts.items() if count > 0
    }

    sentiment_percentages = {
        sentiment: abs(score) / total_sentiment_count * 100
        for sentiment, score in transcript_sentiment_counts.items() if abs(score) > 0
    }

    return overall_sentiment, sentiment_percentages, non_zero_word_count

# Driver function
def execute(normalized_transcripts):
    overall_sentiment, sentiment_percentages, non_zero_word_count = sentiment_analysis(normalized_transcripts)
    return overall_sentiment, sentiment_percentages, non_zero_word_count
    