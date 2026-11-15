
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from portfolio import system_prompt, get_response

app = FastAPI()
conversations = {}

class ChatRequest(BaseModel):
    session_id: str
    question: str

@app.get("/")
def home():
    return {
        "message": "Portfolio Chatbot API is running"
    }

@app.post("/chat")
def chat(request: ChatRequest):

    session_id = request.session_id
    question = request.question

    if not session_id.strip() or not question.strip():
        raise HTTPException(
            status_code=400,
            detail="Session ID and question cannot be empty"
        )

    if session_id not in conversations:

        conversations[session_id] = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

    messages = conversations[session_id]

    messages.append({
        "role": "user",
        "content": question
    })

    try:

        answer = get_response(messages)

        messages.append({
            "role": "assistant",
            "content": answer
        })

        return {
            "session_id": session_id,
            "question": question,
            "answer": answer
        }

    except Exception:
        messages.pop()

        raise HTTPException(
            status_code=500,
            detail="Something went wrong while generating the response"
        )
