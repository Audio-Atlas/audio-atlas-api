from flask import  Blueprint, jsonify, request, send_file
import os
import torch
import numpy as np
import pickle
import laion_clap
from .utils import formatAudioResponseData


main = Blueprint("main", __name__)
audio = Blueprint("audio", __name__)
# sfx = Blueprint("sfx", __name__)
retrieve = Blueprint("retrieve", __name__)


DATA_DIR = os.getenv("DATA_DIR")
MP3_PARENT_DIR = os.getenv("MP3_PARENT_DIR")
WAV_PARENT_DIR = os.getenv("WAV_PARENT_DIR")
INDEX_FILENAME = os.getenv("INDEX_FILENAME")
EMBEDDINGS_FILENAME = os.getenv("EMBEDDINGS_FILENAME")

AudioVectors = torch.load(os.path.join(DATA_DIR, EMBEDDINGS_FILENAME))
NUM_FILES = len(AudioVectors)

with open(os.path.join(DATA_DIR, INDEX_FILENAME), "rb") as pickle_file:
    FileIndex = pickle.load(pickle_file)
    Keys = np.array(list(FileIndex.keys()))

AudioFeatureExtractor = laion_clap.CLAP_Module(enable_fusion=False)
AudioFeatureExtractor.load_ckpt()


@main.route("/")
def hello_world():
    return {"message": "Hello, World!"}

@main.route("/health")
def health_check():
    print(request.access_control_request_headers)
    return {"status": "ok", "statusCode": 200}

@audio.route("/file/<AudioID>")
def get_audio_clip(AudioID):
    print(f"Recieved {AudioID}")

    if AudioID not in FileIndex.keys():
        return jsonify({
            "error": "File not found",
            "message": f"There is not file with the ID of {AudioID}"
        }), 404

    fileFormat = request.args.get("format", default="wav", type=str).lower()
    if fileFormat not in ["wav", "mp3"]:
        return jsonify({
            "error": "Unsupported file type",
            "message": f"{fileFormat} file types are not supported or do not exist"
        }), 400


    try:
        filePath = FileIndex[AudioID]["path"]
        return send_file(os.path.join(DATA_DIR, WAV_PARENT_DIR if fileFormat == "wav" else MP3_PARENT_DIR, f"{filePath}.{fileFormat}"))
    except Exception as e:
        return jsonify({
            "error": "Server error",
            "message": f"An unexpected error occurred: {str(e)}"
        }), 500

@audio.route("/")
def get_audio_data():
    numFiles = request.args.get("batchSize", default=50, type=int)
    batchNumber = request.args.get("batchNumber", default=0, type=int)

    if numFiles > 100:
        return jsonify({
            "error": "Too many files",
            "message": "You can request a maximum of 100 files at a time. Please reduce the number of files requested."
        }), 400
    
    totalBatches = NUM_FILES // numFiles - 1
    if batchNumber > totalBatches:
        return jsonify({
            "error": "Invalid Batch Number",
            "message": "The batch number exceeds the total number of available batches for the requested number of files. Please try a smaller batch number."
        }), 400


    data = []
    for i in range(numFiles * batchNumber, min(numFiles * (batchNumber + 1), NUM_FILES)):
        fileData = FileIndex[Keys[i]]
        data.append({
            "id": Keys[i],
            "name": fileData["name"],
            "length": fileData["formattedLength"]
        })

    return jsonify(data)
        
@retrieve.route("/")
def retrieve_similar_clips():
    if request.method == "POST":
        if len(request.data) == 0:
                return jsonify({
                    "error": "No audio file",
                    "message": "No audio file was provided. Please include byte data in post request."
                }), 400
        # generatedAudioEmbedding = AudioFeatureExtractor.get_audio_embedding_from_filelist([os.path.join("/home/jose/", "audio-atlas-api", "foley_bottles_beer_6_pack_in_cardboard_case_movement_clink_001_75069.wav")], use_tensor=True)
        generatedAudioEmbedding = AudioFeatureExtractor.get_audio_embedding_from_data(x = request.data, use_tensor=True)
        
        generatedAudioEmbedding = torch.nn.functional.normalize(generatedAudioEmbedding, p=2, dim=-1)

        cosineSimilarities = torch.mm(generatedAudioEmbedding, AudioVectors.T)
        _, topKIdxs = torch.topk(cosineSimilarities, 10)
        topKIdxs = topKIdxs.flatten()
        topKKeys = Keys[topKIdxs]
        topKClips =  [FileIndex[key] for key in topKKeys]
        similarClipsData = formatAudioResponseData(topKClips, topKKeys)
        

        return jsonify(similarClipsData)

    return jsonify({"Message": "Be post"})

# def formatAudioResponseData(idxs):
#     data = []
#     for clipID in Keys[idxs]:
#         fileData = FileIndex[clipID]
#         data.append({
#             "id": clipID,
#             "name": fileData["name"],
#             "length": fileData["formattedLength"]
#         })
        
        
#     return data
        


