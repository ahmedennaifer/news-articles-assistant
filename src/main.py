"""entry point that groups all pipelines"""

from haystack import Document, Pipeline, SuperComponent
from haystack.components.agents import Agent
from haystack.components.routers import ConditionalRouter
from haystack.document_stores.in_memory import InMemoryDocumentStore

from assistant.components.base_llm import get_base_chat_llm
from assistant.components.query_classifier import get_query_classifier_pipeline
from assistant.components.string_to_chat_message import StringToChatMessage
from assistant.pipelines.index_pipeline import index
from assistant.pipelines.rag_pipeline import query_pipeline
from assistant.prompts.agent import AGENT_PROMPT
from assistant.routes.query_classifier_routes import routes
from assistant.tools.dummy_tool import WeatherTool

# TODO : connect agent to tool
RAG_PARAGRAPH = "A groundbreaking paper published in the Journal of Molecular Biology explores the intricate relationship between mitochondrial function and cellular aging. The researchers utilized advanced microscopy techniques to observe real-time changes in mitochondrial morphology as cells progress through their life cycle. Their findings suggest that specific proteins regulating mitochondrial fusion and fission play a crucial role in determining cellular lifespan, potentially offering new targets for age-related disease interventions. What makes this study particularly noteworthy is its novel approach to tracking individual mitochondria over extended periods, revealing previously unobserved patterns of deterioration that precede cellular senescence. The implications extend beyond basic research, pointing toward potential therapeutic strategies that could modify these pathways to promote cellular health and longevity in aging populations"


def main():
    """testing"""
    store = InMemoryDocumentStore()
    index(store, Document(content=RAG_PARAGRAPH))  # TODO: i dont like this
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
            tools=[WeatherTool()],
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

    tool_query = "What is the weather today in berlin?"
    rag_query = "What does the paper on biology talk about?"
    db_query = "What are our regional sales for Q4?"
    general_query = "What is the capital of Paris?"

    queries = [tool_query, rag_query]
    for q in queries:
        result = pipe.run(
            {
                "classifier": {"query": q},
                "router": {"query": q},
            }
        )
        if "agent" in result and result["agent"]:
            print("Tool Assistant:", result["agent"]["messages"][-1]._content[0].text)
        else:
            print("Rag Assistant:", result["rag_pipe"]["replies"][0])


if __name__ == "__main__":
    main()
