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
        """
        Initialize the PineconeConnection object.

        Parameters:
        - connection_name (str): The name of the connection.
        - environment (str): The Pinecone environment to connect to.
        - api_key (str): The Pinecone API key for authentication.
        - **kwargs: Additional keyword arguments for ExperimentalBaseConnection.

        """
        self.environment = environment
        self.api_key = api_key
        super().__init__(connection_name, **kwargs)

    def _connect(self):
        """
        Connect to Pinecone using the provided API key and environment.

        Returns:
        - pinecone.Connection: The Pinecone connection object.

        """
        api_key = self.api_key or self._secrets.get("Pinecone_API_KEY")
        environment = self.environment
        return pinecone.init(api_key=api_key, environment=environment)

    def list_indexes(self):
        """
        Get a list of available indexes in the Pinecone environment.

        Returns:
        - list: List of index names.

        """
        self._connect()
        self.indexes = pinecone.list_indexes()
        return self.indexes

    def _connect_index(self, index_name):
        """
        Connect to a specific index in the Pinecone environment.

        Parameters:
        - index_name (str): The name of the index to connect to.

        Returns:
        - pinecone.Index: The Pinecone index object.

        """
        self._connect()
        self.index_name = index_name
        self.index = pinecone.Index(index_name)
        return self.index

    def query(
        self, index_name: str, query_vector, top_k: int = 5, ttl: int = 3600, **kwargs
    ) -> dict:
        """
        Perform a query on the specified index using the given query vector.

        Parameters:
        - index_name (str): The name of the index to query.
        - query_vector: The vector representation of the query.
        - top_k (int): The number of results to retrieve (default is 5).
        - ttl (int): Time-to-live for caching the query results (default is 3600 seconds).
        - **kwargs: Additional keyword arguments for the query.

        Returns:
        - dict: Dictionary containing the query results.

        """

        @st.cache_data(ttl=ttl)
        def _query(index_name: str, query_vector, top_k: int = 5, **kwargs):
            """
            Internal function to perform the actual query.

            Parameters:
            - index_name (str): The name of the index to query.
            - query_vector: The vector representation of the query.
            - top_k (int): The number of results to retrieve.
            - **kwargs: Additional keyword arguments for the query.

            Returns:
            - dict: Dictionary containing the query results.

            """
            index = self._connect_index(index_name)
            query_results = index.query(query_vector, top_k=top_k, **kwargs)
            results = query_results.to_dict()
            return results

        results = _query(index_name, query_vector, top_k, **kwargs)
        return results

    def cursor(self):
        """
        Get a cursor to the Pinecone connection.

        Returns:
        - pinecone.Connection: The Pinecone connection object.

        """
        return self._connect()
