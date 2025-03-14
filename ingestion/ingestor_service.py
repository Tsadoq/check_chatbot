import os
from tqdm import tqdm

from db_service.db_service import DataBaseService
from ingestion.embedders.openai_embedder import OpenAIEmbedder
from ingestion.parsers.blogpost_ingestion import load_blogposts_chunks
from ingestion.parsers.docs_ingestion import load_asciidoc_files_chunks
from ingestion.parsers.integration_ingestion import load_integrations


class IngestorService:
    def __init__(self):
        self.embedder = OpenAIEmbedder()
        self.db_service = DataBaseService(embedder_name=self.embedder.embedder_name)
        base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/assets"
        self.blogpost_folder = f"{base_path}/blogposts_samples"
        self.integration_folder = f"{base_path}/integrations_samples"
        self.documentation_folder = f"{base_path}/docs"
        self.batch_size = 100

    def ingest_blogposts(self) -> None:
        """
        Ingest blogposts into the blogpost collection
        :return: None
        """
        df_blogposts = load_blogposts_chunks(self.blogpost_folder)
        all_embeddings = []
        print(f"Loaded {len(df_blogposts)} blogposts")
        for start in tqdm(range(0, len(df_blogposts), self.batch_size), desc="Embedding batches"):
            end = start + self.batch_size
            batch_texts = df_blogposts.iloc[start:end]['chunk'].tolist()
            batch_embeddings = self.embedder.embed(batch_texts)
            all_embeddings.extend(batch_embeddings)

        metadata = df_blogposts.drop(columns=['chunk']).to_dict(orient='records')
        self.db_service.add_blogpost_docs(df_blogposts, all_embeddings, metadata)


    def ingest_integration(self) -> None:
        """
        Ingest integration into the integration collection
        :return: None
        """

        df_integrations = load_integrations(self.integration_folder)
        all_embeddings = []
        print(f"Loaded {len(df_integrations)} integrations")
        for start in tqdm(range(0, len(df_integrations), self.batch_size), desc="Embedding batches"):
            end = start + self.batch_size
            batch_texts = df_integrations.iloc[start:end]['content'].tolist()
            batch_embeddings = self.embedder.embed(batch_texts)
            all_embeddings.extend(batch_embeddings)

        metadata = df_integrations.drop(columns=['content']).to_dict(orient='records')
        self.db_service.add_integration_docs(df_integrations, all_embeddings, metadata)


    def ingest_documentation(self) -> None:
        """
        Ingest documentation into the documentation collection
        :return: None
        """

        df_documentation = load_asciidoc_files_chunks(self.documentation_folder)
        print(f"Loaded {len(df_documentation)} documentation chunks")
        all_embeddings = []
        for start in tqdm(range(0, len(df_documentation), self.batch_size), desc="Embedding batches"):
            end = start + self.batch_size
            batch_texts = df_documentation.iloc[start:end]['chunk'].tolist()
            batch_embeddings = self.embedder.embed(batch_texts)
            all_embeddings.extend(batch_embeddings)

        metadata = df_documentation.drop(columns=['chunk']).to_dict(orient='records')
        self.db_service.add_documentation_docs(df_documentation, all_embeddings, metadata)

    def get_db_service(self) -> DataBaseService:
        """
        Get the database service object
        :return: DataBaseService object
        """
        return self.db_service
