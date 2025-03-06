import requests
import os
from dotenv import load_dotenv

load_dotenv()

def convert_currency(from_currency, to_currency, amount):
    """
    Convert an amount from one currency to another.
    
    Args:
        from_currency (str): Source currency code (e.g., USD)
        to_currency (str): Target currency code (e.g., EUR)
        amount (float): Amount to convert
    
    Returns:
        dict: Conversion result
    """
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    
    if not api_key:
        return {"error": "Exchange rate API key not configured in .env file"}
    
    try:
        # Validate input
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        amount = float(amount)
        
        # Make API request
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}/{amount}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("result") == "success":
                return {
                    "from": from_currency,
                    "to": to_currency,
                    "amount": amount,
                    "converted_amount": data.get("conversion_result"),
                    "rate": data.get("conversion_rate")
                }
            else:
                return {"error": f"API error: {data.get('error', 'Unknown error')}"}
        else:
            return {"error": f"API request failed with status code {response.status_code}"}
    except ValueError:
        return {"error": "Invalid amount format"}
    except Exception as e:
        return {"error": f"Currency conversion failed: {str(e)}"}

def get_exchange_rates(base_currency):
    """
    Get exchange rates for a base currency.
    
    Args:
        base_currency (str): Base currency code (e.g., USD)
    
    Returns:
        dict: Exchange rates for the base currency
    """
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    
    if not api_key:
        return {"error": "Exchange rate API key not configured in .env file"}
    
    try:
        # Validate input
        base_currency = base_currency.upper()
        
        # Make API request
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("result") == "success":
                return {
                    "base_currency": base_currency,
                    "rates": data.get("conversion_rates", {}),
                    "last_updated": data.get("time_last_update_utc")
                }
            else:
                return {"error": f"API error: {data.get('error', 'Unknown error')}"}
        else:
            return {"error": f"API request failed with status code {response.status_code}"}
    except Exception as e:
        return {"error": f"Failed to get exchange rates: {str(e)}"}