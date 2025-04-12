from flask import Flask, request, jsonify
from inference import generate_response
import sys
import os
from loguru import logger

from shared.rbac import requires_auth, requires_role

app = Flask(__name__)
import sys
sys.path.append('/app')


# تكوين الـ logger لتسجيل كل الأنشطة
logger.add('log_service/responses_logs/chatbot_logs.log', rotation='1 MB', retention='7 days', compression='zip')

@app.route("/chat", methods=["POST"])
@requires_auth
@requires_role("analyst")  # You can change to 'admin' or make it dynamic
def chat():
    data = request.get_json()
    prompt = data.get("prompt", "")
    
    # إنشاء سجل لطلب الـ prompt
    if not prompt:
        logger.warning(f"Request failed - Missing prompt")
        return jsonify({"error": "Prompt is required"}), 400
    
    # تسجيل المحادثة قبل الرد
    logger.info(f"Received prompt: {prompt}")
    
    response = generate_response(prompt)
    
    # تسجيل الرد
    logger.info(f"Generated response: {response}")
    
    return jsonify({
        "user": request.user["username"],
        "role": request.user["role"],
        "prompt": prompt,
        "response": response
    })

#if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=5101)


