from __future__ import absolute_import

from celery import Celery

app = Celery('CeleryExample',
             broker='amqp://',
             backend='rpc://',
             include=['CeleryExample.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()

app.conf.update(
    CELERY_ROUTES = {
        'proj.tasks.add': {'queue': 'hipri'},
    },
)