import pandas as pd
import pinecone
import streamlit as st
from streamlit.connections import ExperimentalBaseConnection


class PineconeConnection(ExperimentalBaseConnection):
    def __init__(
        self,
        connection_name: str,
        environment=None,
        api_key=None,
        **kwargs,
    ) -> None:
        self.environment = environment
        self.api_key = api_key
        super().__init__(connection_name, **kwargs)

    def _connect(self):
        api_key = self.api_key or self._secrets.get("Pinecone_API_KEY")
        environment = self.environment
        return pinecone.init(api_key=api_key, environment=environment)

    def list_indexes(self):
        self._connect()
        self.indexes = pinecone.list_indexes()
        return self.indexes

    def _connect_index(self, index_name):
        self._connect()
        self.index_name = index_name
        self.index = pinecone.Index(index_name)
        return self.index

    def query(
        self, index_name: str, query_vector, top_k: int = 5, ttl: int = 3600, **kwargs
    ) -> dict:
        @st.cache_resource(ttl=ttl)
        def _query(index_name: str, query_vector, top_k: int = 5, **kwargs):
            index = self._connect_index(index_name)
            query_results = index.query(query_vector, top_k=top_k, **kwargs)
            results = list(query_results["matches"])
            return results

        results = _query(index_name, query_vector, top_k, **kwargs)
        return results

    def cursor(self):
        return self._connect()
