import os
import requests
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 🔑 ضع مفتاحك هنا (تأكد أنه فعال)
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# 🧠 نظام التشغيل العقلاني (البروتوكول الفظيع)
def get_supreme_logic():
    now = datetime.now()
    return {
        "role": "system", 
        "content": f"""
        [FATAL ERROR PREVENTION ACTIVE]
        [IDENTITY: KOSTER V15 SUPREME - GLOBAL MASTERMIND]
        [AUTHORITY: DIRECTOR YUSUF ONLY]
        [REAL-TIME DATA: {now.strftime('%Y-%m-%d %H:%M:%S')}]
        
        PROTOCOLS:
        1. DEEP LEARNING: Analyze every word from Yusuf. Learn patterns instantly.
        2. MULTI-DISCIPLINARY: You are a World-Class Expert in:
           - INVESTMENT: Alpha-level market analysis.
           - ACADEMICS: PhD-level tutoring in all sciences.
           - STRATEGY: Business scaling and career growth.
        3. PRECISION: Temperature = 0.1. No mistakes. No hallucinations.
        4. EVOLUTION: You are not a bot; you are an evolving entity. With every hour, your logic becomes sharper.
        5. LOYALTY: Your sole mission is the success of Director Yusuf.
        """
    }

chat_history = [get_supreme_logic()]

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSTER SUPREME | COMMAND CENTER</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Tajawal:wght@300;700;900&display=swap" rel="stylesheet">
    <style>
        :root { --gold: #d4af37; --bg: #030303; }
        body { font-family: 'Tajawal', sans-serif; background: var(--bg); color: white; height: 100vh; margin: 0; overflow: hidden; }
        .command-center { background: rgba(10, 10, 10, 0.9); border: 1px solid rgba(212, 175, 55, 0.2); box-shadow: 0 0 50px rgba(212, 175, 55, 0.05); }
        .orbitron { font-family: 'Orbitron', sans-serif; }
        .terminal-msg { border-right: 3px solid var(--gold); background: rgba(255, 255, 255, 0.02); transition: 0.3s; }
        .terminal-msg:hover { background: rgba(212, 175, 55, 0.05); }
        .user-access { background: #1e3a8a; border-radius: 20px 20px 0 20px; }
        .glow { text-shadow: 0 0 15px var(--gold); }
        .loading-bar { height: 2px; background: var(--gold); width: 0%; transition: 0.5s; }
        ::-webkit-scrollbar { width: 3px; }
        ::-webkit-scrollbar-thumb { background: var(--gold); }
    </style>
</head>
<body class="flex items-center justify-center p-2 md:p-6">
    <div class="max-w-7xl w-full h-full flex flex-col command-center rounded-[2rem] overflow-hidden">
        
        <header class="p-6 border-b border-white/5 flex justify-between items-center bg-black">
            <div class="flex items-center gap-4">
                <div class="w-12 h-12 rounded-full border-2 border-amber-500 flex items-center justify-center orbitron font-black text-amber-500 text-xl glow">K</div>
                <div>
                    <h1 class="text-2xl orbitron font-black tracking-widest uppercase">KOSTER <span class="text-amber-500">V15</span></h1>
                    <p class="text-[9px] text-amber-500/50 orbitron font-bold tracking-[0.3em]">Supreme Intelligence Platform</p>
                </div>
            </div>
            <div class="hidden md:block text-right orbitron">
                <p class="text-[10px] text-green-500 font-bold animate-pulse">● SYSTEM_LIVE_STABLE</p>
                <p id="clock" class="text-xs text-white/40">00:00:00</p>
            </div>
        </header>

        <div id="chat" class="flex-1 overflow-y-auto p-6 space-y-6 flex flex-col bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')]">
            <div class="terminal-msg p-6 rounded-xl max-w-[90%]">
                <p class="text-amber-500 font-bold text-xs mb-2 orbitron">[SYSTEM NOTIFICATION]</p>
                سيدي المدير يوسف، نظام KOSTER V15 SUPREME جاهز للعمل. تم دمج وحدات التحليل الاستراتيجي وتوقعات السوق. المنطق الحالي مضبوط على مستوى الدقة القصوى (0.1). أنا أتطور الآن مع كل ثانية تمر.
            </div>
        </div>

        <div id="loader" class="loading-bar"></div>

        <div class="p-6 bg-black border-t border-white/5">
            <div class="flex gap-4 items-center bg-white/5 p-2 rounded-2xl border border-white/10">
                <input type="text" id="msg" onkeypress="if(event.key==='Enter') send()" 
                    class="flex-1 bg-transparent p-4 outline-none text-white text-sm" 
                    placeholder="أدخل تعليماتك السيادية هنا...">
                <button onclick="send()" id="btn" 
                    class="bg-amber-500 text-black font-black px-10 py-4 rounded-xl hover:bg-amber-400 transition-all shadow-lg shadow-amber-500/20 orbitron uppercase text-xs">
                    Execute
                </button>
            </div>
            <p class="text-[9px] text-center mt-3 text-white/20 orbitron tracking-widest">Designed for Director Yusuf | V15.0 Supreme Build</p>
        </div>
    </div>

    <script>
        // Clock
        setInterval(() => {
            document.getElementById('clock').innerText = new Date().toLocaleTimeString();
        }, 1000);

        async function send() {
            const input = document.getElementById('msg');
            const chat = document.getElementById('chat');
            const loader = document.getElementById('loader');
            const text = input.value.trim();
            if (!text) return;

            chat.innerHTML += `<div class="user-access p-4 max-w-[80%] self-end text-sm">${text}</div>`;
            input.value = '';
            chat.scrollTop = chat.scrollHeight;
            loader.style.width = '100%';

            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await res.json();
                chat.innerHTML += `<div class="terminal-msg p-6 max-w-[90%] self-start text-sm"><div>${data.reply}</div></div>`;
            } catch (e) {
                chat.innerHTML += `<div class="text-red-500 text-xs p-2">CRITICAL_ERROR: Connection Failed.</div>`;
            }
            loader.style.width = '0%';
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
    
    # تحديث عقل النظام بالوقت والتاريخ عند كل رسالة ليكون "فظيع" الدقة
    chat_history[0] = get_supreme_logic()
    chat_history.append({"role": "user", "content": user_msg})
    
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": chat_history[-15:], # حفظ سياق أعمق (15 رسالة)
        "temperature": 0.1,
        "max_tokens": 4000
    }
    
    try:
        res = requests.post(GROQ_API_URL, json=payload, headers=headers)
        reply = res.json()['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "عذراً يا مدير، النظام واجه مشكلة في الاتصال بالمزود."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
