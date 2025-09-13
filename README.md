# FunHackerMode 🚀

An epic Python program that simulates a cool hacker interface with animated slideshows, Matrix-style effects, and data visualizations. Perfect for impressing friends or just having fun with a "hacker aesthetic"!

## Features ✨

- **Animated Slideshow**: Display your custom images with smooth transitions
- **Matrix Effect**: Falling code animation in the background
- **System Monitoring**: Real-time animated graphs showing CPU, memory, and network usage
- **Radar Sweep**: Cool radar animation with random blips
- **Sound Effects**: Typing sounds, beeps, and other audio feedback
- **Terminal Aesthetic**: Green-on-black hacker theme
- **Startup Sequence**: Epic boot sequence that looks like you're launching serious software

## Quick Start 🎯

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Program**:
   ```bash
   python launcher.py
   ```

3. **Or run directly**:
   ```bash
   python main.py
   ```

## Controls 🎮

- **SPACE**: Next image in slideshow
- **ENTER**: Skip startup sequence
- **ESC**: Exit program
- **Ctrl+C**: Force quit

## Customization 🎨

### Adding Your Own Images

1. Place your image files in the project directory
2. Update the `load_images()` method in `main.py` to load your actual images
3. Modify the slideshow data structure to include your image paths

### Modifying the Slideshow Content

Edit the `slideshow_images` list in the `load_images()` method:

```python
self.slideshow_images = [
    {"text": "YOUR TEXT HERE", "color": self.BLUE, "subtext": "Subtitle"},
    # Add more slides...
]
```

### Changing Colors

Modify the color constants in `main.py`:

```python
self.GREEN = (0, 255, 0)        # Matrix green
self.BLUE = (0, 100, 255)       # Accent blue
self.RED = (255, 0, 0)          # Alert red
# etc.
```

## File Structure 📁

```
FunHackerMode/
├── main.py              # Main program with slideshow and Matrix effects
├── graph_animations.py  # Data visualization and monitoring graphs
├── sound_effects.py     # Audio effects and sound generation
├── launcher.py          # Cool startup script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Technical Details 🔧

- **Framework**: Pygame for graphics and animations
- **Graphics**: Real-time rendering with 60 FPS
- **Audio**: Synthetic sound generation using pygame
- **Animations**: Smooth transitions and effects
- **Compatibility**: Windows, macOS, Linux

## Troubleshooting 🛠️

### Common Issues

1. **"Module not found" errors**: Run `pip install -r requirements.txt`
2. **No sound**: Check your system audio settings
3. **Performance issues**: Reduce the number of Matrix characters in `init_matrix_effect()`

### Dependencies

- Python 3.7+
- pygame 2.5.2+
- numpy 1.24.3+
- matplotlib 3.7.2+
- Pillow 10.0.0+

## Contributing 🤝

Feel free to fork this project and add your own features! Some ideas:

- Add more animation effects
- Implement image loading for actual photos
- Add more sound effects
- Create different themes
- Add networking simulation

## License 📄

This project is open source and available under the MIT License.

## Fun Facts 🎉

- The Matrix effect uses random ASCII characters (33-126)
- The system monitoring graphs simulate realistic data patterns
- The radar sweep rotates at 2 degrees per frame
- Sound effects are generated synthetically using mathematical functions

---

**Enjoy your FunHackerMode experience!** 🎮✨

*Remember: This is just for fun - no actual hacking involved! 😄*
