# MARK: - Command Line Interface (CLI) for PyToolkit

import argparse, io, importlib

from .stats import log_call, word_stats
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

###LEGACY###
'''
@log_call
def safe_read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"\nError: {path} not found")
        return ""
'''

@log_call
def read_lines(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                yield line.rstrip("\n")

@log_call
def count_lines(path):
    return sum(1 for _ in read_lines(path))

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
    apply_plugin = None
    if plugin:
        apply_plugin = load_plugin(plugin)
    try:
        counter, by_prefix, word_count, line_count, character_count = word_stats(
            read_lines(path),
            apply_plugin
        )
    except FileNotFoundError:
        print(f"Error: {path} not found")
        return
    output = f"\nWords: {word_count}"

    if verbose:
        output += f"\nCharacters: {character_count}"
        output += f"\nLines: {line_count}"
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