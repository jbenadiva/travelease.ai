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
              f"those traveling with you. You have a new client and want to make a perfect, detailed itinerary with "
              f"very specific recommendations with specific bars and restaurants. Here is their itinerary:\n{itinerary}\n"
              f" They enjoy {preferences}."
              f" Please generate a very specific and personalized itinerary in terms of locations and restaurants for your new client!"
              f" Please optimize travel times.")

    return prompt


if __name__ == "__main__":
    app.run()
