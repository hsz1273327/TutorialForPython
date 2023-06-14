import unittest
import nsa.pa as pa
import nsa.pb as pb


class Test_load(unittest.TestCase):

    def test_load(self) -> None:
        self.assertEqual(pa.ME, "pa")
        self.assertEqual(pb.ME, "pb")
