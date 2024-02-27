from fastapi import FastAPI
from pydantic import BaseModel
import csv
import uvicorn

from predict import predict
from typing import Union
from main_app import app


if __name__ == "__main__":
    uvicorn.run("main_app:app", port=8000, host="0.0.0.0", reload=True)

