web: gunicorn -b :$PORT --access-logfile - --error-logfile - --log-level debug app:app
worker: celery -A app.celery worker --loglevel=info