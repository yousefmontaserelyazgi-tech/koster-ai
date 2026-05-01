import os
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# إعداد الربط مع MongoDB
MONGO_URI = os.getenv("MONGO_URI")
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client['koster_ai']
    messages_col = db['history']
    client.admin.command('ping')
    print("✅ Connected to MongoDB Successfully")
except Exception as e:
    print(f"❌ MongoDB Error: {e}")
    messages_col = None

@app.route('/')
def index():
    # هذا السطر هو اللي بيفتح واجهة الشات
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # هنا كود الدردشة الخاص بك (Groq)
    return jsonify({"status": "working"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
