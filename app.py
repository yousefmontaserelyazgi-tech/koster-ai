import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__, template_folder='templates')

# إعداد مفتاح Groq - تأكد إنك ضفته في Environment Variables في Render
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    try:
        # إرسال الرسالة لـ Groq
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "أنت 'كوستر'، مساعد ذكي تم تطويرك بواسطة يوسف اليازجي. ردودك ذكية وقصيرة."},
                {"role": "user", "content": user_message}
            ]
        )
        response_text = completion.choices[0].message.content
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"response": f"عذراً يوسف، في مشكلة بالمفتاح: {str(e)}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
