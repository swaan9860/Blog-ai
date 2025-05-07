# BlogAI/moderation/keyword_moderation.py
import re

def moderate_keywords(text):
    # Dictionary of inappropriate phrases with severity scores
    keyword_scores = {
        r'\b(hate|hateful|offensive|stupid|idiot)\b': 0.8,
        r'\b(damn|hell|bastard|fuck|fucker|asshole|ass|bullshit|arse)\b': 0.9,
        r'\b(racist|sexist|bigot|crap|cunt|dickhead|cock|piss|pissed|balls)\b': 0.95,
        r'\b(kill|murder|violence|stab|slash|mutilate|desecrate)\b': 0.95,
        r'\b(bitch|shit|bollocks|bloody|bugger)\b': 0.9,
        r'\b(motherfucker|son of a bitch|sow|arsehole)\b': 0.95
    }

    matches = []
    max_score = 0.0
    is_flagged = False

    # Check each pattern
    for pattern, score in keyword_scores.items():
        regex = re.compile(pattern, re.IGNORECASE)
        found = regex.findall(text)
        if found:
            is_flagged = True
            matches.extend(found)
            max_score = max(max_score, score)

    return is_flagged, matches, max_score if is_flagged else 0.0