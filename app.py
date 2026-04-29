import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# 🔑 تأكد من وضع مفتاحك هنا
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# 🧠 ذاكرة حديدية + تعليمات صارمة جداً
chat_history = [
    {
        "role": "system", 
        "content": (
            "You are KOSTER V15 PRO, a super-intelligent and rational AI. "
            "STRICT INSTRUCTION: Speak ONLY in the language used by the user. "
            "If the user speaks Arabic, every single character you write must be Arabic. "
            "DO NOT mix English words like 'Hamd' or 'Smart' within Arabic sentences. "
            "Be precise, logical, and maintain a professional tone."
        )
    }
]

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSTER V15 PRO | النمط العقلاني</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #020617; color: white; font-family: 'Segoe UI', sans-serif; height: 100vh; margin: 0; overflow: hidden; }
        .glass { background: rgba(15, 23, 42, 0.95); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; }
        .user-msg { background: #1d4ed8; padding: 12px; border-radius: 15px 15px 0 15px; align-self: flex-end; max-width: 80%; }
        .bot-msg { background: #1e293b; border-right: 4px solid #f59e0b; padding: 12px; border-radius: 15px 15px 15px 0; align-self: flex-start; max-width: 80%; }
        .custom-scroll::-webkit-scrollbar { width: 5px; }
        .custom-scroll::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
    </style>
</head>
<body class="flex items-center justify-center p-4">
    <div class="max-w-4xl w-full h-[92vh] flex flex-col glass p-6 shadow-2xl">
        <header class="pb-4 border-b border-white/10 mb-4 flex justify-between items-center">
            <h1 class="text-2xl font-bold text-amber-500">KOSTER V15 PRO</h1>
            <span class="text-green-500 font-mono text-sm">● MODE: RATIONAL_MEMORY</span>
        </header>
        
        <div id="chat" class="flex-1 overflow-y-auto space-y-4 flex flex-col pr-4 custom-scroll">
            <div class="bot-msg">نظام KOSTER في خدمتكم يا مدير يوسف. تم تفعيل وحدة المنطق والذاكرة المستمرة. كيف أساعدك؟</div>
        </div>

        <div class="mt-4 flex gap-3 bg-slate-900 p-3 rounded-2xl border border-white/10">
            <input type="text" id="msg" class="flex-1 bg-transparent outline-none text-white" placeholder="أمرك مطاع...">
            <button onclick="send()" id="btn" class="bg-amber-500 hover:bg-amber-400 text-black px-8 py-2 rounded-xl font-bold transition-all">إرسال</button>
        </div>
    </div>

    <script>
        async function send() {
            const input = document.getElementById('msg');
            const chat = document.getElementById('chat');
            const btn = document.getElementById('btn');
            if (!input.value.trim() || btn.disabled) return;

            const text = input.value;
            chat.innerHTML += `<div class="user-msg">${text}</div>`;
            input.value = '';
            btn.disabled = true;
            chat.scrollTop = chat.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await response.json();
                chat.innerHTML += `<div class="bot-msg">${data.reply}</div>`;
            } catch (e) {
                chat.innerHTML += `<div class="bot-msg text-red-400">خطأ فني في الربط.</div>`;
            }
            btn.disabled = false;
            chat.scrollTop = chat.scrollHeight;
        }
        document.getElementById('msg').addEventListener('keypress', (e) => { if(e.key==='Enter') send(); });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message")
    chat_history.append({"role": "user", "content": user_msg})
    
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": chat_history,
        "temperature": 0.3,  # 📉 تم خفضها جداً ليكون عقلانياً ولا يخلط اللغات
        "top_p": 0.85,       # تقليل العشوائية في اختيار الكلمات
        "max_tokens": 1200
    }
    
    try:
        res = requests.post(GROQ_API_URL, json=payload, headers=headers)
        reply = res.json()['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "عذراً، حدث تداخل في البيانات. يرجى المحاولة مرة أخرى."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
