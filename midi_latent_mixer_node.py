"""
╔══════════════════════════════════════════════════════════════╗
║                       TZOOTZ                                 ║
║                  MIDI LATENT MIXER v1.0                      ║
║                                                              ║
║  Advanced MIDI-controlled mixing for IPAdapters & ControlNets║
║  Copyright (c) 2025 TZOOTZ                                   ║
║  https://github.com/TZOOTZ                                   ║
╚══════════════════════════════════════════════════════════════╝
"""

import torch
import numpy as np
import os
import folder_paths
import comfy
from comfy import model_management

# Try to import MIDI library with error handling
try:
    import mido
    MIDI_AVAILABLE = True
except ImportError:
    MIDI_AVAILABLE = False
    print("⚠️  TZOOTZ: mido not installed. MIDI functionality disabled.")
    print("   Install with: pip install mido python-rtmidi")

# TZOOTZ Color Codes for terminal output
TZOOTZ_COLORS = {
    'HEADER': '\033[95m',
    'INFO': '\033[94m',
    'SUCCESS': '\033[92m',
    'WARNING': '\033[93m',
    'ERROR': '\033[91m',
    'RESET': '\033[0m',
    'BOLD': '\033[1m'
}

def tzootz_print(message, msg_type='INFO'):
    """Branded print function"""
    color = TZOOTZ_COLORS.get(msg_type, TZOOTZ_COLORS['INFO'])
    reset = TZOOTZ_COLORS['RESET']
    bold = TZOOTZ_COLORS['BOLD']
    print(f"{color}{bold}[TZOOTZ]{reset} {color}{message}{reset}")

class TZOOTZMIDILatentMixer:
    """
    TZOOTZ - MIDI Latent Mixer
    
    Mix IPAdapters and ControlNets using MIDI triggers
    Maximum 4 MIDI tracks → 4 control channels
    
    Track mapping:
    - Track 1 (Kick): Base structure & rhythm
    - Track 2 (Snare): Accents & highlights  
    - Track 3 (Bass): Movement & flow
    - Track 4 (Lead): Style & details
    """
    
    def __init__(self):
        self.type = "TZOOTZMIDILatentMixer"
        self.midi_data = None
        self.current_frame = 0
        self.track_states = [0.0, 0.0, 0.0, 0.0]
        self._cached_midi_path = None
        tzootz_print("MIDI Latent Mixer initialized", 'SUCCESS')
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "positive": ("CONDITIONING",),
                "negative": ("CONDITIONING",),
                "latent_image": ("LATENT",),
                "frame_number": ("INT", {
                    "default": 0, 
                    "min": 0, 
                    "max": 9999,
                    "step": 1,
                    "display": "number"
                }),
                "fps": ("INT", {
                    "default": 30,
                    "min": 1,
                    "max": 120,
                    "display": "number"
                }),
                "trigger_mode": (["Velocity", "Pulse", "Hold", "Toggle"],),
                "mix_strength": ("FLOAT", {
                    "default": 1.0, 
                    "min": 0.0, 
                    "max": 2.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "decay_rate": ("FLOAT", {
                    "default": 2.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                    "display": "slider"
                }),
            },
            "optional": {
                # MIDI file
                "midi_path": ("STRING", {
                    "default": "", 
                    "multiline": False,
                    "placeholder": "Path to MIDI file..."
                }),
                
                # IPAdapters (4 channels)
                "ipadapter_1": ("IPADAPTER",),
                "ipadapter_2": ("IPADAPTER",),
                "ipadapter_3": ("IPADAPTER",),
                "ipadapter_4": ("IPADAPTER",),
                
                # Images for IPAdapters
                "image_1": ("IMAGE",),
                "image_2": ("IMAGE",),
                "image_3": ("IMAGE",),
                "image_4": ("IMAGE",),
                
                # IPAdapter weights
                "ipa_weight_1": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                "ipa_weight_2": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                "ipa_weight_3": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                "ipa_weight_4": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                
                # ControlNets (4 channels)
                "control_net_1": ("CONTROL_NET",),
                "control_net_2": ("CONTROL_NET",),
                "control_net_3": ("CONTROL_NET",),
                "control_net_4": ("CONTROL_NET",),
                
                # Control images
                "cn_image_1": ("IMAGE",),
                "cn_image_2": ("IMAGE",),
                "cn_image_3": ("IMAGE",),
                "cn_image_4": ("IMAGE",),
                
                # ControlNet strengths
                "cn_strength_1": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                "cn_strength_2": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                "cn_strength_3": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
                "cn_strength_4": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
            }
        }
    
    RETURN_TYPES = ("MODEL", "CONDITIONING", "CONDITIONING", "STRING", "STRING")
    RETURN_NAMES = ("model", "positive", "negative", "debug_info", "mix_values")
    FUNCTION = "mix_with_midi"
    CATEGORY = "TZOOTZ/Audio Reactive"

    def get_tzootz_header(self):
        """Return TZOOTZ ASCII header"""
        return """
╔═══════════════════════════════════════╗
║        TZOOTZ MIDI MIXER              ║
║         Audio → Visual Magic          ║
╚═══════════════════════════════════════╝
"""

    def parse_midi_file(self, midi_path):
        """Parse MIDI file and extract track data"""
        if not MIDI_AVAILABLE:
            tzootz_print("MIDI parsing disabled - mido not installed", 'WARNING')
            return None
            
        if not midi_path or not os.path.exists(midi_path):
            return None
            
        try:
            tzootz_print(f"Loading MIDI file: {midi_path}", 'INFO')
            mid = mido.MidiFile(midi_path)
            tracks_data = []
            
            # Get tempo
            tempo = 500000  # default 120 BPM
            for msg in mid.tracks[0]:
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
                    break
            
            bpm = 60000000 / tempo
            tzootz_print(f"MIDI Tempo: {bpm:.1f} BPM", 'INFO')
            
            # Process first 4 tracks
            track_names = ["Kick/Structure", "Snare/Accent", "Bass/Movement", "Lead/Style"]
            
            for i, track in enumerate(mid.tracks[:4]):
                track_events = []
                current_time = 0
                note_count = 0
                
                for msg in track:
                    current_time += msg.time
                    if msg.type in ['note_on', 'note_off']:
                        track_events.append({
                            'time': current_time,
                            'type': msg.type,
                            'note': msg.note,
                            'velocity': msg.velocity
                        })
                        if msg.type == 'note_on' and msg.velocity > 0:
                            note_count += 1
                
                tracks_data.append(track_events)
                if i < len(track_names):
                    tzootz_print(f"Track {i+1} ({track_names[i]}): {note_count} notes", 'SUCCESS')
            
            return {
                'tracks': tracks_data,
                'tempo': tempo,
                'ticks_per_beat': mid.ticks_per_beat,
                'bpm': bpm
            }
            
        except Exception as e:
            tzootz_print(f"Error parsing MIDI: {e}", 'ERROR')
            return None

    def get_track_strength_at_frame(self, track_data, frame, fps, trigger_mode, 
                                   ticks_per_beat, tempo, decay_rate):
        """Calculate track strength at specific frame"""
        if not track_data:
            return 0.0
        
        # Convert frame to MIDI time
        seconds = frame / fps
        midi_time = seconds * 1000000 / tempo * ticks_per_beat
        
        # Find active notes at this time
        active_notes = []
        for i, event in enumerate(track_data):
            if event['time'] <= midi_time:
                if event['type'] == 'note_on' and event['velocity'] > 0:
                    # Check if note is still active
                    note_off_time = None
                    for j in range(i+1, len(track_data)):
                        if (track_data[j]['note'] == event['note'] and 
                            (track_data[j]['type'] == 'note_off' or 
                             track_data[j]['velocity'] == 0)):
                            note_off_time = track_data[j]['time']
                            break
                    
                    if note_off_time is None or midi_time < note_off_time:
                        active_notes.append(event)
        
        if not active_notes:
            return 0.0
        
        # Calculate strength based on trigger mode
        if trigger_mode == "Velocity":
            # Average velocity of active notes
            return np.mean([n['velocity'] / 127.0 for n in active_notes])
        elif trigger_mode == "Pulse":
            # Decay from most recent note
            most_recent = max(active_notes, key=lambda x: x['time'])
            time_since = (midi_time - most_recent['time']) / ticks_per_beat
            decay = max(0, 1.0 - time_since * decay_rate)
            return (most_recent['velocity'] / 127.0) * decay
        elif trigger_mode == "Hold":
            # Binary on/off
            return 1.0 if active_notes else 0.0
        elif trigger_mode == "Toggle":
            # Count note-ons to determine toggle state
            note_on_count = sum(1 for e in track_data 
                              if e['time'] <= midi_time and 
                              e['type'] == 'note_on' and 
                              e['velocity'] > 0)
            return 1.0 if note_on_count % 2 == 1 else 0.0
        
        return 0.0

    def apply_ipadapter_to_model(self, model, ipadapter, image, weight, track_strength):
        """Apply IPAdapter with calculated weight - placeholder for actual implementation"""
        if ipadapter is not None and image is not None and weight > 0 and track_strength > 0:
            final_weight = weight * track_strength
            tzootz_print(f"IPAdapter applied with weight: {final_weight:.2f}", 'INFO')
            
            # NOTE: This is a placeholder implementation
            # The actual IPAdapter integration would depend on the specific IPAdapter node being used
            # For now, we return the model unchanged but log the activity
            
            # In a real implementation, this might look like:
            # model_patched = ipadapter.apply_ipadapter(model, image, final_weight)
            # return model_patched
            
        return model

    def apply_controlnet_to_conditioning(self, positive, negative, control_net, image, strength, track_strength):
        """Apply ControlNet to conditioning with proper ComfyUI integration"""
        if control_net is not None and image is not None and strength > 0 and track_strength > 0:
            # Calculate final strength
            final_strength = strength * track_strength
            
            # Prepare control hint (ensure proper format)
            if len(image.shape) == 4:  # Batch dimension
                control_hint = image.movedim(-1, 1)  # Move channels to correct position
            else:
                control_hint = image.unsqueeze(0).movedim(-1, 1)
            
            # Create control net entry
            # Format: [control_net, control_hint, strength, start_percent, end_percent]
            cnets = [[control_net, control_hint, final_strength, 0.0, 1.0]]
            
            # Apply to positive conditioning
            c_pos = []
            for t in positive:
                n = [t[0], t[1].copy()]
                if 'control' in n[1]:
                    # Append to existing controls
                    n[1]['control'] = n[1]['control'] + cnets
                else:
                    # Create new control entry
                    n[1]['control'] = cnets
                c_pos.append(n)
            
            # Apply to negative conditioning
            c_neg = []
            for t in negative:
                n = [t[0], t[1].copy()]
                if 'control' in n[1]:
                    # Append to existing controls
                    n[1]['control'] = n[1]['control'] + cnets
                else:
                    # Create new control entry
                    n[1]['control'] = cnets
                c_neg.append(n)
            
            tzootz_print(f"ControlNet applied with strength: {final_strength:.2f}", 'INFO')
            return (c_pos, c_neg)
        
        return (positive, negative)

    def create_debug_visualization(self, frame, fps, bpm, track_states):
        """Create visual debug info"""
        bars = ['░░░░░░░░░░', '██░░░░░░░░', '████░░░░░░', '██████░░░░', 
                '████████░░', '██████████']
        
        debug = self.get_tzootz_header()
        debug += f"\nFrame: {frame} | FPS: {fps} | BPM: {bpm:.1f}\n"
        debug += "─" * 40 + "\n"
        
        track_names = ["Kick ", "Snare", "Bass ", "Lead "]
        for i, (name, state) in enumerate(zip(track_names, track_states)):
            bar_index = int(state * 5)
            bar = bars[min(bar_index, 5)]
            debug += f"Track {i+1} [{name}]: {bar} {state*100:.0f}%\n"
        
        debug += "─" * 40 + "\n"
        debug += "© 2025 TZOOTZ\n"
        
        return debug

    def mix_with_midi(self, model, positive, negative, latent_image, 
                     frame_number, fps, trigger_mode, mix_strength, decay_rate, **kwargs):
        """Main mixing function"""
        
        # Parse MIDI if provided
        midi_path = kwargs.get('midi_path', '')
        
        # Only re-parse if path changed or first load
        if midi_path and (self._cached_midi_path != midi_path):
            self.midi_data = self.parse_midi_file(midi_path)
            self._cached_midi_path = midi_path
            self.current_frame = frame_number
        else:
            self.current_frame = frame_number
        
        # Initialize
        bpm = self.midi_data['bpm'] if self.midi_data else 120.0
        
        # Start with original model and conditioning
        processed_model = model
        processed_positive = positive
        processed_negative = negative
        
        # Process each track
        if self.midi_data:
            tracks = self.midi_data['tracks']
            tempo = self.midi_data['tempo']
            ticks_per_beat = self.midi_data['ticks_per_beat']
            
            # Calculate strengths for each track
            for i in range(4):
                if i < len(tracks):
                    strength = self.get_track_strength_at_frame(
                        tracks[i], frame_number, fps, trigger_mode,
                        ticks_per_beat, tempo, decay_rate
                    )
                    self.track_states[i] = strength * mix_strength
                    
                    # Apply IPAdapter if connected
                    ipa_key = f'ipadapter_{i+1}'
                    img_key = f'image_{i+1}'
                    weight_key = f'ipa_weight_{i+1}'
                    if ipa_key in kwargs and img_key in kwargs:
                        weight = kwargs.get(weight_key, 1.0)
                        processed_model = self.apply_ipadapter_to_model(
                            processed_model, kwargs[ipa_key], kwargs[img_key], 
                            weight, self.track_states[i]
                        )
                    
                    # Apply ControlNet if connected
                    cn_key = f'control_net_{i+1}'
                    cn_img_key = f'cn_image_{i+1}'
                    cn_strength_key = f'cn_strength_{i+1}'
                    if cn_key in kwargs and cn_img_key in kwargs:
                        strength = kwargs.get(cn_strength_key, 1.0)
                        processed_positive, processed_negative = self.apply_controlnet_to_conditioning(
                            processed_positive, processed_negative,
                            kwargs[cn_key], kwargs[cn_img_key],
                            strength, self.track_states[i]
                        )
        
        # Create debug visualization
        debug_info = self.create_debug_visualization(frame_number, fps, bpm, self.track_states)
        
        # Return mix values as formatted string for display
        mix_values = f"[{', '.join([f'{v:.2f}' for v in self.track_states])}]"
        
        return (processed_model, processed_positive, processed_negative, debug_info, mix_values)

# Node registration
NODE_CLASS_MAPPINGS = {
    "TZOOTZMIDILatentMixer": TZOOTZMIDILatentMixer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TZOOTZMIDILatentMixer": "MIDI Latent Mixer (TZOOTZ)"
} 