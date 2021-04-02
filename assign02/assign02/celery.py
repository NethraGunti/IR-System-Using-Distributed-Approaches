import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assign02.settings')
BACKEND_URL = 'redis://localhost:6379'
BROKER_URL = 'amqp://localhost'
app = Celery('django_writer', broker=BROKER_URL, backend=BACKEND_URL)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS + settings.INSTALLED_APPS_WITH_APPCONFIGS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
