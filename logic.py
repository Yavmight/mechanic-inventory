def is_low_stock(quantity, threshold=5):
    return quantity <= threshold

def get_low_stock_parts(parts):
    return [part for part in parts if is_low_stock(part['quantity'], part['low_stock_threshold'])]