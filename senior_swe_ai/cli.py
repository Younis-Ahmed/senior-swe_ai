""" SeniorSWE cli tool utilize AI to help you with your project """
from argparse import ArgumentParser, Namespace
import sys


def main() -> None:
    """ __main__ """
    parser = ArgumentParser(
        description='SeniorSWE cli tool utilize AI to help you with your project'
    )

    parser.add_argument(
        'options', choices=['init', 'chat'], 
        help="'init': initialize the app. 'chat': chat with the AI"
    )

    args: Namespace = parser.parse_args()

    if args.options == 'init':
        print('Initializing the app...')
        config_init() # TODO: Implement this function
        sys.exit()

if __name__ == '__main__':
    main()
