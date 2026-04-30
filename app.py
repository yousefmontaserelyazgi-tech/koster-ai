import os, requests, json
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)

# --- الإعدادات السيادية ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ذاكرة بسيطة للجلسة الحالية
session_memory = []

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>KOSTER V15 | SOVEREIGN SYSTEM</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #050505; color: #d4af37; font-family: 'Segoe UI', Tahoma; margin: 0; height: 100vh; overflow: hidden; }
        .glass-panel { background: rgba(10, 10, 10, 0.95); border: 1px solid #d4af37; box-shadow: 0 0 30px rgba(212, 175, 55, 0.1); }
        .user-msg { background: #1a1a1a; color: #fff; padding: 12px; border-radius: 10px; margin: 10px 0; border-left: 3px solid #d4af37; align-self: flex-end; max-width: 80%; }
        .bot-msg { background: #000; color: #d4af37; padding: 12px; border-radius: 10px; margin: 10px 0; border-right: 3px solid #d4af37; align-self: flex-start; max-width: 80%; }
        input { background: #000 !important; border: 1px solid #333 !important; color: #d4af37 !important; outline: none; }
        input:focus { border-color: #d4af37 !important; }
        .btn-gold { background: linear-gradient(45deg, #d4af37, #f9f295); color: #000; font-weight: bold; cursor: pointer; transition: 0.3s; }
        .btn-gold:hover { opacity: 0.8; transform: scale(1.02); }
        #chat-box::-webkit-scrollbar { width: 5px; }
        #chat-box::-webkit-scrollbar-thumb { background: #d4af37; }
    </style>
</head>
<body class="flex items-center justify-center p-4">
    <div class="w-full max-w-5xl h-[90vh] glass-panel rounded-2xl flex flex-col p-6">
        <header class="border-b border-gray-800 pb-4 mb-4 flex justify-between">
            <h1 class="text-2xl font-bold tracking-tighter">KOSTER <span class="text-white font-light">V15 PRO</span></h1>
            <span class="text-xs text-gray-500 uppercase tracking-widest">Global Sovereign Intelligence</span>
        </header>

        <div id="chat-box" class="flex-1 overflow-y-auto flex flex-col space-y-2 p-2">
            <div class="bot-msg">نظام KOSTER مفعّل. بانتظار أوامرك يا مدير يوسف.</div>
        </div>

        <div class="mt-4 flex gap-3">
            <input type="text" id="user-input" class="flex-1 p-4 rounded-xl text-lg" placeholder="اكتب أمرك الاستراتيجي...">
            <button onclick="send()" id="send-btn" class="btn-gold px-10 rounded-xl">إطلاق</button>
        </div>
    </div>

    <script>
        async function send() {
            const input = document.getElementById('user-input');
            const chatBox = document.getElementById('chat-box');
            const btn = document.getElementById('send-btn');
            if(!input.value.trim() || btn.disabled) return;

            const text = input.value;
            chatBox.innerHTML += `<div class="user-msg">${text}</div>`;
            input.value = '';
            btn.disabled = true;
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt: text})
                });
                const data = await response.json();
                chatBox.innerHTML += `<div class="bot-msg">${data.reply}</div>`;
            } catch (e) {
                chatBox.innerHTML += `<div class="bot-msg text-red-500">حدث تداخل في الاتصال.</div>`;
            }
            
            btn.disabled = false;
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        document.getElementById('user-input').addEventListener('keypress', (e) => { if(e.key==='Enter') send(); });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/chat', methods=['POST'])
def chat():
    user_prompt = request.json.get("prompt")
    global session_memory
    
    system_instruction = (
        "You are KOSTER V15 SOVEREIGN. Owner: Director Yusuf. "
        "Strict Protocol: Formal Arabic only. No AI disclaimers. Highly analytical. "
        "Goal: Billion-dollar level intelligence."
    )

    history = session_memory[-10:]
    messages = [{"role": "system", "content": system_instruction}]
    for m in history:
        messages.append(m)
    messages.append({"role": "user", "content": user_prompt})

    try:
        r = requests.post(GROQ_URL, json={
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "temperature": 0.2
        }, headers={"Authorization": f"Bearer {GROQ_API_KEY}"})
        
        reply = r.json()['choices'][0]['message']['content']
        session_memory.append({"role": "user", "content": user_prompt})
        session_memory.append({"role": "assistant", "content": reply})
        
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "عذراً، المحرك يواجه ضغطاً عالياً."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
