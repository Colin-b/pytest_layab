# -*- coding: utf-8 -*-

import uuid
import logging

from celery import states
from celery.result import EagerResult

logger = logging.getLogger('celery_mock')


def async_result_stub(task_id, **kargs):
    return TaskResultStore.get_by_id(task_id)



## when you use celery in eager mode, when you call apply_async it returns an EagerResult (instead of AsyncResult).
## In pycommon_server, we use AsyncResult. you cannot get an EagerResult from an AsyncResult.
## With this line of code, any new AsyncResult for a given task id, will return an EagerResult where we can actually fetch the result
## stored in AsyncTaskProxy
import pycommon_server.celery_common
pycommon_server.celery_common.celery_results.AsyncResult = async_result_stub


class EagerResultWithStateSupport(EagerResult):

    def ready(self):
        return self._state == states.READY_STATES


class TaskResultStore:

    __task_store = {}

    @classmethod
    def put(cls, result):
        cls.__task_store[result.id] = result

    @classmethod
    def get_by_id(cls, id):
        return cls.__task_store[id] if id in cls.__task_store else EagerResultWithStateSupport(id, None, states.PENDING )


class TestCeleryAppProxy:
    """
    Celery App proxy. This proxy configures celery app in "task always eager" mode.
    This proxy intercepts task decorator so apply_async is working in this mode.
    """

    def __init__(self, celery_app):
        self.__celery_app = celery_app
        self.__celery_app.conf.update(task_always_eager=True, result_backend='cache', cache_backend='memory',
                                       task_eager_propagates=True)
        self.__task_store = {}

    def __getattr__(self, name):
        if name == 'task':
            def task_interceptor(*aa, **oo):
                result = getattr(self.__celery_app, 'task')(*aa, **oo)

                class AsyncTaskProxy:
                    def __init__(self, method, *a, **o):
                        self.__method = method

                    def apply_async(self, args=None, kwargs=None, task_id=None, producer=None,
                                    link=None, link_error=None, shadow=None, **options):
                        args = args or ()
                        kwargs = kwargs or {}
                        method_result = self.__method(*args, **kwargs)
                        task_id = task_id if task_id else str(uuid.uuid4())
                        celery_result = EagerResult(task_id, method_result, states.SUCCESS)
                        TaskResultStore.put(celery_result)
                        return celery_result

                return AsyncTaskProxy

            return task_interceptor
        else:
            return getattr(self.__celery_app, name)
