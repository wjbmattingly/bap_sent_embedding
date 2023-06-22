# The Bitter Aloe Project's Collection of Streamlit Applications

Welcome to the Bitter Aloe Project's repository of Streamlit applications! This collection is designed to aid researchers in querying, understanding, and interpreting the testimonies and other data gathered by South Africa's Truth and Reconciliation Commission (TRC).

## About the Truth and Reconciliation Commission (TRC)

The TRC was a court-like body established in South Africa after the end of apartheid. Its primary objective was to bear witness to, record, and in some cases, grant amnesty to the perpetrators of crimes relating to human rights violations, as well as offering reparation and rehabilitation to the victims. A vital component of this transition period, the TRC heard testimonies of gross human rights violations, hate crimes, and other severe acts of violence from both the apartheid state and the liberation forces.

## About the Bitter Aloe Project (BAP)

The Bitter Aloe Project aims to provide a deep, data-driven examination of the TRC testimonies and other related data. Our tools allow researchers to semantically query these testimonies, drawing new insights from a pivotal period in South Africa's history.

## The Streamlit Applications

Our Streamlit applications provide an intuitive interface for researchers to interact with the data from the TRC. 

**Live Streamlit Applications:**

Our applications are also live! You can access them directly [here](https://streamlit.as.uky.edu/bap_sent_embedding/).

Here's a brief overview of each application:

1. **🌍 SAHA-Infocomm Map (Alpha Testing)**: This application lets you visually explore the SAHA-Infocomm database (Volume 7 of the TRC final report) as a map. Users can populate multiple layers, distinguished by unique colors, based on four fields: Organization(s), Place(s), Homeland(s), and Human Rights Violation(s) (HRV). Upcoming features include the ability to download data and map as a zip file and to change results by date.

2. **💻 SAHA-Infocomm (Complete)**: The Volume 7 Database allows you to interrogate the data from Volume 7 of the TRC's final report. Here, you can narrow your searches based on parameters such as victim's name and a search across all descriptions.

3. **🔎 Testimony Search Engine (BM25) (Complete)**: This is a traditional search engine for the TRC testimonies. It uses the BM25 algorithm for matching relevant material from a query. It is not case sensitive.

4. **🔎 Testimony Search Engine (ML)**: This is a machine learning-assisted search engine of ~700,000 segments of testimony from the TRC. It allows users to search the testimonies semantically. More specificity here will yield better results.

5. **📖 Top2Vec Analysis**: At the core of this tool is a model trained through the Top2Vec library. This tool allows you to dynamically search across documents by vector similarity. It is a bit more robust than the Sentence Embedding Analysis tool due to the Top2Vec library's built-in functions for analyzing document similarity in numerous ways.

6. **📄 Opening Statements (Complete)**: This page allows you to examine the opening statements of all testimonies. Often, these are important because the commissioner uses the moment to welcome the speakers and frame the conversation.
