# Times around the world

Strava application that calculates how many times you've circled the world based on your recorded Strava activites.

## Getting started

Create a new virtual environment for the project and install dependencies:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with the following properties:

```
DEBUG=True
FLASK_ENV=development
FLASK_APP=app.py
REDIRECT_URI=http://localhost:5000/calculate
CLIENT_ID=<strava-app-client-id>
CLIENT_SECRET=<strava-app-client-secret>
REFRESH_TOKEN=<strava-app-refresh-token>
```

Start the application:

```
flask run
```

You should be able to open the application now on `localhost:5000`.
