import io
import soundfile
import time

from base64 import b64encode

from flask import Flask, render_template, request, url_for, send_file
from flask_cors import CORS, cross_origin

from models import models, ALL_MODELS
from file_handler import FileHandler

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

_valid_model_types = [key for key in models if key is not ALL_MODELS]


@app.route("/", methods=["GET"])
@cross_origin()
def index():
    return render_template("speechSynthesis.html", existing_models=models.keys())


@app.route("/synthesize/", methods=["POST"])
@cross_origin()
def synthesize():
    request_json = request.get_json()

    text = request_json["text"]
    model_type = request_json["voice"]

    options = {
        "rate": float(request_json.get("rate", 1.0)),
        "pitch": float(request_json.get("pitch", 1.0)),
        "volume": float(request_json.get("volume", 0.0))
    }

    try:
        model = models[model_type]

        audio = model.synthesize(text, **options)
        sample_rate = model.sample_rate

        wav_file = io.BytesIO()
        soundfile.write(wav_file, audio, sample_rate, format='WAV')

        wav_file.seek(0)
        return send_file(
            wav_file,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='%s.wav' % time.time()
        )
    except Exception as e:
        return {
            "response_code": 1,
            "response": str(e)
        }


@app.route("/synthesize_and_save/", methods=["POST"])
@cross_origin()
def synthesize_and_save():
    request_json = request.get_json()

    text = request_json["text"]
    model_type = request_json["voice"]

    options = {
        "rate": float(request_json.get("rate", 1.0)),
        "pitch": float(request_json.get("pitch", 1.0)),
        "volume": float(request_json.get("volume", 0.0))
    }

    response_code, results = FileHandler.get_synthesized_audio(text, model_type, **options)

    if response_code == 0:
        for result in results:
            filename = result.pop("filename")
            audio_bytes = result.pop("response_audio")
            result["response_audio_url"] = url_for("media_file", filename=filename)
            result["response_audio"] = b64encode(audio_bytes).decode("utf-8")

    return {
        "response_code": response_code,
        "response": results
    }


class InvalidVoice(Exception):
    pass


# Removed: /get_user_dict/, /update_user_dict/, /replace_user_dict/ and /media/<path:filename>
#   because it looks like backdoor
if __name__ == "__main__":
    app.run()
