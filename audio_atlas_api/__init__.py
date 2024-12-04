from flask import Flask
from .routes import main, audio
from dotenv import load_dotenv
# from torch

load_dotenv()
ENDPOINT_PREFIX = "/api/v1"

app = Flask(__name__)
app.register_blueprint(main, url_prefix=ENDPOINT_PREFIX)
app.register_blueprint(audio, url_prefix=f"{ENDPOINT_PREFIX}/audio")


# python3 -m flask --app audio_atlas_api run
# 4HeC2hUOYbllz9TM


