get_option_chain_data Function

Overview
The get_option_chain_data function fetches the option chain data for a specific instrument (such as "NIFTY" or "BANKNIFTY") and expiration date from the Upstox API. It returns the highest bid price for put options (PE) or the highest ask price for call options (CE), based on the specified parameters.

This function is designed for developers working with the Upstox API to analyze option chains programmatically. It retrieves and processes option data for given parameters and returns a pandas DataFrame for easy data handling and analysis.

Requirements
Python 3.x
requests library for making HTTP requests.
pandas library for handling data in a structured format.
Install the required libraries:

bash
Copy code
```bash
pip install requests pandas
```
Parameters
The function accepts the following parameters:

instrument_name (str): The name of the instrument (e.g., "NIFTY" or "BANKNIFTY").
expiry_date (str): The expiration date for the options in "YYYY-MM-DD" format.
side (str): The option type, either "PE" for Put options or "CE" for Call options.
Returns
The function returns a pandas.DataFrame with the following columns:

Instrument Name: Name of the instrument.
Strike Price: Strike price of the option.
Option Type: Either "PE" or "CE", as specified in the input.
Bid/Ask Price: The highest bid price for PE options or the highest ask price for CE options.
If no relevant data is found, the function will return None.

Setup Instructions
Obtain your API Key and Access Token from Upstox after registering your application.
Update the ACCESS_TOKEN variable in the code with your valid access token.
Set up a Redirect URI in your Upstox application settings, ensuring it matches the one provided in your code.
Code Explanation
python
``` python
#Copy code
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
API Setup: The function defines the Upstox API URL (https://api.upstox.com/v2/option/chain) and prepares the authorization headers.
```
Request Parameters: The parameters required for the API request are:

instrument_key: Derived by appending "NSE_INDEX|" with the instrument_name.
expiry_date: The specified expiration date.
Making the API Request:

python
Copy code
``` python
response = requests.get(url, headers=headers, params=params, verify=False)
response.raise_for_status()
data = response.json().get("data", [])
The function sends a GET request to the Upstox API and retrieves the option chain data.
If no data is returned, a sample dataset is used for testing purposes.
Filtering and Processing Data:
```
python
Copy code
``` python
records = []
for option in data:
    strike_price = option.get("strike_price")
    if side == "PE" and "put_options" in option:
        bid_price = option["put_options"]["market_data"].get("bid_price", 0)
        records.append([instrument_name, strike_price, "PE", bid_price])
    elif side == "CE" and "call_options" in option:
        ask_price = option["call_options"]["market_data"].get("ask_price", 0)
        records.append([instrument_name, strike_price, "CE", ask_price])
```
The function iterates over each option in the response and extracts the strike price and the highest bid or ask price depending on the side ("PE" or "CE").
Records are appended as lists and later converted into a pandas.DataFrame.
Output Formatting:


Copy code
``` python
df = pd.DataFrame(records, columns=["Instrument Name", "Strike Price", "Option Type", "Bid/Ask Price"])
```
The list of records is converted into a structured DataFrame, which allows for easy data analysis.
Error Handling:

python
Copy code
``` python
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")
```
Errors such as HTTP issues or general exceptions are caught, and relevant error messages are printed.
Example Usage
python
Copy code
```python
df_pe = get_option_chain_data("NIFTY", "2024-02-15", "PE")
df_ce = get_option_chain_data("NIFTY", "2024-02-15", "CE")

if df_pe is not None:
    print("\nPut Options (PE):")
    print(df_pe.to_string(index=False))

if df_ce is not None:
    print("\nCall Options (CE):")
    print(df_ce.to_string(index=False))
```
Notes
ACCESS_TOKEN: Ensure this token is valid for successful API calls.
API Rate Limits: Be mindful of rate limits imposed by Upstox when making frequent API requests.
Sample Output
mathematica
Copy code
Put Options (PE):
Instrument Name  Strike Price  Option Type  Bid/Ask Price
        NIFTY       19500            PE           0.65

Call Options (CE):
Instrument Name  Strike Price  Option Type  Bid/Ask Price
        NIFTY       19500            CE        2302.25
Troubleshooting
Empty Data: If the DataFrame is empty, it may be due to a lack of relevant data for the specified parameters or invalid API credentials.
HTTP Errors: Ensure that the ACCESS_TOKEN is valid and permissions are granted in Upstox for this endpoint.




calculate_margin_and_premium Function
Overview
The calculate_margin_and_premium function calculates the margin required and premium earned for options contracts in a DataFrame. Using the options data returned by get_option_chain_data, this function retrieves margin data from an API and computes the premium based on a specified lot size. It adds two new columns to the DataFrame: margin_required and premium_earned.

Parameters
data (pd.DataFrame): A DataFrame with options data, which includes columns such as instrument_name, strike_price, side, and bid/ask prices.
lot_size (int, optional): The number of contracts in each lot. Default is 300, commonly used for indices like NIFTY. This is used to calculate the total premium.
Returns
pd.DataFrame: The updated DataFrame containing the following new columns:
margin_required: The margin required for each options contract (retrieved via API).
premium_earned: The premium earned from selling the option.
Requirements
Python 3.x
pandas and requests libraries
Install the required libraries:

bash
Copy code
```bash
pip install pandas requests
```
Example Usage
Here's an example showing how to use calculate_margin_and_premium with sample options data:
```python
import pandas as pd
import requests

# Sample data similar to what get_option_chain_data might return
df = pd.DataFrame({
    "instrument_name": ["NIFTY"],
    "strike_price": [19500],
    "side": ["PE"],
    "bid/ask": [0.65]
})

# Call the function to calculate margin and premium
result_df = calculate_margin_and_premium(df)

# Display the updated DataFrame with margin and premium columns
print(result_df.to_string(index=False))
```
The above code will print the DataFrame with new columns: margin_required and premium_earned.

Function Explanation
Below is the code for the calculate_margin_and_premium function, along with comments explaining each section.
```python
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

    # Iterate over each row in the DataFrame to calculate margin and premium
    for index, row in data.iterrows():
        instrument_name = row['instrument_name']
        strike_price = row['strike_price']
        side = row['side']
        bid_ask_price = row['bid/ask']

        # URL for margin calculation; replace with the actual URL when available
        margin_url = "https://api.upstox.com/v2/margin"

        try:
            # API call to get margin requirement for the specific options contract
            response = requests.get(margin_url, params={
                'transaction_type': 'Sell',
                'option_type': side,
                'strike_price': strike_price,
                'lot_size': lot_size
            }, headers={'Authorization': f'Bearer {ACCESS_TOKEN}'})
            response.raise_for_status()
            
            # Parse response JSON to extract margin requirement
            margin_data = response.json()
            margin_required = margin_data.get('margin', 0)  # Adjust key based on actual response structure
            data.at[index, 'margin_required'] = margin_required
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred for row {index}: {http_err}")
            data.at[index, 'margin_required'] = 0.0  # Default to 0 if an error occurs

        # Calculate premium earned by multiplying the bid/ask price by the lot size
        premium_earned = bid_ask_price * lot_size
        data.at[index, 'premium_earned'] = premium_earned

    return data
```
Explanation of Key Sections
Initialize Columns: New columns margin_required and premium_earned are added to the DataFrame with initial values of 0.0.
API Call for Margin: For each row, the function calls the Upstox margin API to fetch the margin requirement based on side, strike_price, and lot_size. If there’s an error, the margin defaults to 0.0 for that entry.
Premium Calculation: The premium is calculated as bid/ask price multiplied by lot_size.
Error Handling: If an API call fails, an error message is printed, and margin_required for that row is set to 0.0.
Additional Notes
Ensure that the ACCESS_TOKEN is defined in your environment before running this function to authorize API requests.
Replace the margin_url with the actual URL for margin calculation when it’s available.
