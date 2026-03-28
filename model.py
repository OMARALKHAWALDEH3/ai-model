import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# تحميل البيانات
df = pd.read_csv("big_data.csv")

# features و labels
X = df["Payload"]
y = df["Type"]

# تحويل النص → أرقام
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# تدريب الموديل
model = LogisticRegression(max_iter=1000)
model.fit(X_vec, y)

print("Model trained on CSV ✅")


def predict(text):
    # تنظيف بسيط
    text = text.lower().strip()

    # تحويل الإدخال
    X_input = vectorizer.transform([text])

    # التوقع
    probs = model.predict_proba(X_input)[0]
    classes = model.classes_

    # أعلى احتمال
    max_index = probs.argmax()
    prediction_label = str(classes[max_index])
    confidence = float(probs[max_index])

    # تحديد normal class (عدّلها حسب الداتا)
    normal_classes = ["normal", "benign", "safe"]

    if prediction_label.lower() in normal_classes:
        risk_score = 0.0
    else:
        risk_score = confidence

    return {
        "risk_score": risk_score,
        "confidence": confidence,
        "prediction_label": prediction_label,
        "prediction_details": {
            "all_probs": {
                str(c): float(p) for c, p in zip(classes, probs)
            }
        },
        "features_used": ["tfidf"]
    }