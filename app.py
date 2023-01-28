import os
from module import counting
from module import denoise
import base64
import json
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


@api.post('/Counting-object')
def Count_object(api_input: Input):
    img_object = base64.b64decode(api_input.base64_img)
    image = cv2.imdecode(np.fromstring(img_object, np.uint8), cv2.IMREAD_COLOR)
    