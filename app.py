import os
import json
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# --- الإعدادات الأساسية ---
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DB_FILE = "koster_db.json"

# --- دالات إدارة الذاكرة (قاعدة البيانات) ---
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "chat_history": [
            {
                "role": "system", 
                "content": "You are KOSTER V15 PRO. A high-end AI system. Rule: Speak ONLY in Arabic. Be rational and precise. Never mix languages."
            }
        ]
    }

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# تحميل الذاكرة عند بدء التشغيل
database = load_data()

# --- واجهة المستخدم (HTML/JS) ---
HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSTER V15 PRO | نظام متكامل</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #020617; color: white; font-family: 'Segoe UI', Tahoma, sans-serif; height: 100vh; margin: 0; overflow: hidden; }
        .glass { background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; }
        .user-msg { background: #2563eb; padding: 12px; border-radius: 15px 15px 0 15px; align-self: flex-end; max-width: 80%; }
        .bot-msg { background: #1e293b; border-right: 4px solid #f59e0b; padding: 12px; border-radius: 15px 15px 15px 0; align-self: flex-start; max-width: 80%; }
        .custom-scroll::-webkit-scrollbar { width: 4px; }
        .custom-scroll::-webkit-scrollbar-thumb { background: #f59e0b; border-radius: 10px; }
    </style>
</head>
<body class="flex items-center justify-center p-4">
    <div class="max-w-4xl w-full h-[95vh] flex flex-col glass p-6 shadow-2xl relative">
        <header class="pb-4 border-b border-white/10 mb-4 flex justify-between items-center">
            <div>
                <h1 class="text-2xl font-bold text-amber-500">KOSTER V15 PRO</h1>
                <p class="text-xs text-gray-400">نظام الذاكرة الدائمة النشط</p>
            </div>
            <button onclick="clearChat()" class="text-xs bg-red-900/30 hover:bg-red-600 p-2 rounded text-red-400 hover:text-white transition-all">تصفير الذاكرة</button>
        </header>
        
        <div id="chat" class="flex-1 overflow-y-auto space-y-4 flex flex-col pr-2 custom-scroll">
            </div>

        <div class="mt-4 flex gap-2 bg-slate-900 p-2 rounded-xl border border-white/5 shadow-inner">
            <input type="text" id="msg" class="flex-1 bg-transparent outline-none p-3 text-white" placeholder="أدخل أمرك يا مدير...">
            <button onclick="send()" id="btn" class="bg-amber-500 text-black px-8 py-2 rounded-lg font-black hover:bg-amber-400 active:scale-95 transition-all">إرسال</button>
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
                chat.innerHTML += `<div class="bot-msg text-red-400">خطأ في الاتصال.</div>`;
            }
            btn.disabled = false;
            chat.scrollTop = chat.scrollHeight;
        }

        async function clearChat() {
            if(confirm("هل تريد مسح ذاكرة النظام بالكامل؟")) {
                await fetch('/clear', {method: 'POST'});
                location.reload();
            }
        }

        // تحميل المحادثات السابقة عند فتح الصفحة
        window.onload = async () => {
            const res = await fetch('/history');
            const data = await res.json();
            const chat = document.getElementById('chat');
            data.forEach(m => {
                if(m.role !== 'system') {
                    const cls = m.role === 'user' ? 'user-msg' : 'bot-msg';
                    chat.innerHTML += `<div class="${cls}">${m.content}</div>`;
                }
            });
            chat.scrollTop = chat.scrollHeight;
        };

        document.getElementById('msg').addEventListener('keypress', (e) => { if(e.key==='Enter') send(); });
    </script>
</body>
</html>
'''

# --- مسارات Flask ---

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/history')
def get_history():
    return jsonify(database["chat_history"])

@app.route('/clear', methods=['POST'])
def clear_history():
    global database
    database = {
        "chat_history": [
            {"role": "system", "content": "You are KOSTER V15 PRO. Speak ONLY in Arabic. Be rational."}
        ]
    }
    save_data(database)
    return jsonify({"status": "success"})

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message")
    database["chat_history"].append({"role": "user", "content": user_msg})
    
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": database["chat_history"],
        "temperature": 0.3, # 🧠 عقلانية قصوى
        "max_tokens": 1000
    }
    
    try:
        res = requests.post(GROQ_API_URL, json=payload, headers=headers)
        reply = res.json()['choices'][0]['message']['content']
        database["chat_history"].append({"role": "assistant", "content": reply})
        
        # حفظ كل شيء فوراً في قاعدة البيانات
        save_data(database)
        
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "عذراً يا مدير يوسف، حدث خطأ في معالجة البيانات."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
