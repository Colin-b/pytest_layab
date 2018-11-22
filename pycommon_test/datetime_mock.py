import datetime


class NowMock(datetime.datetime):
    date_time = None

    @classmethod
    def now(cls, tz=None):
        return cls.date_time


def mock_now(date_time: str='2018-10-11T15:05:05') -> None:
    """
    Mock datetime.now() function.

    :param date_time: The datetime returned by datetime.now()
    """
    NowMock.date_time = datetime.datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S')
    datetime.datetime = NowMock
