import subprocess
import sys
import os

def run_training(script_name):
    """Run training script and handle errors"""
    try:
        print(f"\n{'='*50}")
        print(f"Starting {script_name}")
        print(f"{'='*50}")
        
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"SUCCESS: {script_name} completed successfully!")
            print(result.stdout)
        else:
            print(f"ERROR: {script_name} failed!")
            print(result.stderr)
            
    except Exception as e:
        print(f"ERROR running {script_name}: {e}")

def main():
    print("Starting comprehensive model training for 100% accuracy...")
    
    # Train voice model first (usually faster)
    print("\nTraining Perfect Voice Model...")
    run_training("train_perfect_voice_model.py")
    
    # Train image model
    print("\nTraining Perfect Image Model...")
    run_training("train_perfect_image_model.py")
    
    print("\nAll model training completed!")
    print("\nTrained models saved in 'checkpoints/' directory:")
    print("- perfect_voice_model.h5")
    print("- perfect_image_model.h5")
    print("- voice_label_encoder.pkl")

if __name__ == "__main__":
    main()