import os
import json
import requests
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 🔑 ضع مفتاحك هنا
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DB_FILE = "koster_final_db.json"

# --- إدارة قاعدة البيانات ---
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"history": []}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

db = load_db()

# --- واجهة النظام الاحترافية ---
HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSTER V15 PRO | RADAR SYSTEM</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #010409; color: #e6edf3; font-family: 'Segoe UI', Tahoma, sans-serif; height: 100vh; margin: 0; overflow: hidden; }
        .radar-container { background: rgba(13, 17, 23, 0.95); border: 1px solid #30363d; border-radius: 20px; box-shadow: 0 0 20px rgba(0,0,0,0.5); }
        .user-msg { background: #238636; padding: 12px; border-radius: 15px 15px 0 15px; align-self: flex-end; max-width: 85%; }
        .bot-msg { background: #161b22; border: 1px solid #30363d; padding: 12px; border-radius: 15px 15px 15px 0; align-self: flex-start; max-width: 85%; border-right: 4px solid #d29922; }
        .custom-scroll::-webkit-scrollbar { width: 3px; }
        .custom-scroll::-webkit-scrollbar-thumb { background: #d29922; }
        .gps-active { color: #3fb950; font-family: monospace; font-size: 10px; }
    </style>
</head>
<body class="flex items-center justify-center p-3">
    <div class="max-w-5xl w-full h-[95vh] flex flex-col radar-container p-5 relative">
        <header class="flex justify-between items-center border-b border-gray-800 pb-4 mb-4">
            <div>
                <h1 class="text-2xl font-black text-amber-500 uppercase tracking-widest">KOSTER V15 PRO</h1>
                <div id="gps-display" class="gps-active">📡 جاري محاذاة الأقمار الصناعية...</div>
            </div>
            <div class="text-right">
                <div id="clock" class="text-xl font-mono text-gray-400">00:00:00</div>
                <button onclick="clearSystem()" class="text-[10px] text-red-500 hover:underline">تصفير النظام</button>
            </div>
        </header>
        
        <div id="chat" class="flex-1 overflow-y-auto space-y-4 flex flex-col pr-2 custom-scroll"></div>

        <div class="mt-4 flex gap-3 bg-[#0d1117] p-3 rounded-xl border border-gray-800 shadow-inner">
            <input type="text" id="msg" class="flex-1 bg-transparent outline-none text-white text-lg" placeholder="أدخل الأمر الاستراتيجي...">
            <button onclick="send()" id="btn" class="bg-amber-600 hover:bg-amber-500 text-black px-10 py-3 rounded-lg font-black transition-all">إرسال</button>
        </div>
    </div>

    <script>
        let currentGPS = "جاري التحديد...";

        // تفعيل الـ GPS الحقيقي
        navigator.geolocation.getCurrentPosition((p) => {
            currentGPS = `Lat: ${p.coords.latitude.toFixed(4)}, Lon: ${p.coords.longitude.toFixed(4)}`;
            document.getElementById('gps-display').innerText = `● GPS LOCKED: ${currentGPS}`;
        }, () => {
            currentGPS = "إذن الموقع مرفوض";
            document.getElementById('gps-display').innerText = "○ GPS OFFLINE (Manual Mode)";
        });

        async function send() {
            const input = document.getElementById('msg');
            const chat = document.getElementById('chat');
            const btn = document.getElementById('btn');
            const text = input.value.trim();
            if(!text || btn.disabled) return;

            chat.innerHTML += `<div class="user-msg">${text}</div>`;
            input.value = '';
            btn.disabled = true;
            chat.scrollTop = chat.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text, gps: currentGPS})
                });
                const data = await response.json();
                chat.innerHTML += `<div class="bot-msg">${data.reply}</div>`;
            } catch {
                chat.innerHTML += `<div class="bot-msg text-red-500">فشل في الاتصال بالقاعدة.</div>`;
            }
            btn.disabled = false;
            chat.scrollTop = chat.scrollHeight;
        }

        async function clearSystem() {
            if(confirm("سيتم محو جميع السجلات. هل أنت متأكد؟")) {
                await fetch('/clear', {method: 'POST'});
                location.reload();
            }
        }

        // تحميل التاريخ عند الفتح
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

        setInterval(() => { document.getElementById('clock').innerText = new Date().toLocaleTimeString(); }, 1000);
        document.getElementById('msg').addEventListener('keypress', (e) => { if(e.key==='Enter') send(); });
    </script>
</body>
</html>
'''

# --- المسارات البرمجية ---

@app.route('/')
def home(): return render_template_string(HTML_PAGE)

@app.route('/history')
def get_history(): return jsonify(db["history"])

@app.route('/clear', methods=['POST'])
def clear_db():
    db["history"] = []
    save_db(db)
    return jsonify({"status": "reset"})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get("message")
    gps_info = data.get("gps")
    
    # 📝 تحديث الوعي اللحظي للنظام
    now = datetime.now()
    system_prompt = (
        f"You are KOSTER V15 PRO. Director Yusuf is your commander. "
        f"TIME: {now.strftime('%Y-%m-%d %H:%M:%S')}. "
        f"LOCATION: {gps_info}. "
        f"RULE: Be extremely rational. Use ONLY Arabic. No English words allowed in Arabic text."
    )

    # بناء المحادثة
    messages = [{"role": "system", "content": system_prompt}]
    messages += db["history"][-15:] # ذاكرة لآخر 15 رسالة لضمان السرعة والدقة
    messages.append({"role": "user", "content": user_msg})

    try:
        res = requests.post(GROQ_API_URL, json={
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "temperature": 0.2, # 📉 عقلانية تامة لمنع الأخطاء اللغوية
            "max_tokens": 1000
        }, headers={"Authorization": f"Bearer {GROQ_API_KEY}"})
        
        reply = res.json()['choices'][0]['message']['content']
        
        # حفظ في القاعدة
        db["history"].append({"role": "user", "content": user_msg})
        db["history"].append({"role": "assistant", "content": reply})
        save_db(db)
        
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "عذراً يا مدير، السيرفر تحت ضغط كبير."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
        
