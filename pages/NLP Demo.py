import streamlit as st
import spacy
import pandas as pd
from spacy import displacy
import srsly
from spacy.language import Language
from spacy.tokens import Span
from spacy_streamlit import visualize_ner
from spacy.util import filter_spans

@Language.component("keep_dates")
def keep_dates(doc):
    ents = []
    for ent in doc.ents:
        if ent.label_ == "DATE":
            ents.append(ent)
    doc.ents = ents
    return doc

@Language.component("find_adverb")
def find_adverb(doc):
    ents = []
    for ent in doc.ents:
        if ent.label_ == "HRV":
            if doc[ent.start-1].pos_ == "ADV" and doc[ent.start-1].text != "then":
                new_ent = Span(doc, ent.start-1, ent.end, label=ent.label_)
                ents.append(new_ent)
            elif doc[ent.start+1].pos_ == "ADV":
                new_ent = Span(doc, ent.start, ent.end+1, label=ent.label_)
                ents.append(new_ent)
            else:
                ents.append(ent)
        else:
            ents.append(ent)
    doc.ents = ents
    return doc

@Language.component("police_stations")
def police_stations(doc):
    ents = list(doc.ents)

    for chunk in doc.noun_chunks:
        if "police station" in chunk.text.lower():
            new_ent = Span(doc, chunk.start, chunk.end, label="POLICE_STATION")
            ents.append(new_ent)
    doc.ents = ents
    return doc

@Language.component("event_finder")
def event_finder(doc):
    event_words = ["boycott", "protest", "gathering", "uprising", "incident"]
    ents = list(doc.ents)
    for chunk in doc.noun_chunks:
        tokens = [token.lemma_.lower() for token in chunk]
        if any(n in tokens for n in event_words):
            new_ent = Span(doc, chunk.start, chunk.end, label="EVENT")
            ents.append(new_ent)
    filtered = filter_spans(ents)
    doc.ents = filtered
    return doc

def create_patterns(data, label, lemma=False):
    if lemma == False:
        return [{"label": label, "pattern": pattern} for pattern in data]
    else:
        return [{"label": label, "pattern": [{"LEMMA": pattern}]} for pattern in data]

@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_feather("data/full_data_00-00-05")
    return df

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def create_pipeline():
    nlp = spacy.load("models/vol7_heuristic")
    nlp.add_pipe("event_finder", before="entity_ruler")
    return nlp


colors = {
"POLICE_STATION": "#fbab0a",
"WEAPON": "#fb0ac4",
"HRV": "#fbf40a",
"PROVINCE": "#a77a61",
# "AFFILIATED_ACTOR": "",
# "UNAFFILIATED_ACTOR": "",
# "PERPE": "",

}

df = load_data()
nlp = create_pipeline()

labels = list(nlp.get_pipe("entity_ruler").labels)+["POLICE_STATION", "DATE", "VIOLENT_ACT"]
num = st.number_input("Select Row", 1, 20000, 1)
doc = nlp(df.description.tolist()[num])
visualize_ner(doc, labels=labels, colors=colors)






























#
