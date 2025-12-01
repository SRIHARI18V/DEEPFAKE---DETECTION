from flask import Flask, request, jsonify, render_template
import torch
from torchvision import models, transforms
import torch.nn as nn
from PIL import Image

app = Flask(__name__)

# Load Pretrained Model (ResNet18)
model = models.resnet18(weights='IMAGENET1K_V1')
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 2)  # 2 classes: real (0) or fake (1)
model.eval()

# Image Preprocessing
def preprocess_image(image):
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    input_tensor = preprocess(image).unsqueeze(0)
    return input_tensor

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    image = Image.open(file).convert('RGB')
    input_batch = preprocess_image(image)

    with torch.no_grad():
        output = model(input_batch)
        probs = torch.softmax(output, dim=1)
        print(probs)  # Debug output
        _, predicted = torch.max(output, 1)
        label = 'fake' if predicted.item() == 0 else 'real'


    return jsonify({'label': label})

if __name__ == '__main__':
    app.run(debug=True)
