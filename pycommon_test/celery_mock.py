# -*- coding: utf-8 -*-

import uuid
import logging

from celery import states
from celery.result import EagerResult

logger = logging.getLogger('celery_mock')

def AsyncResultStub(task_id, **kargs):
    return TaskResultStore().get_by_id(task_id)

## setup asyncresultstub
try:
    import pycommon_server.celery_common
    pycommon_server.celery_common.celery_results.AsyncResult = AsyncResultStub
    logger.info("AsyncResultStub installed")
except ImportError:
    logger.error("Fail to install AsyncResultStub")


class Singleton(type):
    """
    Singleton pattern implementation based on metaclass
    Example:
        class MySingleton(metaclass=Singleton):
            pass
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TaskResultStore(metaclass=Singleton):
    __task_store = {}

    def put(self, result):
        self.__task_store[result.id] = result

    def get_by_id(self, id):
        return self.__task_store[id]


class TestCeleryAppProxy:
    """
    Flask rest-plus Namespace proxy.
    This proxy namespace add a decorator 'async_route' that will generate 2 extra endpoint : /status and /result
    to query the status or the result of the celery task
    """

    def __init__(self, celery_app):
        self.celery_app = celery_app
        self.__task_store = {}

    def __getattr__(self, name):
        if name == 'task':
            def task_interceptor(*args, **opts):
                result = getattr(self.celery_app, 'task')(*args, **opts)

                class AsyncTaskProxy:
                    def __init__(self, *a, **o):
                        self.method = a[0]

                    def apply_async(self, *aa, **oo):
                        method_result = self.method(*aa, **oo)
                        task_id = str(uuid.uuid4())
                        celery_result = EagerResult(task_id, method_result, states.SUCCESS)
                        TaskResultStore().put(celery_result)
                        return celery_result

                return AsyncTaskProxy

            return task_interceptor
        else:
            return getattr(self.celery_app, name)
