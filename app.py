from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# 🔑 ضع مفتاحك هنا
GROQ_API_KEY = "ضع_مفتاحك_هنا"

# 🧠 نظام الذاكرة: تخزين رسائل المحادثة
chat_history = [
    {"role": "system", "content": "أنت مساعد ذكي ومحترف اسمه KOSTER V15. تذكر دائماً ما قاله المستخدم سابقاً وكن دقيقاً في إجاباتك."}
]

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSTER V15 | PRO EDITION</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #020617; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .glass-panel { background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(14, 165, 233, 0.3); backdrop-filter: blur(10px); }
        .user-bubble { background: #0ea5e9; border-radius: 20px 20px 0 20px; box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3); }
        .bot-bubble { background: #1e293b; border-radius: 20px 20px 20px 0; border: 1px solid #334155; }
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-thumb { background: #0ea5e9; border-radius: 10px; }
    </style>
</head>
<body class="h-screen flex items-center justify-center p-2 sm:p-6">
    <div class="max-w-2xl w-full h-full flex flex-col glass-panel rounded-[2.5rem] shadow-2xl overflow-hidden">
        
        <header class="p-5 border-b border-white/10 flex justify-between items-center bg-slate-900/50">
            <div>
                <h1 class="text-xl font-bold bg-gradient-to-l from-sky-400 to-white bg-clip-text text-transparent">KOSTER V15 PRO</h1>
                <div class="flex items-center gap-2">
                    <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                    <p class="text-[10px] text-sky-300/70 uppercase tracking-widest">نظام الذاكرة النشط</p>
                </div>
            </div>
            <button onclick="window.location.reload()" class="text-xs bg-white/5 hover:bg-white/10 px-3 py-1 rounded-lg transition">مسح الذاكرة</button>
        </header>

        <div id="chat" class="flex-1 overflow-y-auto p-4 space-y-6">
            <div class="bot-bubble p-4 max-w-[90%] text-sm leading-relaxed">
                مرحباً يوسف! أنا الآن أمتلك ذاكرة مطورة. اسألني عن أي شيء، وسأذكر ما قلته لي لاحقاً.
            </div>
        </div>

        <div class="p-4 bg-slate-900/80 border-t border-white/5">
            <div class="relative flex items-center">
                <input type="text" id="msg" onkeypress="if(event.key==='Enter') send()" 
                    class="w-full bg-slate-800/50 border border-white/10 p-4 pr-16 rounded-2xl outline-none focus:ring-2 ring-sky-500 transition-all text-sm" 
                    placeholder="اكتب رسالتك هنا...">
                <button onclick="send()" class="absolute left-2 bg-sky-500 hover:bg-sky-600 text-white px-5 py-2.5 rounded-xl font-bold transition-all active:scale-95">
                    إرسال
                </button>
            </div>
        </div>
    </div>

    <script>
        async function send() {
            const input = document.getElementById('msg');
            const chat = document.getElementById('chat');
            const text = input.value.trim();
            if(!text) return;

            // إضافة رسالة المستخدم
            chat.innerHTML += `<div class="flex justify-end"><div class="user-bubble p-4 max-w-[85%] text-sm shadow-lg">${text}</div></div>`;
            input.value = "";
            
            // مؤشر الانتظار
            const loader = document.createElement('div');
            loader.className = "bot-bubble p-4 max-w-[80%] text-sm animate-pulse text-sky-400";
            loader.innerText = "جاري استرجاع الذاكرة والرد...";
            chat.appendChild(loader);
            chat.scrollTop = chat.scrollHeight;

            try {
                const res = await fetch('/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await res.json();
                loader.classList.remove('animate-pulse', 'text-sky-400');
                loader.innerText = data.reply;
            } catch {
                loader.innerText = "❌ حدث خطأ في الاتصال بالسيرفر.";
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

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message')
    
    # 1. إضافة رسالة المستخدم للذاكرة
    chat_history.append({"role": "user", "content": user_message})
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY.strip()}",
        "Content-Type": "application/json"
    }
    
    # 2. إرسال المحادثة كاملة (chat_history) وليس رسالة واحدة فقط
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": chat_history,
        "temperature": 0.6
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            bot_reply = response.json()['choices'][0]['message']['content']
            
            # 3. حفظ رد البوت في الذاكرة لكي يتذكره في المرة القادمة
            chat_history.append({"role": "assistant", "content": bot_reply})
            
            return jsonify({"reply": bot_reply})
        else:
            return jsonify({"reply": f"⚠️ خطأ {response.status_code}"})
    except Exception as e:
        return jsonify({"reply": "📡 السيرفر العالمي لا يستجيب حالياً."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
