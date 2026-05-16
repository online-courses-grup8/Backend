from django.test import SimpleTestCase
from unittest.mock import MagicMock
from datetime import date, time
from users.serializers.my_events import EventSummarySerializer


# EventSummarySerializer için birim testler
class EventSummarySerializerTest(SimpleTestCase):

    def setUp(self):
        self.serializer = EventSummarySerializer()

    def _make_event(self, event_date=None, start_time=None, end_time=None):
        # mock Event objesi oluşturur
        event = MagicMock()
        event.date = event_date
        event.start_time = start_time
        event.end_time = end_time
        return event

    # get_year Testleri

    def test_year_returns_string(self):
        # yılı string olarak döndürmeli
        event = self._make_event(event_date=date(2026, 5, 16))
        result = self.serializer.get_year(event)
        self.assertEqual(result, "2026")
        self.assertIsInstance(result, str)

    # get_day Testleri

    def test_day_zero_padded(self):
        # tek haneli günleri başına sıfır ekleyerek döndürmeli
        cases = [
            (date(2026, 5, 1), "01"),
            (date(2026, 5, 9), "09"),
            (date(2026, 5, 10), "10"),
            (date(2026, 5, 31), "31"),
        ]
        for event_date, expected in cases:
            with self.subTest(event_date=event_date):
                event = self._make_event(event_date=event_date)
                result = self.serializer.get_day(event)
                self.assertEqual(result, expected)

    # get_month Testleri

    def test_month_returns_uppercase_abbreviation(self):
        # ay kısaltması büyük harf ve ingilizce olmalı
        cases = [
            (date(2026, 1, 1), "JAN"),
            (date(2026, 5, 1), "MAY"),
            (date(2026, 6, 1), "JUN"),
            (date(2026, 9, 1), "SEP"),
            (date(2026, 12, 1), "DEC"),
        ]
        for event_date, expected in cases:
            with self.subTest(event_date=event_date):
                event = self._make_event(event_date=event_date)
                result = self.serializer.get_month(event)
                self.assertEqual(result, expected)

    # get_timeRange Testleri

    def test_time_range_format(self):
        # başlangıç ve bitiş saatinden doğru AM/PM formatı üretmeli
        cases = [
            (time(10, 0), time(17, 0), "10:00 AM - 05:00 PM"),
            (time(9, 30), time(13, 30), "09:30 AM - 01:30 PM"),
            (time(0, 0), time(12, 0), "12:00 AM - 12:00 PM"),
            (time(0, 0), time(23, 59), "12:00 AM - 11:59 PM"),
        ]
        for start, end, expected in cases:
            with self.subTest(start=start, end=end):
                event = self._make_event(start_time=start, end_time=end)
                result = self.serializer.get_timeRange(event)
                self.assertEqual(result, expected)

    def test_time_range_with_noon_and_midnight(self):
        # öğle ve gece yarısı gibi kritik saatleri doğru dönmeli
        event = self._make_event(start_time=time(12, 0), end_time=time(0, 0))
        result = self.serializer.get_timeRange(event)
        # 12:00 PM (Öğle) - 12:00 AM (Gece yarısı)
        self.assertEqual(result, "12:00 PM - 12:00 AM")