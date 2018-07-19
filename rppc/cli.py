import argparse

from . import init

def parse_args():
    parser = argparse.ArgumentParser(description='Package Creator')
    subparsers = parser.add_subparsers(dest='cmd')
    init_parser = subparsers.add_parser('init')

    return parser.parse_args()

def main():
    args = parse_args()
    if args.cmd == 'init':
        init()

if __name__ == '__main__':
    main()