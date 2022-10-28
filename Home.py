import streamlit as st
from pathlib import Path
import os
import gdown
# st.sidebar.image(r"./images/bitter_aloe_logo.jpg")
st.set_page_config(layout="wide", page_title="Bitter Aloe Project")
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def download_files():
    # a file
    url = "https://drive.google.com/file/d/1oYiPGElzOnljjo3jWa-fHD-Bk5iguO-3/view?usp=sharing"

    if os.path.exists("./data/testimony-top2vec-model"):
        pass
    else:
        output = "./data/testimony-top2vec-model"
        gdown.download(url, output, quiet=False, fuzzy=True)
        print("Download Complete")

    csv_url = "https://drive.google.com/file/d/1XHU8rY-ZH1PiM3axQX26M6gWkWzNqmDf/view?usp=sharing"

    if os.path.exists("./data/speaker_dialogue.csv"):
        pass
    else:
        output = "./data/testimonies_complete.csv"
        gdown.download(csv_url, output, quiet=False, fuzzy=True)
        print("Download Complete")

    ann_url = "https://drive.google.com/file/d/1Mngfqd-TPTI2AH8Mv9hlm2j7vprus6R3/view?usp=sharing"

    if os.path.exists("./data/speaker_dialogue.csv"):
        pass
    else:
        output = "./data/testimonies_complete.ann"
        gdown.download(ann_url, output, quiet=False, fuzzy=True)
        print("Download Complete")


download_files()
def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

home_page = read_markdown_file("markdown_files/home.md")
st.markdown(home_page, unsafe_allow_html=True)
