#!/usr/bin/env python3
"""
TZOOTZ MIDI Latent Mixer - Installation Script
Automatically installs required dependencies for ComfyUI
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    print(f"Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def main():
    print("""
╔═══════════════════════════════════════╗
║     TZOOTZ MIDI LATENT MIXER          ║
║        Dependency Installer           ║
╚═══════════════════════════════════════╝
""")
    
    # Required packages
    packages = [
        "mido>=1.2.10",
        "python-rtmidi>=1.4.0"
    ]
    
    success_count = 0
    total_count = len(packages)
    
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 Installation Summary:")
    print(f"   Successfully installed: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 All dependencies installed successfully!")
        print("   You can now restart ComfyUI to use the MIDI Latent Mixer.")
    else:
        print("⚠️  Some dependencies failed to install.")
        print("   Please install them manually:")
        for package in packages:
            print(f"   pip install {package}")

if __name__ == "__main__":
    main() 