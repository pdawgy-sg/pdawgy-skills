import unittest
from ledgerbox.service import summarize


class ServiceTest(unittest.TestCase):
    def test_summary(self):
        self.assertEqual(summarize([1, 2]), "Total: 3")
