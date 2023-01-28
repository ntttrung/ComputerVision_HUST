import json
import base64
import os
import requests
from PIL import Image
import cv2
import streamlit as st
from pydantic import BaseModel

menu = ["1. Object Counting", "2. Image Retrieval"]
active_tab = st.sidebar.selectbox("Menu", menu)



if active_tab == "1. Object Counting":
    st.title('Object counting')
    uploaded_file = st.file_uploader('Upload photo for counting', type=['jpg', 'jpeg', 'png', 'webp'])
    col1, col2 = st.columns([3, 2])

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        is_click = st.button('Counting')
        with col1:
            if is_click:
                base64_img = base64.b64encode(bytes_data)
                base64_img = base64_img.decode('utf-8')
                try:
                    url = 'http://0.0.0.0:8008/Counting-object'
                    data = {'base64_img': base64_img}
                    response = requests.post(url=url, data=json.dumps(data))
                    content = json.loads(response.content)
                    
                    
                    img_object = base64.b64decode(base64_img)
                    image = cv2.imdecode(np.fromstring(img_object, np.uint8), cv2.IMREAD_COLOR)
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    st.image(image)
                except:
                    st.write('Fetch api failed')
        with col2:
            if is_click:
                st.write('Results:')
                st.write('The image has 100 objects')





if active_tab == "2. Image Retrieval":
    st.title('Image retrieval using global feature')