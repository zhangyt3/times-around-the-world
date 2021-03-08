from flask import Flask, render_template, request
import requests
import os
import json


app = Flask(__name__)
app.config["REDIRECT_URI"] = os.environ.get("REDIRECT_URI")
app.config["CLIENT_ID"] = os.environ.get("CLIENT_ID")
app.config["CLIENT_SECRET"] = os.environ.get("CLIENT_SECRET")
app.config["REFRESH_TOKEN"] = os.environ.get("REFRESH_TOKEN")


@app.route("/")
def index():
    return render_template("index.html", oauth_link=get_strava_oauth_link(app.config["REDIRECT_URI"]))


@app.route("/calculate")
def calculate():
    authcode = request.args.get("code")
    athlete, access_token = get_access_token(authcode)
    name = f"{athlete['firstname']} {athlete['lastname']}"
    return render_template("calculate.html", name=name)


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


def get_strava_oauth_link(redirect_uri):
    return f"https://www.strava.com/oauth/authorize?client_id={app.config['CLIENT_ID']}&response_type=code&redirect_uri={redirect_uri}&approval_prompt=force&scope=read,activity:read_all"


if __name__ == "__main__":
    app.run(threaded=True)
