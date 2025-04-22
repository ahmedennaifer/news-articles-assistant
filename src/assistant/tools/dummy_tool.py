"""dummy tool, will be replaced by actual tools"""

from haystack.tools import Tool

# TODO: rewrite better

WEATHER_TOOL_PARAMS = {
    "type": "object",
    "properties": {"city": {"type": "string"}},
    "required": ["city"],
}


def get_weather(city: str) -> str:
    """dummy tool"""
    return f" weather in {city} is 20 degrees celcius"


def weather_tool(tool_params: dict = WEATHER_TOOL_PARAMS) -> Tool:
    """returns a formatted Tool object"""
    return Tool(
        name="weather_tool",
        description="This tool fetches the current weather",
        parameters=tool_params,
        function=get_weather,
    )
