# An interface for GUI Automation based on pyautogui
Pyautogui: https://github.com/asweigart/pyautogui

It is used to control the mouse and keyboard to automate interactions with other applications:
- Click, double click on a point or a located image.
- Key combination, type a string, press a key, hold a key.
- Capture screenshot.

# How to use:
- cd src/code and run: python main.py

- In setting: the "confidence" specifies the accuracy with which the function should locate the image on screen. This is helpful in case the function is not able to locate an image due to negligible pixel differences. Use "Region" to only search a smaller region of the screen instead of the full screen when locating an image.
- Press "S" to get the coordinate of mouse pointer for clicking, region for screenshot and locating images.
- Ctrl-Alt-S to start clicking, Ctrl-Alt-E to stop clicking, Ctrl-Alt-P to pause/resume.
