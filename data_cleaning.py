# data_cleaning.py
import pandas as pd
import json

def load_data(file_path):
    """
    Load the dataset from the specified file path.
    """
    return pd.read_csv(file_path)

def clean_data(df):
    """
    Perform cleaning operations such as datetime conversion, 
    creating new columns for analysis, and extracting hashtags/mentions.
    """
    # Convert 'created_at' to datetime
    df['created_at'] = pd.to_datetime(df['created_at'])

    # Create a date column for easier grouping
    df['date'] = df['created_at'].dt.date

    # Calculate tweet length
    df['tweet_length'] = df['text'].str.len()

    # Extract hashtags from 'entities' column
    df['hashtags'] = df['entities'].apply(extract_hashtags)

    # Count hashtags
    df['hashtag_count'] = df['hashtags'].apply(len)

    # Extract mentions from 'entities' column
    df['mentions'] = df['entities'].apply(extract_mentions)

    # Count mentions
    df['mentions_count'] = df['mentions'].apply(len)

    return df

def extract_hashtags(entities):
    """
    Extract hashtags from the 'entities' column (JSON-like string).
    """
    try:
        entity_dict = json.loads(entities.replace("'", '"'))
        return [tag['tag'] for tag in entity_dict.get('hashtags', [])]
    except:
        return []

def extract_mentions(entities):
    """
    Extract mentions from the 'entities' column (JSON-like string).
    """
    try:
        entity_dict = json.loads(entities.replace("'", '"'))
        return [mention['username'] for mention in entity_dict.get('mentions', [])]
    except:
        return []

def main():
    """
    Main function to load, clean, and save the data.
    """
    # Load the raw data
    raw_data = load_data('data/Gymnastics_tweets.csv')

    # Clean the data
    cleaned_data = clean_data(raw_data)

    # Save cleaned data to a new file
    cleaned_data.to_csv('data/cleaned_gymnastics_tweets.csv', index=False)

    print("Data cleaned and saved to 'data/cleaned_gymnastics_tweets.csv'")

if __name__ == "__main__":
    main()
