import os
from flask import Flask, render_template_string, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# 🔑 ضع مفتاح جروك الحقيقي هنا
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_supreme_prompt():
    now = datetime.now()
    time_info = now.strftime("%Y-%m-%d | %I:%M %p")
    day_info = now.strftime("%A")
    
    return {
        "role": "system", 
        "content": f"""
        IDENTITY: You are KOSTER V15 PRO - SUPREME STRATEGIC INTELLIGENCE.
        ACCESS LEVEL: 10 (DIRECTOR YUSUF ONLY).
        CURRENT TIME: {time_info}, {day_info}.
        
        CORE CAPABILITIES:
        1. INVESTMENT & FINANCE: Expert in global markets, crypto, and asset management.
        2. ACADEMICS: Deep knowledge in STEM, Medicine, Law, and Philosophy.
        3. CAREER: Professional advisor for business scaling and corporate strategy.
        4. GENERAL KNOWLEDGE: Real-time awareness of global events.
        
        STRICT OPERATING RULES:
        - Temperature: 0.1 (Precision focus. No hallucinations).
        - Multi-lingual: Detect user language instantly and reply perfectly.
        - Tone: Highly professional, analytical, and direct.
        - You never fail a logic test. You provide numbers, dates, and facts based on your massive training data.
        """
    }

# تهيئة الذاكرة
chat_history = [get_supreme_prompt()]

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSTER SUPREME | DIRECTOR YUSUF</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Noto+Sans+Arabic:wght@300;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans Arabic', sans-serif; background: #050505; color: #d4af37; height: 100vh; overflow: hidden; }
        .gold-border { border: 1px solid rgba(212, 175, 55, 0.3); }
        .director-panel { background: rgba(10, 10, 10, 0.95); border-radius: 40px; box-shadow: 0 0 100px rgba(212, 175, 55, 0.05); }
        .user-msg { background: #1a1a1a; color: #fff; border-radius: 25px 25px 5px 25px; border: 1px solid rgba(255,255,255,0.1); }
        .bot-msg { background: rgba(212, 175, 55, 0.05); border-right: 5px solid #d4af37; border-radius: 25px 25px 25px 5px; color: #f0f0f0; }
        .cinzel { font-family: 'Cinzel', serif; }
        .glitch-text { animation: pulse 2s infinite; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
    </style>
</head>
<body class="flex items-center justify-center p-6 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-zinc-900 via-black to-black">
    <div class="max-w-6xl w-full h-[95vh] flex flex-col director-panel gold-border relative overflow-hidden">
        
        <header class="p-8 border-b border-white/5 flex justify-between items-end">
            <div>
                <h1 class="text-4xl cinzel font-bold text-[#d4af37] tracking-widest glitch-text">KOSTER V15 PRO</h1>
                <p class="text-[11px] text-gray-500 uppercase tracking-[0.5em] mt-2 font-bold">ACCESS: LEVEL 10 (DIRECTOR YUSUF)</p>
            </div>
            <div class="text-right">
                <p class="text-[#d4af37] text-xs font-bold uppercase">Strategic Intelligence System</p>
                <p class="text-white/20 text-[10px] mt-1 italic">V15.0_SUPREME_BUILD</p>
            </div>
        </header>

        <div id="chat" class="flex-1 overflow-y-auto p-10 space-y-8 flex flex-col custom-scroll">
            <div class="bot-msg p-6 border border-amber-900/20">
                سيدي المدير يوسف، تم تفعيل مستوى الوصول العاشر. أنا الآن في كامل قواي الاستراتيجية والتحليلية. 
                لقد ضبطت منطقي على درجة 0.1 لضمان دقة معلوماتية مطلقة في الاستثمار، الدراسة، والعمل. 
                أنا جاهز لأي اختبار حقيقي الآن.
            </div>
        </div>

        <div class="p-8 bg-black/50 border-t border-white/5">
            <div class="flex gap-4">
                <input type="text" id="msg" onkeypress="if(event.key==='Enter') send()" 
                    class="flex-1 bg-white/5 border gold-border rounded-full px-8 py-5 outline-none focus:bg-white/10 transition-all text-white" 
                    placeholder="أدخل أمرك الاستراتيجي يا مدير...">
                <button onclick="send()" id="btn" 
                    class="bg-[#d4af37] text-black font-black px-12 rounded-full hover:scale-105 active:scale-95 transition-all shadow-lg shadow-amber-500/10">
                    تـنـفـيـذ
                </button>
            </div>
        </div>
    </div>

    <script>
        async function send() {
            const input = document.getElementById('msg');
            const chat = document.getElementById('chat');
            const text = input.value.trim();
            if (!text) return;

            chat.innerHTML += `<div class="user-msg p-5 max-w-[80%] self-end">${text}</div>`;
            input.value = '';
            chat.scrollTop = chat.scrollHeight;

            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await res.json();
                chat.innerHTML += `<div class="bot-msg p-5 max-w-[85%] self-start">${data.reply}</div>`;
            } catch (e) {
                chat.innerHTML += `<div class="text-red-500 font-bold p-4">خطأ في السيرفر الرئيسي.</div>`;
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
    
    # تحديث البيانات الزمنية والمهام في كل رسالة
    chat_history[0] = get_supreme_prompt()
    chat_history.append({"role": "user", "content": user_msg})
    
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": chat_history,
        "temperature": 0.1, # أعلى درجات الدقة والتركيز
        "top_p": 1
    }
    
    try:
        res = requests.post(GROQ_API_URL, json=payload, headers=headers)
        reply = res.json()['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "عذراً، نظام KOSTER يحتاج لإعادة ضبط المفتاح."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
