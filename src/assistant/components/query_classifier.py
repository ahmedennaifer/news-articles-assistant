"""component, which is a pipeline, for classifying a query into a category"""

from haystack import Pipeline, SuperComponent
from haystack.components.builders import PromptBuilder
from haystack.components.generators.openai import OpenAIGenerator
from haystack.utils import Secret

from assistant.prompts.query_classifier_prompt import query_classifier_prompt
from assistant.components.base_llm import get_base_llm


def get_query_classifier_pipeline(
    template: str = query_classifier_prompt,
) -> SuperComponent:
    """This is a pipeline that will be turned into a `SuperComponent`.
    It returns the query and its category, defined in the prompt.
    :param template: the jinja template of the prompt
    """

    prompt_builder = PromptBuilder(template=template, required_variables=["query"])
    pipe = Pipeline()
    pipe.add_component("prompt", prompt_builder)
    pipe.add_component("llm", get_base_llm())
    pipe.connect("prompt.prompt", "llm.prompt")
    return SuperComponent(pipe)
