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

We built a Streamlit demo with this connector, called "YouTube Q&A", designed to search through [Youtube Video Transcriptions](https://huggingface.co/datasets/pinecone/yt-transcriptions). It uses advanced Semantic Search techniques and the Pinecone Vector Database to efficiently match your query with video transcripts. Moreover, it provides direct links to the exact timestamps in the videos where your questions are answered.

### How it Works:

1. Enter your question in natural language in the search box.
2. The app will use the Pinecone Vector Database (using the Streamlit Connection API) to find the most relevant videos and their corresponding timestamps for your query.
3. Get instant access to the YouTube videos that best match your search.

The live demo of the "YouTube Q&A" app is accessible through [Streamlit Community Cloud](https://st-pinecone-connection.streamlit.app/).

### Demo:

[st-pinecone-connection-yt-search-demo.webm](https://github.com/awinml/st-pinecone-connection/assets/97467100/e584d06f-77bd-4d7c-b980-c1404648c0d2)


### Dataset:

The app's dataset is sourced from HuggingFace, specifically the [Youtube Video Transcriptions](https://huggingface.co/datasets/pinecone/yt-transcriptions) dataset.

### Important Links:

- [Hackathon Link](https://discuss.streamlit.io/t/connections-hackathon/47574)
- [GitHub Repo](https://github.com/awinml/st-pinecone-connection)
- [Pinecone Vector Database](https://www.pinecone.io/)

### Note:

- Some URLs and images may not appear for certain keywords due to missing values in the original dataset. However, this does not impact the performance of the vector database or the app.
- Try searching for topics like "What is Reinforcement Learning?", "Explain GANs.", or "What is the difference between Tensorflow and Keras?".

### Made by:

**[Ashwin Mathur](https://github.com/awinml)**
