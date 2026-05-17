"""
Test Case #280 / Task #280 - Events module unit tests
Azure DevOps Work Item: https://dev.azure.com/grup8devops/Online_Course/_workitems/edit/280

Goal:
Verify event serializer helper logic without touching the database.

Flow:
1. Create mock event objects with start and end times
2. Call HomeEventSerializer.get_timeRange
3. Verify the returned time range uses HH:MM - HH:MM format
"""

from datetime import time
from unittest.mock import MagicMock

from django.test import SimpleTestCase

from events.serializers import HomeEventSerializer


class HomeEventSerializerTest(SimpleTestCase):
    def setUp(self):
        self.serializer = HomeEventSerializer()

    def _make_event(self, start_time=None, end_time=None):
        event = MagicMock()
        event.start_time = start_time
        event.end_time = end_time
        return event

    def test_time_range_format(self):
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
