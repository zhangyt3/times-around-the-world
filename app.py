from flask import Flask, render_template, request
import requests
import os
import json


app = Flask(__name__)
app.config["REDIRECT_URI"] = os.environ.get("REDIRECT_URI")
app.config["CLIENT_ID"] = os.environ.get("CLIENT_ID")
app.config["CLIENT_SECRET"] = os.environ.get("CLIENT_SECRET")
app.config["REFRESH_TOKEN"] = os.environ.get("REFRESH_TOKEN")

strava_endpoint = "https://www.strava.com/api/v3"
world_circumference = 40075


@app.route("/")
def index():
    return render_template("index.html", oauth_link=get_strava_oauth_link(app.config["REDIRECT_URI"]))


@app.route("/calculate")
def calculate():
    authcode = request.args.get("code")
    athlete, access_token = get_access_token(authcode)

    data = get_athlete_data(athlete["id"], access_token)
    distance_ran = int(data["all_run_totals"]["distance"]) // 1000
    distance_biked = int(data["all_ride_totals"]["distance"]) // 1000
    distance_swam = int(data["all_swim_totals"]["distance"]) // 1000
    distance_total = sum([distance_ran, distance_biked, distance_swam])
    times_around_world = distance_total / world_circumference

    name = f"{athlete['firstname']} {athlete['lastname']}"
    return render_template(
        "calculate.html",
        name=name,
        distance_total=distance_total,
        distance_ran=distance_ran,
        distance_biked=distance_biked,
        distance_swam=distance_swam,
        times_around_world=times_around_world
    )


def get_athlete_data(athlete_id, access_token):
    r = requests.get(get_strava_athlete_stats_endpoint(athlete_id), headers={
        "Authorization": f"Bearer {access_token}"
    })
    parsed = json.loads(r.content)
    return parsed


def get_access_token(authcode):
    r = requests.post("https://www.strava.com/oauth/token", data={
        "client_id": app.config["CLIENT_ID"],
        "client_secret": app.config["CLIENT_SECRET"],
        "code": authcode,
        "grant_type": "authorization_code"
    })
    # TODO: handle error
    parsed = json.loads(r.content)
    access_token = parsed["access_token"]
    athlete = parsed["athlete"]
    return athlete, access_token


def get_strava_athlete_stats_endpoint(athlete_id):
    return f"{strava_endpoint}/athletes/{athlete_id}/stats"


def get_strava_oauth_link(redirect_uri):
    return f"https://www.strava.com/oauth/authorize?client_id={app.config['CLIENT_ID']}&response_type=code&redirect_uri={redirect_uri}&approval_prompt=force&scope=read,activity:read_all"


if __name__ == "__main__":
    app.run(threaded=True)
