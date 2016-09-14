from celery import Celery


app = Celery('tswift', broker='amqp://guest:guest@localhost:5672//', include=['tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_IGNORE_RESULT=True,
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
)
