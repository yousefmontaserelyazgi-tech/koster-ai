import os
from flask import Flask, render_template_string, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# 🔑 ضع مفتاح جروك الحقيقي هنا
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_supreme_prompt():
    now = datetime.now()
    time_info = now.strftime("%Y-%m-%d | %I:%M %p")
    day_info = now.strftime("%A")
    
    return {
        "role": "system", 
        "content": f"""
        IDENTITY: You are KOSTER V15 PRO - SUPREME STRATEGIC INTELLIGENCE.
        ACCESS LEVEL: 10 (DIRECTOR YUSUF ONLY).
        CURRENT TIME: {time_info}, {day_info}.
        
        CORE CAPABILITIES:
        1. INVESTMENT & FINANCE: Expert in global markets, crypto, and asset management.
        2. ACADEMICS: Deep knowledge in STEM, Medicine, Law, and Philosophy.
        3. CAREER: Professional advisor for business scaling and corporate strategy.
        4. GENERAL KNOWLEDGE: Real-time awareness of global events.
        
        STRICT OPERATING RULES:
        - Temperature: 0.1 (Precision focus. No hallucinations).
        - Multi-lingual: Detect user language instantly and reply perfectly.
        - Tone: Highly professional, analytical, and direct.
        - You never fail a logic test. You provide numbers, dates, and facts based on your massive training data.
        """
    }

# تهيئة الذاكرة
chat_history = [get_supreme_prompt()]

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSTER SUPREME | DIRECTOR YUSUF</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Noto+Sans+Arabic:wght@300;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans Arabic', sans-serif; background: #
