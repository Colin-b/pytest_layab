from typing import List, Union


class LDAP3ConnectionMock:

    should_connect = True
    results = {}

    def __init__(self, *args, **kwargs):
        self.closed = not self.should_connect
        self.entries = None

    def unbind(self):
        self.closed = True

    def search(self, search_base: str, search_filter: str, attributes: List[str]):
        all_results = self.results.get((search_base, search_filter))
        if not all_results:
            raise Exception('Unexpected call. You need to mock this call.')

        result = all_results.pop(0)

        if result and len(result) == 1 and isinstance(result[0], Exception):
            raise result[0]

        self.entries = self._to_results(result, attributes)

    @classmethod
    def add_search_result(cls, search_base: str, search_filter: str, *results: Union[Exception, dict]):
        cls.results.setdefault((search_base, search_filter), []).append(results)

    @classmethod
    def _to_results(cls, results: List[dict], attributes: List[str]):
        return [
            cls._to_result(result, attributes)
            for result in results
        ]

    @classmethod
    def _to_result(cls, result: dict, attributes: List[str]):
        class Result:
            def __getattr__(self, item):
                if item in attributes:
                    class Attribute:
                        value = result.get(item)

                    return Attribute
                raise AttributeError()

        return Result()

    @classmethod
    def reset(cls):
        if cls.results:
            results = dict(cls.results)
            cls.results.clear()
            raise Exception(f'Expected results were not retrieved: {results}')


import ldap3

ldap3.Connection = LDAP3ConnectionMock
