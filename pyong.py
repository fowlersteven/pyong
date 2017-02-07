# pyong.py
# Python Pong for Raspberry Pi with Unicorn HAT and Logitech Joystick
#
# Steven Fowler, 2017
#
# Version 0.1.0
#
# Pong game for python, implements OOP and concurrency to play a pong-like game
# on the Pimoroni Unicorn Hat LED Matrix. Requires: unicornhat module from
# Pimoroni, evdev, and root priviledges to run under the Raspberry Pi.
#
# Python library available from GitHib https://github.com/pimoroni/unicorn-hat
# installation instructions contained in README.md
#

# imports: required module for the HAT, time for the sleep method
# random for random number gen
# thread for threaded processes of joystick listeners
# evdev for dealing with our controller input
import unicornhat as unicorn
import time
import random
import thread
from evdev import InputDevice, categorize, ecodes

# Define global constants
DEBUG_MODE = True   # set to false for non-verbose running
ONE_SECOND = 1000   # 1000ms = 1 second

# TODO: Class for paddle
class Paddle:
    """Pong Paddle"""
    def __init__(self, size):
        self.size = size
        self.pos = 0

    def moveDown(self):
        pass

    def moveUp(self):
        pass


# TODO: Class for ball
class Ball:
    """Pong Ball"""
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
        # TODO set a travel direction


    def move(self):
        pass

# TODO: listeners for joystick input
# implement with threads checking input and updating an accessible object
# to let any observers know whether each stick is pressed and in what direction
# so we can access it during the main game loop. Is this the observer pattern?
class JoystickInformant:
    """
    """
    def __init__(self):
        self.position = 0
    def notifyPosition(self, position):
        self.position = position

class JoystickHandler:
    """
    """
    def __init__(self, informant, vector):
        pass
        # infinite loop checking joystick's status and notifying the informant


# TODO: Game logic
class PongGame:
    """
    Pong Game Logic class
    speed = frames per second float
    size = game square dimensions
    """

    def __init__(self, speed, gamesize, paddlesize):
        self.speed = speed
        self.gamesize = gamesize

        ball = Ball((gamesize / 2), (gamesize / 2))
        left_paddle = Paddle(paddlesize)
        right_paddle = Paddle(paddlesize)

    def start(self):
        while (True):
            pass
            time.sleep(ONE_SECOND / self.speed)

    def getPositions():
        pass

    def showBoard():
        pass

    def checkVictory():
        pass

def debugPrint(print_string):
    if (DEBUG_MODE):
        print print_string

def main():
    width, height = unicorn.get_shape()

    # set constants
    FPS = 24.0
    PADDLESIZE = 2

    # set gamesize, make sure we use the shortest side so there are no issues
    # the board should be an 8x8 square but just in case it isn't...
    gamesize = width
    if (width > height):
        gamesize = height


    game = PongGame(FPS, gamesize, PADDLESIZE)
    game.start()

    unicorn.off()
main()
