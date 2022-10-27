import streamlit as st
from pathlib import Path
import os
import gdown
# st.sidebar.image(r"./images/bitter_aloe_logo.jpg")
st.set_page_config(layout="wide", page_title="Bitter Aloe Project")
st.markdown("# Text Analysis App")

def download_files():
    # a file
    url = "https://drive.google.com/file/d/1oYiPGElzOnljjo3jWa-fHD-Bk5iguO-3/view?usp=sharing"

    if os.path.exists("./data/testimony-top2vec-model"):
        pass
    else:
        output = "./data/testimony-top2vec-model"
        gdown.download(url, output, quiet=False, fuzzy=True)
        print("Download Complete")

    url = "https://drive.google.com/file/d/1ij0v7TvNPrzONFTIUkczbFHToBNo0PSd/view?usp=sharing"

    if os.path.exists("./data/speaker_dialogue.csv"):
        pass
    else:
        output = "./data/speaker_dialogue.csv"
        gdown.download(url, output, quiet=False, fuzzy=True)
        print("Download Complete")

download_files()
def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

home_page = read_markdown_file("markdown_files/home.md")
st.markdown(home_page, unsafe_allow_html=True)
