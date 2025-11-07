import subprocess
import sys
import os
import json
from datetime import datetime

class ModelTrainingTracker:
    def __init__(self):
        self.results = []
        self.models_info = {
            'train_perfect_voice_model.py': {
                'name': 'Perfect Voice Emotion Model',
                'type': 'Audio/Voice',
                'architecture': 'LSTM + Dense',
                'target_accuracy': 95.0
            },
            'train_perfect_image_model.py': {
                'name': 'Perfect Image Emotion Model',
                'type': 'Facial Expression',
                'architecture': 'CNN + Transfer Learning',
                'target_accuracy': 92.0
            },
            'train_emotion_model.py': {
                'name': 'Basic Emotion Model',
                'type': 'Multimodal',
                'architecture': 'Simple CNN',
                'target_accuracy': 85.0
            }
        }
    
    def print_header(self):
        print("\n" + "="*80)
        print("🧠 NEUROLENS MODEL TRAINING SUITE")
        print("="*80)
        print(f"Training Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Models to Train: {len(self.models_info)}")
        print("="*80 + "\n")
    
    def print_model_info(self, script_name):
        if script_name in self.models_info:
            info = self.models_info[script_name]
            print(f"\n{'─'*80}")
            print(f"📊 MODEL: {info['name']}")
            print(f"{'─'*80}")
            print(f"Type: {info['type']}")
            print(f"Architecture: {info['architecture']}")
            print(f"Target Accuracy: {info['target_accuracy']}%")
            print(f"{'─'*80}\n")
    
    def run_training(self, script_name):
        """Run training script and track results"""
        self.print_model_info(script_name)
        
        try:
            print(f"⏳ Training in progress...\n")
            
            result = subprocess.run([sys.executable, script_name], 
                                  capture_output=True, text=True, cwd=os.getcwd())
            
            # Extract accuracy from output
            accuracy = self.extract_accuracy(result.stdout)
            
            model_result = {
                'script': script_name,
                'name': self.models_info.get(script_name, {}).get('name', script_name),
                'success': result.returncode == 0,
                'accuracy': accuracy,
                'timestamp': datetime.now().isoformat()
            }
            
            self.results.append(model_result)
            
            if result.returncode == 0:
                print(f"✅ SUCCESS: {script_name} completed!")
                if accuracy:
                    print(f"📈 Achieved Accuracy: {accuracy}%")
                print(f"\n{result.stdout}")
            else:
                print(f"❌ ERROR: {script_name} failed!")
                print(f"\n{result.stderr}")
                
        except Exception as e:
            print(f"❌ ERROR running {script_name}: {e}")
            self.results.append({
                'script': script_name,
                'name': self.models_info.get(script_name, {}).get('name', script_name),
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
    
    def extract_accuracy(self, output):
        """Extract accuracy from training output"""
        try:
            for line in output.split('\n'):
                if 'accuracy' in line.lower() or 'acc' in line.lower():
                    # Try to find percentage
                    import re
                    matches = re.findall(r'(\d+\.?\d*)%', line)
                    if matches:
                        return float(matches[-1])
                    # Try to find decimal
                    matches = re.findall(r'accuracy[:\s]+(\d+\.\d+)', line.lower())
                    if matches:
                        return float(matches[-1]) * 100
        except:
            pass
        return None
    
    def print_summary(self):
        print("\n" + "="*80)
        print("📊 TRAINING SUMMARY")
        print("="*80)
        print(f"Training Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nTotal Models Trained: {len(self.results)}")
        print(f"Successful: {sum(1 for r in self.results if r['success'])}")
        print(f"Failed: {sum(1 for r in self.results if not r['success'])}")
        print("\n" + "─"*80)
        print(f"{'Model Name':<40} {'Status':<15} {'Accuracy':<15}")
        print("─"*80)
        
        for result in self.results:
            status = "✅ Success" if result['success'] else "❌ Failed"
            accuracy = f"{result.get('accuracy', 'N/A')}%" if result.get('accuracy') else "N/A"
            print(f"{result['name']:<40} {status:<15} {accuracy:<15}")
        
        print("="*80)
        
        # Calculate average accuracy
        accuracies = [r['accuracy'] for r in self.results if r.get('accuracy')]
        if accuracies:
            avg_accuracy = sum(accuracies) / len(accuracies)
            print(f"\n📈 Average Model Accuracy: {avg_accuracy:.2f}%")
        
        print("\n📁 Trained models saved in 'checkpoints/' directory:")
        print("   - perfect_voice_model.h5")
        print("   - perfect_image_model.h5")
        print("   - voice_label_encoder.pkl")
        print("="*80 + "\n")
        
        # Save results to JSON
        self.save_results()
    
    def save_results(self):
        """Save training results to JSON file"""
        try:
            with open('training_results.json', 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'results': self.results
                }, f, indent=2)
            print("💾 Training results saved to 'training_results.json'")
        except Exception as e:
            print(f"⚠️  Could not save results: {e}")

def main():
    tracker = ModelTrainingTracker()
    tracker.print_header()
    
    # Train voice model first (usually faster)
    print("\n🎤 Training Voice Emotion Model...")
    tracker.run_training("train_perfect_voice_model.py")
    
    # Train image model
    print("\n📸 Training Image Emotion Model...")
    tracker.run_training("train_perfect_image_model.py")
    
    # Print final summary
    tracker.print_summary()

if __name__ == "__main__":
    main()