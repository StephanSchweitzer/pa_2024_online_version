import sys
from pathlib import Path

Add the parent directory of 'ml' to the Python path
sys.path.append(str(Path(file).resolve().parent.parent.parent))

from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
import fasttext
import numpy as np
from ml.fastapimodel.dependencies import predict_class

class PredictionRequest(BaseModel):
    text: str

class PredictionClass(BaseModel):
    id: int
    text: str
    is_hateful: int
    user: str

class PredictionRequestBatch(BaseModel):
    messages: List[PredictionClass]

app = FastAPI()

Load FastText model
file_path = Path(__file).resolve().parent.parent / "ml_core" / "data" / "embedding_data" / "cc.fr.300.bin"
if not file_path.exists():
    raise ValueError(f"{file_path} cannot be opened for loading!")

print(file_path.absolute())

ft = fasttext.load_model(file_path.as_posix())

def text_to_vector(text):
    words = text.split(' ')
    word_vectors = [ft.get_word_vector(word) for word in words if word in ft.words]
    if not word_vectors:
        return np.zeros(300)
    return np.mean(word_vectors, axis=0)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("//classify/")
async def classify(request: PredictionRequest):
    print(request.text)

    ### call the embedder
    text_to_vectors = np.expand_dims(text_to_vector(request.text), axis=0)

    ### call for prediction
    classification = predict_class(text_to_vectors)

    print(f"CLASSIFICATION \n {classification[0][0]}")

    if classification is None:
        raise HTTPException(status_code=404, detail="Classification failed")
    return {"class": str(classification[0][0])}


@app.post("//classify_best/")
async def classify(request: PredictionRequest):
    #print(request.text)

    ### call the embedder
    text_to_vectors = np.expand_dims(text_to_vector("test"), axis=0)

    ### call for prediction
    classification = predict_class(text_to_vectors)

    print(f"CLASSIFICATION \n {classification[0][0]}")

    if classification is None:
        raise HTTPException(status_code=404, detail="Classification failed")
    return {"class": str(classification[0][0])}

@app.post("//classify_batch/")
async def classifyBatch(request: List[PredictionClass]):
    print("auieauie")

    array_message = request

    ### call the embedder
    array_text_to_vectors = [
        {
            'id': array.id,
            'text': array.text,
            'is_hateful': 1 if predict_class(np.expand_dims(text_to_vector(array.text), axis=0))[0][0] > 0.5 else 0,
            'user': array.user
        } for array in array_message
    ]
    print(array_text_to_vectors)
    return array_text_to_vectors