import os, json, requests
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 🔑 الإعدادات الأساسية
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MEMORY_FILE = "koster_elite_brain.json"

def get_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {"data": []}

def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

memory = get_memory()

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSTER V15 | GLOBAL ELITE</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #050505; color: #d4af37; font-family: 'Times New Roman', serif; height: 100vh; overflow: hidden; }
        .gold-border { border: 1px solid #d4af37; box-shadow: 0 0 30px rgba(212, 175, 55, 0.1); }
        .user-bubble { background: #1a1a1a; color: #fff; padding: 15px; border-radius: 10px; border-left: 3px solid #d4af37; margin-bottom: 15px; width: fit-content; max-width: 80%; align-self: flex-end; }
        .bot-bubble { background: #000; color: #d4af37; padding: 15px; border-radius: 10px; border-right: 3px solid #d4af37; margin-bottom: 15px; width: fit-content; max-width: 80%; align-self: flex-start; font-size: 1.1rem; }
        .luxury-btn { background: linear-gradient(45deg, #d4af37, #f9f295, #d4af37); color: #000; font-weight: 900; transition: 0.3s; }
        .luxury-btn:hover { transform: scale(1.05); filter: brightness(1.2); }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-thumb { background: #d4af37; }
    </style>
</head>
<body class="flex items-center justify-center p-4">
    <div class="max-w-6xl w-full h-[92vh] flex flex-col gold-border bg-[#0a0a0a] p-8 rounded-sm relative">
        <header class="border-b border-gray-800 pb-6 mb-6 flex justify-between items-baseline">
            <div>
                <h1 class="text-3xl font-serif tracking-[0.2em] text-[#d4af37]">KOSTER V15 PRO</h1>
                <p class="text-[10px] uppercase tracking-widest text-gray-500">Global Strategic Intelligence System</p>
            </div>
            <div class="text-right font-mono text-xs text-gray-600">
                <p id="date">--/--/--</p>
                <p class="text-[#d4af37]">ACCESS: LEVEL 10 (DIRECTOR YUSUF)</p>
            </div>
        </header>

        <div id="display" class="flex-1 overflow-y-auto flex flex-col space-y-4 pr-4">
            <div class="bot-bubble">نظام KOSTER مفعّل بالكامل. في انتظار توجيهاتك الاستراتيجية يا مدير يوسف.</div>
        </div>

        <div class="mt-8 flex gap-4">
            <input type="text" id="query" class="flex-1 bg-transparent border-b border-gray-700 outline-none p-2 text-white text-lg placeholder-gray-800" placeholder="اكتب أمرك التنفيذي هنا...">
            <button onclick="execute()" id="btn" class="luxury-btn px-12 py-3 uppercase text-sm tracking-widest">إرسال</button>
        </div>
    </div>

    <script>
        async function execute() {
            const input = document.getElementById('query');
            const display = document.getElementById('display');
            const btn = document.getElementById('btn');
            if(!input.value.trim() || btn.disabled) return;

            const val = input.value;
            display.innerHTML += `<div class="user-bubble">${val}</div>`;
            input.value = '';
            btn.disabled = true;
            display.scrollTop = display.scrollHeight;

            const response = await fetch('/process', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt: val})
            });
            const data = await response.json();
            display.innerHTML += `<div class="bot-bubble">${data.result}</div>`;
            btn.disabled = false;
            display.scrollTop = display.scrollHeight;
        }

        document.getElementById('date').innerText = new Date().toLocaleDateString('en-GB');
        document.getElementById('query').addEventListener('keypress', (e) => { if(e.key==='Enter') execute(); });
    </script>
</body>
</html>
'''

@app.route('/')
def main(): return render_template_string(HTML_PAGE)

@app.route('/process', methods=['POST'])
def process():
    user_query = request.json.get("prompt")
    
    # 🏦 بروتوكول النخبة
    elite_prompt = (
        "You are the KOSTER V15 PRO Global Intelligence. "
        "User: Director Yusuf (The Owner). "
        "Tone: Highly sophisticated, professional, and world-class. "
        "STRICT PROTOCOL: Respond only in formal Arabic. No casual talk. No mixed languages. "
        "Provide insights worthy of a billion-dollar company. Be brief but extremely powerful."
    )

    history = memory["data"][-15:]
    
    try:
        r = requests.post(GROQ_API_URL, json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": elite_prompt}] + history + [{"role": "user", "content": user_query}],
            "temperature": 0.1
        }, headers={"Authorization": f"Bearer {GROQ_API_KEY}"})
        
        output = r.json()['choices'][0]['message']['content']
        memory["data"].append({"role": "user", "content": user_query})
        memory["data"].append({"role": "assistant", "content": output})
        save_memory(memory)
        
        return jsonify({"result": output})
    except:
        return jsonify({"result": "عذراً، حدث خطأ في النظام السيادي."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
