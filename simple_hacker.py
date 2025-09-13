#!/usr/bin/env python3
"""
Simple Hacker Mode - Image Slideshow with Crash Simulation
=========================================================

A simple program that:
1. Shows images from the Logos folder
2. Simulates a program crash with error messages
3. Shows blue screen images
"""

import pygame
import sys
import os
import time
import random
import glob

# Initialize Pygame
pygame.init()

class SimpleHackerMode:
    def __init__(self):
        # Get full screen dimensions
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption("System.exe - Running...")
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        
        # Fonts
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        
        # Animation variables
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_mode = "popup"
        self.image_timer = 0
        self.crash_timer = 0
        self.error_messages = []
        self.blue_screen_index = 0
        
        # Grid variables - use actual screen dimensions
        self.grid_width = self.screen_width
        self.grid_height = self.screen_height
        self.active_images = []  # List of (x, y, image, timer)
        self.popup_timer = 0
        self.max_images = 10  # 10 images on screen at a time (all of them)
        self.image_indices = []  # Array of integers representing image indices
        self.shown_images = set()  # Track which images have been shown
        self.all_images_shown = False  # Flag to track if all images have been shown
        
        # Load images
        self.load_images()
        
    def load_images(self):
        """Load all images from the Logos folder"""
        self.logo_images = []
        self.blue_screen_images = []
        
        # Load logo images
        logo_paths = glob.glob("Logos/*.png") + glob.glob("Logos/*.jpg") + glob.glob("Logos/*.webp")
        for path in logo_paths:
            try:
                image = pygame.image.load(path)
                # Scale image to fit screen while maintaining aspect ratio
                image = self.scale_image(image, 800, 600)
                self.logo_images.append(image)
                print(f"Loaded: {path}")
            except Exception as e:
                print(f"Could not load {path}: {e}")
        
        # Load blue screen images
        blue_screen_paths = ["BlueScreen1.jpg", "BlueScreen2.png"]
        for path in blue_screen_paths:
            if os.path.exists(path):
                try:
                    image = pygame.image.load(path)
                    # Scale to full screen
                    image = pygame.transform.scale(image, (self.screen_width, self.screen_height))
                    self.blue_screen_images.append(image)
                    print(f"Loaded blue screen: {path}")
                except Exception as e:
                    print(f"Could not load {path}: {e}")
        
        print(f"Loaded {len(self.logo_images)} logo images and {len(self.blue_screen_images)} blue screen images")
        
        # Initialize image indices array - one number per image file
        if self.logo_images:
            self.image_indices = list(range(len(self.logo_images)))  # [0,1,2,3,4,5,6,7,8,9]
            self.shuffled_indices = self.image_indices.copy()
            random.shuffle(self.shuffled_indices)
            self.current_index = 0
            print(f"Total images: {len(self.logo_images)}")
            print(f"Image indices array: {self.image_indices}")
            print(f"Fixed shuffled array: {self.shuffled_indices}")
            print(f"Each number corresponds to one image file:")
            for i, path in enumerate(glob.glob("Logos/*.png") + glob.glob("Logos/*.jpg") + glob.glob("Logos/*.webp")):
                if i < len(self.logo_images):
                    print(f"  {i}: {os.path.basename(path)}")
    
    def scale_image(self, image, max_width, max_height):
        """Scale image to fit within max dimensions while maintaining aspect ratio"""
        width, height = image.get_size()
        
        # Calculate scaling factor
        scale_x = max_width / width
        scale_y = max_height / height
        scale = min(scale_x, scale_y)
        
        # Scale image
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        return pygame.transform.scale(image, (new_width, new_height))
    
    def get_random_position(self, image_width, image_height):
        """Get a random position within 1920x1080 bounds using actual image size"""
        # Try multiple times to find a non-overlapping position
        for attempt in range(50):  # Try up to 50 times
            max_x = self.grid_width - image_width
            max_y = self.grid_height - image_height
            
            # Ensure we don't go negative
            if max_x < 0:
                max_x = 0
            if max_y < 0:
                max_y = 0
                
            x = random.randint(0, max_x)
            y = random.randint(0, max_y)
            
            # Check if this position overlaps with existing images
            overlaps = False
            for existing_x, existing_y, existing_image, _ in self.active_images:
                # Check if rectangles overlap
                if (x < existing_x + existing_image.get_width() and 
                    x + image_width > existing_x and
                    y < existing_y + existing_image.get_height() and 
                    y + image_height > existing_y):
                    overlaps = True
                    break
            
            if not overlaps:
                return x, y
        
        # If we couldn't find a non-overlapping position, return any valid position
        max_x = self.grid_width - image_width
        max_y = self.grid_height - image_height
        if max_x < 0:
            max_x = 0
        if max_y < 0:
            max_y = 0
        
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        
        # Final safety check - ensure we never exceed screen bounds
        if x + image_width > self.grid_width:
            x = self.grid_width - image_width
        if y + image_height > self.grid_height:
            y = self.grid_height - image_height
        if x < 0:
            x = 0
        if y < 0:
            y = 0
            
        return x, y
    
    def draw_popup_images(self):
        """Draw images popping up randomly on screen"""
        self.screen.fill(self.WHITE)  # White background
        
        # Add new images gradually with fade-in effect
        self.popup_timer += 1
        if self.popup_timer > 30 and len(self.active_images) < self.max_images:  # Add new image every 0.5 seconds
            if self.logo_images and self.shuffled_indices:
                # Check if we've gone through all images in current shuffled array
                if self.current_index >= len(self.shuffled_indices):
                    # Reset to start of same shuffled array (no new array)
                    self.current_index = 0
                    print(f"Reset to start of same shuffled array: {self.shuffled_indices}")
                
                # Get next image from shuffled array
                image_index = self.shuffled_indices[self.current_index]
                self.current_index += 1
                
                image = self.logo_images[image_index]
                
                # Check if this is O4U4.jpg or O4U1.jpg - don't scale these
                image_paths = glob.glob("Logos/*.png") + glob.glob("Logos/*.jpg") + glob.glob("Logos/*.webp")
                if image_index < len(image_paths):
                    current_path = image_paths[image_index]
                    if "O4U4.jpg" in current_path or "O4U1.jpg" in current_path:
                        # Don't scale these images - use original size
                        scaled_image = image
                    else:
                        # Scale other images to twice as big (400x400 max)
                        scaled_image = self.scale_image(image, 400, 400)
                else:
                    # Fallback - scale all images
                    scaled_image = self.scale_image(image, 400, 400)
                
                # Get position using actual image dimensions
                x, y = self.get_random_position(scaled_image.get_width(), scaled_image.get_height())
                print(f"Image {image_index}: size={scaled_image.get_width()}x{scaled_image.get_height()}, pos=({x},{y}), max_x={x+scaled_image.get_width()}, max_y={y+scaled_image.get_height()}")
                self.active_images.append((x, y, scaled_image, 0))
            self.popup_timer = 0
        
        # Draw all active images
        for i, (x, y, image, timer) in enumerate(self.active_images):
            # Fade in effect
            alpha = min(255, timer * 5)
            if alpha > 0:
                # Create a surface with alpha
                image_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
                image_surface.blit(image, (0, 0))
                image_surface.set_alpha(alpha)
                self.screen.blit(image_surface, (x, y))
        
        # Update timers and remove old images
        self.active_images = [(x, y, image, timer + 1) for x, y, image, timer in self.active_images if timer < 360]  # Keep for 6 seconds
        
        # Check if we should move to blue screen phase (after all images have been shown and disappeared OR after 20 seconds)
        if (len(self.active_images) == 0 and self.current_index >= len(self.shuffled_indices)) or self.popup_timer > 1200:  # 20 seconds at 60 FPS
            self.current_mode = "blue_screen"
            self.blue_screen_index = 1  # Go directly to BlueScreen2.png (index 1)
            self.popup_timer = 0  # Reset timer
    
    def reset_popup_phase(self):
        """Reset the popup phase"""
        self.current_mode = "popup"
        self.active_images = []
        self.popup_timer = 0
        # Reset to start of same shuffled array (no new array)
        self.current_index = 0
        print(f"Reset to start of same shuffled array: {self.shuffled_indices}")
        print("Ready to populate all 10 images at once!")
    
    def generate_error_messages(self):
        """Generate random error messages for crash simulation"""
        error_templates = [
            "ERROR: Memory access violation at 0x{:08X}",
            "CRITICAL: Stack overflow detected",
            "FATAL: Null pointer dereference",
            "ERROR: Division by zero exception",
            "CRITICAL: Buffer overflow in module {}",
            "FATAL: Access violation reading 0x{:08X}",
            "ERROR: Invalid instruction at 0x{:08X}",
            "CRITICAL: Heap corruption detected",
            "FATAL: Unhandled exception in thread {}",
            "ERROR: Stack corruption at 0x{:08X}",
            "CRITICAL: Memory leak detected ({} bytes)",
            "FATAL: System call failed: {}",
            "ERROR: Invalid memory address 0x{:08X}",
            "CRITICAL: Deadlock detected in thread pool",
            "FATAL: Corrupted heap block at 0x{:08X}"
        ]
        
        self.error_messages = []
        for _ in range(20):  # Generate 20 error messages
            template = random.choice(error_templates)
            if "0x" in template:
                error_msg = template.format(random.randint(0x10000000, 0xFFFFFFFF))
            elif "{}" in template:
                error_msg = template.format(random.randint(1000, 99999))
            else:
                error_msg = template
            
            self.error_messages.append(error_msg)
    
    def draw_crash_screen(self):
        """Draw the crash simulation with error messages"""
        self.screen.fill(self.BLACK)
        
        # Draw error messages
        y_offset = 50
        messages_to_show = min(len(self.error_messages), self.crash_timer // 30)  # Show one message every 0.5 seconds
        
        for i in range(messages_to_show):
            if i < len(self.error_messages):
                error_text = self.error_messages[i]
                error_surface = self.font_small.render(error_text, True, self.RED)
                self.screen.blit(error_surface, (50, y_offset + i * 30))
        
        # Draw crash message
        if self.crash_timer > 600:  # After 10 seconds
            crash_text = "SYSTEM CRASH DETECTED"
            crash_surface = self.font_large.render(crash_text, True, self.RED)
            crash_rect = crash_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(crash_surface, crash_rect)
            
            # Draw blue screen message
            if self.crash_timer > 900:  # After 15 seconds
                blue_screen_text = "Initiating Blue Screen of Death..."
                blue_surface = self.font_medium.render(blue_screen_text, True, self.BLUE)
                blue_rect = blue_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
                self.screen.blit(blue_surface, blue_rect)
        
        # Move to blue screen after crash simulation
        if self.crash_timer > 1200:  # After 20 seconds
            self.current_mode = "blue_screen"
            self.blue_screen_index = 0
        
        self.crash_timer += 1
    
    def draw_blue_screen(self):
        """Draw the blue screen images"""
        if self.blue_screen_images:
            current_blue_screen = self.blue_screen_images[self.blue_screen_index]
            self.screen.blit(current_blue_screen, (0, 0))
            
            # Auto-advance blue screen images
            self.image_timer += 1
            if self.image_timer > 300:  # 5 seconds per blue screen
                self.blue_screen_index = (self.blue_screen_index + 1) % len(self.blue_screen_images)
                self.image_timer = 0
                
                # If we've shown all blue screens, restart
                if self.blue_screen_index == 0:
                    self.reset_popup_phase()
        else:
            # Fallback: draw a simple blue screen
            self.screen.fill(self.BLUE)
            error_text = "BLUE SCREEN OF DEATH"
            error_surface = self.font_large.render(error_text, True, self.WHITE)
            error_rect = error_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(error_surface, error_rect)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_F11:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    if self.current_mode == "popup":
                        self.current_mode = "blue_screen"
                        self.blue_screen_index = 1  # Go directly to BlueScreen2.png
                    elif self.current_mode == "blue_screen":
                        self.reset_popup_phase()
    
    def update(self):
        """Update game state"""
        pass  # No updates needed for current modes
    
    def draw(self):
        """Draw the current frame"""
        if self.current_mode == "popup":
            self.draw_popup_images()
        elif self.current_mode == "blue_screen":
            self.draw_blue_screen()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        print("🚀 Starting Simple Hacker Mode...")
        print("📸 Loading images from Logos folder...")
        print("🖥️  Preparing blue screen...")
        print("🖥️  Blue screen images ready...")
        print("\nControls:")
        print("- SPACE: Skip to next phase")
        print("- ESC or F11: Exit fullscreen")
        print("\nStarting image popup sequence...")
        print(f"Screen resolution: {self.screen_width}x{self.screen_height}")
        print(f"Grid: {self.grid_width}x{self.grid_height} (should be 1920x1080)")
        print(f"DEBUG: grid_width={self.grid_width}, grid_height={self.grid_height}")
        print(f"Max images on screen: {self.max_images} (gradual popup, no overlapping)")
        print(f"Image size: 400x400 pixels max (twice as big) - except O4U4.jpg and O4U1.jpg (original size)")
        print(f"Image duration: 6 seconds each")
        print(f"Auto-transition to blue screen: 20 seconds")
        print(f"Background: White")
        print(f"Total logos to cycle through: {len(self.logo_images)}")
        print(f"Shuffled array system: Fixed random order [0-9], positions randomized each cycle")
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        print("👋 Simple Hacker Mode terminated!")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    try:
        hacker_mode = SimpleHackerMode()
        hacker_mode.run()
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        pygame.quit()
        sys.exit()
    except Exception as e:
        print(f"❌ Error: {e}")
        pygame.quit()
        sys.exit()
