from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# 🔑 ضع مفتاحك (API Key) الخاص بـ Groq هنا
GROQ_API_KEY = "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"

# 🧠 نظام الذاكرة لتخزين المحادثة
chat_history = [
    {"role": "system", "content": "أنت KOSTER V15، مساعد ذكي يتذكر تفاصيل المحادثة بدقة ويساعد المستخدم بلغة عربية واضحة."}
]

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSTER V15 | السيرفر العالمي</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #020617; color: white; font-family: sans-serif; }
        .main-container { background: rgba(15, 23, 42, 0.9); border: 1px solid #0ea5e9; border-radius: 2rem; }
        .user-msg { background: #0ea5e9; color: black; font-weight: bold; padding: 12px; border-radius: 15px 15px 0 15px; align-self: flex-end; }
        .bot-msg { background: #1e293b; padding: 12px; border-radius: 15px 15px 15px 0; border-right: 4px solid #0ea5e9; }
    </style>
</head>
<body class="h-screen flex items-center justify-center p-4 bg-slate-950">
    <div class="max-w-2xl w-full h-[90vh] flex flex-col main-container overflow-hidden shadow-2xl">
        <header class="p-6 border-b border-white/10 text-center">
            <h1 class="text-2xl font-black text-sky-400">KOSTER <span class="text-white">V15 PRO</span></h1>
            <p class="text-[10px] text-green-400 uppercase tracking-widest mt-1">متصل بالسيرفر العالمي ✅</p>
        </header>

        <div id="chat" class="flex-1 overflow-y-auto p-4 space-y-4 flex flex-col scroll-smooth">
            <div class="bot-msg">أهلاً يوسف! أنا الآن أعمل من السيرفر السحابي بذاكرة كاملة. كيف أساعدك اليوم؟</div>
        </div>

        <div class="p-4 bg-black/20 border-t border-white/5 flex gap-2">
            <input type="text" id="msg" onkeypress="if(event.key==='Enter') send()" class="flex-1 bg-slate-800 p-4 rounded-2xl outline-none focus:ring-2 ring-sky-500" placeholder="اكتب هنا...">
            <button onclick="send()" class="bg-sky-500 text-black px-8 rounded-2xl font-bold active:scale-95 transition-all">إرسال</button>
        </div>
    </div>

    <script>
        async function send() {
            const input = document.getElementById('msg');
            const chat = document.getElementById('chat');
            const text = input.value.trim();
            if(!text) return;

            chat.innerHTML += `<div class="user-msg">${text}</div>`;
            input.value = "";
            chat.scrollTop = chat.scrollHeight;
            
            const load = document.createElement('div');
            load.className = "bot-msg animate-pulse text-sky-400";
            load.innerText = "جاري التفكير...";
            chat.appendChild(load);

            try {
                const res = await fetch('/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({p: text})
                });
                const data = await res.json();
                load.innerText = data.r;
                load.classList.remove('animate-pulse', 'text-sky-400');
            } catch {
                load.innerText = "❌ حدث خطأ في الاتصال بالسيرفر.";
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
    prompt = request.json.get('p')
    chat_history.append({"role": "user", "content": prompt})
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": chat_history,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            ans = response.json()['choices'][0]['message']['content']
            chat_history.append({"role": "assistant", "content": ans})
            return jsonify({"r": ans})
        return jsonify({"r": "عذراً، واجهت مشكلة في الاتصال بمحرك جروك."})
    except:
        return jsonify({"r": "السيرفر العالمي متوقف حالياً."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
