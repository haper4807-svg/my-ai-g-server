# -*- coding: utf-8 -*-
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from gigachat import GigaChat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Используй свой токен напрямую, чтобы точно работало
CREDENTIALS = "MDE5ZGE5ZTgtMGE4MC03ZWMxLWJkYTEtYjFjZTlkNWZlMTIxOjg4ZmUxMmEwLWFlMGUtNGI0Yy04ODFlLWNmMWQzYTBkMjQ0MA=="

@app.get("/ask_ai")
async def ask_ai(question: str):
    try:
        with GigaChat(credentials=CREDENTIALS, verify_ssl_certs=False) as giga:
            # Отправляем просто текст, так надежнее для теста
            response = giga.chat(question)
            answer = response.choices[0].message.content
        return {"answer": str(answer)}
    except Exception as e:
        # Если ошибка, мы увидим её текст вместо undefined
        return {"answer": f"Ошибка на стороне AI: {str(e)}"}

@app.get("/")
async def root():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
