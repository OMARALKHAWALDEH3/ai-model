from flask import Flask, request, jsonify
import time
import pickle
import logging
from collections import defaultdict

# =========================
# 🔧 إعدادات
# =========================
app = Flask(__name__)

# Logging
logging.basicConfig(level=logging.INFO)

# Rate limiting (بسيط)
request_counts = defaultdict(int)
RATE_LIMIT = 100  # requests لكل IP

# =========================
# 📥 تحميل المودل (مرة وحدة فقط)
# =========================
with open("model.pkl", "rb") as f:
    model, vectorizer = pickle.load(f)


# =========================
# 🧹 تنظيف النص (نفس المودل)
# =========================
import re
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# =========================
# 🔮 predict (بدون import model.py)
# =========================
def predict(text):
    text = clean_text(text)

    X_input = vectorizer.transform([text])
    probs = model.predict_proba(X_input)[0]
    classes = model.classes_

    max_index = probs.argmax()
    prediction_label = str(classes[max_index])
    confidence = float(probs[max_index])

    normal_classes = ["normal", "benign", "safe"]

    if prediction_label.lower() in normal_classes:
        risk_score = 0.0
    else:
        risk_score = round(confidence * 100, 2)

    return {
        "risk_score": risk_score,
        "confidence": round(confidence, 4),
        "prediction_label": prediction_label,
        "prediction_details": {
            "all_probs": {
                str(c): float(p) for c, p in zip(classes, probs)
            }
        },
        "features_used": ["tfidf", "ngrams"]
    }


# =========================
# 🏥 Health Check
# =========================
@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "AI API running 🔥"
    })


# =========================
# 🚫 Rate Limit Middleware
# =========================
@app.before_request
def limit_requests():
    ip = request.remote_addr
    request_counts[ip] += 1

    if request_counts[ip] > RATE_LIMIT:
        return jsonify({
            "error": "Too many requests"
        }), 429


# =========================
# 🔐 Predict API
# =========================
@app.route("/predict", methods=["POST"])
def predict_route():
    start_time = time.time()

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    payload = data.get("payload", "")

    if not payload or not isinstance(payload, str):
        return jsonify({"error": "Valid payload is required"}), 400

    try:
        result = predict(payload)

        processing_time = int((time.time() - start_time) * 1000)
        result["processing_time"] = processing_time

        # Logging
        logging.info(f"Request: {payload} | Result: {result['prediction_label']} | Risk: {result['risk_score']}")

        return jsonify(result)

    except Exception as e:
        logging.error(str(e))
        return jsonify({"error": "Internal server error"}), 500


# =========================
# 🚀 تشغيل السيرفر
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)