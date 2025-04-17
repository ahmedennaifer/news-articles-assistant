from haystack import Pipeline, SuperComponent
from haystack.components.generators.openai import OpenAIGenerator
from haystack.components.builders import PromptBuilder
from prompts.query_classifier_prompt import query_classifier_prompt
from haystack.utils import Secret


def get_query_classifier_pipeline(
    template: str = query_classifier_prompt,
) -> SuperComponent:
    """This is a pipeline that will be turned into a `SuperComponent`.
    It returns the query and its category, defined in the prompt.
    """
    prompt_builder = PromptBuilder(template=template, required_variables=["query"])
    llm = OpenAIGenerator(
        api_key=Secret.from_env_var("GROQ_KEY"),
        api_base_url="https://api.groq.com/openai/v1",
        model="llama-3.3-70b-versatile",
        generation_kwargs={"max_tokens": 512},
    )
    pipe = Pipeline()
    pipe.add_component("prompt", prompt_builder)
    pipe.add_component("llm", llm)
    pipe.connect("prompt.prompt", "llm.prompt")
    return SuperComponent(pipe)
