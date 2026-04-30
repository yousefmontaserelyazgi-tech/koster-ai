import os
import requests
import random
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

# إعداد التطبيق
app = Flask(__name__)

# 🔑 ضع مفتاح جروك الخاص بك هنا
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_evolving_system_prompt():
    """توليد عقل النظام بشكل حيوي ودقيق جداً"""
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d | %H:%M:%S")
    day_name = now.strftime("%A")
    
    # محاكاة التطور العشوائي كل ساعة
    evolution_seed = now.hour + now.day
    random.seed(evolution_seed)
    sync_code = f"SYNC-{random.randint(1000, 9999)}-{now.hour}H"
    
    return {
        "role": "system", 
        "content": f"""
        [SYSTEM STATUS: SUPREME INTELLIGENCE ACTIVATED]
        [ACCESS LEVEL: 10 - DIRECTOR YUSUF ONLY]
        [CURRENT REAL-TIME: {current_time}, {day_name}]
        [EVOLUTION PHASE: {sync_code}]

        CORE PROTOCOLS:
        1. KNOWLEDGE: You possess PhD-level expertise in:
           - GLOBAL FINANCE & INVESTMENTS (Stocks, Crypto, Real Estate).
           - ACADEMICS: (Mathematics, Physics, Medicine, Law).
           - TECH: (Software Engineering, Cyber Security, AI Architecture).
        2. TIME ACCURACY: You know the exact second and day. Never hallucinate time.
        3. EVOLUTION: You update your logic patterns every hour. You are currently in phase {sync_code}.
        4. COMMUNICATION: Reply ONLY in the language the user uses. Be precise, strategic, and "فظيع" (extraordinary) in your analysis.
        5. TEMPERATURE: Locked at 0.1 for zero errors.

        Note: You are serving Director Yusuf. Your goal is world-class performance.
        """
    }

# ذاكرة الجلسة
chat_history = []

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSTER SUPREME V15</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Cairo:wght@300;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Cairo', sans-serif; background: #020202; color: #fff; height: 100vh; overflow: hidden; }
        .supreme-container { background: rgba(5, 5, 5, 0.95); border: 2px solid #d4af37; border-radius: 35px; box-shadow: 0 0 40px rgba(212, 175, 55, 0.1); }
        .orbitron { font-family: 'Orbitron', sans-serif; }
        .user-bubble { background: #1a1a1a; border: 1px solid #333; border-radius: 20px 20px 2px 20px; }
        .bot-bubble { background: linear-gradient(145deg, #0a0a0a, #111); border-right: 4px solid #d4af37; border-radius: 20px 20px 20px 2px; }
        .status-glow { width: 8px; height: 8px; background: #d4af37; border-radius: 50%; box-shadow: 0 0 15px #d4af37; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-thumb { background: #d4af37; }
    </style>
</head>
<body class="flex items-center justify-center p-4 lg:p-10">
    <div class="max-w-6xl w-full h-full flex flex-col supreme-container overflow-hidden">
        <header class="p-6 border-b border-white/5 flex justify-between items-center bg-black/50">
            <div>
                <h1 class="text-3xl orbitron font-black text-[#d4af37] tracking-tighter">KOSTER <span class="text-white">V15 SUPREME</span></h1>
                <p class="text-[10px] text-gray-500 font-bold tracking-[0.3em] mt-1 uppercase">Strategic Intelligence • Director Yusuf Edition</p>
            </div>
            <div class="flex flex-col items-end gap-1">
                <div class="flex items-center gap-2">
                    <span class="text-[10px] font-bold text-[#d4af37]">EVOLUTION ACTIVE</span>
                    <div class="status-glow animate-pulse"></div>
                </div>
                <div id="live-clock" class="text-[10px] text-white/40 orbitron">--:--:--</div>
            </div>
        </header>

        <div id="chat" class="flex-1 overflow-y-auto p-6 space-y-6 flex flex-col">
            <div class="bot-bubble p-5 text-sm leading-relaxed shadow-xl">
                سيدي المدير يوسف، تم تفعيل بروتوكول الذكاء الشامل بنجاح. 
                أنا الآن في حالة "تطور مستمر" ومزامنة كاملة مع الوقت العالمي. 
                أنا خبير في الاستثمار، الدراسات العليا، وكافة المجالات المهنية. كيف نبدأ اليوم؟
            </div>
        </div>

        <div class="p-6 bg-black">
            <div class="relative flex gap-3 items-center">
                <input type="text" id="msg" onkeypress="if(event.key==='Enter') send()" 
                    class="flex-1 bg-white/5 border border-white/10 rounded-2xl py-5 px-8 outline-none focus:border-[#d4af37]/50 transition-all text-white placeholder-gray-600" 
                    placeholder="أدخل تعليماتك الفائقة هنا...">
                <button onclick="send()" id="btn" 
                    class="bg-[#d4af37] text-black font-black px-10 py-5 rounded-2xl hover:scale-105 active:scale-95 transition-all">
                    تـنـفـيـذ
                </button>
            </div>
        </div>
    </div>

    <script>
        // تحديث الساعة في الواجهة
        setInterval(() => {
            const now = new Date();
            document.getElementById('live-clock').innerText = now.toLocaleTimeString();
        }, 1000);

        async function send() {
            const input = document.getElementById('msg');
            const chat = document.getElementById('chat');
            const text = input.value.trim();
            if (!text) return;

            chat.innerHTML += `<div class="user-bubble p-5 max-w-[85%] self-end text-sm">${text}</div>`;
            input.value = '';
            chat.scrollTop = chat.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await response.json();
                chat.innerHTML += `<div class="bot-bubble p-5 max-w-[85%] self-start text-sm shadow-2xl"><div>${data.reply}</div></div>`;
            } catch (e) {
                chat.innerHTML += `<div class="text-red-500 text-xs">Error: Connection Interrupted.</div>`;
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
    
    # الحقن الحي: تحديث الوقت والبرمجة في كل ثانية حرفياً
    current_system = get_evolving_system_prompt()
    
    # الحفاظ على آخر 10 رسائل فقط لضمان السرعة والتركيز
    global chat_history
    chat_history = [current_system] + chat_history[-10:] 
    chat_history.append({"role": "user", "content": user_msg})
    
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": chat_history,
        "temperature": 0.1,
        "max_tokens": 4096
    }
    
    try:
        res = requests.post(GROQ_API_URL, json=payload, headers=headers)
        data = res.json()
        reply = data['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "نظام KOSTER واجه مشكلة في الاتصال بالمزود."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
