# MARK: - Core Statistics Functions for PyToolkit

from collections import Counter, defaultdict
from functools import lru_cache, wraps

def log_call(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"Calling {fn.__name__}", end=" #### ")
        return fn(*args, **kwargs)
    return wrapper

@lru_cache(maxsize=32)
@log_call
def cached_word_count(text):
    return len(text.split())

@log_call
def word_stats(words, plugin=None):
    normalized_words = [w.lower().strip(".,!?") for w in words if w]
    if plugin:
        normalized_text = " ".join(normalized_words)
        normalized_text = plugin(normalized_text)
        normalized_words = normalized_text.split()

    counter = Counter(normalized_words)
    by_prefix = defaultdict(list)
    for w in counter:
        by_prefix[w[0]].append(w)
    return counter, by_prefix