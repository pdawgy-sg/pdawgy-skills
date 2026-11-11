import argparse
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    if not args.source.is_file():
        print('Source must be a file', file=sys.stderr)
        return 1
    try:
        content = args.source.read_text()
        args.destination.parent.mkdir(parents=True, exist_ok=True)
        args.destination.write_text(content)
    except OSError as error:
        print(error, file=sys.stderr)
        return 1
    print(f'Copied {args.source} -> {args.destination}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
