#!/usr/bin/env python3
"""
Sound Effects Module for FunHackerMode
======================================

This module provides sound effects and audio feedback for the hacker interface.
"""

import pygame
import random
import math
from typing import Optional

class SoundEffects:
    def __init__(self):
        self.sounds_enabled = True
        self.typing_sound = None
        self.beep_sound = None
        self.error_sound = None
        self.success_sound = None
        
        # Initialize sound effects
        self.init_sounds()
    
    def init_sounds(self):
        """Initialize all sound effects"""
        try:
            # Create synthetic sounds using pygame
            self.create_typing_sound()
            self.create_beep_sound()
            self.create_error_sound()
            self.create_success_sound()
        except Exception as e:
            print(f"Warning: Could not initialize sounds: {e}")
            self.sounds_enabled = False
    
    def create_typing_sound(self):
        """Create a synthetic typing sound"""
        try:
            # Generate a short beep sound
            sample_rate = 22050
            duration = 0.1
            frequency = 800
            
            frames = int(duration * sample_rate)
            arr = []
            
            for i in range(frames):
                time = float(i) / sample_rate
                wave = 4096 * math.sin(frequency * 2 * math.pi * time)
                # Add some noise for realism
                wave += random.randint(-200, 200)
                arr.append([int(wave), int(wave)])
            
            sound_array = pygame.sndarray.make_sound(pygame.array.array('i', arr))
            self.typing_sound = sound_array
        except Exception as e:
            print(f"Could not create typing sound: {e}")
    
    def create_beep_sound(self):
        """Create a beep sound"""
        try:
            sample_rate = 22050
            duration = 0.2
            frequency = 1000
            
            frames = int(duration * sample_rate)
            arr = []
            
            for i in range(frames):
                time = float(i) / sample_rate
                # Fade out
                volume = 1.0 - (float(i) / frames)
                wave = 4096 * volume * math.sin(frequency * 2 * math.pi * time)
                arr.append([int(wave), int(wave)])
            
            sound_array = pygame.sndarray.make_sound(pygame.array.array('i', arr))
            self.beep_sound = sound_array
        except Exception as e:
            print(f"Could not create beep sound: {e}")
    
    def create_error_sound(self):
        """Create an error sound"""
        try:
            sample_rate = 22050
            duration = 0.3
            frequency = 200
            
            frames = int(duration * sample_rate)
            arr = []
            
            for i in range(frames):
                time = float(i) / sample_rate
                # Low frequency with some modulation
                wave = 4096 * math.sin(frequency * 2 * math.pi * time)
                wave *= math.sin(10 * 2 * math.pi * time)  # Modulation
                arr.append([int(wave), int(wave)])
            
            sound_array = pygame.sndarray.make_sound(pygame.array.array('i', arr))
            self.error_sound = sound_array
        except Exception as e:
            print(f"Could not create error sound: {e}")
    
    def create_success_sound(self):
        """Create a success sound"""
        try:
            sample_rate = 22050
            duration = 0.4
            frequency_start = 400
            frequency_end = 800
            
            frames = int(duration * sample_rate)
            arr = []
            
            for i in range(frames):
                time = float(i) / sample_rate
                # Rising frequency
                frequency = frequency_start + (frequency_end - frequency_start) * (float(i) / frames)
                wave = 4096 * math.sin(frequency * 2 * math.pi * time)
                arr.append([int(wave), int(wave)])
            
            sound_array = pygame.sndarray.make_sound(pygame.array.array('i', arr))
            self.success_sound = sound_array
        except Exception as e:
            print(f"Could not create success sound: {e}")
    
    def play_typing(self):
        """Play typing sound effect"""
        if self.sounds_enabled and self.typing_sound:
            try:
                self.typing_sound.play()
            except:
                pass
    
    def play_beep(self):
        """Play beep sound effect"""
        if self.sounds_enabled and self.beep_sound:
            try:
                self.beep_sound.play()
            except:
                pass
    
    def play_error(self):
        """Play error sound effect"""
        if self.sounds_enabled and self.error_sound:
            try:
                self.error_sound.play()
            except:
                pass
    
    def play_success(self):
        """Play success sound effect"""
        if self.sounds_enabled and self.success_sound:
            try:
                self.success_sound.play()
            except:
                pass
    
    def toggle_sounds(self):
        """Toggle sound effects on/off"""
        self.sounds_enabled = not self.sounds_enabled
        return self.sounds_enabled
