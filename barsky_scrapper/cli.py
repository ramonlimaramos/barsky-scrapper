from barsky_scrapper.services import DealerRaterService
from barsky_scrapper.domain import AdapterBuickReview
from pprint import pprint


def suspicious(model):
    dealer_rater_service = DealerRaterService()

    for x in range (0,5):  
        b = "Loading" + "." * x
        print (b, end="\r")

    reviews = AdapterBuickReview(service=dealer_rater_service)
    suspicious = reviews.most_suspicious

    for item in suspicious['reviews']:
        print('Title:', item['title'])
        print('User:', item['user'])
        print('Date:', item['date'])
        print('Class:', item['fakeLevelLabel'])
        print('Score:', item['fakeLevelValue'])
        print('Ratings:')
        pprint(item['ratings'])
        print('Employees:')
        pprint(item['employees'])
        print(item['text'])
        print('\n')


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
