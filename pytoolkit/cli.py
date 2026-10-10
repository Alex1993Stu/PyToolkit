# MARK: - Command Line Interface (CLI) for PyToolkit

import argparse, io, importlib

from .stats import log_call, cached_word_count, word_stats
from contextlib import redirect_stdout
from functools import partial

@log_call
def build_parser():
    parser = argparse.ArgumentParser(description="PyToolkit text utilities")
    sub = parser.add_subparsers(dest="command", required=True)
    analyze = sub.add_parser("analyze", help="Analyze a text file")
    analyze.add_argument("-f", "--file", required=True, help="Input file")
    analyze.add_argument("-v", "--verbose", action="store_true")
    analyze.add_argument("-p", "--plugin", help="Plugin to apply to the text")
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
def load_plugin(name):
    module = importlib.import_module(f"pytoolkit.plugins.{name}")
    return module.apply

@log_call
def capture_report(path):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print(f"Analyzing {path}")  
    return buffer.getvalue()

@log_call
def analyze_file(path, verbose=False, plugin=None):
    text = safe_read(path)
    words = text.split()
    apply_plugin = None

    if plugin:
        apply_plugin = load_plugin(plugin)
    counter, by_prefix = word_stats(words, apply_plugin)
    output = f"\nWords: {cached_word_count(text)}"

    if verbose:
        output += f"\nCharacters: {len(text)}"
        output += f"\nMost common words: {counter.most_common(5)}"
        output += f"\nBy prefix: {by_prefix}"
    print(output)

_analyze_upper = partial(analyze_file, verbose=False, plugin="uppercase")
_analyze_short = partial(analyze_file, verbose=False)

@log_call
def analyze_short(path, plugin=None):
    return _analyze_short(path, plugin=plugin)
        
@log_call
def main():
    args = build_parser().parse_args()
    if args.command == "analyze":
        if args.verbose:
            analyze_file(args.file, verbose=True, plugin=args.plugin)
        else:
            analyze_short(args.file, plugin=args.plugin)
        
        ''' Work in progress '''
        report = capture_report(args.file)
        print("\nCaptured report:", report)
        ''' Previous funtion call '''
        #analyze_file(args.file, args.verbose)

if __name__ == "__main__":
    main()