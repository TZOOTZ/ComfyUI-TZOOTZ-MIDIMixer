# TZOOTZ MIDI Latent Mixer for ComfyUI

<div align="center">
  <img src="https://raw.githubusercontent.com/TZOOTZ/TZOOTZ/main/logo.png" alt="TZOOTZ Logo" width="200"/>
  
  # 🎛️ MIDI Latent Mixer
  
  **Transform MIDI into Visual Magic**
  
  [![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/TZOOTZ/ComfyUI-TZOOTZ-MIDIMixer)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
  [![ComfyUI](https://img.shields.io/badge/ComfyUI-Compatible-brightgreen.svg)](https://github.com/comfyanonymous/ComfyUI)
  [![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
</div>

---

## 🎵 Overview

The **TZOOTZ MIDI Latent Mixer** brings the power of musical control to ComfyUI's image generation pipeline. Control IPAdapters and ControlNets with MIDI tracks, creating audio-reactive visuals that pulse, morph, and transform in sync with your music.

### 🌟 Key Features

- **🎹 4-Track MIDI Control** - Map up to 4 MIDI tracks to visual parameters
- **🎯 Multiple Trigger Modes** - Velocity, Pulse, Hold, and Toggle responses
- **📊 Real-time Visualization** - See your MIDI activity with ASCII meters
- **🔧 Seamless Integration** - Works with existing ComfyUI workflows
- **⚡ Optimized Performance** - Efficient processing for smooth animations

## 📸 Screenshots

<div align="center">
  <img src="docs/images/node_interface.png" alt="Node Interface" width="600"/>
  <p><i>MIDI Latent Mixer node in ComfyUI</i></p>
</div>

## 🚀 Installation

### Method 1: Git Clone (Recommended)

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/TZOOTZ/ComfyUI-TZOOTZ-MIDIMixer
cd ComfyUI-TZOOTZ-MIDIMixer
pip install -r requirements.txt
```

### Method 2: Manual Download

1. Download the latest release from [Releases](https://github.com/TZOOTZ/ComfyUI-TZOOTZ-MIDIMixer/releases)
2. Extract to `ComfyUI/custom_nodes/`
3. Install dependencies: `pip install mido python-rtmidi`

### Method 3: Auto-Install Script

```bash
cd ComfyUI/custom_nodes/ComfyUI-TZOOTZ-MIDIMixer
python install.py
```

### Requirements

- ComfyUI (latest version)
- Python 3.8+
- Dependencies: `mido>=1.2.10`, `python-rtmidi`

## 🎮 Usage

### Basic Setup

1. Find the node under: **TZOOTZ/Audio Reactive/MIDI Latent Mixer**
2. Connect your base components:
   - Model (from checkpoint loader)
   - Positive/Negative conditioning
   - Latent image
3. Load a MIDI file
4. Connect IPAdapters and/or ControlNets
5. Configure trigger mode and strength
6. Generate!

### 🎛️ Track Mapping

| Track | Default Role | Best For |
|-------|-------------|----------|
| **Track 1** | Kick/Bass Drum | Structure & Rhythm |
| **Track 2** | Snare/Clap | Accents & Highlights |
| **Track 3** | Bass | Movement & Flow |
| **Track 4** | Lead/Melody | Style & Details |

### ⚙️ Parameters

#### Required Inputs
- **Model**: Your loaded checkpoint
- **Positive/Negative**: Text conditioning
- **Latent Image**: Input latent
- **Frame Number**: Current frame for animation
- **FPS**: Frames per second (1-120)
- **Trigger Mode**: How MIDI notes affect parameters
- **Mix Strength**: Global intensity (0.0-2.0)
- **Decay Rate**: Pulse fade speed (0.1-10.0)

#### Optional Inputs
- **MIDI Path**: Path to your .mid file
- **IPAdapters 1-4**: Image adaptation models
- **Images 1-4**: Reference images for IPAdapters
- **ControlNets 1-4**: Pose/depth/edge control
- **CN Images 1-4**: Control images
- **Weights & Strengths**: Per-channel fine-tuning

### 🎵 Trigger Modes Explained

#### **Velocity Mode**
- Directly maps MIDI velocity to parameter strength
- Perfect for: Dynamic, expressive control
- Example: Louder notes = stronger effect

#### **Pulse Mode**
- Creates attack/decay envelope from each note
- Perfect for: Rhythmic pulsing effects
- Example: Each kick drum creates a visual "pulse"

#### **Hold Mode**
- Binary on/off while note is held
- Perfect for: Sustained effects
- Example: Bass note holds a style transformation

#### **Toggle Mode**
- Each note switches state on/off
- Perfect for: Switching between styles
- Example: Snare hits toggle between two looks

## 🎨 Example Workflows

### Basic Audio-Reactive Animation
```
1. Load checkpoint → MIDI Latent Mixer
2. Add 4 different style images as IPAdapters
3. Load a drum loop MIDI
4. Set to "Pulse" mode
5. Animate through frames
```

### Advanced Style Morphing
```
1. Use ControlNet for structure (Track 1)
2. IPAdapters for style variations (Tracks 2-4)
3. Map melody to style strength
4. Use "Velocity" mode for expressive control
```

## 📊 Performance Tips

- **Optimize MIDI**: Simpler patterns = better performance
- **Frame Rate**: 30 FPS is usually sufficient
- **Batch Processing**: Process multiple frames in parallel
- **GPU Memory**: Each IPAdapter/ControlNet uses VRAM

## 🛠️ Troubleshooting

### Common Issues

**"MIDI file not found"**
- Check file path is correct
- Use absolute paths for reliability

**"No effect visible"**
- Ensure MIDI has notes in first 4 tracks
- Check mix strength > 0
- Verify IPAdapters/ControlNets are connected

**"Memory error"**
- Reduce number of active channels
- Lower image resolution
- Use fewer IPAdapters simultaneously

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Roadmap

- [ ] Real-time MIDI input support
- [ ] Custom track mapping UI
- [ ] Preset system for common patterns
- [ ] BPM detection and sync
- [ ] Multi-channel mixing matrix
- [ ] OSC protocol support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- ComfyUI community for the amazing platform
- Mido library for MIDI parsing
- All the creative coders pushing boundaries

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/TZOOTZ/ComfyUI-TZOOTZ-MIDIMixer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/TZOOTZ/ComfyUI-TZOOTZ-MIDIMixer/discussions)
- **Email**: hello@tzootz.com

---

<div align="center">
  <b>Made with ❤️ by TZOOTZ</b><br>
  <i>Bridging Audio and Visual Worlds</i><br><br>
  
  <a href="https://github.com/TZOOTZ">GitHub</a> • 
  <a href="https://twitter.com/TZOOTZ">Twitter</a> • 
  <a href="https://tzootz.com">Website</a>
</div>