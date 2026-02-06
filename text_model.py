from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis")

def analyze_text(text):
    result = sentiment_model(text)[0]
    label = result['label']
    score = result['score']
    return label, score