import io

import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder

import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from streamlit import session_state as ss
from streamlit.runtime.uploaded_file_manager import UploadedFile

from langchain_community.document_loaders import PyPDFLoader


# interact with FastAPI endpoint
backend = "http://fastapi:8000/segmentation"

def process(pdf, server_url: str):

    # m = MultipartEncoder(fields={"file": ("filename", image, "image/jpeg")})
    # images: list[Image.Image] = convert_from_path('/home/belval/example.pdf')
    # r = requests.post(
    #     server_url, data=images, headers={"Content-Type": images.content_type}, timeout=8000
    # )


    return r

st.title("Parse Income Statement")
st.write("""Parse the income statement of DAX/MEX/PAX to get indicative limit""")

image_file: UploadedFile | None = st.file_uploader("Upload Image file", type=('jpg', 'png'), key='image')

if st.button("Parse income statement"):

    col1, col2 = st.columns(2)

    if ss.pdf_ref:
        statement_info: dict = process(input_income_statement, backend)
        col1.header("Original")
        # Now you can access "pdf_ref" anywhere in your app.
        binary_data = ss.pdf_ref.getvalue()
        pdf_viewer(input=binary_data, width=700)
        
        col2.header("Parsed")
        col2.json(statement_info)

    else:
        # handle case with no image
        st.write("Upload a file!")