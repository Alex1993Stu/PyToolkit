# MARK: - Core Statistics Functions for PyToolkit

from collections import Counter
from functools import lru_cache, wraps
from itertools import groupby, combinations

def log_call(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"Calling {fn.__name__}", end=" #### ")
        return fn(*args, **kwargs)
    return wrapper

@lru_cache(maxsize=128)
def normalize_word(word):
    return word.lower().strip(".,!?")

def prefix_groups(words):
    for prefix, group in groupby(sorted(words), key=lambda w: w[0]):
        yield prefix, list(group)

def word_pairs(words, n=2):
    return list(combinations(words[:6], n))

@log_call
def word_stats(lines, transform=None):
    cache_before = normalize_word.cache_info()
    counter = Counter()
    line_count = 0
    word_count = 0
    character_count = 0
    sample_words = []
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
        for word in normalized_words:
            if len(sample_words) < 6:
                sample_words.append(word)
        word_count += len(normalized_words)
        counter.update(normalized_words)
    
    ###LEGACY###
    '''
    by_prefix = defaultdict(list)
    for word in counter:
        by_prefix[word[0]].append(word)
    '''
    
    by_prefix = dict(prefix_groups(counter.keys()))
    pairs = word_pairs(sample_words)

    cache_after = normalize_word.cache_info()
    hits = cache_after.hits - cache_before.hits
    misses = cache_after.misses - cache_before.misses
    print(f"normalize_word cache: {hits} hits, {misses} misses")
    return counter, by_prefix, pairs, word_count, line_count, character_count
