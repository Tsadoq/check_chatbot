from typing import List

from haystack.tools import Tool

from db_service.db_service import DataBaseService


def return_search_tools(db_service: DataBaseService) -> List[Tool]:
    """
    Return the search tools
    :param db_service: DataBaseService, the database service
    :return: List of the search tools
    """

    def search_docs(query: str) -> str:
        """
        Search the documentation collection
        :param query: str, the query to search in the documentation collection
        :return: str, the search results as a string
        """
        results = db_service.search(
            query=query,
            collection_name="documentation"
        )

        return '\n\n'.join(
            [f"DOC_ID: {result['id']}\n\nDOC_CONTENT: {result['document']}" for result in results]
        )

    def search_integrations(query: str) -> str:
        """
        Search the integrations collection
        :param query: str, the query to search in the integrations collection
        :return: str, the search results as a string
        """
        results =  db_service.search(
            query=query,
            collection_name="integrations"
        )

        return '\n\n'.join(
            [f"DOC_ID: {result['id']}\n\nDOC_CONTENT: {result['document']}" for result in results]
        )

    def search_blogposts(query: str) -> str:
        """
        Search the blogposts collection
        :param query: str, the query to search in the blogposts collection
        :return: str, the search results as a string
        """
        results = db_service.search(
            query=query,
            collection_name="blogposts"
        )

        return '\n\n'.join(
            [f"DOC_ID: {result['id']}\n\nDOC_CONTENT: {result['document']}" for result in results]
        )

    documentation_search_tool = Tool(
        name="documentation_search",
        function=search_docs,
        description="Used to search the documentation of CheckMK",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
            },
            "required": ["query"]
        }
    )

    integrations_search_tool = Tool(
        name="integrations_search",
        function=search_integrations,
        description="Used to search the integrations of CheckMK",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
            },
            "required": ["query"]
        }
    )

    blogposts_search_tool = Tool(
        name="blogposts_search",
        function=search_blogposts,
        description="Used to search the blogposts of CheckMK",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
            },
            "required": ["query"]
        }
    )

    return [
        documentation_search_tool,
        integrations_search_tool,
        blogposts_search_tool
    ]