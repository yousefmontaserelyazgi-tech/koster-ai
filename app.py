import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__, template_folder='templates')

# ربط العقل بمفتاح API من ريندر واستخدام أحدث موديل
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        
        # تعليمات صارمة ليكون ذكياً جداً ومنظماً في الرد
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system", 
                    "content": "أنت 'كوستر'، ذكاء اصطناعي فائق. ردودك يجب أن تكون عميقة، مفصلة، ومنظمة جداً. استخدم النقاط المرقمة، العناوين، والخط العريض لتوضيح الأفكار التقنية المعقدة."
                },
                {"role": "user", "content": user_message}
            ]
        )
        response_text = completion.choices[0].message.content
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"response": f"يوسف، حدث خطأ تقني: {str(e)}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
