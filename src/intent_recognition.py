import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
import numpy as np

class IntentRecognitionModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(IntentRecognitionModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size)
        self.fc = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        out, _ = self.lstm(x)
        x = self.fc(out[:, -1, :])
        return self.softmax(x)

# Example usage
if __name__ == "__main__":
    # Sample data - this would be replaced with real data
    texts = [
        "Can you help me find information on climate change?",
        "I'm feeling frustrated with this task.",
        "Show me how to tie a knot.",
        "What's the capital of France?",
        "I need to calm down and breathe deeply.",
        "Explain the theory of relativity simply.";
    
    # Convert text to numerical features (simplified for example)
    import hashlib
    features = [np.frombuffer(hashlib.md5(t.encode()).digest(), dtype=np.float32) for t in texts]
    
    # Sample labels (0: information, 1: emotional, 2: instructional, 3: general)
    labels = [0, 1, 2, 0, 1, 3]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2)
    
    # Create model
    model = IntentRecognitionModel(input_size=16, hidden_size=32, output_size=4)
    
    # Train
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    
    # Simple training loop
    epochs = 100
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(torch.tensor(np.array(X_train), dtype=torch.float32))
        loss = criterion(outputs, torch.tensor(y_train, dtype=torch.long))
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')
    
    # Test
    with torch.no_grad():
        test_outputs = model(torch.tensor(np.array(X_test), dtype=torch.float32))
        predicted = torch.argmax(test_outputs, dim=1).numpy()
        
    print('
Test Results:')
    print(f'Actual: {y_test}')
    print(f'Predicted: {predicted}')