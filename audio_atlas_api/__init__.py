from flask import Flask
from .routes import main, audio, retrieve
from dotenv import load_dotenv
import os
# from torch

load_dotenv()
ENDPOINT_PREFIX = os.getenv("ENDPOINT_PREFIX")

app = Flask(__name__)
app.register_blueprint(main, url_prefix=ENDPOINT_PREFIX)
app.register_blueprint(audio, url_prefix=f"{ENDPOINT_PREFIX}/audio")
app.register_blueprint(retrieve, url_prefix=f"{ENDPOINT_PREFIX}/retrieve")

# app.run(host="0.0.0.0", port=5000)


# python3 -m flask --app audio_atlas_api run
# 4HeC2hUOYbllz9TM

