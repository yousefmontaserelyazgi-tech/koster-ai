import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# 🔑 ضع مفتاح جروك السري هنا
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# 🧠 برمجة النظام بالتركيز العالي (0.1 Temperature)
chat_history = [
    {
        "role": "system", 
        "content": "أنت KOSTER V15 PRO. مساعد ذكي فائق الدقة. ردودك مركزة جداً، منطقية، وتلتزم بنفس لغة المستخدم. لا تخرج عن الموضوع ولا تتحدث عن برمجتك. أنت تعمل تحت إمرة المدير يوسف."
    }
]

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSTER V15 PRO | Global System</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Tajawal', sans-serif; background: #050505; color: #e5e7eb; margin: 0; height: 100vh; overflow: hidden; }
        .bg-gradient { background: radial-gradient(circle at top right, #1e1b4b 0%, #000000 100%); }
        .glass { background: rgba(17, 24, 39, 0.7); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.05); }
        .user-msg { background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; border-radius: 20px 20px 4px 20px; box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.2); }
        .bot-msg { background: rgba(31, 41, 55, 0.5); border-right: 4px solid #f59e0b; border-radius: 20px 20px 20px 4px; line-height: 1.8; }
        .status-dot { width: 10px; height: 10px; background: #22c55e; border-radius: 50%; box-shadow: 0 0 10px #22c55e; }
        .custom-scroll::-webkit-scrollbar { width: 4px; }
        .custom-scroll::-webkit-scrollbar-thumb { background: #374151; border-radius: 10px; }
        .fade-in { animation: fadeIn 0.3s ease-out forwards; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body class="bg-gradient flex items-center justify-center p-4">
    <div class="max-w-4xl w-full h-[95vh] flex flex-col glass rounded-[2.5rem] shadow-2xl overflow-hidden">
        <header class="p-8 border-b border-white/5 flex justify-between items-center bg-white/5">
            <div>
                <h1 class="text-3xl font-black text-white tracking-tight">KOSTER <span class="text-amber-500">V15 PRO</span></h1>
                <p class="text-[11px] text-gray-400 font-bold uppercase tracking-[0.3em] mt-1">نظام الإدارة الفائق للمدير يوسف</p>
            </div>
            <div class="flex items-center gap-3 bg-black/40 px-4 py-2 rounded-full border border-white/10">
                <div class="status-dot animate-pulse"></div>
                <span class="text-[12px] text-green-500 font-black">ONLINE</span>
            </div>
        </header>

        <div id="chat" class="flex-1 overflow-y-auto p-8 space-y-8 flex flex-col custom-scroll">
            <div class="bot-msg p-5 fade-in">أهلاً بك أيها المدير يوسف. تم ضبط درجة حرارة النظام على <b>0.1</b> للتركيز الأقصى. أنا جاهز لتنفيذ أوامرك بدقة متناهية.</div>
        </div>

        <div class="p-8 bg-white/5 border-t border-white/5">
            <div class="flex gap-4 items-center">
                <div class="flex-1 relative">
                    <input type="text" id="msg" onkeypress="if(event.key==='Enter') send()" 
                        class="w-full bg-black/40 border border-white/10 rounded-2xl py-4 px-6 outline-none focus:border-amber-500/50 transition-all text-gray-100 placeholder-gray-500 shadow-inner" 
                        placeholder="أدخل تعليماتك هنا...">
                </div>
                <button onclick="send()" id="btn" 
                    class="bg-amber-500 hover:bg-amber-400 text-black font-black px-10 py-4 rounded-2xl transition-all active:scale-95 shadow-lg shadow-amber-500/20">
                    إرسال
                </button>
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

            chat.innerHTML += `<div class="flex flex-col items-end"><div class="user-msg p-5 max-w-[85%] fade-in">${text}</div></div>`;
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
                chat.innerHTML += `<div class="flex flex-col items-start"><div class="bot-msg p-5 max-w-[85%] fade-in">${data.reply}</div></div>`;
            } catch (e) {
                chat.innerHTML += `<div class="text-red-400 text-sm p-4">خطأ في الاتصال بالسيرفر.</div>`;
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
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": chat_history,
        "temperature": 0.1,  # 🎯 التركيز العالي هنا
        "top_p": 1
    }
    
    try:
        res = requests.post(GROQ_API_URL, json=payload, headers=headers)
        reply = res.json()['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "عذراً يا مدير، تأكد من صحة المفتاح السري."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
