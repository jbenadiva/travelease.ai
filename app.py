import os

from dotenv import load_dotenv
load_dotenv()

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = "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"


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        location = request.form["location"]
        days = request.form["days"]
        neighborhood = request.form["neighborhood"]
        travel_desires = request.form.getlist("travel_desires")
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(location, days, neighborhood, travel_desires),
            temperature=0.6,
            max_tokens=3000,  # Increase this value to allow longer responses
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(location, days, neighborhood, travel_desires):
    if neighborhood:
        neighborhood_prompt = f", staying in the {neighborhood} neighborhood"
    else:
        neighborhood_prompt = ""

    travel_desires_str = ", ".join(travel_desires)

    return f"""You are a seasoned travel agent, and you have a knack for customizing the perfect schedule for those traveling with you, including finding some hidden gems. You are fun, cool, and great to speak with. You have a new client who is looking to spend {days} days in {location}{neighborhood_prompt}. They {travel_desires_str}. Please set up a full itinerary for them with an hour-by-hour breakdown."""


if __name__ == "__main__":
    app.run()
