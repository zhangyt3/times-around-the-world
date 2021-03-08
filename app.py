from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Welcome</h1>"


if __name__ == "__main__":
    app.run(threaded=True)
