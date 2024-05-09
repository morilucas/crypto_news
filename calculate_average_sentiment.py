import pandas as pd

# Load the CSV file
df = pd.read_csv('scraped_data_w_sentiment.csv')

# Convert 'date_scraped' to datetime and extract the date part
df['date_scraped'] = pd.to_datetime(df['date_scraped']).dt.date

# Map sentiment values to numerical scores
sentiment_mapping = {'Positive': 1, 'Negative': -1, 'Neutral': 0}
df['FinBERT_sentiment'] = df['FinBERT_sentiment'].map(sentiment_mapping)

# Remove duplicate headlines within each date group
df = df.groupby(['date_scraped', 'headline']).first().reset_index()

# Aggregate data by 'date_scraped' and calculate the average sentiment
average_sentiment_per_day = df.groupby('date_scraped')['FinBERT_sentiment'].mean().reset_index()

# Save the results to a CSV file
average_sentiment_per_day.to_csv('meanperday.csv', index=False)

# Display the results
print(average_sentiment_per_day)
