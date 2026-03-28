from flask import Flask, request, jsonify
from model import predict
import time

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "AI API running 🔥"
    })


@app.route("/predict", methods=["POST"])
def predict_route():
    start_time = time.time()

    # تحقق من JSON
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    payload = data.get("payload", "")

    if not payload:
        return jsonify({"error": "Payload is required"}), 400

    try:
        # استدعاء الموديل
        result = predict(payload)

        processing_time = int((time.time() - start_time) * 1000)

        # إضافة وقت المعالجة
        result["processing_time"] = processing_time

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)