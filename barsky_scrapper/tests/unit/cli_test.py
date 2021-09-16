from unittest import TestCase
from barsky_scrapper.tests.cli_spec import ScrapperDealerRaterCLISpec
from barsky_scrapper.cli import parse_arguments


class ScrapperDealerRaterCLITest(ScrapperDealerRaterCLISpec, TestCase):

    def setUp(self):
        super(ScrapperDealerRaterCLITest, self).setUp()
        self._parser = self._create_parser()

    def tearDown(self):
        super(ScrapperDealerRaterCLITest, self).tearDown()
        self._parsed = ''

    def _create_parser(args, **kwargs):
        return parse_arguments()

    def when_execute_cli(self, *args):
        self._arg = [*args]

    def assert_triggered_with_code(self, exit_code):
        with self.assertRaises(SystemExit) as cm:
            self._parsed = self._parser.parse_args(self._arg)
            self.assertEqual(cm.exception.code, exit_code)