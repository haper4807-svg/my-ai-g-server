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

# Твой токен
CREDENTIALS = "MDE5ZGE5ZTgtMGE4MC03ZWMxLWJkYTEtYjFjZTlkNWZlMTIxOjg4ZmUxMmEwLWFlMGUtNGI0Yy04ODFlLWNmMWQzYTBkMjQ0MA=="

# Глобальный список для хранения истории (Память)
# Мы добавляем системную роль, чтобы ИИ знал, кто он
chat_history = [{"role": "system", "content": "Ты полезный ИИ-ассистент под именем AI G."}]

@app.get("/ask_ai")
async def ask_ai(question: str):
    global chat_history
    try:
        # 1. Запоминаем вопрос пользователя
        chat_history.append({"role": "user", "content": question})
        
        # 2. Ограничиваем память (храним только последние 10 сообщений, чтобы не зависало)
        if len(chat_history) > 11:
            chat_history = [chat_history[0]] + chat_history[-10:]

        with GigaChat(credentials=CREDENTIALS, verify_ssl_certs=False) as giga:
            # 3. Отправляем ВСЮ историю сообщений
            response = giga.chat({"messages": chat_history})
            answer = response.choices[0].message.content
            
            # 4. Запоминаем ответ ИИ
            chat_history.append({"role": "assistant", "content": answer})
            
        return {"answer": str(answer)}
    except Exception as e:
        return {"answer": f"Ошибка памяти AI: {str(e)}"}

@app.get("/")
async def root():
    return {"status": "ok", "history_len": len(chat_history)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
