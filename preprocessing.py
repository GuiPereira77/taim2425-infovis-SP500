import pandas as pd
import os

# Verify file paths
sp500_path = 'data/s&p500.xlsx'
sp500_top10_holders_path = 'data/sp500_top10_holders.xlsx'

if not os.path.exists(sp500_path):
    print(f"Current location: {os.getcwd()}")
    raise FileNotFoundError(f"File not found: {sp500_path}")

if not os.path.exists(sp500_top10_holders_path):
    raise FileNotFoundError(f"File not found: {sp500_top10_holders_path}")


sp500 = pd.read_excel('data/s&p500.xlsx')
sp500_top10_holders = pd.read_excel('data/sp500_top10_holders.xlsx')

# Fix index and column names
sp500.columns = sp500.iloc[0]
sp500 = sp500[1:]

sp500_top10_holders.columns = sp500_top10_holders.iloc[0]
sp500_top10_holders = sp500_top10_holders[1:]

# Delete rows 'Top mutual fund holders' in 'class' column
sp500_top10_holders = sp500_top10_holders[sp500_top10_holders['class'] != 'Top mutual fund Holders']

# Remove duplicated rows
sp500_top10_holders = sp500_top10_holders.drop_duplicates()

# Merge data
merged_df = pd.merge(sp500_top10_holders, sp500, on=['symbol', 'isin'])

# Function to convert values with 'B' and 'M' suffixes to numeric
def convert_shares(value):
    if 'B' in value:
        value = float(value.replace('B', '')) * 1e9
    elif 'M' in value:
        value = float(value.replace('M', '')) * 1e6
    elif 'k' in value:
        value = float(value.replace('k', '')) * 1e3
    else:
        value = float(value)
    return '${:,.2f}'.format(value)

# Apply the function to the 'shares' column
merged_df['shares'] = merged_df['shares'].apply(convert_shares)

# List of columns to convert to numeric
columns_to_numeric = [
    '%', 'value', 'marketCap', 'enterpriseValue', 'totalCash', 'totalCashPerShare',
    'ebitda', 'totalDebt', 'quickRatio', 'currentRatio', 'totalRevenue', 'debtToEquity',
    'revenuePerShare', 'returnOnAssets', 'returnOnEquity', 'freeCashflow', 'operatingCashflow',
    'earningsGrowth', 'revenueGrowth', 'grossMargins', 'ebitdaMargins', 'operatingMargins'
]

# Convert specified columns to numeric
merged_df[columns_to_numeric] = merged_df[columns_to_numeric].apply(pd.to_numeric, errors='coerce')

# Store data in a seperate csv file
merged_df.to_csv('data/merged_sp500_data.csv', index=False)
