import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# 🔑 ضع مفتاح جروك الحقيقي هنا مباشرة بين علامتي التنصيص
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# 🧠 التعليمات السرية (بدون تعقيد لضمان عدم تضارب اللغات)
chat_history = [
    {
        "role": "system", 
        "content": "You are KOSTER V15 PRO. You are a world-class AI. Rule #1: Detect the user's language and reply ONLY in that language. Do not mix languages. Do not talk about your programming. Just answer the user's request professionally."
    }
]

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSTER V15 PRO</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #020617; color: white; font-family: 'Segoe UI', Tahoma, sans-serif; height: 100vh; margin: 0; overflow: hidden; }
        .glass { background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; }
        .user-msg { background: #2563eb; padding: 12px; border-radius: 15px 15px 0 15px; align-self: flex-end; max-width: 85%; }
        .bot-msg { background: #1e293b; border-right: 4px solid #f59e0b; padding: 12px; border-radius: 15px 15px 15px 0; align-self: flex-start; max-width: 85%; }
    </style>
</head>
<body class="flex items-center justify-center p-4">
    <div class="max-w-3xl w-full h-[90vh] flex flex-col glass p-4 shadow-2xl">
        <header class="pb-4 border-b border-white/10 mb-4 flex justify-between items-center">
            <h1 class="text-xl font-bold text-amber-500">KOSTER V15 PRO</h1>
            <span class="text-green-500 text-xs font-mono">● ONLINE SYSTEM</span>
        </header>
        
        <div id="chat" class="flex-1 overflow-y-auto space-y-4 flex flex-col pr-2 custom-scroll">
            <div class="bot-msg">أهلاً بك أيها المدير يوسف. أنا نظام KOSTER العالمي، جاهز لتنفيذ أوامرك بكل لغات العالم وبدقة تامة.</div>
        </div>

        <div class="mt-4 flex gap-2 bg-slate-900 p-2 rounded-xl border border-white/5">
            <input type="text" id="msg" onkeypress="if(event.key==='Enter') send()" class="flex-1 bg-transparent outline-none p-2 text-white" placeholder="أمرك مطاع يا مدير...">
            <button onclick="send()" id="btn" class="bg-amber-500 text-black px-6 py-2 rounded-lg font-bold hover:bg-amber-400 transition-all">إرسال</button>
        </div>
    </div>

    <script>
        async function send() {
            const input = document.getElementById('msg');
            const chat = document.getElementById('chat');
            const text = input.value.trim();
            if (!text) return;

            chat.innerHTML += `<div class="user-msg">${text}</div>`;
            input.value = '';
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
                chat.innerHTML += `<div class="bot-msg text-red-400">خطأ: تأكد من مفتاح الجروك (Groq Key).</div>`;
            }
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
    
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "llama-3.3-70b-versatile", "messages": chat_history}
    
    try:
        res = requests.post(GROQ_API_URL, json=payload, headers=headers)
        if res.status_code != 200:
            return jsonify({"reply": "المدير يوسف، يبدو أن مفتاح جروك غير مفعل أو فيه مشكلة."})
        reply = res.json()['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "عذراً، حدث خطأ تقني في الاتصال بالسيرفر."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
