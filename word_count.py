"""Demo script created as part of a sub-agent usage demonstration.
Counts lines, words, and characters in a file or stdin, similar to `wc`.
"""

import sys


def count_stats(text):
    lines = text.count("\n")
    if text and not text.endswith("\n"):
        lines += 1
    words = len(text.split())
    chars = len(text)
    return lines, words, chars


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        with open(path, "r") as f:
            text = f.read()
        label = path
    else:
        text = sys.stdin.read()
        label = ""

    lines, words, chars = count_stats(text)
    print(f"{lines:8d} {words:8d} {chars:8d} {label}".rstrip())


if __name__ == "__main__":
    main()
