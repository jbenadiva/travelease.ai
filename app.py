import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from celery import Celery

load_dotenv()

import openai

app = Flask(__name__)
openai.api_key = os.environ["OPENAI_API_KEY"]

def make_celery(app_name, broker):
    celery = Celery(app_name, broker=broker)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app.config.update(
    CELERY_BROKER_URL=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
    CELERY_RESULT_BACKEND=os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
)

celery = make_celery('myapp', app.config['CELERY_BROKER_URL'])

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        # Update these lines to get the correct input values from the form
        locations = request.form.getlist("locations")
        nights = request.form.getlist("nights")
        travel_desires = request.form.getlist("travel_desires")

        prompt = generate_prompt(locations, nights, travel_desires)
        print(f"Generated Prompt: {prompt}")  # Print the generated prompt to the console
        openai_task.delay(prompt)
        return "Your request is being processed. Please check back later for the result.", 202

    return render_template("index.html")


@celery.task()
def openai_task(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # use the new chat model
        messages=[
            {"role": "system", "content": "You are a seasoned travel agent with a knack for creating detailed and personalized travel itineraries."},
            {"role": "user", "content": prompt},
        ],
    )
    result = response.choices[0].message['content'].strip()
    # Store the result somewhere like a database or a cache for retrieval


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
    app.run()