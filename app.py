import os

from dotenv import load_dotenv
load_dotenv()

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.environ["OPENAI_API_KEY"]


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        locations = request.form.getlist("location")
        nights = request.form.getlist("nights")
        neighborhoods = request.form.getlist("neighborhood")
        travel_desires = request.form.getlist("travel_desires")

        prompt = generate_prompt(locations, nights, neighborhoods, travel_desires)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.6,
            max_tokens=3000,  # Increase this value to allow longer responses
        )
        result = response.choices[0].text
        return render_template("index.html", result=result)

    return render_template("index.html")


def generate_prompt(locations, nights, neighborhoods, travel_desires):
    travel_desires_prompt = ", ".join(travel_desires)
    itinerary_prompts = []

    for i, location in enumerate(locations):
        nights_str = str(nights[i]) if i < len(nights) else "unknown number of"
        neighborhood_prompt = f" and they would like to stay in {neighborhoods[i]}" if i < len(neighborhoods) and \
                                                                                       neighborhoods[i] else ""
        itinerary_prompt = f"Destination {i + 1}: {location}\nYou have a new client who is looking to spend {nights_str} days in {location}{neighborhood_prompt}."
        itinerary_prompts.append(itinerary_prompt)

    itinerary_prompt_combined = "\n".join(itinerary_prompts)
    prompt = f"Here is your client's travel itinerary:\n{itinerary_prompt_combined}\n\nThey have mentioned that they are interested in the following activities: {travel_desires_prompt} Please create a personalized travel itinerary for them."

    return prompt


if __name__ == "__main__":
    app.run()
