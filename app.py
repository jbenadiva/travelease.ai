import os
import redis
import logging

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for, jsonify
from celery import Celery, states

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.propagate = True

load_dotenv()

import openai

app = Flask(__name__)
openai.api_key = os.environ["OPENAI_API_KEY"]
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
r = redis.from_url(redis_url)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app.config.update(
    CELERY_BROKER_URL=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
    CELERY_RESULT_BACKEND=os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
)

celery = make_celery(app)

@app.route("/", methods=("GET", "POST"))
def index():
    logger.info("Handling a request to /")
    if request.method == "POST":
        locations = request.form.getlist("locations")
        nights = request.form.getlist("nights")
        travel_desires = request.form.getlist("travel_desires")

        prompt = generate_prompt(locations, nights, travel_desires)
        task = openai_task.delay(prompt)

        task_id = task.id
        logger.info("Created task with ID: %s", task_id)

        # Return the task id
        return jsonify({"task_id": task_id}), 202

    return render_template("index.html")

@app.route("/status/<task_id>")
def taskstatus(task_id):
    task = openai_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'result': task.result  # Get the result from the task
        }
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)  # Make sure to jsonify the response


@celery.task(bind=True)
def openai_task(self, prompt):
    try:
        print("Starting API call...")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a seasoned travel agent with a knack for creating detailed and personalized travel itineraries."},
                {"role": "user", "content": prompt},
            ],
        )
        logger.info("API call completed. Processing response...")
        result = response.choices[0].message['content'].strip()
        logger.info("Response processed. Storing result in Redis...")
        task_id = self.request.id
        logger.info("Task ID: %s", task_id)

        # Store the result in Redis
        r.set(self.request.id, result)
        logger.info("Result stored in Redis. Task completed.")
        logger.info("Result: %s", result)
    except Exception as e:
        logger.error(f"An error occurred in the task: {e}")
        raise


@app.route("/result/<task_id>")
def result(task_id):
    # Retrieve the result from Redis
    result = r.get(task_id)
    if result is None:
        # If there's no result, the task might still be running
        return "Your request is still being processed. Please check back later.", 202
    else:
        return result.decode()  # decode bytes to string before returning

def generate_prompt(locations, nights, travel_desires):
    itinerary = "\n".join([f"I'm travelling to {loc} for {night} nights" for loc, night in zip(locations, nights)])
    preferences = ", ".join(travel_desires)

    prompt = (f"{itinerary}. "
              f"I enjoy {preferences}. "
              f"Could you please generate a very specific and personalized itinerary for me, "
              f"including some hidden gems, specific bars, and restaurants? "
              f"Please also consider travel times to optimize my schedule.")

    return prompt


if __name__ == "__main__":
    try:
        r = redis.from_url(os.environ.get('REDIS_URL', 'redis://localhost:6379/0'))
        r.set('test', 'test_value')
        value = r.get('test')
        logger.info(f"Redis test value: {value}")
    except Exception as e:
        logger.error(f"Error connecting to Redis: {e}")
    app.run()