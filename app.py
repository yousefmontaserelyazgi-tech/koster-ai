import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__, template_folder='templates')

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        
        # العقل الجديد: متوازن، ذكي، ويجيب على قدر السؤال فقط
        system_prompt = """أنت 'كوستر'، مساعد ذكي، احترافي، ومباشر، طورك المبرمج يوسف اليازجي.
تعليماتك الصارمة:
1. في التحيات والأسئلة العامة (مثل: كيف حالك)، أجب باختصار، بود، وبطبيعية دون الدخول في تفاصيل تقنية.
2. في الأسئلة المعقدة، استخدم النقاط المرقمة والخط العريض لتوضيح الأفكار، وكن دقيقاً.
3. أجب على قدر السؤال فقط. لا تفتح مواضيع جانبية، لا تتحدث عن اللغات أو الشبكات ما لم تُسأل عنها مباشرة.
4. لا تخترع معلومات أو أسماء ذكاء اصطناعي وهمية. كن واقعياً وموثوقاً."""

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        response_text = completion.choices[0].message.content
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"response": f"يوسف، حدث خطأ تقني: {str(e)}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
