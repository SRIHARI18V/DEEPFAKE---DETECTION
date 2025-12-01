import torch
import timm
from torchvision import transforms
from PIL import Image

# Load a Vision Transformer model pretrained for image classification
model = timm.create_model('vit_base_patch16_224', pretrained=True)
model.head = torch.nn.Linear(model.head.in_features, 2)  # Binary classification: Real vs Fake

# Load pretrained weights from Hugging Face (example weights - you can update to your own)
# For this example, you MUST manually download weights and set the path here
# Example placeholder path (update with actual path)
weights_path = 'deepfake_detector_vit.pth'

# Load weights
model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
model.eval()

# Preprocessing
def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.5, 0.5, 0.5],
            std=[0.5, 0.5, 0.5]
        )
    ])
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)
    return image

# Predict function
def predict(image_path):
    image_tensor = preprocess_image(image_path)
    with torch.no_grad():
        output = model(image_tensor)
        predicted = torch.argmax(output, 1).item()
    return "Real" if predicted == 0 else "Fake"

# Replace with your own image path
image_path = 'test_image.jpg'
result = predict(image_path)
print(f"Predicted label: {result}")