import streamlit as st
from top2vec import Top2Vec
import pandas as pd
import json

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

def get_data(method:str, num_docs=5, doc_ids=[0], topic_num=0, keywords=["burn"], testimony=False, testimony_data=0):
    if method == "dbd":
        documents, document_scores, document_ids = model.search_documents_by_documents(doc_ids=doc_ids, num_docs=num_docs)
    elif method == "dbt":
        documents, document_scores, document_ids = model.search_documents_by_topic(topic_num=topic_num, num_docs=num_docs)
    elif method == "dbk":
        documents, document_scores, document_ids = model.search_documents_by_keywords(keywords=keywords, num_docs=num_docs)
    files = []
    for doc, score, doc_id in zip(documents, document_scores, document_ids):
            # st.header(f"Victim: {names[doc_id]}")
            # if testimony == False:
            st.write(f"Document: {doc_id}")
            if testimony == True:
                st.write(f"Filename: {testimony_data[str(doc_id)][0]}")
                if testimony_data[str(doc_id)][0] not in files:
                    files.append(testimony_data[str(doc_id)][0])
                st.write(f"File Index: {testimony_data[str(doc_id)][1]}")
            st.write(f"Score: {score}")
            st.write(f"Description: {doc}")
            st.write("-----------")
            st.write()
            st.write()
    files.sort()
    return files

model_type = st.sidebar.selectbox("Select Type of Top2Vec Model", ["Volume 7", "Testimonies"])
if model_type == "Testimonies":
    model_type = "data/testimony-top2vec-model"
    model, num_topics, topic_sizes, topic_nums, topic_words, word_scores, topic_nums = load_model(model_type)
    testimony_data = cache_testimony_data()


    style = st.sidebar.selectbox("Select Top2Vec Search Style",
                            [
                            "Search by Topic",
                            "Search by Document",
                            "Search by Keywords"
                            ])
    # test_data = cache_testimonies()


    if style=="Search by Topic":
        st.markdown("# Sentence Embedding Analysis with Top2Vec(New)")
        st.write(f"There are {num_topics} topics across all Volume 7 Data")

        topic_num = st.number_input("Which Topic Number would you like to search?", 0, max_value=num_topics)
        num_docs = st.number_input("How many documents do you want to see from this topic?", 10, max_value=topic_sizes[topic_num])

        st.header(f"Topic {topic_num} Data")
        data_expander = st.expander("data")
        files_expander = st.expander("files_data")
        res = {"Topic Words": topic_words[topic_num], "Similarity to Topic": word_scores[topic_num]}
        res_df = pd.DataFrame(res)

        data_expander.table(res_df)

        st.write(f"There are a total of {topic_sizes[topic_num]} available. Currently only displaying the top-{num_docs} results.")
        files = get_data("dbt", topic_num=topic_num, num_docs=num_docs, testimony=True, testimony_data=testimony_data)
        files_expander.write(files)



    elif style == "Search by Document":
        st.markdown("# Search by Document")
        document_ids = st.text_input("Which Documents would you like to search? (Use the Victim Index Numbers)", 0)
        num_docs = st.number_input("How many documents do you want to see from this topic?", 5)
        doc_ids = [int(d.strip()) for d in document_ids.split(",")]
        st.header(f"Documents used in Query")
        data_expander = st.expander("Document Data")
        data_expander = st.expander("Document Data")
        for id in doc_ids:
            data_expander.write(f"{id}")
        files_expander = st.expander("files_data")
        # for id in doc_ids:
        #     data_expander.write(f"{names[id]}: {descriptions[id]}")
        files = get_data("dbd",  doc_ids=doc_ids, num_docs=num_docs, testimony=True, testimony_data=testimony_data)
        files_expander.write(files)
        # get_data("dbd", doc_ids=doc_ids, num_docs=num_docs)

    elif style== "Search by Keywords":
        keywords = st.text_input("Which Documents would you like to search? (Use the Victim Index Numbers)", "burn")
        num_docs = st.number_input("How many documents do you want to see from this topic?", 5)
        document_keywords = [k.strip() for k in keywords.split(",")]
        files_expander = st.expander("files_data")
        # get_data("dbk", keywords=document_keywords, num_docs=num_docs)
        files = get_data("dbk",  keywords=document_keywords, num_docs=num_docs, testimony=True, testimony_data=testimony_data)
        files_expander.write(files)


#### Original Vol 7 portion
elif model_type == "Volume 7":
    df, names, descriptions = cache_df()
    model_type = "data/top2vec-model"
    model, num_topics, topic_sizes, topic_nums, topic_words, word_scores, topic_nums = load_model(model_type)


    style = st.sidebar.selectbox("Select Top2Vec Search Style",
                            [
                            "Search by Topic",
                            "Search by Document",
                            "Search by Keywords"
                            ])

    if style=="Search by Topic":
        st.markdown("# Sentence Embedding Analysis with Top2Vec(New)")
        st.write(f"There are {num_topics} topics across all Volume 7 Data")

        topic_num = st.number_input("Which Topic Number would you like to search?", 0, max_value=num_topics)
        num_docs = st.number_input("How many documents do you want to see from this topic?", 10, max_value=topic_sizes[topic_num])

        st.header(f"Topic {topic_num} Data")
        data_expander = st.expander("data")
        res = {"Topic Words": topic_words[topic_num], "Similarity to Topic": word_scores[topic_num]}
        res_df = pd.DataFrame(res)

        data_expander.table(res_df)

        st.write(f"There are a total of {topic_sizes[topic_num]} available. Currently only displaying the top-{num_docs} results.")
        get_data("dbt", topic_num=topic_num, num_docs=num_docs)



    elif style == "Search by Document":
        st.markdown("# Search by Document")
        document_ids = st.text_input("Which Documents would you like to search? (Use the Victim Index Numbers)", 0)
        num_docs = st.number_input("How many documents do you want to see from this topic?", 5)
        doc_ids = [int(d.strip()) for d in document_ids.split(",")]
        st.header(f"Documents used in Query")
        data_expander = st.expander("Document Data")
        for id in doc_ids:
            data_expander.write(f"{names[id]}: {descriptions[id]}")
        get_data("dbd", doc_ids=doc_ids, num_docs=num_docs)

    elif style== "Search by Keywords":
        keywords = st.text_input("Which Documents would you like to search? (Use the Victim Index Numbers)", "burn")
        num_docs = st.number_input("How many documents do you want to see from this topic?", 5)
        document_keywords = [k.strip() for k in keywords.split(",")]
        get_data("dbk", keywords=document_keywords, num_docs=num_docs)








    #
