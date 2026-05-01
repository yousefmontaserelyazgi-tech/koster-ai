import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

# إعداد التطبيق - يتوقع وجود مجلد اسمه templates وبداخله index.html
app = Flask(__name__, template_folder='templates')

# إعداد اتصال Groq
try:
    # سيقرأ المفتاح من الـ Environment Variables في Render
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception:
    client = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not client:
        return jsonify({"response": "خطأ: لم يتم ضبط مفتاح API في Render (Environment Variables)"})
    
    try:
        data = request.json
        user_message = data.get("message", "")
        
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "أنت 'كوستر'، مساعد ذكي طورك يوسف اليازجي. ردودك سريعة وذكية."},
                {"role": "user", "content": user_message}
            ]
        )
        response_text = completion.choices[0].message.content
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"response": f"حدث خطأ في النظام: {str(e)}"})

if __name__ == "__main__":
    # التشغيل على بورت 10000 المتوافق مع Render
    app.run(host='0.0.0.0', port=10000)
