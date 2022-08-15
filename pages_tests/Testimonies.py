import streamlit as st
import json
import pandas as pd
import glob
import pathlib
import datetime

'''
This page is now out-dated. We are replacing this with BM25 and txtai
'''

st.sidebar.image(r"./images/bitter_aloe_logo.jpg")

@st.cache(allow_output_mutation=True)
def cache_speakers():
    with open ("./data/all_speakers.json", "r") as f:
        speakers = json.load(f)
    return speakers

def write_data(data, keywords=False):
    for i, segment in enumerate(data["testimony"]):
        if segment[0] in corrected_people:
            st.markdown(f"(Index {i}) **{segment[0]}**: {segment[1]}")
    st.write("-----")

st.title("")
style = st.sidebar.selectbox("Select Testimony Analysis Method", [
                                                            "By Testimony",
                                                            "By Person",
                                                            "By Keyword"
                                                                ])
if style == 'By Keyword':
    st.title("Testimony Analysis by Keyword(s)")
    files = glob.glob(f"./data/data_saha/*/*/*.json")
    keywords = st.sidebar.text_input('Enter Search').split(",")
    keywords = [k.strip().lower() for k in keywords]

    if st.sidebar.button("Search"):

        st.write(keywords)
        if len(keywords) > 0:
            found_files = []
            for filename in files:
                with open (filename, 'r') as f:
                    data = json.load(f)
                for i, segment in enumerate(data["testimony"]):
                    for k in keywords:
                        if k.lower() in segment[1].lower():
                            if filename not in found_files:
                                st.header(f"File: {filename}")
                                found_files.append(filename)
                            st.markdown(f"(Index {i}) **{segment[0]}**: {segment[1].replace(k, f'<mark>{k}</mark>')}", unsafe_allow_html=True)
                            st.write("-----")


if style == "By Testimony":
    st.title("Testimony Analysis by Testimony")
    testimony_type = st.selectbox("Select Testimony Type", [
                                            # "Amnesty Decisions",
                                            "Amnesty Hearings",
                                            "Human Rights Violation Hearings",
                                            "Special Hearings"
                                            ])

    testimony_type_file = testimony_type.lower().replace(" ", "_")
    files = glob.glob(f"./data/data_saha/{testimony_type_file}/*/*.json")
    places = list(set([x.replace("\\", "/").split("/")[-2].replace("_", " ").title() for x in files]))
    places.sort()
    if testimony_type == "Special Hearings":
        location = st.selectbox("Select Testimony Category", places)
    else:
        location = st.selectbox("Select Location", places)
    file_location = location.lower().replace(" ", "_")
    loc_files = glob.glob(f"./data/data_saha/{testimony_type_file}/{file_location}/*.json")
    potential_files = [x.replace("\\", "/").split("/")[-1] for x in loc_files]
    testimony_file = st.selectbox("Select Testimony", potential_files)
    with open(f"./data/data_saha/{testimony_type_file}/{file_location}/{testimony_file}", "r") as f:
        data = json.load(f)
    speakers = ["All"]+data['header']['speakers']
    speakers = [x.replace("\n", "") for x in speakers]
    narrow_speakers = st.multiselect("Select Speaker(s)", speakers, ["All"])
    st.write("-----")
    st.header("Header Metadata")
    for item in data['header']:
        st.write(f"{item.title()}: {data['header'][item]}")
    st.write("-----")
    st.header("Testimony")
    st.write("-----")
    for i, segment in enumerate(data["testimony"]):
        if "All" in narrow_speakers or segment[0] in narrow_speakers:
            st.markdown(f"(Index {i}) **{segment[0]}**: {segment[1]}")

elif style == "By Person":
    st.markdown("**This is in Development**")
    st.title("Testimony Analysis by Person")
    all_speakers = cache_speakers()
    speaker_names = list(all_speakers.keys())
    speaker_names.sort()
    people = st.multiselect("Select People", speaker_names)
    corrected_people = [p.replace("\n", "") for p in people]
    date_check = st.checkbox("Check to use Dates")
    if date_check:
        date_style = st.selectbox("Select Style of Date Analysis", ["On Date", "Before Date", "After Date"])
        test_date = st.date_input("Select Date", datetime.date(1998,4,28))

    for person in people:
        st.header(f"Displaying the Data for {person}")
        for filename in all_speakers[person]:
            filename = filename.replace("\\", "/").replace("..", ".")
            st.markdown(f"**Displaying Dialogue Found in**: {filename}")
            with open (filename, "r") as f:
                data = json.load(f)
                testimony = data["testimony"]
            st.markdown(f"**Date**: {data['header']['starting date']}")
            for i, segment in enumerate(testimony):
                if segment[0] in corrected_people:
                    if date_check:
                        if data["header"]["starting date"] != "UNKNOWN":
                            year, month, day = data["header"]["starting date"].split("-")
                            tmp_date = datetime.date(int(year), int(month), int(day))
                            if date_style == "On Date" and tmp_date == test_date:
                                st.markdown(f"(Index {i}) **{segment[0]}**: {segment[1]}")
                                st.write("-----")
                            elif date_style == "Before Date" and tmp_date < test_date:
                                st.markdown(f"(Index {i}) **{segment[0]}**: {segment[1]}")
                                st.write("-----")
                            elif date_style == "After Date" and tmp_date > test_date:
                                st.markdown(f"(Index {i}) **{segment[0]}**: {segment[1]}")
                                st.write("-----")
                    else:
                        st.markdown(f"(Index {i}) **{segment[0]}**: {segment[1]}")
                        st.write("-----")
























            #
