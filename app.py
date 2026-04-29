import os
import json
import requests
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DB_FILE = "koster_pro_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {"history": []}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)

db = load_db()

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSTER V15 PRO | RADAR MODE</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #010409; color: #c9d1d9; font-family: 'Segoe UI', sans-serif; height: 100vh; overflow: hidden; }
        .radar-panel { background: rgba(13, 17, 23, 0.9); border: 1px solid #30363d; border-radius: 15px; }
        .user-msg { background: #238636; color: white; padding: 12px; border-radius: 15px 15px 0 15px; align-self: flex-end; }
        .bot-msg { background: #161b22; border: 1px solid #30363d; padding: 12px; border-radius: 15px 15px 15px 0; align-self: flex-start; }
        .status-dot { width: 8px; height: 8px; background: #238636; border-radius: 50%; display: inline-block; animation: pulse 2s infinite; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    </style>
</head>
<body class="flex items-center justify-center p-2">
    <div class="max-w-5xl w-full h-[95vh] flex flex-col radar-panel p-4 shadow-2xl">
        <header class="flex justify-between items-center border-b border-gray-800 pb-3 mb-4">
            <div>
                <h1 class="text-xl font-black text-amber-500 tracking-tighter">KOSTER V15 PRO <span class="text-xs text-gray-500">v15.2.0</span></h1>
                <p id="location-status" class="text-[10px] text-gray-400">جاري تحديد الموقع...</p>
            </div>
            <div class="text-right text-[10px] font-mono">
                <div class="flex items-center gap-1"><span class="status-dot"></span> GPS LINKED</div>
                <div id="clock">00:00:00</div>
            </div>
        </header>

        <div id="chat" class="flex-1 overflow-y-auto space-y-4 flex flex-col p-2 custom-scroll"></div>

        <div class="mt-4 flex gap-2">
            <input type="text" id="msg" class="flex-1 bg-[#0d1117] border border-[#30363d] rounded-lg p-3 outline-none focus:border-amber-500" placeholder="أمرك مطاع يا مدير...">
            <button onclick="send()" id="btn" class="bg-amber-600 hover:bg-amber-500 text-black font-bold px-6 py-2 rounded-lg transition-all">إرسال</button>
        </div>
    </div>

    <script>
        let userLocation = "غير معروف";

        // وظيفة الـ GPS الحقيقية
        navigator.geolocation.getCurrentPosition((pos) => {
            userLocation = `Lat: ${pos.coords.latitude}, Lon: ${pos.coords.longitude}`;
            document.getElementById('location-status').innerText = `متصل: ${userLocation}`;
        }, () => {
            document.getElementById('location-status').innerText = "تم رفض إذن الموقع - الوضع اليدوي";
        });

        async function send() {
            const input = document.getElementById('msg');
            const chat = document.getElementById('chat');
            if (!input.value.trim()) return;

            const text = input.value;
            chat.innerHTML += `<div class="user-msg">${text}</div>`;
            input.value = '';
            chat.scrollTop = chat.scrollHeight;

            const res = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: text, location: userLocation})
            });
            const data = await res.json();
            chat.innerHTML += `<div class="bot-msg">${data.reply}</div>`;
            chat.scrollTop = chat.scrollHeight;
        }

        setInterval(() => {
            document.getElementById('clock').innerText = new Date().toLocaleTimeString();
        }, 1000);
    </script>
</body>
</html>
'''

@app.route('/')
def home(): return render_template_string(HTML_PAGE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get("message")
    user_loc = data.get("location")
    
    # 📝 نظام الوعي الكامل (الزمان، المكان، الهوية)
    now = datetime.now()
    system_instruction = (
        f"You are KOSTER V15 PRO. A high-intelligence AI Agent. "
        f"CONTEXT: Current Time: {now.strftime('%Y-%m-%d %H:%M:%S')}. "
        f"USER LOCATION: {user_loc}. "
        f"IDENTITY: Talking to Director Yusuf. "
        f"STRICT RULE: Be sharp, rational, and speak ONLY Arabic. "
        f"If the user asks where they are, use the location coordinates provided."
    )

    messages = [{"role": "system", "content": system_instruction}]
    # دمج الذاكرة الدائمة
    for m in db["history"][-20:]: # آخر 20 رسالة لسرعة الاستجابة
        messages.append(m)
    messages.append({"role": "user", "content": user_msg})

    try:
        res = requests.post(GROQ_API_URL, json={
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "temperature": 0.2 # خفض الحرارة لأقصى درجة من العقلانية
        }, headers={"Authorization": f"Bearer {GROQ_API_KEY}"})
        
        reply = res.json()['choices'][0]['message']['content']
        db["history"].append({"role": "user", "content": user_msg})
        db["history"].append({"role": "assistant", "content": reply})
        save_db(db)
        
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "خطأ في الرادار التكتيكي."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
