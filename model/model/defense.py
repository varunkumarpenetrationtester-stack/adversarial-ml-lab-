def sanitize_data(df):
    return df.drop_duplicates().reset_index(drop=True)

def confidence_filter(prob):
    if prob < 0.6:
        return "⚠️ Uncertain – Manual Review Recommended"
    return "✅ Confident Prediction"
