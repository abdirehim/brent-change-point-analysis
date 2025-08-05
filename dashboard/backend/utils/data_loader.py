import pandas as pd
import numpy as np

def load_and_preprocess_data(file_path):
    """
    Loads, preprocesses, and enriches the Brent oil prices data.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The preprocessed data with log returns and volatility.
    """
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')
    df = df.sort_values(by='Date').reset_index(drop=True)
    
    # Handle missing values, if any
    df['Price'] = df['Price'].fillna(method='ffill')
    
    # Calculate log returns
    df['log_price'] = np.log(df['Price'])
    df['log_return'] = df['log_price'].diff()
    
    # Calculate rolling volatility (30-day)
    df['volatility'] = df['log_return'].rolling(window=30).std() * np.sqrt(252)
    
    # Drop rows with NaN values created by diff() and rolling()
    df = df.dropna()
    
    return df

if __name__ == '__main__':
    # Example usage:
    file_path = 'C:/Users/Cyber Defense/Desktop/week10/brent-change-point-analysis/data/raw/BrentOilPrices.csv'
    preprocessed_data = load_and_preprocess_data(file_path)
    print(preprocessed_data.head())
    print('\nData Description:')
    print(preprocessed_data.describe())