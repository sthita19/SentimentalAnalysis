import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Cleaning data
def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()

    return text

# Tokenizing
def tokenize_text(text):
    tokens = word_tokenize(text)
    return tokens

# Normalizing
def normalize_text(tokens):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    normalized_tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return normalized_tokens

# Driver function
def execute(transcripts):
    cleaned_transcripts = [clean_text(transcript) for transcript in transcripts]
    tokenized_transcripts = [tokenize_text(transcript) for transcript in cleaned_transcripts]
    normalized_transcripts = [normalize_text(transcript) for transcript in tokenized_transcripts]
    return normalized_transcripts