# import re
# from rapidfuzz import fuzz


# NUM_WORDS = {
#     "zero": "0",
#     "one": "1",
#     "two": "2",
#     "three": "3",
#     "four": "4",
#     "five": "5",
#     "six": "6",
#     "seven": "7",
#     "eight": "8",
#     "nine": "9",
#     "ten": "10",
#     "eleven": "11",
#     "twelve": "12",
#     "thirteen": "13",
#     "fourteen": "14",
#     "fifteen": "15",
# }
# FUZZY_ANCHORS = [
#     "regulation",
#     "reg",
#     "regulation-",
#     "regltn",
#     "reggulation",
#     "regulashun",
# ]
# def convert_num_words_to_digits(text):
#     words = text.lower().split()
#     converted = [NUM_WORDS.get(word, word) for word in words]
#     return " ".join(converted)


# def extract_regulation_number(query, anchor_keywords=FUZZY_ANCHORS, threshold=80):
#     print("In extract regulation number")
#     words = query.lower().split()
#     numbers_found = []

#     for i, word in enumerate(words):
#         for anchor in anchor_keywords:
#             if fuzz.partial_ratio(word, anchor) >= threshold:
#                 # Only check the next word after anchor for a number
#                 for j in range(i + 1, min(i + 4, len(words))):
#                     if re.match(r"^\d{1,2}$", words[j]):
#                         numbers_found.append(words[j])
#                         # Also look for 'and <num>' or ', <num>'
#                 if i + 3 < len(words) and words[i+2] in {"and", ","}:
#                     if re.match(r"^\d{1,2}$", words[i+3]):
#                         numbers_found.append(words[i+3])
#     print("number found: ",list(set(numbers_found)))
#     return list(set(numbers_found))
