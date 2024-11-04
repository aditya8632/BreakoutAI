#!/usr/bin/env python
# coding: utf-8

# # Python Assessment Notebook

# In[1]:


import pandas as pd

def get_option_chain_data(instrument_name: str, expiry_date: str, side: str) -> pd.DataFrame:
    """
    Mock version of get_option_chain_data to simulate fetching option chain data.
    This function generates mock data instead of calling a live API.
    
    Parameters:
        instrument_name (str): Name of the instrument (e.g., 'NIFTY' or 'BANKNIFTY').
        expiry_date (str): Expiration date of the options in 'YYYY-MM-DD' format.
        side (str): Option type to retrieve ('PE' for Put, 'CE' for Call).
        
    Returns:
        pd.DataFrame: DataFrame containing instrument_name, strike_price, side, and bid/ask price.
    """
    # Sample mock data to simulate an API response
    mock_data = [
        {"strike_price": 19500, "side": "PE", "bid_price": 0.65, "ask_price": None},
        {"strike_price": 19500, "side": "CE", "bid_price": None, "ask_price": 2302.25},
        {"strike_price": 19600, "side": "PE", "bid_price": 1.10, "ask_price": None},
        {"strike_price": 19600, "side": "CE", "bid_price": None, "ask_price": 2250.00},
    ]
    
    # Filter mock data by the option type
    option_chain = []
    for option in mock_data:
        if option['side'] == side:
            price = option['bid_price'] if side == "PE" else option['ask_price']
            option_chain.append({
                "instrument_name": instrument_name,
                "strike_price": option['strike_price'],
                "side": side,
                "bid/ask": price
            })
    
    # Convert to DataFrame
    df = pd.DataFrame(option_chain)
    return df


# In[2]:


def calculate_margin_and_premium(data: pd.DataFrame) -> pd.DataFrame:
    """
    Mock version of calculate_margin_and_premium to simulate margin calculation.
    This function uses mock data instead of calling a live API for margin requirements.
    
    Parameters:
        data (pd.DataFrame): DataFrame returned by get_option_chain_data.
    
    Returns:
        pd.DataFrame: Modified DataFrame with new columns 'margin_required' and 'premium_earned'.
    """
    LOT_SIZE = 75  # Mock lot size
    
    # Initialize margin and premium columns
    data['margin_required'] = 0
    data['premium_earned'] = 0.0
    
    # Mock margin calculation based on strike price
    for idx, row in data.iterrows():
        # Simulate margin as a function of strike price for demonstration purposes
        data.at[idx, 'margin_required'] = row['strike_price'] * 10  # Example mock margin logic
        
        # Calculate premium earned
        premium = row['bid/ask'] * LOT_SIZE if row['bid/ask'] is not None else 0
        data.at[idx, 'premium_earned'] = premium

    return data


# In[3]:


# Test Part 1: Fetch Option Chain Data (Mock)
df_option_chain = get_option_chain_data("NIFTY", "2024-11-02", "PE")
print("Option Chain Data (Mock):")
print(df_option_chain)

# Test Part 2: Calculate Margin and Premium (Mock)
df_margin_premium = calculate_margin_and_premium(df_option_chain)
print("\nOption Chain with Margin and Premium (Mock):")
print(df_margin_premium)


# # API Code

# In[24]:


import urllib.parse
import pandas as pd
import requests


# In[25]:


apikey = 'a4370935-4ad1-4039-bffa-ecec31f6df0e'
secretkey = 'xo8osxe08x'
rurl = urllib.parse.quote('https://127.0.0.1:5000/', safe='')


# In[26]:


url = f'https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={apikey}&redirect_uri={rurl}'
print(url)


# In[27]:


code = 'DchmTc'


# In[28]:


# Define the URL and payload
url = 'https://api.upstox.com/v2/login/authorization/token'
payload = {
    'code': code,
    'client_id': apikey,
    'client_secret': secretkey,
    'redirect_uri': 'https://127.0.0.1:5000/',
    'grant_type': 'authorization_code'
}

# Set headers
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Make the POST request
response = requests.post(url, headers=headers, data=payload)

# Print the response
response_data = response.json()
print(response_data)


# In[29]:


ACCESS_TOKEN = response_data['access_token']
ACCESS_TOKEN


# In[31]:


import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url = "https://api.upstox.com/v2/option/chain"
params = {
    "instrument_key": "NSE_INDEX|NIFTY 50",  # Replace with the actual instrument key you need
    "expiry_date": "2024-02-15"  # Replace with the desired expiry date in YYYY-MM-DD format
}

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Accept': 'application/json'
}

try:
    # Making the GET request with parameters
    response = requests.get(url, headers=headers, params=params, verify=False)
    
    # Check if the response was successful
    response.raise_for_status()
    print(response.json())  # Print the JSON response if successful

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"Other error occurred: {err}")


# In[38]:


from typing import Optional

def get_option_chain_data(instrument_name: str, expiry_date: str, side: str) -> Optional[pd.DataFrame]:
    """
    Fetches option chain data for a given instrument and expiry date, returning the highest bid or ask price.

    Parameters:
    - instrument_name: Name of the instrument (e.g., "NIFTY" or "BANKNIFTY").
    - expiry_date: Expiration date of the options, in "YYYY-MM-DD" format.
    - side: Type of option to retrieve, "PE" for Put and "CE" for Call.

    Returns:
    - A DataFrame with columns: instrument_name, strike_price, side, and bid/ask (highest bid for PE, highest ask for CE).
    """
    
    # Define the API URL and access token
    url = "https://api.upstox.com/v2/option/chain"
    
    # Prepare request headers and parameters
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Accept': 'application/json'
    }
    params = {
        "instrument_key": f"NSE_INDEX|{instrument_name}",
        "expiry_date": expiry_date
    }
    
    # Make the API request
    try:
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        data = response.json().get("data", [])

        # If no data from API, use sample data for testing
        if not data:
            print("No option chain data available from API; using sample data for testing.")
            data = [
                {
                    "expiry": "2024-02-15",
                    "strike_price": 19500,
                    "call_options": {
                        "market_data": {"ask_price": 2302.25}
                    },
                    "put_options": {
                        "market_data": {"bid_price": 0.65}
                    }
                }
            ]

        # Debug: Print the raw data for inspection
        print("Data received or used as sample:", data)

        # Process and filter data based on the side ("PE" or "CE")
        records = []
        for option in data:
            strike_price = option.get("strike_price")
            
            # Select highest bid/ask price based on the side
            if side == "PE" and "put_options" in option:
                bid_price = option["put_options"]["market_data"].get("bid_price", 0)
                records.append([instrument_name, strike_price, "PE", bid_price])
                
            elif side == "CE" and "call_options" in option:
                ask_price = option["call_options"]["market_data"].get("ask_price", 0)
                records.append([instrument_name, strike_price, "CE", ask_price])

        # Convert records into a DataFrame
        df = pd.DataFrame(records, columns=["Instrument Name", "Strike Price", "Option Type", "Bid/Ask Price"])

        # Set the display format for the DataFrame
        pd.set_option("display.colheader_justify", "center")
        pd.set_option("display.float_format", "{:.2f}".format)

        # Check if DataFrame is empty and print message if so
        if df.empty:
            print("No relevant options data found.")
            return None

        # Return the resulting DataFrame
        return df
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

    return None

# Example call to test the function
df_pe = get_option_chain_data("NIFTY", "2024-02-15", "PE")
df_ce = get_option_chain_data("NIFTY", "2024-02-15", "CE")

# Neatly display the output
if df_pe is not None:
    print("\nPut Options (PE):")
    print(df_pe.to_string(index=False))

if df_ce is not None:
    print("\nCall Options (CE):")
    print(df_ce.to_string(index=False))
else:
    print("Function returned no data.")


# In[41]:


def calculate_margin_and_premium(data: pd.DataFrame, lot_size: int = 300) -> pd.DataFrame:
    """
    Calculates margin required and premium earned for the options in the provided DataFrame.

    Parameters:
    - data: The DataFrame returned by get_option_chain_data.
    - lot_size: The number of contracts in a lot (default is 300).

    Returns:
    - A DataFrame with new columns: margin_required and premium_earned.
    """
    
    # Ensure the new columns are initialized
    data['margin_required'] = 0.0  # Placeholder for margin; can be updated later
    data['premium_earned'] = 0.0

    for index, row in data.iterrows():
        instrument_name = row['instrument_name']
        strike_price = row['strike_price']
        side = row['side']
        bid_ask_price = row['bid/ask']

        # Sample URL for margin calculation; replace with correct URL when known
        margin_url = "https://api.upstox.com/v2/margin"

        try:
            # Make API call to get margin requirements (if available)
            response = requests.get(margin_url, params={
                'transaction_type': 'Sell',
                'option_type': side,
                'strike_price': strike_price,
                'lot_size': lot_size
            }, headers={'Authorization': f'Bearer {ACCESS_TOKEN}'})
            response.raise_for_status()
            margin_data = response.json()
            margin_required = margin_data.get('margin', 0)  # Adjust key based on actual response structure
            data.at[index, 'margin_required'] = margin_required
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred for row {index}: {http_err}")
            data.at[index, 'margin_required'] = 0.0  # Default to 0 if error occurs

        # Calculate premium earned
        premium_earned = bid_ask_price * lot_size
        data.at[index, 'premium_earned'] = premium_earned

    return data

# Example usage with a DataFrame that simulates API response data
df = pd.DataFrame({
    "instrument_name": ["NIFTY"],
    "strike_price": [19500],
    "side": ["PE"],
    "bid/ask": [0.65]
})

# Calculate margin and premium
result_df = calculate_margin_and_premium(df)

# Print the resulting DataFrame with desired output
print(result_df.to_string(index=False))


# In[ ]:





# In[ ]:





# In[ ]:




