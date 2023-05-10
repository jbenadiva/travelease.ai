from celery import Celery

def make_celery(app_name, broker):
    app = Celery(app_name, broker=broker)
    return app

def add(x, y):
    return x + y