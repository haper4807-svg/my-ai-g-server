# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from gigachat import GigaChat

app = FastAPI()

# --- ТВОЙ ТОКЕН ТУТ ---
GIGACHAT_CREDENTIALS = "MDE5ZGE5ZTgtMGE4MC03ZWMxLWJkYTEtYjFjZTlkNWZlMTIxOjg4ZmUxMmEwLWFlMGUtNGI0Yy04ODFlLWNmMWQzYTBkMjQ0MA==" 

chat_history = [{"role": "system", "content": "Ты полезный ИИ-ассистент под именем AI G."}]

@app.get("/", response_class=HTMLResponse)
async def get_app():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI G Assistant</title>
        <style>
            :root {
                --primary: #6366f1;
                --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            }
            body { font-family: 'Segoe UI', Roboto, sans-serif; background: var(--bg-gradient); height: 100vh; margin: 0; display: flex; justify-content: center; align-items: center; }
            
            .phone { 
                width: 360px; height: 720px; background: #ffffff; 
                border: 10px solid #000; border-radius: 40px; 
                display: flex; flex-direction: column; overflow: hidden; 
                box-shadow: 0 50px 100px rgba(0,0,0,0.5); 
            }
            
            /* НОВЫЙ ЗАГОЛОВОК */
            .header { 
                padding: 45px 20px 20px; background: #fff; border-bottom: 1px solid #f3f4f6; 
                text-align: center; font-weight: 700; font-size: 22px; color: var(--primary);
                letter-spacing: -0.5px;
            }
            
            .chat { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; background: #f8fafc; }
            
            .msg { padding: 12px 16px; border-radius: 18px; font-size: 14px; max-width: 85%; line-height: 1.5; animation: fadeIn 0.2s ease; word-wrap: break-word; }
            @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
            
            .user { align-self: flex-end; background: var(--primary); color: white; border-bottom-right-radius: 4px; }
            .ai { align-self: flex-start; background: white; color: #1e293b; border-bottom-left-radius: 4px; border: 1px solid #e2e8f0; }
            
            .typing { font-size: 11px; color: #94a3b8; margin: 5px 25px; display: none; font-style: italic; }

            .input-bar { padding: 15px 20px; background: white; display: flex; align-items: center; gap: 12px; border-top: 1px solid #f1f5f9; }
            input { flex: 1; border: none; padding: 12px 18px; background: #f1f5f9; border-radius: 20px; outline: none; font-size: 14px; color: #1e293b; }
            
            /* НОВАЯ КНОПКА МИКРОФОНА */
            .mic-btn { 
                width: 42px; height: 42px; border-radius: 50%; border: none; 
                background: #f1f5f9; color: #64748b; cursor: pointer; 
                display: flex; align-items: center; justify-content: center; font-size: 18px; transition: 0.2s;
            }
            .mic-btn.listening { background: #ef4444; color: white; animation: pulse 1.5s infinite; }
            
            /* НОВАЯ КНОПКА ОТПРАВИТЬ */
            .send-btn { 
                width: 42px; height: 42px; border-radius: 50%; border: none; 
                background: var(--primary); color: white; cursor: pointer; 
                display: flex; align-items: center; justify-content: center; font-size: 18px; transition: 0.2s;
                box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3);
            }
            .send-btn:hover { transform: scale(1.05); background: #4f46e5; }

            @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); } 70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); } 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); } }
        </style>
    </head>
    <body>
        <div class="phone">
            <div class="header">AI G Assistant</div>
            <div class="chat" id="chat">
                <div class="msg ai">Привет! Я <b>AI G</b>. О чем сегодня поговорим?</div>
            </div>
            <div id="typingIndicator" class="typing">AI G печатает...</div>
            <div class="input-bar">
                <button class="mic-btn" id="micBtn" onclick="toggleListen()">🎤</button>
                <input type="text" id="query" placeholder="Сообщение..." onkeypress="if(event.keyCode==13) sendMessage()">
                <button class="send-btn" onclick="sendMessage()">➤</button>
            </div>
        </div>

        <script>
            const micBtn = document.getElementById('micBtn');
            const queryInput = document.getElementById('query');
            const chat = document.getElementById('chat');
            const typingIndicator = document.getElementById('typingIndicator');

            const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            let recognition;
            if (Recognition) {
                recognition = new Recognition();
                recognition.lang = 'ru-RU';
                recognition.onresult = (e) => { 
                    queryInput.value = e.results[0][0].transcript; 
                    micBtn.classList.remove('listening'); 
                    sendMessage(); 
                };
                recognition.onend = () => micBtn.classList.remove('listening');
                recognition.onerror = () => micBtn.classList.remove('listening');
            }

            function toggleListen() {
                if (!recognition) return alert("Микрофон не поддерживается");
                micBtn.classList.add('listening');
                recognition.start();
            }

            async function sendMessage() {
                const text = queryInput.value.trim();
                if (!text) return;
                chat.innerHTML += `<div class="msg user">${text}</div>`;
                queryInput.value = '';
                chat.scrollTop = chat.scrollHeight;
                typingIndicator.style.display = 'block';

                try {
                    const response = await fetch(`/ask_ai?question=${encodeURIComponent(text)}`);
                    const data = await response.json();
                    typingIndicator.style.display = 'none';
                    chat.innerHTML += `<div class="msg ai">${data.answer}</div>`;
                } catch (e) {
                    typingIndicator.style.display = 'none';
                    chat.innerHTML += `<div class="msg ai" style="color:#ef4444">Ошибка связи</div>`;
                }
                chat.scrollTop = chat.scrollHeight;
            }
        </script>
    </body>
    </html>
    """

@app.get("/ask_ai")
async def ask_ai(question: str):
    global chat_history
    try:
        chat_history.append({"role": "user", "content": question})
        with GigaChat(credentials=GIGACHAT_CREDENTIALS, verify_ssl_certs=False) as giga:
            response = giga.chat({"messages": chat_history})
            answer = response.choices[0].message.content
            chat_history.append({"role": "assistant", "content": answer})
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Ошибка AI: {str(e)}"}

if __name__ == "__main__":
    import os
    # Порт будет выдан сервером автоматически
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
