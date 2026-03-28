<<<<<<< HEAD
from flask import Flask, request, jsonify
from model import predict
import time
=======
 
  from flask import Flask, request, jsonify
  from model import predict
>>>>>>> 626616b53783c663e5bcb27ecc91db1b85ff6f41

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict_route():
    start_time = time.time()

    # تحقق من وجود JSON
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    payload = data.get("payload", "")

    if not payload:
        return jsonify({"error": "Payload is required"}), 400

    # استدعاء الموديل
    result = predict(payload)

    # تأكد من القيم الافتراضية (حتى لو الموديل بسيط)
    risk_score = float(result.get("risk_score", 0.0))
    confidence = float(result.get("confidence", 0.0))
    prediction_label = result.get("prediction_label", "unknown")
    prediction_details = result.get("prediction_details", {})
    features_used = result.get("features_used", [])

    processing_time = int((time.time() - start_time) * 1000)

    return jsonify({
        "risk_score": risk_score,
        "confidence": confidence,
        "prediction_label": prediction_label,
        "prediction_details": prediction_details,
        "features_used": features_used,
        "processing_time": processing_time
    })

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "AI API running 🔥"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
