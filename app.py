import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# 🔑 ضع مفتاحك السري هنا مباشرة لكي يعمل فوراً بدون مشاكل الرندر
# امسح كلمة YOUR_API_KEY_HERE وضع مفتاحك الذي يبدأ بـ gsk_ داخل علامات التنصيص
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# 🧠 عقل النظام (مخفي عن المستخدم، يفهم كل اللغات لكن لا يتكلم عنها)
chat_history = [
    {
        "role": "system", 
        "content": "أنت KOSTER V15 PRO، مساعد ذكي واحترافي. أجب دائماً بذكاء وبنفس اللغة التي يكلمك بها المستخدم. لا تتحدث أبداً عن قدراتك اللغوية، فقط أجب على السؤال مباشرة."
    }
]

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSTER V15 | Enterprise</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: radial-gradient(circle at center, #0f172a 0%, #020617 100%); color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; height: 100vh; margin: 0; overflow: hidden; }
        .glass { background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 24px; }
        .gold-text { background: linear-gradient(to right, #fbbf24, #d97706); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
        .user-msg { background: linear-gradient(135deg, #0ea5e9, #2563eb); color: white; border-radius: 20px 20px 0 20px; padding: 12px 18px; align-self: flex-end; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3); max-width: 80%; }
        .bot-msg { background: rgba(255, 255, 255, 0.05); border-right: 4px solid #fbbf24; border-radius: 20px 20px 20px 0; padding: 12px 18px; align-self: flex-start; max-width: 80%; line-height: 1.6; }
        .custom-scroll::-webkit-scrollbar { width: 5px; }
        .custom-scroll::-webkit-scrollbar-thumb { background: rgba(251, 191, 36, 0.3); border-radius: 10px; }
    </style>
</head>
<body class="flex items-center justify-center p-4">
    <div class="max-w-4xl w-full h-[90vh] flex flex-col glass shadow-2xl">
        <header class="p-5 border-b border-white/5 flex justify-between items-center bg-black/20 rounded-t-3xl">
            <div>
                <h1 class="text-2xl gold-text">KOSTER <span class="text-white">V15 PRO</span></h1>
            </div>
            <div class="flex items-center gap-2">
                <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                <span class="text-xs text-green-500 font-medium">متصل</span>
            </div>
        </header>

        <div id="chat" class="flex-1 overflow-y-auto p-6 space-y-6 flex flex-col custom-scroll">
            <div class="bot-msg">أهلاً بك أيها المدير يوسف. أنا نظام KOSTER، وجاهز لتنفيذ أوامرك فوراً.</div>
        </div>

        <div class="p-5 bg-black/30 border-t border-white/5 rounded-b-3xl">
            <div class="flex gap-3 bg-slate-900/50 p-2 rounded-2xl border border-white/10">
                <input type="text" id="msg" onkeypress="if(event.key==='Enter') send()" class="flex-1 bg-transparent p-3 outline-none text-white" placeholder="اكتب رسالتك هنا...">
                <button onclick="send()" id="btn" class="bg-gradient-to-r from-amber-500 to-orange-600 text-white px-8 rounded-xl font-bold transition-all">إرسال</button>
            </div>
        </div>
    </div>

    <script>
        async function send() {
            const input = document.getElementById('msg');
            const chat = document.getElementById('chat');
            const btn = document.getElementById('btn');
            const text = input.value.trim();
            if (!text) return;

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
                chat.innerHTML += `<div class="bot-msg text-red-400">عذراً، يوجد خطأ في الاتصال.</div>`;
            }
            btn.disabled = false;
            chat.scrollTop = chat.scrollHeight;
        }
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
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": chat_history
    }
    
    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        
        # التأكد من صحة الرد من المفتاح
        if response.status_code != 200:
            return jsonify({"reply": "عذراً أيها المدير، يبدو أن المفتاح السري غير صالح أو مفقود."})
            
        reply = response.json()['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "حدث خطأ داخلي، الرجاء التأكد من المفتاح."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
