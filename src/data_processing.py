import pandas as pd
import numpy as np
from pathlib import Path

def load_ratings():
    """Load and clean analyst ratings data"""
    ratings = pd.read_csv(Path('..')/'data'/'raw'/'analyst_ratings'/'raw_analyst_ratings.csv',
                         parse_dates=['date'])
    
    # Clean ratings
    ratings['rating_score'] = ratings['rating'].map({
        'Buy': 1,
        'Outperform': 0.75,
        'Hold': 0.5,
        'Underperform': 0.25,
        'Sell': 0
    })
    
    return ratings

def merge_with_prices(ratings, lookback_days=5, forward_days=5):
    """Merge ratings with corresponding stock prices"""
    merged_data = []
    
    for ticker, group in ratings.groupby('stock'):
        try:
            prices = pd.read_csv(
                Path('..')/'data'/'raw'/'stock_prices'/f'{ticker}_historical_data.csv',
                parse_dates=['Date']
            )
            
            for _, row in group.iterrows():
                date_mask = (
                    (prices['Date'] >= row['date'] - pd.Timedelta(days=lookback_days)) &
                    (prices['Date'] <= row['date'] + pd.Timedelta(days=forward_days))
                )
                window = prices[date_mask].copy()
                window['days_from_rating'] = (window['Date'] - row['date']).dt.days
                window['rating_score'] = row['rating_score']
                merged_data.append(window)
                
        except FileNotFoundError:
            continue
            
    return pd.concat(merged_data)

def load_merged_data():
    """Main function to get processed data"""
    ratings = load_ratings()
    return merge_with_prices(ratings)