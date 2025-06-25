from fastapi import FastAPI
from src.assistant.pipelines.main_pipeline import run_main_pipe

from fastapi.middleware.cors import CORSMiddleware

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__file__)


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate/{message}")
async def generate(message: str):
    if message == "":
        raise ValueError("Message cannot be empty")
    logger.info(f"Got: {message}")
    response = run_main_pipe(message)
    return {"response": response}
