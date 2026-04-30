import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# 🔑 السطر الأهم: ضع مفتاح جروك (gsk_...) هنا مباشرة بين علامتي التنصيص
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# 🧠 ذاكرة النظام: برمجناه ليفهم كل لغات العالم ويرد فوراً بنفس لغة المستخدم
chat_history = [
    {
        "role": "system", 
        "content": "You are KOSTER V15 PRO, a professional global AI. You must detect the user's language and respond ONLY in that same language. Be highly professional and execute Director Yousef's orders perfectly."
    }
]

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSTER V15 PRO | المدير يوسف</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #020617; color: #e2e8f0; font-family: 'Segoe UI', sans-serif; height: 100vh; margin: 0; }
        .glass-panel { background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 24px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); }
        .user-msg { background: #2563eb; color: white; border-radius: 20px 20px 0 20px; padding: 14px 18px; align-self: flex-end; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2); }
        .bot-msg { background: #1e293b; border-right: 4px solid #f59e0b; border-radius: 20px 20px 20px 0; padding: 14px 18px; align-self: flex-start; line-height: 1.6; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
    </style>
</head>
<body class="flex items-center justify-center p-4">
    <div class="max-w-4xl w-full h-[92vh] flex flex-col glass-panel overflow-hidden">
        <header class="p-6 bg-black/20 border-b border-white/5 flex justify-between items-center">
            <div>
                <h1 class="text-2xl font-black text-amber-500 tracking-tighter">KOSTER <span class="text-white">V15 PRO</span></h1>
                <p class="text-[10px] text-gray-500 uppercase tracking-widest mt-1">نظام الإدارة العالمية للمدير يوسف</p>
            </div>
            <div class="flex items-center gap-2 bg-green-500/10 px-3 py-1 rounded-full border border-green-500/20">
                <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                <span class="text-[10px] text-green-500 font-bold">ONLINE</span>
            </div>
        </header>

        <div id="chat" class="flex-1 overflow-y-auto p-6 space-y-6 flex flex-col">
            <div class="bot-msg">أهلاً بك أيها المدير يوسف. أنا نظام KOSTER، جاهز تماماً لتنفيذ أوامرك بكل لغات العالم وبدقة تامة. ما هي تعليماتك القادمة؟</div>
        </div>

        <div class="p-6 bg-black/40 border-t border-white/5">
            <div class="flex gap-3 bg-slate-900/50 p-2 rounded-2xl border border-white/10">
                <input type="text" id="msg" onkeypress="if(event.key==='Enter') send()" class="flex-1 bg-transparent p-3 outline-none text-white text-sm" placeholder="اكتب أمرك هنا يا مدير...">
                <button onclick="send()" id="btn" class="bg-gradient-to-r from-amber-500 to-orange-600 text-black px-8 rounded-xl font-bold hover:scale-105 active:scale-95 transition-all">إرسال</button>
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
            chat.scrollTop = chat.scrollHeight;
            btn.disabled = true;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await response.json();
                chat.innerHTML += `<div class="bot-msg">${data.reply}</div>`;
            } catch (e) {
                chat.innerHTML += `<div class="bot-msg text-red-400">خطأ في الاتصال: تأكد من مفتاح جروك الخاص بك.</div>`;
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
    
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "llama-3.3-70b-versatile", "messages": chat_history}
    
    try:
        res = requests.post(GROQ_API_URL, json=payload, headers=headers)
        if res.status_code != 200:
            return jsonify({"reply": "عذراً يا مدير، يبدو أن مفتاح جروك يحتاج للتجديد أو أنه غير صحيح."})
        reply = res.json()['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "نظام KOSTER واجه تضارباً تقنياً، يرجى المحاولة مرة أخرى."})

if __name__ == '__main__':
    # Render يستخدم المنفذ 10000 افتراضياً
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
