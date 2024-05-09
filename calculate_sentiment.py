import pandas as pd
from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# Ensure the VADER lexicon is downloaded
print("Downloading VADER lexicon...")
nltk.download('vader_lexicon')

# Load CSV
print("Loading CSV file...")
df = pd.read_csv('scraped_data.csv')

# Check and create sentiment columns if they do not exist
print("Checking for existing sentiment columns...")
if 'TextBlob_sentiment' not in df.columns:
    df['TextBlob_sentiment'] = None
    print("Created TextBlob_sentiment column.")
if 'VADER_sentiment' not in df.columns:
    df['VADER_sentiment'] = None
    print("Created VADER_sentiment column.")
if 'FinBERT_sentiment' not in df.columns:
    df['FinBERT_sentiment'] = None
    print("Created FinBERT_sentiment column.")

# Clean headlines (only for rows that are new and need sentiment analysis)
print("Cleaning headlines for new data entries...")
df.loc[df['TextBlob_sentiment'].isna(), 'clean_headline'] = df.loc[df['TextBlob_sentiment'].isna(), 'headline'].str.replace("[^a-zA-Z]", " ").str.lower()

# Initialize sentiment analyzers
print("Initializing sentiment analyzers...")
sia = SentimentIntensityAnalyzer()
finbert = pipeline('sentiment-analysis', model='yiyanghkust/finbert-tone', tokenizer='yiyanghkust/finbert-tone')

# Function to get TextBlob sentiment
def get_textblob_sentiment(text):
    return TextBlob(text).sentiment.polarity

# Function to get VADER sentiment
def get_vader_sentiment(text):
    return sia.polarity_scores(text)['compound']

# Function to get FinBERT sentiment
def get_finbert_sentiment(text):
    results = finbert(text)
    return results[0]['label']

# Apply sentiment analysis only to new rows
print("Applying sentiment analysis...")
mask = df['TextBlob_sentiment'].isna()
df.loc[mask, 'TextBlob_sentiment'] = df.loc[mask, 'clean_headline'].apply(get_textblob_sentiment)
df.loc[mask, 'VADER_sentiment'] = df.loc[mask, 'clean_headline'].apply(get_vader_sentiment)
df.loc[mask, 'FinBERT_sentiment'] = df.loc[mask, 'clean_headline'].apply(get_finbert_sentiment)

# Save the updated DataFrame to a new CSV
print("Saving the updated data...")
df.to_csv('scraped_data_w_sentiment.csv', index=False)
print("Data saved successfully. Process completed.")
