# Streamlit-Pinecone Connection

[![Pinecone](https://img.shields.io/static/v1?label=Built%20with&message=Pinecone&color=green&style=flat-square)](https://www.pinecone.io/) [![Pinecone](https://img.shields.io/static/v1?label=%20made%20with%20%E2%9D%A4%20for&message=Streamlit&color=red&style=flat-square)](https://streamlit.io/)

This project is a submission for the [Streamlit Connections Hackathon 2023](https://discuss.streamlit.io/t/connections-hackathon/47574).
It delivers a Streamlit connector for the [Pinecone](https://www.pinecone.io/) vector database.

## Overview

The Streamlit-Pinecone Connector enables developers to connect to a Pinecone database with the following Python code:

 ```python 
    conn = st.experimental_connection(
        "Pinecone",
        type=PineconeConnection,
        environment="Pinecone_cloud_environment",
        api_key="Pinecone_API_KEY",
    )
 ```

We built a Streamlit demo with this connector, called "YouTube Q/A", designed to search through [Youtube Video Transcriptions](https://huggingface.co/datasets/pinecone/yt-transcriptions.) and perform Semantic Search. The live demo is accessible through [Streamlit Community Cloud](https://st-pinecone-connection.streamlit.app/).

The app matches the natural language question to the video transcripts and finds you similar videos. It will give you links to YouTube Videos that match your search question.

The app will query a vector database (Pinecone) and perform Semantic Search. 

The dataset was taken from HuggingFace: [Youtube Video Transcriptions](https://huggingface.co/datasets/pinecone/yt-transcriptions).
