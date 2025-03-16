import os
from typing import List

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

load_dotenv(find_dotenv())


class OpenAIEmbedder:
    def __init__(self, embedder_name=None):
        """
        Initialize the OpenAI client and the text embedding model name
        :param embedder_name: The name of the text embedding model to use
        """
        self.client: OpenAI = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        self.embedder_name: str = "text-embedding-3-small" if embedder_name is None else embedder_name

    def embed(self, text: str | List[str]) -> List[float] | List[List[float]]:
        """
        Embed a str or a list of strings using the OpenAI API
        :param text: str | List[str], the text to embed or a list of texts to embed
        :return: List[float] | List[List[float]], the embeddings of the text or texts
        """
        resp = self.client.embeddings.create(
            model=self.embedder_name,
            input=text,
            encoding_format="float"
        )
        if isinstance(text, str):
            return resp.data[0].embedding
        else:
            return [r.embedding for r in resp.data]

