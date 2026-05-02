import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

# إعداد التطبيق
app = Flask(__name__, template_folder='templates')

# ربط العقل (Groq) باستخدام المفتاح الموجود في Render
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        
        # استخدام الموديل الجديد llama-3.1-8b-instant
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "أنت كوستر، مساعد ذكي ومرح طورك يوسف اليازجي."},
                {"role": "user", "content": user_message}
            ]
        )
        response_text = completion.choices[0].message.content
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"response": f"يوسف، في مشكلة تقنية: {str(e)}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
