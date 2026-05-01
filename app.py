import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

# تأكد من كتابة Flask بحرف كبير هنا
app = Flask(__name__, template_folder='templates')

# استدعاء العقل (Groq)
try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except:
    client = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    
    if not client:
        return jsonify({"response": "خطأ: لم يتم إضافة مفتاح GROQ_API_KEY في Render"})

    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "أنت كوستر، مساعد ذكي ومرح."},
                {"role": "user", "content": user_msg}
            ]
        )
        return jsonify({"response": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"response": f"حدث خطأ: {str(e)}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
