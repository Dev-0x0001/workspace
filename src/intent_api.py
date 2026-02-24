from flask import Flask, request, jsonify
from src.intent_recognition import IntentRecognitionModel
import torch
import numpy as np

app = Flask(__name__)

# Load pre-trained model
model = IntentRecognitionModel(input_size=16, hidden_size=32, output_size=4)
model.load_state_dict(torch.load('models/intent_model.pth'))
model.eval()

# Sample intent mapping
INTENT_MAP = {
    0: 'information',
    1: 'emotional_support',
    2: 'instructional',
    3: 'general'
}

@app.route('/recognize_intent', methods=['POST'])
def recognize_intent():
    data = request.json
    
    if 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    # Convert text to features (simplified for example)
    import hashlib
    text = data['text']
    features = np.frombuffer(hashlib.md5(text.encode()).digest(), dtype=np.float32)
    
    # Make prediction
    with torch.no_grad():
        input_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
        output = model(input_tensor)
        intent_id = torch.argmax(output).item()
        
    return jsonify({
        'text': text,
        'intent': INTENT_MAP.get(intent_id, 'unknown'),
        'confidence': float(output[0][intent_id].item())
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)