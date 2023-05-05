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
        # Update these lines to get the correct input values from the form
        locations = request.form.getlist("locations")
        nights = request.form.getlist("nights")
        travel_desires = request.form.getlist("travel_desires")

        prompt = generate_prompt(locations, nights, travel_desires)
        print(f"Generated Prompt: {prompt}")  # Print the generated prompt to the console
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=3000,  # Increase this value to allow longer responses
        )
        result = response.choices[0].text.strip()
        return render_template("index.html", result=result)

    return render_template("index.html")


def generate_prompt(locations, nights, travel_desires):
    itinerary = "\n".join([f"They are travelling to {loc} for {night} nights" for loc, night in zip(locations, nights)])
    preferences = ", ".join(travel_desires)

    prompt = (f"You are a seasoned travel agent, and you have a knack for customizing the perfect schedule for "
              f"those traveling with you, including finding some hidden gems. You are fun, cool, and great to "
              f"speak with. You have a new client and want to make a great impression on what an creative travel "
              f"agent you are with very specific recommendations with specific bars and restauarants if possible. Here is their itinerary:\n{itinerary}\n"
              f" As for their travel preferences, they enjoy {preferences}."
              f" Please generate a very detailed, very specific in terms of locations and restaurants, and fun itinerary for your new client!")

    return prompt


if __name__ == "__main__":
    app.run()
