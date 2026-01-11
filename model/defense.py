def sanitize_data(df):
    return df.drop_duplicates().reset_index(drop=True)

def confidence_filter(confidence):
    if confidence < 0.6:
        return "⚠️ Low confidence – Manual review recommended"
    return "✅ High confidence prediction"
