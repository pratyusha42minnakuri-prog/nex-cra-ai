create FastAPI app NEX CRA AI wit GET / and GET / ask and POST /ask

import os
from typing import List, Literal
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import AsyncOpenAI

APP_NAME = "NEX CRA AI"
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title=APP_NAME,
    description="AI Homework Assistant API",
    version="1.0.0"
)

# CORS configuration for FlutterFlow and other clients
allowed_origins = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncOpenAI(api_key=API_KEY) if API_KEY else None

SYSTEM_PROMPT = """
You are NEX CRA AI, a helpful AI homework and learning assistant.
Answer questions accurately, clearly and in simple language.
Support mathematics, science, programming, English, history,
geography and other academic subjects.
Explain calculations step by step when appropriate.
If a question is unclear, ask for clarification.
Never invent facts or pretend uncertain information is verified.
"""


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=10000)


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1, max_length=10000)


class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., min_length=1, max_length=50)


def get_ai_client():
    if client is None:
        raise HTTPException(
            status_code=503,
            detail="AI service is not configured. Set OPENAI_API_KEY."
        )
    return client


async def generate_answer(messages):
    ai = get_ai_client()

    try:
        response = await ai.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ],
            temperature=0.3
        )

        answer = response.choices[0].message.content

        return answer or "Sorry, I could not generate an answer."

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="AI provider request failed. Please try again."
        )


@app.get("/")
async def home():
    return {
        "app": APP_NAME,
        "status": "running",
        "message": "Welcome to NEX CRA AI",
        "documentation": "/docs"
    }


@app.get("/health")
async def health():
    return {
        "app": APP_NAME,
        "status": "healthy",
        "ai_configured": client is not None
    }


@app.get("/ask")
async def ask_get(question: str = Field(..., min_length=1, max_length=10000)):
    answer = await generate_answer([
        {"role": "user", "content": question}
    ])

    return {
        "app": APP_NAME,
        "question": question,
        "answer": answer
    }


@app.post("/ask")
async def ask_post(request: AskRequest):
    answer = await generate_answer([
        {"role": "user", "content": request.question}
    ])

    return {
        "app": APP_NAME,
        "question": request.question,
        "answer": answer
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    messages = [
        {"role": message.role, "content": message.content}
        for message in request.messages
    ]

    answer = await generate_answer(messages)

    return {
        "app": APP_NAME,
        "answer": answer,
        "model": MODEL_NAME
    }

fastapi
uvicorn[standard]
openai
pydantic

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENV PORT=8080

EXPOSE 8080

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
pip install -r requirements.txtfrom fastapi import FastAPI, HTTPException, Query{
  "messages": [
    {
      "role": "user",
      "content": "What is Python?"
    },
    {
      "role": "assistant",
      "content": "Python is a programming language."
    },
    {
      "role": "user",
      "content": "Where is Python used?"
    }
 