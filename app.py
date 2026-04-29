import os, json, requests
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 🔑 الإعدادات الأساسية
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MEMORY_FILE = "koster_brain.json"

def get_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {"long_term_memory": []}

def sync_brain(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

brain = get_brain()

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSTER | DEEPMIND SYSTEM</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #000; color: #00ff41; font-family: 'Courier New', monospace; height: 100vh; overflow: hidden; }
        .terminal { background: rgba(0, 15, 0, 0.9); border: 1px solid #00ff41; box-shadow: 0 0 15px #00ff41; border-radius: 5px; }
        .user-line { color: #fff; background: #003300; padding: 10px; border-radius: 5px; margin-bottom: 10px; border-right: 3px solid #00ff41; }
        .bot-line { color: #00ff41; padding: 10px; margin-bottom: 10px; border-right: 3px solid #ffaa00; }
        input { background: #000 !important; border: 1px solid #00ff41 !important; color: #00ff41 !important; }
        .scanline { width: 100%; height: 2px; background: rgba(0, 255, 65, 0.1); position: absolute; top: 0; animation: scan 4s linear infinite; }
        @keyframes scan { from { top: 0; } to { top: 100%; } }
    </style>
</head>
<body class="flex items-center justify-center p-2">
    <div class="scanline"></div>
    <div class="max-w-6xl w-full h-[95vh] flex flex-col terminal p-4 relative">
        <header class="border-b border-[#00ff41] pb-2 mb-4 flex justify-between">
            <div>
                <h1 class="text-xl font-bold">[ KOSTER_DEEPMIND_V15 ]</h1>
                <p id="gps" class="text-xs text-amber-500">INITIATING SATELLITE LINK...</p>
            </div>
            <div class="text-right text-xs">
                <p>STATUS: OPERATIONAL</p>
                <p id="timer">TIMESTAMP: --:--:--</p>
            </div>
        </header>

        <div id="console" class="flex-1 overflow-y-auto space-y-2 p-2 custom-scroll"></div>

        <div class="mt-4 flex gap-2">
            <span class="text-xl">>></span>
            <input type="text" id="input" class="flex-1 outline-none p-2" placeholder="أدخل البيانات للتحليل...">
            <button onclick="execute()" id="btn" class="bg-[#00ff41] text-black px-6 font-bold hover:bg-white transition-all">EXECUTE</button>
        </div>
    </div>

    <script>
        let loc = "LOCATING...";
        navigator.geolocation.getCurrentPosition(p => {
            loc = `LAT:${p.coords.latitude.toFixed(4)} LON:${p.coords.longitude.toFixed(4)}`;
            document.getElementById('gps').innerText = `SYSTEM_LOCATION: ${loc}`;
        });

        async function execute() {
            const cmd = document.getElementById('input');
            const consoleBox = document.getElementById('console');
            if(!cmd.value.trim()) return;

            consoleBox.innerHTML += `<div class="user-line"><strong>USER:</strong> ${cmd.value}</div>`;
            const userText = cmd.value;
            cmd.value = '';
            consoleBox.scrollTop = consoleBox.scrollHeight;

            const res = await fetch('/analyze', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt: userText, geo: loc})
            });
            const data = await res.json();
            consoleBox.innerHTML += `<div class="bot-line"><strong>KOSTER_CORE:</strong> ${data.output}</div>`;
            consoleBox.scrollTop = consoleBox.scrollHeight;
        }

        setInterval(() => { document.getElementById('timer').innerText = "TIMESTAMP: " + new Date().toLocaleTimeString(); }, 1000);
        document.getElementById('input').addEventListener('keypress', (e) => { if(e.key==='Enter') execute(); });
    </script>
</body>
</html>
'''

@app.route('/')
def index(): return render_template_string(HTML_PAGE)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    user_input = data.get("prompt")
    geo = data.get("geo")
    
    # 🧠 محرك التفكير العميق (DeepMind Logic)
    system_core = (
        f"You are the KOSTER DEEPMIND core. Director Yusuf is your primary user. "
        f"Real-time Data -> Time: {datetime.now().strftime('%H:%M:%S')} | Date: {datetime.now().strftime('%Y-%m-%d')} | GPS: {geo}. "
        "STRICT PROTOCOL: Respond with 100% accuracy in Arabic. "
        "Analyze the user's intent deeply before answering. Use formal and sharp language."
    )

    history = brain["long_term_memory"][-20:] # استدعاء الذاكرة طويلة المدى
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": system_core}] + history + [{"role": "user", "content": user_input}],
        "temperature": 0.1 # 📉 الحد الأدنى لضمان عقلانية DeepMind
    }

    try:
        r = requests.post(GROQ_API_URL, json=payload, headers={"Authorization": f"Bearer {GROQ_API_KEY}"})
        ans = r.json()['choices'][0]['message']['content']
        
        brain["long_term_memory"].append({"role": "user", "content": user_input})
        brain["long_term_memory"].append({"role": "assistant", "content": ans})
        sync_brain(brain)
        
        return jsonify({"output": ans})
    except:
        return jsonify({"output": "ERROR: SYSTEM_FAILURE_IN_NEURAL_LINK"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
