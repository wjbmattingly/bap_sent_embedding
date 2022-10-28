import streamlit as st
import json
import glob
from rank_bm25 import BM25Okapi
import pickle
import pandas as pd

st.set_page_config(layout="wide", page_title="Testimony Search | Bitter Aloe Project")
@st.cache(allow_output_mutation=True)
def load_model(df):
    tokenized_corpus = [str(text).lower().split() for text in df.dialogue.tolist()]
    index = df.index
    bm25 = BM25Okapi(tokenized_corpus)
    return bm25, index


@st.cache(allow_output_mutation=True)
def load_df():
    df = pd.read_csv("data/testimonies_complete.csv")
    return df

df = load_df()
bm25, index = load_model(df)

query = st.sidebar.text_input("Enter Search Here")
num_results = st.sidebar.number_input("Number of Results", 100,1000)
if st.sidebar.button("Search"):
    tokenized_query = query.lower().split(" ")
    res_index = bm25.get_top_n(tokenized_query, index, n=num_results)
    res = df.iloc[res_index]
    links = [f"<a href='{row.saha_page}#line{row.saha_loc-1}'>link</a>".replace("'", "") for idx, row in res.iterrows()]
    res["link"] = links
    res = res[["speaker", "dialogue", "link"]]
    res["dialogue"] = [dialogue.replace("\n", "<br><br>") for dialogue in res["dialogue"].tolist()]
    st.write(res.to_markdown(), unsafe_allow_html=True)
