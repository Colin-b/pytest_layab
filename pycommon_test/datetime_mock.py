import datetime

previous_datetime_module = datetime.datetime


class NowMock(datetime.datetime):
    date_time = None

    @classmethod
    def now(cls, tz=None):
        return cls.date_time

    @classmethod
    def utcnow(cls):
        return cls.date_time


def mock_now(date_time: str='2018-10-11T15:05:05.663979') -> None:
    """
    Mock datetime.datetime.now() and datetime.datetime.utcnow() functions.

    :param date_time: The datetime returned by datetime.datetime.now() and datetime.datetime.utcnow()
    """
    NowMock.date_time = datetime.datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S.%f')
    datetime.datetime = NowMock


def revert_now() -> None:
    """
    Revert datetime.datetime to the non-mocked version.
    """
    datetime.datetime = previous_datetime_module
