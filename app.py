from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    # هذا السطر سيفتح ملف index.html الموجود في مجلد templates
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # كود مؤقت للتأكد من أن الإرسال يعمل
    return jsonify({"response": "أنا أسمعك يا يوسف! السيرفر متصل الآن بنجاح."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
