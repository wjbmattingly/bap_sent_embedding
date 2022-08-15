# Contents of ~/my_app/pages/page_2.py
import streamlit as st
import pandas as pd
import json
from sentence_transformers import util
from pathlib import Path

st.sidebar.image(r"./images/bitter_aloe_logo.jpg")

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

st.markdown("# Sentence Embedding Analysis")
st.sidebar.markdown("# Sentence Embedding App")


@st.cache(allow_output_mutation=True)
def cache_df():
    df = pd.read_json("data/vol7.json")
    names = df.names.tolist()
    descriptions = df.descriptions.tolist()
    return df, names, descriptions

@st.cache(allow_output_mutation=True)
def cache_paras():
    return (load_data("data/paraphrases-10.json"))

def search(num, df, res_container):
    descs = df.descriptions
    names = df.names
    x=1
    res_container.header (f"Searching for Similarity to:")
    res_container.write (f"Victim: {names[num]} ({num})")
    res_container.write(f"Description: {descs[num]}")
    for paraphrase in paraphrases:
        score, i, j = paraphrase
        if i == num:
            sent1 = descs[i]
            sent2 = descs[j]
            res_container.header(f"Result {x}")
            res_container.write (f"Victim: {names[j]} ({j})")
            res_container.write(f"{sent2}")
            res_container.write(f"")
            res_container.write (f" Degree of Similarity: {score}")
            res_container.write(f"")
            res_container.write(f"")
            x=x+1

def load_data(file):
    with open (file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)

def write_data(file, data):
    with open (file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

res_container =st.expander("Results")
df, names, descs = cache_df()
paraphrases = cache_paras()

search_form = st.sidebar.form("Search Form")
search_num = search_form.number_input("Search", step=1)

search_button = search_form.form_submit_button("Search")

st.table(df)
if search_button:
    st.sidebar.write(f"You can see the results for a search on {names[search_num]} under Results.")
    res = search(search_num, df, res_container)
