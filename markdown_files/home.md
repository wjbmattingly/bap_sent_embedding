# TRC Text Analysis App

**This app is still in development**

This is the Bitter Aloe Project's application. It is designend in Streamlit and is a work in progress. On this application, you will be able to use some of the tools we are developing for analysis of documents related to South Africa's Truth and Reconciliation Commission (TRC). You can navigate to different tools through the portal on the left.

### :earth_africa: SAHA-Infocomm Map
**This application is in alpha testing**
This application lets you explore the SAHA-Infocomm database (Volume 7 of the TRC final report) visually as a map. Users can populate multiple layers whose colors are distinct in the graph. It is built upon [pydeck](https://deckgl.readthedocs.io/en/latest/). Users can create layers with four fields:
- Organization(s)
- Place(s)
- Homeland(s)
- Human Rights Violation(s) (HRV)

Fothcoming features include:
- Download data and map as a zip file
- Ability to change results by date

### :computer: SAHA-Infocomm
**This application is complete and working**
The Volume 7 Database allows you to interrogate the data from Volume 7 of the TRC's final report. Here, you will be able to narrow your searches based on parameters, such as victim's name and a search across all descriptions.

### :mag_right: Testimony Search Engine (BM25)
**This application is complete and working**
This is a traditional search engine for the TRC testimonies. It is based around BM25, an algorithm for identifying and matching relevant material from a query. It is not case sensitive.

### :mag_right: Testimony Search Engine (ML)
This is a machine learn-assisted search engine of ~700,000 segments of testimony from the TRC. A segment is defined as any time a person speaks in the testimonies. We created this by first converting all testimonies into vectors with the `all-MiniLM-L6-v2` model from the Sentence Transformer Python library. These embeddings capture the semantic meaning of document. This means that users can search the testimonies semantically. We then mapped these embeddings onto an Annoy index using the Annoy Python library. Annoy uses trees to map distance between the embeddings. The result is a quick and effective machine learning-assisted search engine. Greater specificty here will yield better results.

### :book: Top2Vec Analysis
At the core of this tool is a model trained through the Top2Vec library. The model was finetuned on the Volume 7 Data. Like the Sentence Embedding Analysis tool, this allows you to dynamically search across documents by vector similarity. It is a bit more robust than the Sentence Embedding Analaysis tool because of the Top2Vec library's built-in functions for analyzing document similarity in a myraid of ways.


### :page_facing_up: Opening Statements
**This application is complete and working**
This page allows you to examine the opening statements of all testimonies. Often, these are important because the commissioner uses the moment to welcome the speakers and frames the conversation.
