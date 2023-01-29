import json
import base64
import os
import requests
from PIL import Image
import cv2
import streamlit as st
import datetime

menu = ["1. Object Counting", "2. Image Retrieval"]
active_tab = st.sidebar.selectbox("Menu", menu)

def save_uploaded_file(path, uploadfile):
    with open(os.path.join(path, uploadfile.name), "wb") as f:
        f.write(uploadfile.getbuffer())


if active_tab == "1. Object Counting":
    st.title('Object counting')
    uploaded_file = st.file_uploader('Upload a photo', type=['jpg', 'jpeg', 'png', 'webp'])
    col1, col2 = st.columns([3, 2])
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        
        is_click = st.button('Counting')
        with col1:
            if is_click:
                # try:
                    ts = datetime.datetime.now().timestamp()
                    name = '.'.join(uploaded_file.name.split('.')[:-1])
                    name += "_" + str(ts) + '.png'
                    uploaded_file.name = name
                    save_uploaded_file('/media/Z/TrungNT108/ComputerVision_HUST/upload_image', uploaded_file)
                    
                    # st.balloons()
                    url = 'http://0.0.0.0:8008/Counting-object'
                    data = {'path': uploaded_file.name}
                    response = requests.post(url=url, data=json.dumps(data))
                    content = json.loads(response.content)
                    # img_path = content['path_image']
                # except:
                #     st.write('Fetch api failed')
        with col2:
            if is_click:
                st.write('Results:')
                st.write('The image has 100 objects')





if active_tab == "2. Image Retrieval":
    st.title('Image retrieval using global feature')