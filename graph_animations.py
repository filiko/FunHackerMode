#!/usr/bin/env python3
"""
Graph Animations Module for FunHackerMode
=========================================

This module provides animated data visualizations that look like
real-time system monitoring, network traffic, and data analysis.
"""

import pygame
import math
import random
import numpy as np
from typing import List, Tuple

class GraphAnimations:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Colors
        self.GREEN = (0, 255, 0)
        self.BRIGHT_GREEN = (50, 255, 50)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 100, 255)
        self.YELLOW = (255, 255, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (100, 100, 100)
        
        # Graph data
        self.cpu_data = []
        self.memory_data = []
        self.network_data = []
        self.max_data_points = 100
        
        # Animation variables
        self.time_counter = 0
        self.pulse_radius = 0
        self.pulse_growing = True
        
    def update(self):
        """Update all graph animations"""
        self.time_counter += 1
        
        # Update pulse animation
        if self.pulse_growing:
            self.pulse_radius += 2
            if self.pulse_radius > 50:
                self.pulse_growing = False
        else:
            self.pulse_radius -= 2
            if self.pulse_radius < 0:
                self.pulse_growing = True
        
        # Update data arrays
        self.update_cpu_data()
        self.update_memory_data()
        self.update_network_data()
    
    def update_cpu_data(self):
        """Update CPU usage simulation"""
        # Simulate realistic CPU usage with some randomness
        base_usage = 30 + 20 * math.sin(self.time_counter * 0.1)
        noise = random.uniform(-10, 10)
        cpu_usage = max(0, min(100, base_usage + noise))
        
        self.cpu_data.append(cpu_usage)
        if len(self.cpu_data) > self.max_data_points:
            self.cpu_data.pop(0)
    
    def update_memory_data(self):
        """Update memory usage simulation"""
        base_usage = 50 + 15 * math.sin(self.time_counter * 0.05)
        noise = random.uniform(-5, 5)
        memory_usage = max(0, min(100, base_usage + noise))
        
        self.memory_data.append(memory_usage)
        if len(self.memory_data) > self.max_data_points:
            self.memory_data.pop(0)
    
    def update_network_data(self):
        """Update network traffic simulation"""
        base_traffic = 40 + 30 * math.sin(self.time_counter * 0.08)
        noise = random.uniform(-15, 15)
        network_traffic = max(0, min(100, base_traffic + noise))
        
        self.network_data.append(network_traffic)
        if len(self.network_data) > self.max_data_points:
            self.network_data.pop(0)
    
    def draw_system_monitor(self, screen: pygame.Surface, x: int, y: int, width: int, height: int):
        """Draw a system monitoring dashboard"""
        # Background
        pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height))
        pygame.draw.rect(screen, self.GREEN, (x, y, width, height), 2)
        
        # Title
        font = pygame.font.Font(None, 24)
        title = font.render("SYSTEM MONITOR", True, self.BRIGHT_GREEN)
        screen.blit(title, (x + 10, y + 10))
        
        # CPU Graph
        self.draw_line_graph(screen, x + 10, y + 40, width - 20, 80, 
                           self.cpu_data, self.RED, "CPU Usage")
        
        # Memory Graph
        self.draw_line_graph(screen, x + 10, y + 130, width - 20, 80, 
                           self.memory_data, self.BLUE, "Memory Usage")
        
        # Network Graph
        self.draw_line_graph(screen, x + 10, y + 220, width - 20, 80, 
                           self.network_data, self.YELLOW, "Network Traffic")
    
    def draw_line_graph(self, screen: pygame.Surface, x: int, y: int, width: int, height: int, 
                       data: List[float], color: Tuple[int, int, int], label: str):
        """Draw a line graph with the given data"""
        if len(data) < 2:
            return
        
        # Draw label
        font = pygame.font.Font(None, 18)
        label_surface = font.render(label, True, self.WHITE)
        screen.blit(label_surface, (x, y - 20))
        
        # Draw graph background
        pygame.draw.rect(screen, (20, 20, 20), (x, y, width, height))
        pygame.draw.rect(screen, self.GRAY, (x, y, width, height), 1)
        
        # Draw grid lines
        for i in range(0, width, 20):
            pygame.draw.line(screen, (40, 40, 40), (x + i, y), (x + i, y + height))
        for i in range(0, height, 20):
            pygame.draw.line(screen, (40, 40, 40), (x, y + i), (x + width, y + i))
        
        # Draw data line
        if len(data) > 1:
            points = []
            for i, value in enumerate(data):
                graph_x = x + int((i / (len(data) - 1)) * width)
                graph_y = y + height - int((value / 100) * height)
                points.append((graph_x, graph_y))
            
            if len(points) > 1:
                pygame.draw.lines(screen, color, False, points, 2)
                
                # Draw current value
                if points:
                    current_point = points[-1]
                    pygame.draw.circle(screen, color, current_point, 3)
                    
                    # Draw value text
                    value_text = f"{data[-1]:.1f}%"
                    value_surface = font.render(value_text, True, color)
                    screen.blit(value_surface, (current_point[0] + 5, current_point[1] - 10))
    
    def draw_radar_sweep(self, screen: pygame.Surface, center_x: int, center_y: int, radius: int):
        """Draw a radar sweep animation"""
        # Draw radar background
        pygame.draw.circle(screen, (0, 50, 0), (center_x, center_y), radius)
        pygame.draw.circle(screen, self.GREEN, (center_x, center_y), radius, 2)
        
        # Draw radar grid
        for i in range(1, 4):
            pygame.draw.circle(screen, (0, 100, 0), (center_x, center_y), radius * i // 4, 1)
        
        # Draw crosshairs
        pygame.draw.line(screen, (0, 100, 0), (center_x - radius, center_y), (center_x + radius, center_y))
        pygame.draw.line(screen, (0, 100, 0), (center_x, center_y - radius), (center_x, center_y + radius))
        
        # Draw sweep line
        sweep_angle = (self.time_counter * 2) % 360
        sweep_rad = math.radians(sweep_angle)
        end_x = center_x + int(radius * math.cos(sweep_rad))
        end_y = center_y + int(radius * math.sin(sweep_rad))
        pygame.draw.line(screen, self.BRIGHT_GREEN, (center_x, center_y), (end_x, end_y), 2)
        
        # Draw random blips
        for _ in range(random.randint(2, 5)):
            blip_angle = random.uniform(0, 2 * math.pi)
            blip_distance = random.uniform(0.3, 0.9) * radius
            blip_x = center_x + int(blip_distance * math.cos(blip_angle))
            blip_y = center_y + int(blip_distance * math.sin(blip_angle))
            pygame.draw.circle(screen, self.YELLOW, (blip_x, blip_y), 2)
    
    def draw_pulse_animation(self, screen: pygame.Surface, center_x: int, center_y: int):
        """Draw a pulsing animation"""
        # Draw multiple concentric circles with decreasing alpha
        for i in range(3):
            radius = self.pulse_radius + (i * 20)
            alpha = max(0, 255 - (i * 80))
            
            # Create a surface with alpha
            pulse_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(pulse_surface, (*self.GREEN, alpha), (radius, radius), radius, 2)
            screen.blit(pulse_surface, (center_x - radius, center_y - radius))
    
    def draw_data_stream(self, screen: pygame.Surface, x: int, y: int, width: int, height: int):
        """Draw a data stream visualization"""
        # Background
        pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height))
        pygame.draw.rect(screen, self.GREEN, (x, y, width, height), 1)
        
        # Title
        font = pygame.font.Font(None, 20)
        title = font.render("DATA STREAM", True, self.BRIGHT_GREEN)
        screen.blit(title, (x + 10, y + 10))
        
        # Draw streaming data
        for i in range(0, width - 20, 30):
            data_height = random.randint(10, height - 40)
            data_y = y + height - data_height - 20
            pygame.draw.rect(screen, self.GREEN, (x + 10 + i, data_y, 20, data_height))
            
            # Add some sparkle effect
            if random.random() < 0.1:
                sparkle_x = x + 10 + i + 10
                sparkle_y = data_y + random.randint(0, data_height)
                pygame.draw.circle(screen, self.WHITE, (sparkle_x, sparkle_y), 1)
