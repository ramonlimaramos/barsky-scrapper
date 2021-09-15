
def suspicious(model):
    print('the list of suspicious ' + model)


def parse_arguments():
    """Parse arguments for cmd line application."""
    import argparse
    parser = argparse.ArgumentParser(
        description="""Welcome to Barsky Scrapper \n
        the main entry point for the command-line app to list most \n
        suspicious reviews from dealerrater.com""")

    parser.add_argument('--model', type=str,
                        help="""The identifier we use to select\
                         the model from dealerrater.com reviews.\n
                         Example: make suspicious model=buick""")

    return parser


if __name__ == '__main__':
    parser = parse_arguments()
    try:
        args = parser.parse_args()
        suspicious(args.model)
    except Exception as e:
        parser.parse_args(['--help'])
