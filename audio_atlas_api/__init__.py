from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return {"message": "Hello, World!"}


@app.route("/api/v1/health")
def health_check():
    return {"status": "ok"}
