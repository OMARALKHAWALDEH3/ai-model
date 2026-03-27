from flask import Flask, request, jsonify
from model import predict

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict_route():
    data = request.json
    payload = data.get("payload", "")

    result = predict(payload)

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)