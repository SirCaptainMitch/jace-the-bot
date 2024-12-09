import unittest
from gatherer import RulesEndpoint


class BulkDataTestCase(unittest.TestCase):

    def test_txt_rules(self):
        res = RulesEndpoint().get_txt_rules()
        self.assertIsNotNone(res)


if __name__ == '__main__':
    unittest.main()
