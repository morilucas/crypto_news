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
df_grouped = df.groupby('date_scraped')['FinBERT_sentiment']
average_sentiment_per_day = df_grouped.mean().reset_index(name='average_sentiment')

# Count the occurrences of each sentiment category
sentiment_counts = df.groupby('date_scraped')['FinBERT_sentiment'].value_counts().unstack(fill_value=0)
# Rename columns based on the numeric mapping to ensure correct labeling
column_names = {1: 'positive', -1: 'negative', 0: 'neutral'}
sentiment_counts.rename(columns=column_names, inplace=True)

# Merge the average sentiment with the counts
result = pd.merge(average_sentiment_per_day, sentiment_counts, on='date_scraped')

# Save the results to a CSV file
result.to_csv('mean_and_count_per_day.csv', index=False)

# Display the results
print(result)