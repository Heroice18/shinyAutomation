# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pyautogui, time, os, logging, sys, random, copy
import win32con
import win32gui, imutils
import pydirectinput
import cv2
import numpy as np
import time
from pynput.keyboard import Key, Controller


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
# logging.disable(logging.DEBUG) # uncomment to block debug log messages

IS_POKEMON_SHINY = 'false'

checkCurrentImage = r"C:\Users\heroi\Pictures\Shiny_Hunting\Electrike test\checkCurrentImage.png"
baseShinyImage = r"C:\Users\heroi\Pictures\Shiny_Hunting\Electrike test\shinyImage.png"

checkTitleImage = r"C:\Users\heroi\Pictures\Shiny_Hunting\Start\checkTitleImage.png"
baseTitleImage = r"C:\Users\heroi\Pictures\Shiny_Hunting\Start\baseTitleImage.png"

baseImage = r"C:\Users\heroi\Pictures\Shiny_Hunting\Electrike test\baseImage.png"

keyboard = Controller()

GAME_REGION = ()

def imPath(filename):
    """A shortcut for joining the 'images/'' file path, since it is used so often. Returns the filename with 'images/' prepended."""
    # dirName = os.path.dirname('/Users/heroi/Pictures/Shiny_Hunting/')
    # return os.path.join(dirName, filename)
    return os.path.join('images', filename)

def getGameRegion():
    """Obtains the region that the Sushi Go Round game is on the screen and assigns it to GAME_REGION. The game must be at the start screen (where the PLAY button is visible)."""
    global GAME_REGION

    # identify the top-left corner
    logging.debug('Finding game region...')
    citraScreen = win32gui.FindWindow(None, "Citra Canary 2171 | Pokémon Alpha Sapphire")
    rect = win32gui.GetWindowRect(citraScreen)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    GAME_REGION = (x, y, w, h)
    logging.debug('Game region found: %s' % (GAME_REGION,))


def runLoop():
    count = 0;
    shinyCheck = False
    # pydirectinput.press('right')
    while not shinyCheck:
        # pydirectinput.press('a')
        image = pyautogui.screenshot(region=GAME_REGION)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cv2.imwrite(checkCurrentImage, image)
        image = imutils.resize(image, width=600)
        topScreen = image[63:206, 240:400]
        cv2.imwrite(checkCurrentImage, topScreen)
        if checkImage(baseShinyImage, checkCurrentImage):
            shinyCheck = True
        count += 1
        print(f"Is Shiny = {shinyCheck}, Count = {count}")

    return shinyCheck
    # pydirectinput.keyDown('q')
    # pydirectinput.keyDown('w')
    # pydirectinput.keyDown('n')
    # time.sleep(1000)
    # runLoop()

def checkImage(baseImage, currentImage):
    img = cv2.imread(baseImage)
    img2 = cv2.imread(currentImage)

    d1 = cv2.subtract(img, img2)
    return not np.any(d1)


def checkForStartMenu():
    titleCheck = False
    while not titleCheck:
        image = pyautogui.screenshot(region=GAME_REGION)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cv2.imwrite(checkTitleImage, image)
        image = imutils.resize(image, width=600)
        topScreen = image[33:236, 130:470]
        cv2.imwrite(checkTitleImage, topScreen)
        if checkImage(baseTitleImage, checkTitleImage):
            titleCheck = True
            print("Check Start Screen = Successful")



def resetGame():

    pydirectinput.keyDown('q')
    pydirectinput.keyDown('w')
    pydirectinput.keyDown('n')
    time.sleep(5)
    pydirectinput.keyUp('q')
    pydirectinput.keyUp('w')
    pydirectinput.keyUp('n')


def main():
    """Runs the entire program. The Sushi Go Round game must be visible on the screen and the PLAY button visible."""
    logging.debug('Program Started. Press Ctrl-C to abort at any time.')
    getGameRegion()
    foundShiny = False
    while not foundShiny:
        print("Checking Start Screen")
        # checkForStartMenu()
        foundShiny = runLoop()
        if not foundShiny:
            resetGame()

    # setupCoordinates()
    # startServing()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
