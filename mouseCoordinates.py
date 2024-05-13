import pyautogui

print('Press Ctrl-C to quit.')

try:
    # Take a single screenshot
    screenshot = pyautogui.screenshot()
    while True:
        pyautogui.PAUSE = 1
        pyautogui.FAILSAFE = True

        width, height = pyautogui.size()

        # Get mouse position
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        pixelColor = screenshot.getpixel((x, y))
        positionStr += ' RGB: (' + str(pixelColor[0]).rjust(3)
        positionStr += ', ' + str(pixelColor[1]).rjust(3)
        positionStr += ', ' + str(pixelColor[2]).rjust(3) + ')'
        print('\b' * len(positionStr), end='', flush=True)
        print(positionStr, end='')    
        
except KeyboardInterrupt:
    print('\nDone.')

