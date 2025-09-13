#!/usr/bin/env python3
"""
FunHackerMode - An Epic Hacker-Style Slideshow Experience
========================================================

A fun program that simulates a cool hacker interface with:
- Animated slideshow with custom images
- Matrix-style falling code animation
- Terminal aesthetic with green text
- Animated graphs and data visualizations
- Sound effects and typing animations

Author: FunHackerMode
Version: 1.0.0
"""

import pygame
import sys
import os
import time
import random
import math
from typing import List, Tuple
import threading
from graph_animations import GraphAnimations
from sound_effects import SoundEffects

# Initialize Pygame
pygame.init()
pygame.mixer.init()

class FunHackerMode:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("FunHackerMode v1.0.0 - Initializing...")
        
        # Colors (hacker theme)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BRIGHT_GREEN = (50, 255, 50)
        self.DARK_GREEN = (0, 150, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 100, 255)
        self.WHITE = (255, 255, 255)
        self.GRAY = (100, 100, 100)
        
        # Fonts
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        self.font_mono = pygame.font.Font("consola.ttf", 20) if os.path.exists("consola.ttf") else pygame.font.Font(None, 20)
        
        # Animation variables
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_mode = "startup"
        self.startup_progress = 0
        self.matrix_chars = []
        self.slideshow_images = []
        self.current_image_index = 0
        self.image_timer = 0
        self.typing_text = ""
        self.typing_index = 0
        self.typing_speed = 50  # milliseconds
        
        # Initialize components
        self.init_matrix_effect()
        self.load_images()
        self.setup_typing_animation()
        
        # Initialize additional components
        self.graph_animations = GraphAnimations(self.screen_width, self.screen_height)
        self.sound_effects = SoundEffects()
        
        # Additional animation variables
        self.show_graphs = False
        self.graph_timer = 0
        
    def init_matrix_effect(self):
        """Initialize the Matrix-style falling code effect"""
        self.matrix_chars = []
        for i in range(50):  # Number of falling columns
            x = random.randint(0, self.screen_width)
            y = random.randint(-500, 0)
            speed = random.randint(1, 3)
            chars = "".join([chr(random.randint(33, 126)) for _ in range(random.randint(10, 30))])
            self.matrix_chars.append({
                'x': x,
                'y': y,
                'speed': speed,
                'chars': chars,
                'char_index': 0
            })
    
    def load_images(self):
        """Load and prepare images for slideshow"""
        # For now, we'll create placeholder rectangles with text
        # In a real implementation, you'd load actual image files
        self.slideshow_images = [
            {"text": "OUT FOR UNDERGRAD", "color": self.BLUE, "subtext": "o4U Logo"},
            {"text": "c4U LIFE SCIENCES", "color": self.GREEN, "subtext": "PILOT PROGRAM"},
            {"text": "SAINT PAUL, MN", "color": self.RED, "subtext": "SEPTEMBER 26-28"},
            {"text": "HACKER MODE", "color": self.BRIGHT_GREEN, "subtext": "ACTIVATED"},
        ]
    
    def setup_typing_animation(self):
        """Setup the typing animation text"""
        self.typing_phrases = [
            "Initializing FunHackerMode...",
            "Loading matrix protocols...",
            "Establishing secure connection...",
            "Accessing mainframe...",
            "Decrypting data streams...",
            "System ready. Welcome to the matrix."
        ]
        self.current_phrase_index = 0
        self.typing_text = ""
        self.typing_index = 0
        self.last_typing_time = 0
    
    def update_matrix_effect(self):
        """Update the Matrix-style falling code animation"""
        for char_data in self.matrix_chars:
            char_data['y'] += char_data['speed']
            char_data['char_index'] = (char_data['char_index'] + 1) % len(char_data['chars'])
            
            # Reset when off screen
            if char_data['y'] > self.screen_height:
                char_data['y'] = random.randint(-500, -100)
                char_data['x'] = random.randint(0, self.screen_width)
    
    def draw_matrix_effect(self):
        """Draw the Matrix-style falling code effect"""
        for char_data in self.matrix_chars:
            x = char_data['x']
            y = char_data['y']
            chars = char_data['chars']
            char_index = char_data['char_index']
            
            # Draw the falling characters
            for i, char in enumerate(chars):
                char_y = y + (i * 20)
                if 0 <= char_y <= self.screen_height:
                    # Fade effect - characters get dimmer as they fall
                    alpha = max(0, 255 - (i * 15))
                    color = (0, alpha, 0)
                    
                    # Highlight the current character
                    if i == char_index:
                        color = self.BRIGHT_GREEN
                    
                    char_surface = self.font_mono.render(char, True, color)
                    self.screen.blit(char_surface, (x, char_y))
    
    def update_typing_animation(self):
        """Update the typing animation"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_typing_time > self.typing_speed:
            if self.current_phrase_index < len(self.typing_phrases):
                current_phrase = self.typing_phrases[self.current_phrase_index]
                if self.typing_index < len(current_phrase):
                    self.typing_text += current_phrase[self.typing_index]
                    self.typing_index += 1
                    # Play typing sound
                    if random.random() < 0.3:  # 30% chance
                        self.sound_effects.play_typing()
                else:
                    # Move to next phrase after a delay
                    time.sleep(1)
                    self.current_phrase_index += 1
                    self.typing_text = ""
                    self.typing_index = 0
            else:
                # All phrases done, switch to slideshow mode
                self.current_mode = "slideshow"
                self.sound_effects.play_success()
            
            self.last_typing_time = current_time
    
    def draw_startup_screen(self):
        """Draw the startup screen with typing animation"""
        # Clear screen
        self.screen.fill(self.BLACK)
        
        # Draw matrix effect in background
        self.draw_matrix_effect()
        
        # Draw main title
        title = self.font_large.render("FunHackerMode v1.0.0", True, self.BRIGHT_GREEN)
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Draw typing animation
        typing_surface = self.font_medium.render(self.typing_text + "_", True, self.GREEN)
        typing_rect = typing_surface.get_rect(center=(self.screen_width // 2, 200))
        self.screen.blit(typing_surface, typing_rect)
        
        # Draw progress bar
        progress_width = 400
        progress_height = 20
        progress_x = (self.screen_width - progress_width) // 2
        progress_y = 300
        
        # Background
        pygame.draw.rect(self.screen, self.DARK_GREEN, (progress_x, progress_y, progress_width, progress_height))
        
        # Progress
        progress = min(1.0, self.current_phrase_index / len(self.typing_phrases))
        current_progress_width = int(progress_width * progress)
        pygame.draw.rect(self.screen, self.GREEN, (progress_x, progress_y, current_progress_width, progress_height))
        
        # Progress text
        progress_text = f"Loading... {int(progress * 100)}%"
        progress_surface = self.font_small.render(progress_text, True, self.WHITE)
        progress_rect = progress_surface.get_rect(center=(self.screen_width // 2, progress_y + 40))
        self.screen.blit(progress_surface, progress_rect)
    
    def draw_slideshow(self):
        """Draw the slideshow mode"""
        # Clear screen
        self.screen.fill(self.BLACK)
        
        # Draw matrix effect in background (dimmed)
        self.draw_matrix_effect()
        
        # Draw current image
        if self.slideshow_images:
            current_image = self.slideshow_images[self.current_image_index]
            
            # Create a semi-transparent overlay
            overlay = pygame.Surface((self.screen_width, self.screen_height))
            overlay.set_alpha(128)
            overlay.fill(self.BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Draw image placeholder (rectangle with text)
            image_width = 600
            image_height = 400
            image_x = (self.screen_width - image_width) // 2
            image_y = (self.screen_height - image_height) // 2
            
            # Draw border with glow effect
            pygame.draw.rect(self.screen, current_image["color"], (image_x, image_y, image_width, image_height), 3)
            
            # Draw main text
            main_text = self.font_large.render(current_image["text"], True, current_image["color"])
            main_rect = main_text.get_rect(center=(self.screen_width // 2, image_y + 150))
            self.screen.blit(main_text, main_rect)
            
            # Draw subtext
            sub_text = self.font_medium.render(current_image["subtext"], True, self.WHITE)
            sub_rect = sub_text.get_rect(center=(self.screen_width // 2, image_y + 200))
            self.screen.blit(sub_text, sub_rect)
        
        # Draw animated graphs in corners
        self.graph_timer += 1
        if self.graph_timer > 300:  # Show graphs every 5 seconds
            self.show_graphs = not self.show_graphs
            self.graph_timer = 0
        
        if self.show_graphs:
            # Draw system monitor in top-right corner
            self.graph_animations.draw_system_monitor(self.screen, 
                                                    self.screen_width - 320, 20, 300, 320)
            
            # Draw radar sweep in bottom-left corner
            self.graph_animations.draw_radar_sweep(self.screen, 150, self.screen_height - 150, 100)
            
            # Draw pulse animation in bottom-right corner
            self.graph_animations.draw_pulse_animation(self.screen, 
                                                     self.screen_width - 100, self.screen_height - 100)
        
        # Draw slideshow controls
        controls_text = "Press SPACE for next image | G for graphs | ESC to exit"
        controls_surface = self.font_small.render(controls_text, True, self.GRAY)
        controls_rect = controls_surface.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        self.screen.blit(controls_surface, controls_rect)
        
        # Auto-advance slideshow
        self.image_timer += 1
        if self.image_timer > 180:  # 3 seconds at 60 FPS
            self.next_image()
            self.image_timer = 0
    
    def next_image(self):
        """Move to the next image in the slideshow"""
        self.current_image_index = (self.current_image_index + 1) % len(self.slideshow_images)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and self.current_mode == "slideshow":
                    self.next_image()
                    self.sound_effects.play_beep()
                elif event.key == pygame.K_RETURN and self.current_mode == "startup":
                    # Skip startup
                    self.current_mode = "slideshow"
                    self.sound_effects.play_success()
                elif event.key == pygame.K_g and self.current_mode == "slideshow":
                    # Toggle graphs
                    self.show_graphs = not self.show_graphs
                    self.sound_effects.play_beep()
                elif event.key == pygame.K_s and self.current_mode == "slideshow":
                    # Toggle sound
                    self.sound_effects.toggle_sounds()
                    self.sound_effects.play_beep()
    
    def update(self):
        """Update game state"""
        if self.current_mode == "startup":
            self.update_typing_animation()
        elif self.current_mode == "slideshow":
            self.update_matrix_effect()
            self.graph_animations.update()
    
    def draw(self):
        """Draw the current frame"""
        if self.current_mode == "startup":
            self.draw_startup_screen()
        elif self.current_mode == "slideshow":
            self.draw_slideshow()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        print("🚀 Starting FunHackerMode...")
        print("💻 Initializing matrix protocols...")
        print("🔐 Accessing mainframe...")
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        print("👋 FunHackerMode terminated. Thanks for hacking!")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    try:
        hacker_mode = FunHackerMode()
        hacker_mode.run()
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        pygame.quit()
        sys.exit()
    except Exception as e:
        print(f"❌ Error: {e}")
        pygame.quit()
        sys.exit()
