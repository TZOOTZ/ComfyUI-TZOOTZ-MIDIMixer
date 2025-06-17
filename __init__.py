"""
TZOOTZ MIDI Latent Mixer for ComfyUI
Advanced MIDI-controlled mixing for IPAdapters & ControlNets

Installation:
1. Place this folder in ComfyUI/custom_nodes/
2. Install requirements: pip install -r requirements.txt
3. Restart ComfyUI

Copyright (c) 2025 TZOOTZ
https://github.com/TZOOTZ
"""

from .midi_latent_mixer_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# Make sure we have all the required mappings
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Print initialization message
print("\n" + "="*50)
print("🎵 TZOOTZ MIDI Latent Mixer v1.0 Loaded")
print("   Advanced MIDI → Visual Control")
print("   https://github.com/TZOOTZ")
print("="*50) 