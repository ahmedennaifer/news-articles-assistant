"""main pipeline that calls other pipelines"""

from typing import List

from haystack import Pipeline, SuperComponent
from haystack.components.agents import Agent
from haystack.components.routers import ConditionalRouter

from src.assistant.components.retrieval_components.base_llm import get_base_chat_llm
from src.assistant.components.retrieval_components.query_classifier import (
    get_query_classifier_pipeline,
)
from src.assistant.components.retrieval_components.string_to_chat_message import (
    StringToChatMessage,
)
from src.assistant.pipelines.rag_pipeline import query_pipeline
from src.assistant.prompts.agent import AGENT_PROMPT
from src.assistant.routes.query_classifier_routes import routes
from src.assistant.tools.read_from_db import read_from_db_tool
from src.assistant.tools.websearch_tool import web_search_tool
from src.assistant.vectordb.db import get_doc_store

GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RESET = "\033[0m"


def run_main_pipe(queries: List[str]) -> List[str]:
    """main query that connects different pipelines and prints
    output to std and returns responses"""
    store = get_doc_store(collection_name="testing")
    query_pipe = query_pipeline(store)
    router = ConditionalRouter(routes)
    classifier_super_component = get_query_classifier_pipeline()

    # setup main pipeline, which consists of the query pipeline, and classifier pipeline of type `SuperComponent`. usefull for readability.
    pipe = Pipeline()
    pipe.add_component("router", router)
    pipe.add_component("classifier", classifier_super_component)
    pipe.add_component("string_to_chat_message", StringToChatMessage())
    pipe.add_component(
        "agent",
        Agent(
            chat_generator=get_base_chat_llm(),
            tools=[read_from_db_tool(), web_search_tool()],
            system_prompt=AGENT_PROMPT,
        ),
    )
    pipe.add_component(
        "rag_pipe",
        SuperComponent(
            query_pipe,
            input_mapping={
                "query": ["text_embed.text", "prompt.query"],
            },
        ),
    )
    pipe.connect("classifier.replies", "router.replies")
    pipe.connect("router.rag_query", "rag_pipe.query")
    pipe.connect("router.tool_query", "string_to_chat_message.messages")
    pipe.connect("string_to_chat_message.messages", "agent.messages")

    responses = []

    for q in queries:
        result = pipe.run(
            {
                "classifier": {"query": q},
                "router": {"query": q},
            }
        )

        if "agent" in result and result["agent"]:
            response_text = result["agent"]["messages"][-1]._content[0].text
            print(
                f"{GREEN}Query: {q}{RESET}\n",
                f"{GREEN}Tool Assistant:{RESET}",
                f"{response_text} \n",  # pylint: disable=protected-access
            )
            responses.append(response_text)

        elif "rag_pipe" in result and result["rag_pipe"]:
            response_text = result["rag_pipe"]["replies"][0]
            print(
                f"{YELLOW}Query: {q}{RESET}\n",
            )
            print(f"{YELLOW}Rag Assistant:{RESET}\n", response_text)
            responses.append(response_text)

        else:
            error_msg = "No valid response generated"
            print(f"Error: {error_msg}")
            responses.append(error_msg)

    return responses
