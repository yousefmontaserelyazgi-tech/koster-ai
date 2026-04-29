import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# 🔑 مفتاح جروك الخاص بك
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# 🧠 الذاكرة الكاملة (ستبقى مخزنة طوال فترة عمل السيرفر)
chat_history = [
    {
        "role": "system", 
        "content": (
            "You are KOSTER V15 PRO. A highly advanced AI. "
            "IMPORTANT: Keep track of everything discussed. "
            "LANGUAGE RULE: You must detect the user's language from the VERY LAST message "
            "and respond ONLY in that language. If the user writes in Arabic, "
            "do not use any English or Russian words. Stay professional."
        )
    }
]

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSTER V15 PRO | الذاكرة الكاملة</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #020617; color: white; font-family: 'Segoe UI', sans-serif; height: 100vh; margin: 0; overflow: hidden; }
        .glass { background: rgba(15, 23, 42, 0.95); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; }
        .user-msg { background: #1d4ed8; padding: 12px; border-radius: 15px 15px 0 15px; align-self: flex-end; max-width: 80%; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
        .bot-msg { background: #1e293b; border-right: 4px solid #f59e0b; padding: 12px; border-radius: 15px 15px 15px 0; align-self: flex-start; max-width: 80%; }
        .custom-scroll::-webkit-scrollbar { width: 6px; }
        .custom-scroll::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
    </style>
</head>
<body class="flex items-center justify-center p-4">
    <div class="max-w-4xl w-full h-[95vh] flex flex-col glass p-6 shadow-2xl">
        <header class="pb-4 border-b border-white/10 mb-4 flex justify-between items-center">
            <div>
                <h1 class="text-2xl font-bold text-amber-500">KOSTER V15 PRO</h1>
                <p class="text-gray-400 text-xs">نظام ذكاء اصطناعي بذاكرة مستمرة</p>
            </div>
            <div class="flex items-center gap-2">
                <span class="relative flex h-3 w-3">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                </span>
                <span class="text-green-500 font-mono text-sm">ACTIVE</span>
            </div>
        </header>
        
        <div id="chat" class="flex-1 overflow-y-auto space-y-4 flex flex-col pr-4 custom-scroll">
            <div class="bot-msg">أهلاً يا مدير يوسف. ذاكرتي جاهزة ولن أنسى أي شيء سنناقشه الآن. بمَ نبدأ؟</div>
        </div>

        <div class="mt-4 flex gap-3 bg-slate-900 p-3 rounded-2xl border border-white/10 shadow-inner">
            <input type="text" id="msg" class="flex-1 bg-transparent outline-none text-white placeholder-gray-500" placeholder="أدخل أوامرك هنا...">
            <button onclick="send()" id="btn" class="bg-amber-500 hover:bg-amber-400 text-black px-8 py-2 rounded-xl font-black transition-all transform active:scale-95">إرسال</button>
        </div>
    </div>

    <script>
        async function send() {
            const input = document.getElementById('msg');
            const chat = document.getElementById('chat');
            const btn = document.getElementById('btn');
            const text = input.value.trim();
            if (!text || btn.disabled) return;

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
                chat.innerHTML += `<div class="bot-msg text-red-400">خطأ في الاتصال بالسيرفر!</div>`;
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
    
    # 📝 تسجيل كل شيء في الذاكرة بدون حذف
    chat_history.append({"role": "user", "content": user_msg})
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": chat_history,
        "temperature": 0.6, # تقليل الحرارة قليلاً لزيادة الدقة اللغوية
        "top_p": 0.9
    }
    
    try:
        res = requests.post(GROQ_API_URL, json=payload, headers=headers)
        if res.status_code == 200:
            reply = res.json()['choices'][0]['message']['content']
            # 📝 إضافة رد البوت للذاكرة أيضاً
            chat_history.append({"role": "assistant", "content": reply})
            return jsonify({"reply": reply})
        else:
            return jsonify({"reply": "عذراً يا مدير، هناك مشكلة في الـ API Key."})
    except:
        return jsonify({"reply": "حدث خطأ فني، سأحاول تذكر ما قلته لاحقاً."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
