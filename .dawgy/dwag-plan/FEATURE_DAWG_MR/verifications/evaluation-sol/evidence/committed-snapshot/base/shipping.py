def quote(weight_kg):
    if weight_kg <= 0:
        raise ValueError("weight must be positive")
    return int(weight_kg) * 5
