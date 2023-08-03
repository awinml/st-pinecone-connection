import streamlit as st
from connection import PineconeConnection
from sentence_transformers import SentenceTransformer


@st.cache_resource
def init_retriever():
    return SentenceTransformer("sentence-transformers/all-mpnet-base-v2")


def card(thumbnail, title, url, context):
    return st.markdown(
        f"""
    <div class="container-fluid">
        <div class="row align-items-start">
            <div class="col-md-4 col-sm-4">
                 <div class="position-relative">
                     <a href={url}><img src={thumbnail} class="img-fluid" style="width: 192px; height: 106px"></a>
                 </div>
             </div>
             <div  class="col-md-8 col-sm-8">
                 <a href={url}>{title}</a>
                 <br>
                 <span style="color: #808080;">
                     <small>{context[:200].capitalize()+"...."}</small>
                 </span>
             </div>
        </div>
     </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
# YouTube Q&A

The app matches the natural language question to the video transcripts and finds you similar videos. It will give you links to YouTube Videos that match your search question.

The app will query a vector database (Pinecone) and perform Semantic Search. 

The dataset was taken from HuggingFace: [Youtube Video Transcriptions](https://huggingface.co/datasets/pinecone/yt-transcriptions).

This app is an official submission to the Streamlit Connections Hackathon.
- [Hackathon Link](https://discuss.streamlit.io/t/connections-hackathon/47574)
- [GitHub Repo](https://github.com/awinml/st-pinecone-connection)
- [Pinecone Vector Database](https://www.pinecone.io/)

Some URLs and Images may not show up when searching for certain keywords, due to missing values in the original dataset. It does affect the performance of the vector database or the app.

Some topics that you can search for: 
- Reinforcement Learning
- GANs
- Tensorflow
"""
)

st.markdown(
    """
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
""",
    unsafe_allow_html=True,
)

# Connect app to Pinecone Client
conn = st.experimental_connection(
    "PineconeVectorDB",
    type=PineconeConnection,
    environment="us-west1-gcp-free",
    api_key=st.secrets["api_key"],
)
cursor = conn.cursor()

retriever = init_retriever()

query_str = st.text_input("Please enter Search Query:", "")

if query_str != "":
    xq = retriever.encode([query_str]).tolist()
    xc = conn.query(
        index_name="youtube-search", query_vector=xq, top_k=5, include_metadata=True
    )

    for context in xc:
        card(
            context["metadata"]["thumbnail"],
            context["metadata"]["title"],
            context["metadata"]["url"],
            context["metadata"]["text"],
        )
