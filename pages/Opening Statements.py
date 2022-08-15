import streamlit as st
from top2vec import Top2Vec
import pandas as pd
import json
import glob

st.sidebar.image(r"./images/bitter_aloe_logo.jpg")

@st.cache(allow_output_mutation=True)
def cache_df():
    df = pd.read_json("data/vol7.json")
    names = df.names.tolist()
    descriptions = df.descriptions.tolist()
    return df, names, descriptions

@st.cache(allow_output_mutation=True)
def cache_testimonies():
    df = pd.read_json("data/testimonies.json")
    names = df.names.tolist()
    descriptions = df.descriptions.tolist()
    return df, names, descriptions

@st.cache(allow_output_mutation=True)
def cache_testimony_data():
    with open ("data/testimony_top2vec_data.json", "r") as f:
        data = json.load(f)
    return data

@st.cache(allow_output_mutation=True)
def load_model(model_type="data/top2vec-model"):
    model = Top2Vec.load(model_type)
    num_topics = model.get_num_topics()
    topic_sizes, topic_nums = model.get_topic_sizes()
    topic_words, word_scores, topic_nums = model.get_topics(num_topics)
    return Top2Vec.load(model_type), num_topics, topic_sizes, topic_nums, topic_words, word_scores, topic_nums
def write_data(data, depth):
    for i, segment in enumerate(data["testimony"]):
        if i < int(depth):
            st.write(f"{segment[0]}: {segment[1]}")
    st.write("-----")

test_type  = st.sidebar.selectbox("Testimonies to Examine", ["Human Rights Violation Hearings", "Amnesty"])
places = glob.glob(f"data/data_saha/{test_type.replace(' ', '_').lower()}/*/*.json")
places = [p.replace("\\", "/").split("/")[-2].replace("_", " ").title() for p in places]
places = list(set(places))
places.sort()
place_select = st.sidebar.selectbox("Select Place", places)
depth = st.sidebar.slider("Select Testimony Depth", 1, 10, 2)
files = glob.glob(f"data/data_saha/{test_type.replace(' ', '_').lower()}/{place_select.replace(' ', '_').lower()}/*.json")
st.header(f"The {str(len(files))} Opening Statements from {place_select}")
for filename in files:
    st.write(filename)
    with open (filename, "r") as f:
        data = json.load(f)
    write_data(data, depth)
