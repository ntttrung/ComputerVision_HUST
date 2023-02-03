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
    col1, col2 = st.columns([3, 3])
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
                    path_upload = '/media/Z/TrungNT108/ComputerVision_HUST/upload_image'
                    save_uploaded_file(path_upload, uploaded_file)
                    
                    # st.balloons()
                    url = 'http://0.0.0.0:8008/Counting-object'
                    data = {'path': uploaded_file.name}
                    response = requests.post(url=url, data=json.dumps(data))
                    content = json.loads(response.content)
                    # img_path = content['path_image']
                    #Original image
                    org_img = Image.open(path_upload + '/' + name)
                    st.image(org_img, caption= 'Original image')
                    
                    #Denoise image
                    denoise_img = Image.open(content['denoise_image'])
                    st.image(denoise_img, caption= 'Denoise image')
                    
                    #Adaptive iamge
                    adapt_img = Image.open(content['path_adaptive'])
                    st.image(adapt_img, caption= 'Applying adaptive thresholding')

                    #Opening iamge
                    open_img = Image.open(content['path_opening'])
                    st.image(open_img, caption= 'Applying opening')
                # except:
                #     st.write('Fetch api failed')
        with col2:
            if is_click:
                st.write('Results:')
                st.write('The image has {} objects'.format(content['total_contours']))

                final_img = Image.open(content['output_image'])
                st.image(final_img, caption= 'Contour and Counting')




if active_tab == "2. Image Retrieval":
    st.title('Image retrieval using global feature')
    #to_do