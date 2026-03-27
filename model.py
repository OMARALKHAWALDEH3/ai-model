import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# تحميل الداتا
df = pd.read_csv("big_data.csv")

# تأكد الأعمدة
print(df.head())

# features و labels
X = df["Payload"]
y = df["Type"]

# تحويل النص → أرقام
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# تدريب الموديل
model = LogisticRegression()
model.fit(X_vec, y)

print("Model trained on CSV ✅")


def predict(text):
    X_input = vectorizer.transform([text])
    prob = model.predict_proba(X_input)[0][1]

    return {
        "label": "Attack" if prob > 0.5 else "Normal",
        "risk_score": float(prob)
    }