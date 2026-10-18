# MARK: - Core Statistics Functions for PyToolkit

from collections import Counter, defaultdict
from functools import lru_cache, wraps

def log_call(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"Calling {fn.__name__}", end=" #### ")
        return fn(*args, **kwargs)
    return wrapper

###LEGACY###
'''
@lru_cache(maxsize=32)
@log_call
def cached_word_count(text):
    return len(text.split())
'''

@lru_cache(maxsize=128)
def normalize_word(word):
    return word.lower().strip(".,!?")

@log_call
def word_stats(lines, transform=None):
    cache_before = normalize_word.cache_info()
    counter = Counter()
    line_count = 0
    word_count = 0
    character_count = 0
    for line in lines:
        line_count += 1
        character_count += len(line)
        normalized_words = []
        for word in line.split():
            cleaned = normalize_word(word)
            if cleaned:
                normalized_words.append(cleaned)
        if transform:
            normalized_text = " ".join(normalized_words)
            normalized_text = transform(normalized_text)
            normalized_words = normalized_text.split()
        word_count += len(normalized_words)
        counter.update(normalized_words)

    by_prefix = defaultdict(list)
    for word in counter:
        by_prefix[word[0]].append(word)

    cache_after = normalize_word.cache_info()
    hits = cache_after.hits - cache_before.hits
    misses = cache_after.misses - cache_before.misses
    print(f"normalize_word cache: {hits} hits, {misses} misses")
    return counter, by_prefix, word_count, line_count, character_count
