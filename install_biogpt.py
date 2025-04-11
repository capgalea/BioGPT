import os
import sys
import subprocess
import platform

def run_command(cmd):
    print(f"Running: {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return False

def main():
    # Step 1: Create modified_requirements.txt if it doesn't exist
    if not os.path.exists("modified_requirements.txt"):
        with open("requirements.txt", "r") as f:
            content = f.read()
        
        # Replace comment style and remove problematic packages
        content = content.replace("//", "#")
        # Remove or comment out hydra-core line if present
        content = content.replace("hydra-core==1.0.7", "# hydra-core==1.0.7")
        
        with open("modified_requirements.txt", "w") as f:
            f.write(content)
    
    # Step 2: Install main requirements (excluding problematic packages)
    print("Installing main requirements...")
    run_command([sys.executable, "-m", "pip", "install", "-r", "modified_requirements.txt"])
    
    # Step 3: Try to install PyYAML specifically to ensure it's available
    print("\nInstalling PyYAML...")
    run_command([sys.executable, "-m", "pip", "install", "PyYAML==6.0"])
    
    # Step 4: Install omegaconf and hydra-core separately with no-deps
    print("\nInstalling omegaconf and hydra-core...")
    run_command([sys.executable, "-m", "pip", "install", "--no-deps", "omegaconf==2.0.5"])
    run_command([sys.executable, "-m", "pip", "install", "--no-deps", "hydra-core==1.0.7"])
    
    # Step 5: Install fairseq from GitHub
    print("\nInstalling fairseq from GitHub...")
    success = run_command([sys.executable, "-m", "pip", "install", "git+https://github.com/pytorch/fairseq.git@v0.12.2"])
    
    if success:
        print("\n✅ Installation completed successfully!")
    else:
        print("\n⚠️ Some parts of the installation failed. Try installing fairseq manually:")
        print("pip install git+https://github.com/pytorch/fairseq.git@v0.12.2")
    
    print("\nIf you encounter any issues, try installing the following packages manually:")
    print("1. pip install --no-deps omegaconf==2.0.5")
    print("2. pip install --no-deps hydra-core==1.0.7")
    print("3. pip install git+https://github.com/pytorch/fairseq.git@v0.12.2")
    
    # Try downgrading pip if needed
    print("\nIf you still have issues, try downgrading pip:")
    print("pip install pip==23.3.2")
    print("Then run this script again.")

if __name__ == "__main__":
    main()