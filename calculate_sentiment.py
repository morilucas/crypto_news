import pandas as pd
from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from datetime import datetime
import os

# Ensure the VADER lexicon is downloaded
print("Downloading VADER lexicon...")
nltk.download('vader_lexicon')

# Load CSV
print("Loading CSV file...")
df = pd.read_csv('scraped_data.csv')

# Convert the 'date' column to datetime format (assuming there's a 'date' column in 'YYYY-MM-DD' format)
df['date_scraped'] = pd.to_datetime(df['date_scraped'], errors='coerce')

# Filter for today's date
today = datetime.now().date()
df = df[df['date_scraped'].dt.date == today]
print(f"Filtered data for today's date: {today}")

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

# Clean headlines for sentiment analysis
print("Cleaning headlines for new data entries...")
df['clean_headline'] = df['headline'].str.replace("[^a-zA-Z]", " ").str.lower()

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

# Apply sentiment analysis to all rows
print("Applying sentiment analysis...")
df['TextBlob_sentiment'] = df['clean_headline'].apply(get_textblob_sentiment)
df['VADER_sentiment'] = df['clean_headline'].apply(get_vader_sentiment)
df['FinBERT_sentiment'] = df['clean_headline'].apply(get_finbert_sentiment)

# Save the updated DataFrame by appending to the existing CSV
print("Appending the data to scraped_data_w_sentiment.csv...")
# Include headers if the file does not exist yet
csv_file = 'scraped_data_w_sentiment.csv'
if os.path.isfile(csv_file):
    df.to_csv(csv_file, mode='a', index=False, header=False)
else:
    df.to_csv(csv_file, mode='w', index=False, header=True)
print("Data appended successfully. Process completed.")

