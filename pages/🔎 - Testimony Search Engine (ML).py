import streamlit as st
from annoy import AnnoyIndex
from sentence_transformers import SentenceTransformer
import pandas as pd

st.set_page_config(layout="wide", page_title="ML Testimony Search Engine | Bitter Aloe Project")
@st.cache(allow_output_mutation=True)
def load_model():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

@st.cache(allow_output_mutation=True)
def cache_speakers():
    df = pd.read_csv("./data/testimonies_complete.csv")
    return df

@st.cache(allow_output_mutation=True)
def load_annoy():
    annoy_index = AnnoyIndex(384, 'angular')
    annoy_index.load('./data/testimonies_complete.ann')
    return annoy_index

model = load_model()
df = cache_speakers()
annoy_index = load_annoy()

query = st.sidebar.text_input("Insert Search Here")
num_results = st.sidebar.number_input("Number of Results", 1, 1000, 100)
if st.sidebar.button("Search"):
    st.header("Results:")
    query_emb = model.encode([query], show_progress_bar=True)[0]
    indices, dists = annoy_index.get_nns_by_vector(query_emb, num_results,
                                        include_distances=True)
    res = df.iloc[indices]
    # res = res[["speaker", "dialogue"]]
    res["distance"] = dists
    # res = res[["score", "speaker", "dialogue", "saha_page"]]
    links = [f"<a href='{row.saha_page}#line{row.saha_loc-1}'>link</a>" for idx, row in res.iterrows()]
    res["link"] = links
    res = res[["distance", "speaker", "dialogue", "link"]]
    res["dialogue"] = [dialogue.replace("\n", "<br><br>") for dialogue in res["dialogue"].tolist()]
    st.write(res.to_markdown(), unsafe_allow_html=True)
