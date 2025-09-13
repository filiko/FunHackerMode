#!/usr/bin/env python3
"""
FunHackerMode Launcher
======================

A cool startup script that makes it look like you're launching
some serious hacking software.
"""

import os
import sys
import time
import random
import subprocess

def print_slow(text, delay=0.03):
    """Print text with a typing effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def print_colored(text, color_code):
    """Print colored text (if terminal supports it)"""
    if os.name == 'nt':  # Windows
        try:
            import colorama
            colorama.init()
            print(f"{color_code}{text}\033[0m")
        except ImportError:
            print(text)
    else:  # Unix-like systems
        print(f"{color_code}{text}\033[0m")

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    """Show the FunHackerMode banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    ███████╗██╗   ██╗███╗   ██╗██╗  ██╗ █████╗  ██████╗██╗  ██╗║
    ║    ██╔════╝██║   ██║████╗  ██║██║ ██╔╝██╔══██╗██╔════╝██║ ██╔╝║
    ║    █████╗  ██║   ██║██╔██╗ ██║█████╔╝ ███████║██║     █████╔╝ ║
    ║    ██╔══╝  ██║   ██║██║╚██╗██║██╔═██╗ ██╔══██║██║     ██╔═██╗ ║
    ║    ██║     ╚██████╔╝██║ ╚████║██║  ██╗██║  ██║╚██████╗██║  ██╗║
    ║    ╚═╝      ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝║
    ║                                                              ║
    ║                    ███╗   ███╗ ██████╗ ██████╗ ███████╗       ║
    ║                    ████╗ ████║██╔═══██╗██╔══██╗██╔════╝       ║
    ║                    ██╔████╔██║██║   ██║██║  ██║█████╗         ║
    ║                    ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝         ║
    ║                    ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗       ║
    ║                    ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝       ║
    ║                                                              ║
    ║                        Version 1.0.0                        ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print_colored(banner, '\033[92m')  # Green color

def simulate_boot_sequence():
    """Simulate a boot sequence"""
    boot_messages = [
        "Initializing FunHackerMode...",
        "Loading matrix protocols...",
        "Establishing secure connection...",
        "Accessing mainframe...",
        "Decrypting data streams...",
        "Loading graphics subsystem...",
        "Initializing sound effects...",
        "Preparing slideshow engine...",
        "System ready. Welcome to the matrix."
    ]
    
    for message in boot_messages:
        print_slow(f"[INFO] {message}", 0.05)
        time.sleep(random.uniform(0.5, 1.5))
    
    print()

def check_dependencies():
    """Check if required dependencies are installed"""
    print_colored("Checking dependencies...", '\033[93m')  # Yellow
    
    required_packages = ['pygame', 'numpy', 'matplotlib', 'Pillow']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print_colored(f"✓ {package} - OK", '\033[92m')
        except ImportError:
            print_colored(f"✗ {package} - MISSING", '\033[91m')
            missing_packages.append(package)
    
    if missing_packages:
        print_colored(f"\nMissing packages: {', '.join(missing_packages)}", '\033[91m')
        print_colored("Installing missing packages...", '\033[93m')
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print_colored("Dependencies installed successfully!", '\033[92m')
        except subprocess.CalledProcessError:
            print_colored("Failed to install dependencies. Please install manually:", '\033[91m')
            print_colored(f"pip install {' '.join(missing_packages)}", '\033[93m')
            return False
    
    return True

def main():
    """Main launcher function"""
    clear_screen()
    show_banner()
    
    print_colored("Welcome to FunHackerMode - The Ultimate Hacker Experience!", '\033[96m')
    print_colored("=" * 60, '\033[96m')
    print()
    
    # Check dependencies
    if not check_dependencies():
        print_colored("Cannot proceed without required dependencies.", '\033[91m')
        return
    
    print()
    simulate_boot_sequence()
    
    print_colored("Launching FunHackerMode...", '\033[92m')
    print_colored("Press Ctrl+C to exit at any time.", '\033[93m')
    print()
    
    # Launch the main program
    try:
        import main
        main.FunHackerMode().run()
    except KeyboardInterrupt:
        print_colored("\nFunHackerMode terminated by user.", '\033[93m')
    except Exception as e:
        print_colored(f"\nError launching FunHackerMode: {e}", '\033[91m')
        print_colored("Please check your installation and try again.", '\033[93m')

if __name__ == "__main__":
    main()
