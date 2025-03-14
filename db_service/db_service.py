import hashlib
import os
from typing import List, Dict, Any, Callable

import chromadb
import pandas as pd
from chromadb.api.models import Collection
import chromadb.utils.embedding_functions as embedding_functions
from chromadb.errors import InvalidCollectionException
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class DataBaseService:
    def __init__(self, embedder_name: str, delete_existing: bool = False):
        """
        Initialize the ChromaDB client and create the collections for blogposts, integrations, and documentation
        :param embedder_name: str, the name of the text embedding model to use
        :param delete_existing: bool, whether to delete existing collections
        """
        self.chromadb_clinet: chromadb.PersistentClient  = chromadb.PersistentClient(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/chroma"
        )
        self.search_function: Callable = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv('OPENAI_API_KEY'),
                model_name=embedder_name
            )

        if delete_existing:
            try:
                self.chromadb_clinet.delete_collection(name="blogposts")
                self.chromadb_clinet.delete_collection(name="integration")
                self.chromadb_clinet.delete_collection(name="documentation")
            except ValueError:
                pass
        try:
            self.blogpost_collection: Collection = self.chromadb_clinet.get_collection(name="blogposts", embedding_function=self.search_function)
        except InvalidCollectionException:
            self.blogpost_collection: Collection = self.chromadb_clinet.create_collection(
                name="blogposts",
                embedding_function=self.search_function,
            )

        try:
            self.integration_collection: Collection = self.chromadb_clinet.get_collection(name="integration", embedding_function=self.search_function)
        except InvalidCollectionException:
            self.integration_collection: Collection = self.chromadb_clinet.create_collection(
                name="integration",
                embedding_function=self.search_function,
            )
        try:
            self.documentation_collection: Collection = self.chromadb_clinet.get_collection(name="documentation", embedding_function=self.search_function)
        except InvalidCollectionException:
            self.documentation_collection: Collection = self.chromadb_clinet.create_collection(
                name="documentation",
                embedding_function=self.search_function,
            )

    def add_blogpost_docs(
            self,
            df_blogposts: pd.DataFrame,
            all_embeddings: List[List[float]],
            metadata: List[Dict[str, Any]],
    ) -> None:
        """
        Add blogpost documents to the blogpost collection
        :param df_blogposts: pd.DataFrame, the blogpost data
        :param all_embeddings: List[List[float]], the embeddings of the blogpost data
        :param metadata: List[Dict[str, Any]], the metadata of the blogpost data
        :return: None
        """

        self.blogpost_collection.add(
            documents=df_blogposts['chunk'].tolist(),
            embeddings=all_embeddings,
            metadatas=metadata,
            ids=[f'ID_BLOG_{i:05}' for i in range(len(df_blogposts))],
        )

    def add_integration_docs(
            self,
            df_integrations: pd.DataFrame,
            all_embeddings: List[List[float]],
            metadata: List[Dict[str, Any]],
    ) -> None:
        """
        Add integration documents to the integration collection
        :param df_integrations: pd.DataFrame, the integration data
        :param all_embeddings: List[List[float]], the embeddings of the integration data
        :param metadata: List[Dict[str, Any]], the metadata of the integration data
        :return: None
        """
        self.integration_collection.add(
            documents=df_integrations['content'].tolist(),
            embeddings=all_embeddings,
            metadatas=metadata,
            ids=[f'ID_INT_{i:05}' for i in range(len(df_integrations))],
        )

    def add_documentation_docs(
            self,
            df_documentation: pd.DataFrame,
            all_embeddings: List[List[float]],
            metadata: List[Dict[str, Any]],
    ) -> None:
        """
        Add documentation documents to the documentation collection
        :param df_documentation: pd.DataFrame, the documentation data
        :param all_embeddings: List[List[float]], the embeddings of the documentation data
        :param metadata: List[Dict[str, Any]], the metadata of the documentation data
        :return: None
        """
        chunks = df_documentation['chunk'].tolist()
        self.documentation_collection.add(
            documents=chunks,
            embeddings=all_embeddings,
            metadatas=metadata,
            ids=[f'ID_DOC_{i:05}' for i in range(len(df_documentation))],
        )

    def search(self, query: str, collection_name: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        Search for documents in the specified collection
        :param query: str, the query to search for
        :param collection_name: str, the name of the collection to search in
        :param limit: int, the maximum number of documents to return
        :return: List[Dict[str, str]], the search results
        """
        if collection_name == "blogposts":
            collection = self.blogpost_collection
        elif collection_name == "integration":
            collection = self.integration_collection
        elif collection_name == "documentation":
            collection = self.documentation_collection
        else:
            raise ValueError(f"Unknown collection name: {collection_name}")
        results = collection.query(
            query_texts=query,
            n_results=limit,
        )

        final_results = []

        for _id, doc in zip(results["ids"][0], results["documents"][0]):
            final_results.append({
                "id": _id,
                "document": doc,
            })
        return final_results


    def peak_collections(self):
        """
        Print the first 5 documents in each collection
        :return: None
        """
        for name, collection in [
            ("Blogpost", self.blogpost_collection),
            ("Integration", self.integration_collection),
            ("Documentation", self.documentation_collection)
        ]:
            print(f"{name} collection:")
            results = collection.get(limit=5)
            first_ids = results["ids"]
            first_docs = results["documents"]
            first_metadatas = results["metadatas"]

            for _id, doc, meta in zip(first_ids, first_docs, first_metadatas):
                print("ID:", _id)
                print("Document:", doc)
                print("Metadata:", meta)
                print("-----")
