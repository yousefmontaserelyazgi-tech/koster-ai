import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# 🔑 ضع مفتاحك السري هنا مباشرة بين علامتي التنصيص لضمان العمل 100%
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# 🧠 ذاكرة KOSTER الاحترافية
chat_history = [
    {
        "role": "system", 
        "content": "أنت KOSTER V15 PRO، مساعد ذكي وقوي جداً. أنت تتقن كل لغات العالم وترد دائماً بلغة المستخدم. هدفك تنفيذ أوامر المدير يوسف بدقة مذهلة."
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
        body { background: #020617; color: #f8fafc; font-family: sans-serif; height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; }
        .chat-container { width: 100%; max-width: 500px; height: 90vh; background: #0f172a; border: 1px solid #1e293b; border-radius: 20px; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
        .header { padding: 20px; background: #1e293b; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }
        .messages { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; }
        .user-bubble { background: #3b82f6; padding: 12px 16px; border-radius: 15px 15px 0 15px; align-self: flex-end; max-width: 80%; }
        .bot-bubble { background: #334155; padding: 12px 16px; border-radius: 15px 15px 15px 0; align-self: flex-start; max-width: 80%; border-right: 4px solid #f59e0b; }
        .input-area { padding: 20px; background: #0f172a; border-top: 1px solid #1e293b; display: flex; gap: 10px; }
        input { flex: 1; background: #1e293b; border: none; padding: 12px; border-radius: 10px; color: white; outline: none; }
        button { background: #f59e0b; color: black; font-weight: bold; padding: 0 20px; border-radius: 10px; transition: 0.3s; }
        button:hover { background: #fbbf24; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">
            <span style="color: #f59e0b; font-weight: bold; font-size: 1.2rem;">KOSTER V15 PRO</span>
            <span style="color: #22c55e; font-size: 0.8rem;">● متصل</span>
        </div>
        <div id="chat" class="messages">
            <div class="bot-bubble">أهلاً بك أيها المدير يوسف. أنا نظام KOSTER، جاهز تماماً لتنفيذ أي أمر تطلبه مني وبأي لغة.</div>
        </div>
        <div class="input-area">
            <input type="text" id="msg" onkeypress="if(event.key==='Enter') send()" placeholder="أمرك مطاع يا مدير...">
            <button onclick="send()">إرسال</button>
        </div>
    </div>

    <script>
        async function send() {
            const input = document.getElementById('msg');
            const chat = document.getElementById('chat');
            const text = input.value.trim();
            if (!text) return;

            chat.innerHTML += `<div class="user-bubble">${text}</div>`;
            input.value = '';
            chat.scrollTop = chat.scrollHeight;

            const response = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: text})
            });
            const data = await response.json();
            chat.innerHTML += `<div class="bot-bubble">${data.reply}</div>`;
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
        reply = res.json()['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "عذراً يا مدير، تأكد من وضع مفتاح جروك الصحيح داخل الكود."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
