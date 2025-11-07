"""
NeuroLens Model Information Viewer
Shows all trained models with their accuracy and details
"""

import os
import json
from datetime import datetime

class ModelInfoViewer:
    def __init__(self):
        self.checkpoint_dir = 'checkpoints'
        self.models = []
        
    def scan_models(self):
        """Scan for trained models"""
        if not os.path.exists(self.checkpoint_dir):
            print(f"⚠️  Checkpoint directory '{self.checkpoint_dir}' not found!")
            return
        
        model_files = [f for f in os.listdir(self.checkpoint_dir) if f.endswith(('.h5', '.pkl', '.pt', '.pth'))]
        
        for model_file in model_files:
            model_path = os.path.join(self.checkpoint_dir, model_file)
            file_size = os.path.getsize(model_path) / (1024 * 1024)  # MB
            modified_time = datetime.fromtimestamp(os.path.getmtime(model_path))
            
            self.models.append({
                'name': model_file,
                'path': model_path,
                'size_mb': round(file_size, 2),
                'modified': modified_time.strftime('%Y-%m-%d %H:%M:%S')
            })
    
    def load_training_results(self):
        """Load training results from JSON"""
        if os.path.exists('training_results.json'):
            try:
                with open('training_results.json', 'r') as f:
                    data = json.load(f)
                    return data.get('results', [])
            except:
                pass
        return []
    
    def display_info(self):
        """Display comprehensive model information"""
        print("\n" + "="*100)
        print("🧠 NEUROLENS - TRAINED MODELS INFORMATION")
        print("="*100)
        
        # Load training results
        training_results = self.load_training_results()
        
        if training_results:
            print("\n📊 TRAINING RESULTS")
            print("─"*100)
            print(f"{'Model Name':<45} {'Status':<15} {'Accuracy':<15} {'Trained On':<25}")
            print("─"*100)
            
            for result in training_results:
                status = "✅ Success" if result['success'] else "❌ Failed"
                accuracy = f"{result.get('accuracy', 'N/A')}%" if result.get('accuracy') else "N/A"
                timestamp = result.get('timestamp', 'Unknown')
                if timestamp != 'Unknown':
                    timestamp = datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                
                print(f"{result['name']:<45} {status:<15} {accuracy:<15} {timestamp:<25}")
            
            # Calculate statistics
            accuracies = [r['accuracy'] for r in training_results if r.get('accuracy')]
            if accuracies:
                print("\n" + "─"*100)
                print(f"📈 Average Accuracy: {sum(accuracies)/len(accuracies):.2f}%")
                print(f"📈 Best Accuracy: {max(accuracies):.2f}%")
                print(f"📈 Lowest Accuracy: {min(accuracies):.2f}%")
        
        # Display model files
        print("\n\n💾 MODEL FILES")
        print("─"*100)
        
        if not self.models:
            print("⚠️  No trained models found in 'checkpoints/' directory")
            print("\n💡 Run 'python train_all_models.py' to train models")
        else:
            print(f"{'Model File':<40} {'Size (MB)':<15} {'Last Modified':<25}")
            print("─"*100)
            
            for model in self.models:
                print(f"{model['name']:<40} {model['size_mb']:<15} {model['modified']:<25}")
            
            total_size = sum(m['size_mb'] for m in self.models)
            print("─"*100)
            print(f"Total Models: {len(self.models)} | Total Size: {total_size:.2f} MB")
        
        # Model architecture info
        print("\n\n🏗️  MODEL ARCHITECTURES")
        print("─"*100)
        
        architectures = {
            'Perfect Voice Model': {
                'Type': 'Audio/Voice Emotion Recognition',
                'Architecture': 'LSTM (128 units) + Dense (64 units) + Dropout (0.5)',
                'Input': 'MFCC features (40 coefficients)',
                'Output': '7 emotions (happy, sad, angry, neutral, surprised, fear, calm)',
                'Target Accuracy': '95%+'
            },
            'Perfect Image Model': {
                'Type': 'Facial Expression Recognition',
                'Architecture': 'CNN (Conv2D + MaxPooling + BatchNorm) + Dense',
                'Input': '48x48 grayscale images',
                'Output': '7 emotions (happy, sad, angry, neutral, surprised, fear, disgust)',
                'Target Accuracy': '92%+'
            }
        }
        
        for model_name, info in architectures.items():
            print(f"\n📦 {model_name}")
            for key, value in info.items():
                print(f"   {key}: {value}")
        
        print("\n" + "="*100)
        print("\n💡 USAGE:")
        print("   - Train models: python train_all_models.py")
        print("   - View this info: python view_model_info.py")
        print("   - Run app: python app.py")
        print("="*100 + "\n")

def main():
    viewer = ModelInfoViewer()
    viewer.scan_models()
    viewer.display_info()

if __name__ == "__main__":
    main()
