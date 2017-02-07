# pyong.py
Python Pong for Raspberry Pi, Unicorn HAT LED Matrix, and Logitech F310 Joystick

[Video Demo](https://www.youtube.com/watch?v=E44lkGB7eHw)

# Installation and Setup
pyong requires Python 2.7 (Available from [Python.org](https://www.python.org/), a Raspberry Pi 3 Model B (Though other Pi models may work the same), the Pimoroni Unicorn Hat Module (available from [Pimoroni](https://shop.pimoroni.com/products/unicorn-hat) or [Adafruit (US)](https://www.adafruit.com/product/2288)), and a Logitech F310 Game Controller. 

pyong's Python dependencies are Unicornhat (Installation instructions on [GitHub](https://github.com/pimoroni/unicorn-hat)) and evdev (Installation instructions on [Read The Docs](https://python-evdev.readthedocs.io/en/latest/install.html)). 

The Logitech Game Controller needs to be plugged into the first (0th) USB port on the Raspberry Pi (The top-left slot on the 3B). You can check that it is plugged into this slot by typing ```ls /dev/input/``` in a terminal to check for ```event0```. Make sure no other USB devices are plugged in. The controller also needs to be on Direct-Input (D) mode, and the Mode light OFF. 

The Unicorn HAT needs to be plugged into the GPIO pins as per the instructions available on their website. 

# Running pyong
Run ```sudo python pyong.py``` in the terminal. The Unicorn HAT requires root priveledges to run on the Pi. Press ```ctrl+c``` to exit the program. 

# Limitations
+ Sometimes the ball appears on the wrong side of the matrix for 1 frame when volleying a fastball located along an edge. 
+ There is currently no way to keep score or exit the game without keyboard interupt

# Future additions
+ Add score tracking
+ Add pause via controller
+ Add exit via controller 
+ Fix bug where ball appears on wrong edge of matrix for one frame
