from fastapi import FastAPI
from src.assistant.pipelines.main_pipeline import run_main_pipe

from fastapi.middleware.cors import CORSMiddleware

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
    response = run_main_pipe([message])
    return {"response": response}
