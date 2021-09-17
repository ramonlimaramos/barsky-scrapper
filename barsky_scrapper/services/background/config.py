from os import environ as env
from urllib.parse import urlparse
import re
from kombu import Queue


__is_worker = env.get('MODE', 'worker').lower() == 'worker'

broker_url = env.get('BROKER_URL', 'amqp://rabbitmq:rabbitmq@barsky-scrapper-rabbit:5672')

broker_url_parsed = urlparse(broker_url)

if broker_url_parsed.scheme == 'amqps':
    broker_transport_options = {'login_method': 'PLAIN'}

if __is_worker:
    result_backend = env.get('BACKEND_URL', 'redis://redis/2')
    redis_retry_on_timeout = env.get('REDIS_RETRY_ON_TIMEOUT', 'false').lower() == 'true'
    redis_socket_keepalive = env.get('REDIS_SOCKET_KEEPALIVE', 'false').lower() == 'true'

task_create_missing_queues = True
result_expires = 60 * 60 * 3  # 3 hours
result_chord_join_timeout = 120
task_acks_late = True
task_reject_on_worker_lost = True
task_serializer = 'json'

task_default_queue = 'barsky_scrapper'

task_queues = (
    Queue('barsky_scrapper',
          routing_key='barsky_scrapper.#'),
    Queue('workflows',
          routing_key='workflow.#')
)

task_routes = ([
    (re.compile(r'^(.*)_workflow$'),
        {'queue': 'workflows',
         'routing_key': 'workflow.task'}),
    ('*', 
        {'queue': 'barsky_scrapper'}),
],)

# TODO: scrapps it all the time without stop buddy!
# beat_schedule = {
#     'beat-worker-schedule-name': {
#         'task': 'barsky_scrapper.services.file_name.task_name',
#         'schedule': 60*30,
#         'options': {
#             'expires': 60*5,
#             'rate_limit': '1/m'
#         }
#     },
# }
