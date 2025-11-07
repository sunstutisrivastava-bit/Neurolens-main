"""
Quick Model Checker - See all trained models and accuracy
Run: python check_models.py
"""

import os
import json
from datetime import datetime

print("\n" + "="*100)
print("🧠 NEUROLENS - TRAINED MODELS STATUS")
print("="*100 + "\n")

# Check for trained models
checkpoint_dir = 'checkpoints'
if os.path.exists(checkpoint_dir):
    models = [f for f in os.listdir(checkpoint_dir) if f.endswith('.h5')]
    
    if models:
        print(f"📦 Found {len(models)} trained model(s):\n")
        print(f"{'Model Name':<40} {'Size (MB)':<15} {'Last Modified':<25}")
        print("-"*100)
        
        for model in models:
            path = os.path.join(checkpoint_dir, model)
            size = os.path.getsize(path) / (1024 * 1024)
            modified = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{model:<40} {size:<15.2f} {modified:<25}")
    else:
        print("❌ No trained models found in 'checkpoints/' directory")
else:
    print("❌ 'checkpoints/' directory not found")

# Check training results
print("\n" + "="*100)
if os.path.exists('training_results.json'):
    with open('training_results.json', 'r') as f:
        data = json.load(f)
        results = data.get('results', [])
        
    if results:
        print("📊 TRAINING ACCURACY RESULTS:\n")
        print(f"{'Model Name':<50} {'Accuracy':<15} {'Status':<15}")
        print("-"*100)
        
        for r in results:
            name = r.get('name', 'Unknown')
            acc = f"{r.get('accuracy', 0):.2f}%" if r.get('accuracy') else "N/A"
            status = "✅ Success" if r.get('success') else "❌ Failed"
            print(f"{name:<50} {acc:<15} {status:<15}")
        
        # Calculate average
        accuracies = [r['accuracy'] for r in results if r.get('accuracy')]
        if accuracies:
            print("\n" + "-"*100)
            print(f"📈 Average Accuracy: {sum(accuracies)/len(accuracies):.2f}%")
            print(f"📈 Best Accuracy: {max(accuracies):.2f}%")
            print(f"📈 Total Models Trained: {len(results)}")
    else:
        print("⚠️  No training results found")
else:
    print("⚠️  training_results.json not found - models haven't been trained yet")

print("\n" + "="*100)
print("\n💡 COMMANDS:")
print("   • Train all models:        python train_all_models.py")
print("   • Train voice model:       python train_perfect_voice_model.py")
print("   • Train angry model:       python train_angry_image_model.py")
print("   • Train happy model:       python train_happy_image_model.py")
print("   • Train sad model:         python train_sad_image_model.py")
print("   • View detailed info:      python view_model_info.py")
print("   • Check models (this):     python check_models.py")
print("="*100 + "\n")
