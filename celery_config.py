from celery import Celery

# The argument to Celery is the name of the current module.
# This is needed so that names can be automatically generated.
app = Celery('myapp', broker='redis://localhost:6379/0')

@app.task
def add(x, y):
    return x + y