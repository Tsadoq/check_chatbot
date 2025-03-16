from haystack.dataclasses import ChatMessage

from agents.agents import return_check_mk_helper_agent
from agents.tools import return_search_tools
from db_service.db_service import DataBaseService
from ingestion.embedders.openai_embedder import OpenAIEmbedder


class HermesService:
    def __init__(self):
        self.embedder = OpenAIEmbedder()
        self.db_service = DataBaseService(embedder_name=self.embedder.embedder_name)
        self.chat_ephemeral_db = {}
        self.agent_tools = return_search_tools(db_service=self.db_service)
        self.agent = return_check_mk_helper_agent(self.agent_tools)

    def chat(self, user_message: str, chat_id: str):
        conversation = self.chat_ephemeral_db.get(chat_id, [])
        conversation.append(ChatMessage.from_user(user_message))
        result = self.agent.run(
            messages=conversation,
        )
        self.chat_ephemeral_db[chat_id] = result["messages"]
        return result["messages"][-1].text
