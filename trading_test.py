from binance.client import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API credentials
api_key = os.getenv('TRADING_API_KEY')
api_secret = os.getenv('TRADING_API_SECRET')

# Print the first and last 4 characters of each key for verification
print(f"API Key: {api_key[:4]}...{api_key[-4:]}")
print(f"API Secret: {api_secret[:4]}...{api_secret[-4:]}")

# Don't proceed with client creation until we verify keys