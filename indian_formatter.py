"""
Indian number formatting utilities for TaxBot 2025
Handles formatting numbers in Indian system (lakhs, crores) with proper commas
"""

def format_indian_number(amount):
    """
    Format number according to Indian number system
    Returns formatted string with proper comma placement
    """
    if amount == 0:
        return "0"
    
    # Convert to string and handle negative numbers
    is_negative = amount < 0
    amount = abs(amount)
    
    # Handle decimals
    if isinstance(amount, float):
        if amount == int(amount):
            amount = int(amount)
        else:
            # Round to 2 decimal places
            amount = round(amount, 2)
            str_amount = str(amount)
            integer_part, decimal_part = str_amount.split('.')
            formatted_integer = format_indian_integer(int(integer_part))
            result = f"{formatted_integer}.{decimal_part}"
            return f"-{result}" if is_negative else result
    
    # Format integer part
    formatted = format_indian_integer(int(amount))
    return f"-{formatted}" if is_negative else formatted

def format_indian_integer(num):
    """
    Format integer according to Indian number system
    """
    if num == 0:
        return "0"
    
    num_str = str(num)
    
    # If less than 1000, no comma needed
    if len(num_str) <= 3:
        return num_str
    
    # For numbers >= 1000, apply Indian comma system
    # First comma after 3 digits from right, then every 2 digits
    result = ""
    length = len(num_str)
    
    # Add commas from right to left
    for i, digit in enumerate(reversed(num_str)):
        if i == 3:  # First comma after 3 digits
            result = "," + result
        elif i > 3 and (i - 3) % 2 == 0:  # Every 2 digits after first comma
            result = "," + result
        result = digit + result
    
    return result

def format_indian_currency(amount):
    """
    Format amount as Indian currency (Rs. X,XX,XXX)
    """
    formatted_amount = format_indian_number(amount)
    return f"Rs. {formatted_amount}"

def format_indian_currency_short(amount):
    """
    Format amount as Indian currency with short notation (Rs. X,XX,XXX)
    """
    formatted_amount = format_indian_number(amount)
    return f"Rs. {formatted_amount}"

def convert_to_words(amount):
    """
    Convert number to Indian words (lakhs, crores)
    """
    if amount == 0:
        return "Zero"
    
    # Handle negative numbers
    if amount < 0:
        return f"Negative {convert_to_words(-amount)}"
    
    # Convert to integer if it's a whole number
    if isinstance(amount, float) and amount == int(amount):
        amount = int(amount)
    
    # Define the Indian number system
    crore = 10000000
    lakh = 100000
    thousand = 1000
    
    result = []
    
    # Crores
    if amount >= crore:
        crores = amount // crore
        result.append(f"{crores} crore{'s' if crores > 1 else ''}")
        amount %= crore
    
    # Lakhs
    if amount >= lakh:
        lakhs = amount // lakh
        result.append(f"{lakhs} lakh{'s' if lakhs > 1 else ''}")
        amount %= lakh
    
    # Thousands
    if amount >= thousand:
        thousands = amount // thousand
        result.append(f"{thousands} thousand")
        amount %= thousand
    
    # Remaining amount
    if amount > 0:
        result.append(str(amount))
    
    return " ".join(result)

def get_indian_amount_display(amount):
    """
    Get a user-friendly display of amount in Indian format
    """
    formatted = format_indian_currency(amount)
    words = convert_to_words(amount)
    return f"{formatted} ({words})"
