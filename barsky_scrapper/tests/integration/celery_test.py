from unittest import TestCase, skip, SkipTest
from multiprocessing import Process
from time import sleep, time
from celery import current_app, shared_task
from celery.bin import worker
from celery.result import AsyncResult
from barsky_scrapper.services import create_celery


@shared_task
def ping(secs=1):
    sleep(secs)
    return 'pong'


class BackgroundTest(TestCase):

    def setUp(self):
        raise SkipTest('TODO: these testes are freezing on travis, need to re-checkt then')
        self.server = None

    def tearDown(self):
        if self.server:
            self.server.terminate()
            self.server.join()
            while (self.server.is_alive()):
                sleep(0.1)

    def given_celery_is_running(self):
        create_celery()
        self.app = current_app._get_current_object()
        self.app.autodiscover_tasks(['barsky_scrapper.tests.integration.celery_test'])
        self.app.conf.task_always_eager = False
        self.worker = worker.worker(app=self.app)

        self.server = Process(target=self.worker.run)
        self.server.start()

    def when_ping(self, secs=1):
        start = time()
        self.result = ping.delay(secs)
        self.exec_time = time() - start
        return self.result

    def assert_result_is_async(self):
        self.assertTrue(isinstance(self.result, AsyncResult))

    def test_task_async(self):
        self.given_celery_is_running()

        self.when_ping()

        self.assert_result_is_async()

    def test_task_is_on_background(self):
        self.given_celery_is_running()

        self.when_ping(10)

        self.assertLess(self.exec_time, 1)

    @skip('TODO')
    def test_result_wait(self):
        self.given_celery_is_running()

        start = time()
        self.when_ping(2).get()
        exec_time = time() - start
        self.assertLess(exec_time, 10)
