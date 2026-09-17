# MARK: - PyToolkit.py

import argparse, io
from collections import Counter, defaultdict
from contextlib import redirect_stdout

buffer = " "
def build_parser():
    parser = argparse.ArgumentParser(description="PyToolkit text utilities")
    sub = parser.add_subparsers(dest="command", required=True)
    analyze = sub.add_parser("analyze", help="Analyze a text file")
    analyze.add_argument("-f", "--file", required=True, help="Input file")
    analyze.add_argument("-v", "--verbose", action="store_true")
    return parser

def safe_read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {path} not found")
        return ""

def capture_report(path):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print(f"Analyzing {path}")  
    return buffer.getvalue()

def word_stats(words):
    counter = Counter(w.lower().strip(".,!?") for w in words if w)
    by_prefix = defaultdict(list)
    for w in counter:
        by_prefix[w[0]].append(w)
    return counter, by_prefix

def analyze_file(path, verbose=False):
    text = safe_read(path)
    words = text.split()
    counter, by_prefix = word_stats(words)
    print(f"Words: {len(words)}")
    if verbose:
        print(f"Characters: {len(text)}")
        print(counter.most_common(5))
        print(by_prefix)
        
def main():
    args = build_parser().parse_args()
    if args.command == "analyze":
        report = capture_report(args.file)
        '''Work in progress: The report is captured but not printed. Uncomment the following lines to see the captured report.'''
        #print("Captured report:")
        #print(report)
        analyze_file(args.file, args.verbose)
        


if __name__ == "__main__":
    main()
