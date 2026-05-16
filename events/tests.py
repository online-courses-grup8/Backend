from django.test import SimpleTestCase
from unittest.mock import MagicMock
from datetime import time
from events.serializers import HomeEventSerializer


# HomeEventSerializer için birim testler
class HomeEventSerializerTest(SimpleTestCase):

    def setUp(self):
        self.serializer = HomeEventSerializer()

    def _make_event(self, start_time=None, end_time=None):
        # mock Event objesi oluşturur
        event = MagicMock()
        event.start_time = start_time
        event.end_time = end_time
        return event

    # --- get_timeRange Testleri ---

    def test_time_range_format(self):
        # start ve end time'dan doğru format üretmeli
        cases = [
            (time(9, 0), time(17, 0), "09:00 - 17:00"),
            (time(10, 30), time(13, 30), "10:30 - 13:30"),
            (time(0, 0), time(23, 59), "00:00 - 23:59"),
        ]
        for start, end, expected in cases:
            with self.subTest(start=start, end=end):
                event = self._make_event(start_time=start, end_time=end)
                result = self.serializer.get_timeRange(event)
                self.assertEqual(result, expected)
