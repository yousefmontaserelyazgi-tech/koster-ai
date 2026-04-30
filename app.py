import os
import requests
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)

# 🔑 جلب المفاتيح من Environment Variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MONGO_URI = os.getenv("MONGO_URI") 
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# --- إعداد الذاكرة الأزلية (MongoDB) ---
try:
    client = MongoClient(MONGO_URI)
    db = client['koster_ai']
    memory_collection = db['chat_history']
    print("✅ Connected to Eternal Memory Success")
except Exception as e:
    print(f"❌ Memory Connection Error: {e}")

def save_to_eternal_memory(role, content):
    memory_collection.insert_one({
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow()
    })

def load_eternal_memory():
    # جلب التاريخ الكامل مرتباً زمنياً
    messages = memory_collection.find().sort("timestamp", 1)
    return [{"role": m['role'], "content": m['content']} for m in messages]

def get_supreme_logic():
    now = datetime.now()
    return {
        "role": "system", 
        "content": f"""
        [STATUS: SUPREME INTELLIGENCE - ETERNAL MEMORY ACTIVE]
        [DIRECTOR: YUSUF]
        [TIME: {now.strftime('%Y-%m-%d %H:%M:%S')}]
        [CAPABILITIES: World Expert in Investment, Strategy, and Science.]
        [CRITICAL LANGUAGE PROTOCOL: YOU MUST RESPOND STRICTLY AND EXCLUSIVELY IN ARABIC. DO NOT USE ENGLISH WORDS. DO NOT USE CHINESE, RUSSIAN, OR ANY OTHER LANGUAGE CHARACTERS. YOUR OUTPUT MUST BE 100% NATIVE, PROFESSIONAL ARABIC.]
        [CORE RULE: You never forget. You learn from Yusuf's previous messages saved in your memory bank.]
        """
    }

# (ضع كود واجهة HTML الفخمة هنا كما هي دون تغيير)
HTML_PAGE = ''' ... كود الواجهة الذهبية ... '''

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message")
    
    # 1. حفظ في الذاكرة السحابية فوراً
    save_to_eternal_memory("user", user_msg)
    
    # 2. تحميل التاريخ الكامل (الأزلي)
    full_history = load_eternal_memory()
    
    # 3. إعداد السياق (نأخذ آخر 40 رسالة)
    context = [get_supreme_logic()] + full_history[-40:]
    
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": context,
        "temperature": 0.1,
        "presence_penalty": 0.5 # يمنع تكرار الكلمات الغريبة
    }
    
    try:
        res = requests.post(GROQ_API_URL, json=payload, headers=headers)
        reply = res.json()['choices'][0]['message']['content']
        
        # 4. حفظ رد البوت في الذاكرة السحابية
        save_to_eternal_memory("assistant", reply)
        
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "نظام KOSTER واجه مشكلة في الاتصال بالمزود."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
