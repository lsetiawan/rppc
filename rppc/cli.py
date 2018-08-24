import argparse

from . import init

def parse_args():
    parser = argparse.ArgumentParser(description='Package Creator')
    subparsers = parser.add_subparsers(dest='cmd', help='Additional Commands')

    init_parser = subparsers.add_parser('init', help='Initialize a repository')
    init_parser.add_argument('-f','--file', type=argparse.FileType('r'), help='Info file')
    init_parser.add_argument('-gh', '--github', action='store_true', help='Upload to github')

    return parser.parse_args()

def main():
    args = parse_args()
    if args.cmd == 'init':
        init(info_file=args.file, init_github=args.github)

if __name__ == '__main__':
    main()