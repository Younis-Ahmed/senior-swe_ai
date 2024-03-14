from argparse import ArgumentParser, Namespace

def main():
    parser = ArgumentParser(description='SeniorSWE cli tool utilize AI to help you with your project')

    parser.add_argument('init', help='initialize the app')


    args: Namespace = parser.parse_args()
    print(args)

if __name__ == '__main__':
    main()