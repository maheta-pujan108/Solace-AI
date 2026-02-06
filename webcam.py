import cv2
import numpy as np
from tensorflow.keras.models import load_model

model = load_model("model/emotion_cnn.h5")
emotions = ['angry','disgust','fear','happy','neutral','sad','surprise']

stress_map = {
    'happy': 0.1,
    'neutral': 0.3,
    'surprise': 0.4,
    'fear': 0.7,
    'sad': 0.8,
    'angry': 0.9,
    'disgust': 0.9
}

def get_risk(stress):
    if stress < 0.4:
        return "Low"
    elif stress < 0.7:
        return "Medium"
    else:
        return "High"

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = cv2.resize(gray, (48,48))
    face = face.reshape(1,48,48,1) / 255.0

    pred = model.predict(face, verbose=0)
    emotion = emotions[np.argmax(pred)]
    stress = stress_map[emotion]
    risk = get_risk(stress)

    cv2.putText(frame, f"Emotion: {emotion}", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
    cv2.putText(frame, f"Stress: {stress:.2f}", (20,80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,200,255), 2)
    cv2.putText(frame, f"Risk: {risk}", (20,120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)

    if risk == "High":
        cv2.putText(frame,
            "You matter. Talk to someone you trust.",
            (20,170),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)

    cv2.imshow("Solace AI - Face Module", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()