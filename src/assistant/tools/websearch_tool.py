"""component for web search that will be converted into a tool"""

from haystack.components.websearch import SerperDevWebSearch
from haystack.tools import ComponentTool
from haystack.utils import Secret


# TODO: replace with duckduckgo


def web_search_tool(top_k: int = 3) -> ComponentTool:
    """web_search_tool returned by `componentTool`
    :param top_k: number of results to fetch"""
    _search = SerperDevWebSearch(
        api_key=Secret.from_env_var("SERPERDEV_API_KEY"), top_k=top_k
    )
    return ComponentTool(
        component=_search,
        name="web_search_tool",
        description="Search the web for current or past information on any topic",
    )
