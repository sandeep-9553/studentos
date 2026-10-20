RULES = {
    "Food": ["breakfast", "lunch", "dinner", "tea", "snack", "canteen", "biryani"],
    "Travel": ["bus", "auto", "metro", "petrol", "train", "cab", "railway"],
    "Shopping": ["amazon", "flipkart", "clothes", "shoes", "headphones"],
    "Recharge/Bills": ["recharge", "wifi", "bill"],
    "Education": ["book", "xerox", "fees", "course", "notes"],
    "Entertainment": ["movie", "game", "netflix"],
}

def categorize(description):
    d = description.lower()
    for category, words in RULES.items():
        if any(word in d for word in words):
            return category
    return "Others"