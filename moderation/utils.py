# moderation/utils.py

import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from transformers import pipeline
import warnings
from transformers.utils import logging as transformers_logging

# ==================== SUPPRESS WARNINGS ====================
warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    module="transformers.tokenization_utils_base",
    message=".*clean_up_tokenization_spaces.*"
)
transformers_logging.set_verbosity_error()

# ==================== PROFANITY FILTER ====================
PROFANITY_WORDS = {
    "fuck", "fucking", "fucked", "fucker", "motherfucker",
    "shit", "shitty", "bullshit", "crap",
    "ass", "asshole", "arse", "arsehole",
    "bitch", "sonofabitch", "bastard",
    "damn", "goddamn", "piss", "pissed",
    "cock", "dick", "prick", "cunt", "twat", "wanker",
    "nigger", "nigga", "faggot", "retard", "spastic"
}

vectorizer = CountVectorizer(vocabulary=PROFANITY_WORDS, lowercase=True, token_pattern=r'\b\w+\b')

# ==================== SENTIMENT PIPELINE ====================
try:
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=-1  # CPU
    )
except Exception as e:
    print(f"Failed to load sentiment model: {e}")
    sentiment_pipeline = None

# ==================== MODERATION FUNCTION ====================
def moderate_content(text: str):
    """
    Returns: (is_flagged: bool, reason: str, score: float)
    """
    if not text or not isinstance(text, str):
        return False, "", 0.0

    text_lower = text.lower()

    # Profanity check
    X = vectorizer.transform([text_lower])
    profanity_count = X.sum()

    if profanity_count > 0:
        return True, "Contains profanity", float(profanity_count)

    # Sentiment analysis (highly negative = potentially toxic)
    if sentiment_pipeline:
        try:
            result = sentiment_pipeline(text[:512])[0]
            label = result['label']
            score = result['score']

            if label == 'NEGATIVE' and score > 0.85:
                return True, "Highly negative/toxic sentiment", score
        except Exception as e:
            print(f"Sentiment analysis error: {e}")

    return False, "", 0.0


# ==================== SENTIMENT SCORE (Separate utility) ====================
def get_post_sentiment_score(text: str) -> float:
    if not sentiment_pipeline or not text:
        return 0.0

    try:
        result = sentiment_pipeline(text[:512])[0]
        score = result['score']
        if result['label'] == 'POSITIVE':
            return score
        else:
            return -score
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        return 0.0