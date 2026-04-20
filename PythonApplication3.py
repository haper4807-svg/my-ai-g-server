# -*- coding: utf-8 -*-
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from gigachat import GigaChat

app = FastAPI()

# Разрешаем запросы от твоего приложения (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ВСТАВЬ СЮДА СВОЙ ТОКЕН ИЗ GIGACHAT STUDIO
GIGACHAT_CREDENTIALS = "MDE5ZGE5ZTgtMGE4MC03ZWMxLWJkYTEtYjFjZTlkNWZlMTIxOjg4ZmUxMmEwLWFlMGUtNGI0Yy04ODFlLWNmMWQzYTBkMjQ0MA=="

chat_history = [{"role": "system", "content": "Ты полезный ИИ-ассистент под именем AI G."}]

@app.get("/ask_ai")
async def ask_ai(question: str):
    global chat_history
    try:
        chat_history.append({"role": "user", "content": question})
        with GigaChat(credentials=GIGACHAT_CREDENTIALS, verify_ssl_certs=False) as giga:
            response = giga.chat({"messages": chat_history})
            # Правильное получение ответа
            answer = response.choices[0].message.content
            chat_history.append({"role": "assistant", "content": answer})
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Ошибка AI G: {str(e)}"}

@app.get("/")
async def root():
    return {"message": "AI G Server is Running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
