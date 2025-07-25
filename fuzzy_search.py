import re
from rapidfuzz import fuzz

FUZZY_ANCHORS=["regulation","reg","regulation-","regltn","reggulation","regulashun"]

def extract_regulation_number(query,anchor_keywords=FUZZY_ANCHORS,threshold=80):
    words=query.lower().split()
    numbers_found=[]
    for i, word in enumerate(words):
        for anchor in anchor_keywords:
            if fuzz.partial_ratio(word,anchor)>=threshold:
                nearby_words=words[max(0,i-2):i+3]
                for w in nearby_words:
                    if re.match(r"^\d{1,2}$", w):
                        numbers_found.append(w)
    return list(set(numbers_found))