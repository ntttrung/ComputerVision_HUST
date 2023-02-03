import os
from module import counting
from module import denoise
import base64
import json
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import warnings
warnings.filterwarnings("ignore")


api = FastAPI(title="Final project CV", version='0.2.0')
origins = ["*"]
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600,
)

class Input(BaseModel):
    base64_img: Optional[str] = None
    text: Optional[str] = None
    list_base64: Optional[list] = None
    path: Optional[str] = None


@api.post('/Counting-object')
def Count_object(api_input: Input):
    path_in = "/media/Z/TrungNT108/ComputerVision_HUST/upload_image/" + api_input.path
    
    # Denoise
    denoise_operation = denoise.Denoise(path_in)
    path_denoise = denoise_operation.denoise()
    
    # Counting operation
    counting_operation = counting.Counting(path_denoise, 1)
    result = counting_operation.counting_object()

    
    return result


@api.post('/Image-retrieval')
def Count_object(api_input: Input):
    