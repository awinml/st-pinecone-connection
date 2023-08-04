import streamlit as st
from st_pinecone_connection import PineconeConnection
from sentence_transformers import SentenceTransformer


# Function to initialize the sentence transformer model
@st.cache_resource
def init_retriever():
    """Initialize and cache the SentenceTransformer model."""
    return SentenceTransformer("sentence-transformers/all-mpnet-base-v2")


# Function to create a card displaying video information
def card(thumbnail, title, url, context):
    """Generate an HTML card to display video information."""
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


# Main Streamlit app code
st.header("YouTube Q&A: Find Similar Videos with Timestamps")
st.markdown(
    """
Welcome to the YouTube Q&A app, an official submission to the Streamlit Connections Hackathon.

The YouTube Q&A app helps you discover videos with similar content to your natural language questions. It leverages advanced Semantic Search techniques and the Pinecone Vector Database to efficiently match your query with video transcripts. Moreover, it provides direct links to the exact timestamps in the videos where your questions are answered.

Happy exploring and enjoy discovering new content with pinpoint accuracy!

"""
)

with st.sidebar:
    st.markdown(
        """
    ### How it Works:
1. Enter your question in natural language in the search box.
2. The app will use the Pinecone Vector Database (using the Streamlit Connection API) to find the most relevant videos and their corresponding timestamps for your query.
3. Get instant access to the YouTube videos that best match your search.

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
"""
    )


# Connect app to Pinecone Client
conn = st.experimental_connection(
    "PineconeVectorDB",
    type=PineconeConnection,
    environment="us-west1-gcp-free",
    api_key=st.secrets["api_key"],  # Your Pinecone API key stored in Streamlit secrets
)

cursor = conn.cursor()
retriever = init_retriever()

# Sample questions

option = st.selectbox(
    "Select Sample Question or type in Search Query below:",
    (
        "---- Select Question ----",
        "What is Reinforcement Learning?",
        "What are GANs?",
        "What is the difference between Tensorflow and Keras?",
    ),
    placeholder="",
)


if option == "---- Select Question ----":
    option = ""


# Input box to enter the search query

query_str = st.text_input("Please enter Search Query:", option)

if query_str != "":
    xq = retriever.encode([query_str]).tolist()  # Encoding the search query
    xc = conn.query(
        index_name="youtube-search", query_vector=xq, top_k=5, include_metadata=True
    )  # Querying Pinecone database with the encoded query

    for context in xc["matches"]:
        # Displaying video information using the card function
        card(
            context["metadata"]["thumbnail"],
            context["metadata"]["title"],
            context["metadata"]["url"],
            context["metadata"]["text"],
        )
