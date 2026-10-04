# MARK: - PyToolkit.py

import argparse, io
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from functools import lru_cache, wraps, partial

def log_call(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"Calling {fn.__name__}", end=" #### ")
        return fn(*args, **kwargs)
    return wrapper

@log_call
def build_parser():
    parser = argparse.ArgumentParser(description="PyToolkit text utilities")
    sub = parser.add_subparsers(dest="command", required=True)
    analyze = sub.add_parser("analyze", help="Analyze a text file")
    analyze.add_argument("-f", "--file", required=True, help="Input file")
    analyze.add_argument("-v", "--verbose", action="store_true")
    return parser

@log_call
def safe_read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"\nError: {path} not found")
        return ""

@log_call
def capture_report(path):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print(f"Analyzing {path}")  
    return buffer.getvalue()

@lru_cache(maxsize=32)
@log_call
def cached_word_count(text):
    return len(text.split())

@log_call
def word_stats(words):
    counter = Counter(w.lower().strip(".,!?") for w in words if w)
    by_prefix = defaultdict(list)
    for w in counter:
        by_prefix[w[0]].append(w)
    return counter, by_prefix

@log_call
def analyze_file(path, verbose=False):
    text = safe_read(path)
    words = text.split()
    counter, by_prefix = word_stats(words)
    print(f"\nWords: {cached_word_count(text)}")
    if verbose:
        print(f"Characters: {len(text)}")
        print(counter.most_common(5))
        print(by_prefix)

_analyze_short = partial(analyze_file, verbose=False)

@log_call
def analyze_short(path):
    return _analyze_short(path)
        
@log_call
def main():
    args = build_parser().parse_args()
    if args.command == "analyze":
        if args.verbose:
            analyze_file(args.file, verbose=True)
        else:
            analyze_short(args.file)
        '''Work in progress'''
        report = capture_report(args.file)
        print("\nCaptured report:", report)
        '''Previous funtion call'''
        #analyze_file(args.file, args.verbose)
        
if __name__ == "__main__":
    main()
