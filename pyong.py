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
# Unicorn library available from GitHib https://github.com/pimoroni/unicorn-hat
# installation instructions contained in README.md
#
# evdev library available from Read The Docs https://python-evdev.readthedocs.io/en/latest/install.html
#
# Logitech gamepad F310 must be plugged into event0 (0th usb slot on Pi) and be
# in D-input (direct) mode with the mode-light toggled OFF
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
from copy import deepcopy

# Define global constants
DEBUG_MODE = True   # set to false for non-verbose running
ONE_SECOND = 1      # 1000ms = 1 second
PX_ON = 1
PX_OFF = 0
LSTICK = 1
RSTICK = 5
BALLSPEED = 5

# TODO: Class for paddle
class Paddle:
    """Pong Paddle"""
    def __init__(self, size, gamesize):
        self.size = size
        self.pos = 0
        self.gamesize = gamesize
        debugPrint("Creating new paddle.")

    def updatePosition(self, amount):
        if ((self.pos + amount) >= 0) and ((self.pos + self.size + amount) <= (self.gamesize)):
            self.pos += amount

    # returns a list of y-coordinates that the paddle occupies
    def getCoords(self):
        coords = []
        for i in range(0, self.size):
            coords.append(self.pos + i)
        return coords



# Class for ball
class Ball:
    """Pong Ball"""
    def __init__(self, posx, posy, ydir, xdir, lpaddle, rpaddle, gamesize, ballspeed):
        self.posx = posx
        self.posy = posy
        self.lpaddle = lpaddle
        self.rpaddle = rpaddle
        self.gamesize = gamesize
        self.ydir = ydir
        self.xdir = xdir
        self.counter = 0
        self.ballspeed = ballspeed
        debugPrint("Creating new ball.")
        # TODO set a travel direction


    def move(self):
        if self.counter == self.ballspeed:
            if (self.posy + self.ydir) < 0:
                self.ydir = 1

            if (self.posy + self.ydir) >= self.gamesize:
                self.ydir = -1

            if (self.posx + self.xdir) == 0:
                if self.posy in self.lpaddle.getCoords():
                    self.xdir = 1

                    if self.ydir == 0:
                        self.ydir = random.sample([-1,1],1)[0]
                    elif random.randint(1,5) == 3:
                        self.ydir = 0


            if (self.posx + self.xdir) == (self.gamesize - 1):
                if self.posy in self.rpaddle.getCoords():
                    self.xdir = -1

                    if self.ydir == 0:
                        self.ydir = random.sample([-1,1],1)[0]
                    elif random.randint(1,5) == 3:
                        self.ydir = 0

            self.posx += self.xdir
            self.posy += self.ydir
            self.counter = 0
        self.counter += 1

# implement with threads checking input and updating an accessible object
# to let any observers know whether each stick is pressed and in what direction
# so we can access it during the main game loop. Is this the observer pattern?
class JoystickInformant:
    """
    -1 = up
    0 = neutral
    1 = down
    """
    def __init__(self):
        self.position = 0
    def notifyPosition(self, position):
        self.position = position

class JoystickHandler:
    """
    takes 2 params, informant, vector
    informant should be a JoystickInformant that was instantiated previously
    vector should be the code value of a joystick on the logitech remote
        -> currently accepts values 5 or 17

    """
    def __init__(self, informant, vector):
        self.stick = -1
        if vector == RSTICK:
            self.stick = 1
        elif vector == LSTICK:
            self.stick = 0

        debugPrint("Creating JoystickHandler\nVector: "+str(vector)+"\nstick: "+str(self.stick))

        if (self.stick == 1) or (self.stick == 0):
            try:
                thread.start_new_thread(self._listen, (informant,))
            except:
                print "Error: unable to start thread"
        else:
            print "Error, invalid joystick vector given"

    def _listen(self, informant):
        debugPrint("Starting new thread...")
        # assume event 0 (ie. the first usb port on the pi)
        dev = InputDevice('/dev/input/event0')
        # infinite loop reading controller input
        for event in dev.read_loop():
            # only read absolute axis movements, if stick 0, only read event code 17
            if (event.type == ecodes.EV_ABS) and (self.stick == 0):
                if event.code == LSTICK:
                    if event.value < 107:
                        # notify up
                        informant.notifyPosition(-1)
                        #debugPrint("right stick up")
                    elif event.value >= 107 and event.value <= 147:
                        # notify neutral
                        informant.notifyPosition(0)
                        #debugPrint("right stick neutral")
                    elif event.value > 147:
                        # notify down
                        informant.notifyPosition(1)
                        #debugPrint("right stick down")


            # otherwise we try to read absolute axis movements where stick 1, and reading event code 5
            elif (event.type == ecodes.EV_ABS) and (self.stick == 1):
                if event.code == RSTICK:

                    if event.value < 107:
                        # notify up
                        informant.notifyPosition(-1)
                        #debugPrint("right stick up")
                    elif event.value >= 107 and event.value <= 147:
                        # notify neutral
                        informant.notifyPosition(0)
                        #debugPrint("right stick neutral")
                    elif event.value > 147:
                        # notify down
                        informant.notifyPosition(1)
                        #debugPrint("right stick down")




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
        debugPrint("Creating new game...")

        # build objects for the game
        self.left_paddle = Paddle(paddlesize, gamesize)
        self.right_paddle = Paddle(paddlesize, gamesize)
        self.ball = Ball((gamesize / 2), (gamesize / 2), -1, -1, self.left_paddle, self.right_paddle, gamesize, BALLSPEED)
        self.game_board = self._generateBoard()


        # instantiate our listeners and informants
        self.informant_left = JoystickInformant()
        self.informant_right = JoystickInformant()
        # calling anonymous JoystickHandler classes starts a thread that listens and
        # notifies the observer as we go. We can now start looking at our informant
        # in the game loop
        JoystickHandler(self.informant_left, LSTICK)
        JoystickHandler(self.informant_right, RSTICK)

    # start() method to be called when starting a new game.
    # No params
    # Contains main game loop, calls other logical handlers found within a
    # PongGame object.
    def start(self):
        self._displaySplashScreen()

        # main game loop
        # TODO: Exit based on a score reached so python can exit cleanly
        while (True):
            # update paddle positions based on controller input
            self.left_paddle.updatePosition(self.informant_left.position)
            self.right_paddle.updatePosition(self.informant_right.position)

            # update the ball position
            self.ball.move()

            # create and show board
            self._getPositions()
            self._showBoard()


            # check for victory and display victory screen
            self._checkVictory()

            # clear the board
            self.game_board = self._generateBoard()

            # sleep for 1 / FPS seconds
            time.sleep(ONE_SECOND / self.speed)

    # generates a blank board, returns as a 2d list of PX_OFF
    def _generateBoard(self):
        temp_list = []
        for i in range(0, self.gamesize):
            temp_list.append([])
            for j in range(0, self.gamesize):
                temp_list[i].append(PX_OFF)
        return temp_list

    def _getPositions(self):
        # set left paddle pixels
        for i in self.left_paddle.getCoords():
            self.game_board[i][0] = PX_ON

        # set right paddle pixels
        for i in self.right_paddle.getCoords():
            self.game_board[i][self.gamesize-1] = PX_ON

        # set ball pixels
        self.game_board[self.ball.posy][self.ball.posx] = PX_ON

    # displays the current state of the board
    def _showBoard(self):

        display_array = deepcopy(self.game_board)
        for i in range(0, len(display_array)):
            for j in range(0, len(display_array[i])):
                if display_array[i][j] == PX_OFF:
                    display_array[i][j] = [0,0,0]
                if display_array[i][j] == PX_ON:
                    display_array[i][j] = [255,255,255]
        unicorn.set_pixels(display_array)
        unicorn.show()



    def _checkVictory(self):

        if (self.ball.posx == 0):
            self._displaySplashScreen()
            startx = random.randint(((self.gamesize / 2)-1),(self.gamesize/2))
            starty = random.randint(((self.gamesize / 2)-1),(self.gamesize/2))
            startdir = random.randint(-1,1)
            self.ball = Ball(startx, starty, startdir, 1, self.left_paddle, self.right_paddle, self.gamesize, BALLSPEED)

        if (self.ball.posx == (self.gamesize - 1)):
            self._displaySplashScreen()
            startx = random.randint(((self.gamesize / 2)-1),(self.gamesize/2))
            starty = random.randint(((self.gamesize / 2)-1),(self.gamesize/2))
            startdir = random.randint(-1,1)
            self.ball = Ball(startx, starty, startdir, -1, self.left_paddle, self.right_paddle, self.gamesize, BALLSPEED)


    def _displaySplashScreen(self):
        debugPrint("Displaying splash screen!")

        self._set_all(255,0,0)
        unicorn.show()
        time.sleep(ONE_SECOND / 3.0)
        self._set_all(0,255,0)
        unicorn.show()
        time.sleep(ONE_SECOND / 3.0)
        self._set_all(0,0,255)
        unicorn.show()
        time.sleep(ONE_SECOND / 3.0)
        self._set_all(255,255,255)
        unicorn.show()
        time.sleep(ONE_SECOND / 3.0)
        unicorn.off()
        debugPrint("Splash screen finished")

    def _set_all(self, r,g,b):
        for i in range(0,self.gamesize):
            for j in range(0,self.gamesize):
                unicorn.set_pixel(i,j,r,g,b)


def debugPrint(print_string):
    if (DEBUG_MODE):
        print print_string

def main():
    # unicorn setup instructions
    width, height = unicorn.get_shape()
    unicorn.brightness(0.3)


    # set constants
    FPS = 14.0
    PADDLESIZE = 2

    # set gamesize, make sure we use the shortest side so there are no issues
    # the board should be an 8x8 square but just in case it isn't...
    gamesize = width
    if (width > height):
        gamesize = height

    # print game information
    debugPrint("Game info:\nGame size="+str(gamesize)+"\nFPS="+str(FPS)+"\nPaddle size="+str(PADDLESIZE))

    # create and start a new game with our previously determined constants and
    # calculated values
    game = PongGame(FPS, gamesize, PADDLESIZE)
    game.start()

    # turn off the unicorn
    unicorn.off()
main()
