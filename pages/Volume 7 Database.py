import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.sidebar.image(r"./images/bitter_aloe_logo.jpg")

@st.cache(allow_output_mutation=True)
def cache_df():
    df = pd.read_json("data/vol7.json")
    names = df.names.tolist()
    descriptions = df.descriptions.tolist()
    return df, names, descriptions

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

st.header("Volume 7 Database")

database_directions = read_markdown_file("markdown_files/database.md")
directions = st.expander("Directions")
directions.markdown(database_directions, unsafe_allow_html=True)

df, people, descs = cache_df()


form_options = st.form("Query Form")
strict_box = form_options.checkbox("Strict Search On")
description_search = form_options.text_input(f"Descriptions ({len(descs)})")
people_select = form_options.multiselect(f"People ({len(people)})", people)
if form_options.form_submit_button():
    if strict_box == True:
        description_search = description_search.split("|")
        cond1 = df['descriptions'].str.findall('|'.join(description_search)).map(lambda x: len(set(x)) == len(description_search))

        new_df = df.loc[cond1, :]
        st.write(f"The Total Number of Results is {len(new_df)}")
        st.table(new_df)
    else:
        if len(description_search) > 0:
            main_cond = df['descriptions'].apply(lambda x: any([k in x for k in description_search.split("|")]))
            if len(people_select) > 0:
                cond2  = [x for x in df['names'].str.contains("|".join(people_select))]
                i=0
                for c in cond2:
                    if c == True:
                        main_cond[i] = True
                    i=i+1
        else:
            if len(people_select) > 0:
                main_cond = [x for x in df['names'].str.contains("|".join(people_select))]


        new_df = df.loc[main_cond, :]
        st.write(f"The Total Number of Results is {len(new_df)}")
        st.table(new_df)
