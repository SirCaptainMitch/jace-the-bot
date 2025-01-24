import unittest
from scryfall.endpoints import CatalogEndpoint, BulkEndpoint


class CatalogEndpointTestCase(unittest.TestCase):
    def test_land_types(self):
        land_types = CatalogEndpoint().get_catalog(name='land-types')
        expected = [
            'Cave'
            , 'Cloud'
            , 'Desert'
            , 'Forest'
            , 'Gate'
            , 'Island'
            , 'Lair'
            , 'Locus'
            , 'Mine'
            , 'Mountain'
            , 'Sphere'
            , 'Plains'
            , 'Power-Plant'
            , 'Swamp'
            , 'Tower'
            , "Urza's"
        ]
        actual = land_types
        self.assertListEqual(sorted(expected), sorted(actual))  # add assertion here


class BulkDataTestCase(unittest.TestCase):
    def test_oracle_cards(self):
        res = BulkEndpoint().get_oracle_cards()
        self.assertIsNotNone(res)

    def test_rulings(self):
        res = BulkEndpoint().get_rulings()
        self.assertIsNotNone(res)

    def test_unique_artwork(self):
        res = BulkEndpoint().get_unique_artwork()
        self.assertIsNotNone(res)

    def test_default_cards(self):
        res = BulkEndpoint().get_default_cards()
        self.assertIsNotNone(res)


if __name__ == '__main__':
    unittest.main()
