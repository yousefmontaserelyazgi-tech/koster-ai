import os
import gradio as gr
from groq import Groq
from datetime import datetime

# --- المحرك السيادي ---
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def koster_sovereign_engine(message, history):
    # تحضير الذاكرة بصيغة القواميس المطلوبة في Gradio 6.0
    messages_for_api = []
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # 1. نظام التوجيهات
    messages_for_api.append({
        "role": "system", 
        "content": f"أنت KOSTER V15 PRO. المالك: يوسف. اليوم: {current_date}. كن نخبوياً ودقيقاً."
    })

    # 2. إضافة تاريخ المحادثة
    for h in history:
        messages_for_api.append({"role": "user", "content": h["content"] if isinstance(h, dict) and h["role"] == "user" else h[0] if isinstance(h, (list, tuple)) else ""})
        messages_for_api.append({"role": "assistant", "content": h["content"] if isinstance(h, dict) and h["role"] == "assistant" else h[1] if isinstance(h, (list, tuple)) else ""})

    # 3. إضافة رسالة المستخدم الحالية
    user_text = message["text"] if isinstance(message, dict) else message
    messages_for_api.append({"role": "user", "content": user_text})

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages_for_api,
            temperature=0.3,
            stream=True
        )
        
        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                # الحل الجذري: نرسل الرد كقائمة قواميس لتجنب الـ Format Error
                current_history = history + [
                    {"role": "user", "content": user_text},
                    {"role": "assistant", "content": full_response}
                ]
                yield current_history

    except Exception as e:
        error_msg = [{"role": "assistant", "content": f"⚠️ تنبيه: {str(e)}"}]
        yield history + error_msg

# --- الواجهة (Stable Build) ---
with gr.Blocks(css=".gradio-container {background-color: #050505; color: #d4af37;}") as demo:
    gr.HTML("<div style='text-align:center; padding:20px; border-bottom:2px solid #d4af37;'>"
            "<h1 style='color: #d4af37; font-size: 30px;'>KOSTER V15 PRO</h1>"
            "<p style='color: #888;'>الذكاء الاستراتيجي للمدير يوسف</p></div>")

    # تحديد النوع "messages" والتعامل معه برمجياً
    chatbot = gr.Chatbot(label="المنصة السيادية", height=550, type="messages")
    
    with gr.Row():
        msg = gr.Textbox(placeholder="أرسل توجيهاتك...", show_label=False, scale=9)
        btn = gr.Button("إطلاق 🚀", scale=1)

    # الربط البرمجي (المخرج هو الشات بوت فقط)
    msg.submit(koster_sovereign_engine, [msg, chatbot], [chatbot])
    msg.submit(lambda: "", None, [msg])
    btn.click(koster_sovereign_engine, [msg, chatbot], [chatbot])
    btn.click(lambda: "", None, [msg])

if __name__ == "__main__":
    demo.queue().launch()
