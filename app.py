from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import os
import base64
import io
import cv2
import numpy as np
from PIL import Image
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Charger le modèle personnalisé
model_path = 'my_model.pt'
model = YOLO(model_path)

# Charger les caractéristiques depuis le fichier JSON
with open('caracteristiques.json', 'r', encoding='utf-8') as f:
    caracteristiques = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    try:
        image_data = request.form['image']
        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        image_np = np.array(image)

        # Appliquer le modèle YOLO
        results = model(image_np)
        result = results[0]

        annotated_frame = result.plot()

        # Générer le nom du fichier
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_detected.jpg"
        output_path = os.path.join("static", "detections", filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, annotated_frame)

        # Extraire les noms des objets détectés
        labels = [model.names[int(cls)] for cls in result.boxes.cls]

        documentation = []
        for label in labels:
            doc = caracteristiques.get(label)
            if doc:
                documentation.append(f"<strong>{label}</strong>: {doc}")
            else:
                documentation.append(f"<strong>{label}</strong>: Aucune documentation trouvée.")

        return jsonify({
            "image_path": f"/static/detections/{filename}",
            "documentation": "<br>".join(documentation)
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
