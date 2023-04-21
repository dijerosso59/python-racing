from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Request(BaseModel):
    driver: int
    circuit: int
    constructors: int
    starting_position: int

@app.post("/predict")
def predict(request: Request):
    return 2.3

# uvicorn main:app --reload --port 7999 
# python3 -m uvicorn main:app --reload --port 7999 