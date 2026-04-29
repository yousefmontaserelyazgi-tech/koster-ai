import os
import json
from flask import Flask, render_template_string, request, jsonify
import requests
from datetime import datetime # 📅 إضافة مكتبة الوقت

app = Flask(__name__)

# --- الإعدادات ---
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DB_FILE = "koster_db.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"chat_history": []} # نبدأ بسجل فارغ ونضيف الـ System لاحقاً

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

database = load_data()

# --- دالة لتحديث تعليمات النظام بالوقت الحالي ---
def get_system_prompt():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    day_name = now.strftime("%A")
    # تحويل اسم اليوم للعربية (اختياري)
    days_ar = {"Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء", 
               "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت", "Sunday": "الأحد"}
    day_ar = days_ar.get(day_name, day_name)
    
    return {
        "role": "system", 
        "content": (
            f"You are KOSTER V15 PRO. A high-end AI system. "
            f"Today is {day_ar}, date: {current_time}. "
            "STRICT RULE: Speak ONLY in Arabic. Be rational and precise."
        )
    }

# (بقية كود الـ HTML يبقى كما هو في الرد السابق)
# ... [كود الـ HTML هنا] ...

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message")
    
    # 📝 الخطوة السحرية: تحديث التاريخ في كل مرة قبل الإرسال
    system_prompt = get_system_prompt()
    
    # إعادة بناء المحادثة مع الـ System Prompt الجديد ليعرف التاريخ الحالي
    messages = [system_prompt] + [m for m in database["chat_history"] if m["role"] != "system"]
    messages.append({"role": "user", "content": user_msg})
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.3
    }
    
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    try:
        res = requests.post(GROQ_API_URL, json=payload, headers=headers)
        reply = res.json()['choices'][0]['message']['content']
        
        # حفظ في الذاكرة الدائمة
        database["chat_history"].append({"role": "user", "content": user_msg})
        database["chat_history"].append({"role": "assistant", "content": reply})
        save_data(database)
        
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "عذراً يا مدير، حدث خطأ في النظام."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
