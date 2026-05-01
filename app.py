from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    return jsonify({"response": "أهلاً يوسف! أنا أعمل الآن من المكان الصحيح."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
