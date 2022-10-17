import streamlit as st
import json
import glob
from rank_bm25 import BM25Okapi
import pickle
import pandas as pd


@st.cache(allow_output_mutation=True)
def load_model():
    files = glob.glob(f"./data/data_saha/*/*/*.json")
    documents = []
    segments = {}
    x=0
    for filename in files:
        with open(filename, "r") as f:
            data = json.load(f)
        testimony = data["testimony"]
        # segments["files"].append(filename)
        for i, segment in enumerate(testimony):
            speaker, dialogue, gender = segment
            if " Today is also one of those difficult days" in dialogue:
                print (x)
                print (filename)
                print (dialogue)
            segments[x] = [filename, i]
            # segments["segments"].append({i})
            documents.append(dialogue)
            x=x+1
    tokenized_corpus = [doc.split(" ") for doc in documents]
    bm25 = BM25Okapi(tokenized_corpus)
    return bm25, documents, segments


@st.cache(allow_output_mutation=True)
def load_df():
    saha_index = pd.read_csv("data/saha_index.csv")
    return saha_index

saha_index = load_df()

bm25, documents, segments = load_model()
query = st.sidebar.text_input("Enter Search Here")
num_results = st.sidebar.number_input("Number of Results", 10,1000)
if st.sidebar.button("Search"):
    tokenized_query = query.split(" ")
    segment_text = bm25.get_top_n(tokenized_query, segments, n=num_results)
    segment_data = bm25.get_top_n(tokenized_query, documents, n=num_results)
    segment_text = [s[0] for s in segment_text]

    segment_text = [html_file.replace("\\", "/").split("/")[-1].replace(".json", "") for html_file in segment_text]
    segment_text = [saha_index.loc[saha_index.id == int(index_num)].src.tolist()[0] for index_num in segment_text]
    # saha_page = saha_index.loc[saha_index.id == int(index_num)].src.tolist()[0]
    # st.write(f"<a href='{saha_page}'>Saha Link</a>", unsafe_allow_html=True)
    segment_text = [f"<a href='{saha_page}'>Saha Link</a>" for saha_page in segment_text]
    res = {"Testimony": segment_text, "Text": segment_data}
    df = pd.DataFrame(res)
    res = df.to_markdown()
    st.markdown(res, unsafe_allow_html=True)
