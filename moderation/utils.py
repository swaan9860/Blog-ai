# moderation/utils.py
from transformers import pipeline
from django.conf import settings

def moderate_content(text):
    # Load pre-trained toxicity classifier
    classifier = pipeline("text-classification", model="unitary/toxic-bert", device=-1)  # CPU
    results = classifier(text, truncation=True, max_length=512)
    
    # Check for toxic content (label 'toxic' with score > threshold)
    for result in results:
        if result['label'] == 'toxic' and result['score'] > 0.7:  # Adjustable threshold
            return True, result['score'], "Toxic content detected"
    return False, 0.0, "Content is clean"