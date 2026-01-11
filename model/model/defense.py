def sanitize_data(df):
    """
    Removes duplicate entries to reduce poisoning impact.
    """
    return df.drop_duplicates().reset_index(drop=True)

def confidence_filter(prob):
    """
    Applies confidence threshold for safe decision making.
    """
    if prob < 0.6:
        return "⚠️ Uncertain – Manual Review Recommended"
    return "✅ Confident Prediction"

