# Poetry + Flask Project

### Install Poetry

Read the [Poetry Installation Guide](https://python-poetry.org/docs/#installation)

### Install Dependencies

```bash
poetry install
```

### Run with Flask (Dev)
```bash
poetry run flask --app audio_atlas_api run --debug
```

### Run with Gunicorn (Prod on Linux)
```bash
poetry run gunicorn --bind 0.0.0.0:5000 audio_atlas_api
```

### More info

- [Flask](https://flask.palletsprojects.com/en/stable/)
- [Gunicorn](https://gunicorn.org/)
- [Poetry](https://python-poetry.org/)


### Endpoints

`/api/v1/audio/?pageSize=50&pageNumber=0`  
Retrieves information on audio files in a batched manner. The available information includes:
- **ID**: The unique identifier for the audio file.
- **Name**: The name of the audio file.
- **Length**: The duration of the audio file.

#### **Parameters:**
| Parameter   | Type     | Description                                                                                      | Default | Constraints                              |
|-------------|----------|--------------------------------------------------------------------------------------------------|---------|------------------------------------------|
| `pageSize` | Integer  | Specifies how many audio clips to retrieve in a single batch.                                    | 50      | Must be between **1 and 100**.           |
| `pageNumber` | Integer | Specifies which batch to retrieve for the given `pageSize`.                                    | 0       | Must be between **0 and (TotalFiles / pageSize - 1)**. |

#### **Example Output:**
```json
[
  {"id": "ID1", "length": "00:01.50", "name": "Audio Clip 1"},
  {"id": "ID2", "length": "00:02.50", "name": "Audio Clip 2"}
]
```

---

`/api/v1/audio/file/<AudioID>?format=wav`  
Retrieves the audio clip from the server with the specified `AudioID`. You can specify the format of the audio file (either WAV or MP3).

#### **Parameters:**
| Parameter | Type   | Description                                     | Default | Constraints                  |
|-----------|--------|-------------------------------------------------|---------|------------------------------|
| `format`  | String | Specifies the format to return the audio in.    | `wav`   | Must be **`wav`** or **`mp3`**. |

#### **Example URL:**
```
/api/v1/audio/file/12345?format=mp3
```

---

`/api/v1/retrieve/?pageSize=50&pageNumber=0&query=<TextQuery>`  
Retrieves the top `k` most similar audio clips from the server based on cosine similarity to the given text query.

#### **Parameters:**
| Parameter | Type    | Description                                                                 | Default | Constraints                       |
|-----------|---------|-----------------------------------------------------------------------------|---------|-----------------------------------|
| `pageSize` | Integer  | Specifies how many similar audio clips to retrieve in a single batch.                                    | 50      | Must be between **1 and 100**.           |
| `pageNumber` | Integer | Specifies which batch to retrieve for the given `pageSize`.                                    | 0       | Must be between **0 and (TotalFiles / pageSize - 1)**. |
| `query`   | String  | The text query used to find similar audio clips. **Must be URL-encoded.**   | None    | Required.                         |

#### **Example URL:**
```
/api/v1/retrieve/?pageSize=50&pageNumber=0&query=bottle+clink
```

#### **Example Output:**
```json
[
{"id": "ID1", "length": "00:00.68", "name": "Audio Clip 1", "similarity": 0.6627258658409119},
{"id": "ID2", "length": "00:01.05", "name": "Audio Clip 1", "similarity": 0.659700870513916}
]
```

---
