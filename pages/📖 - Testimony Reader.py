import streamlit as st
import pandas as pd

@st.cache(allow_output_mutation=True)
def cache_data():
    df = pd.read_csv("./data/testimonies_complete.csv")
    hearing_types = df.hearing_type.unique()
    locs = df.location.unique()
    return df, hearing_types, locs

df, hearing_types, locs = cache_data()
res = df.iloc[0]
hearing_type = st.sidebar.selectbox("Hearing Type", hearing_types)
temp = df.loc[df["hearing_type"] == hearing_type]
location = st.sidebar.selectbox("Location",  temp.location.unique())
temp = temp.loc[temp["location"] == location]
number = st.sidebar.selectbox("Testimony Number", temp.file_num.unique())
res = temp.loc[temp["file_num"] == number]


links = [f"<a href='{row.saha_page}#line{row.saha_loc-1}'>link</a>" for idx, row in res.iterrows()]
res["link"] = links
res = res[["speaker", "dialogue", "link"]]
res["dialogue"] = [dialogue.replace("\n", "<br><br>") for dialogue in res["dialogue"].tolist()]

opening_statements = st.sidebar.checkbox("Opening Statements Only")
if opening_statements:
    length_os = st.sidebar.number_input("Length of Opening", 1, 10)
    res = res[:length_os]

st.write(res.to_markdown(), unsafe_allow_html=True)
