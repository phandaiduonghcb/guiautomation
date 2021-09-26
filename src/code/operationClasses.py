import pyautogui
import time, random
import ast

def getPositionFromImage(path,region,confidence=0.8):
    pos = pyautogui.locateCenterOnScreen(path,region=region,confidence=confidence)
    return pos
class Click:
    def __init__(self,name,interval,choosePos,location,duration=None) -> None:
        self.name = name
        self.interval = interval
        self.choosePos = choosePos
        self.location = location
        self.duration = duration
    
    def execute(self,region,confidence):
        
        if self.choosePos == 1:
            pos = ast.literal_eval(self.location)
        elif self.choosePos == 2:
            pos = getPositionFromImage(self.location,region,confidence)
            pos[0]
        time.sleep(float(self.interval))
        if self.name=='Left click':
            pyautogui.leftClick(pos[0],pos[1])
        elif self.name == 'Right click':
            pyautogui.rightClick(pos[0],pos[1])
        elif self.name == 'Middle click':
            pyautogui.middleClick(pos[0],pos[1])
        elif self.name == 'Double left click':
            pyautogui.doubleClick(pos[0],pos[1])

class Scroll:
    def __init__(self,name, interval, clicks,location=None,duration=None) -> None:
        self.name = name
        self.interval = interval
        self.clicks = clicks
        self.location = location
        self.duration = duration
    
    def execute(self,region,confidence):
        time.sleep(float(self.interval))
        if self.name == 'Scroll up':
            pyautogui.scroll(float(self.clicks))
        else:
            pyautogui.scroll(-float(self.clicks))

class KeyPress:
    def __init__(self, interval, key, location=None,duration = None) -> None:
        self.name = 'Press a key'
        self.interval = interval
        self.key = key
        self.location = location
        self.duration = duration

    def execute(self,region,confidence):
        print(self.key)
        time.sleep(float(self.interval))
        pyautogui.press(self.key)

class KeyCombination:
    def __init__(self, interval, keyComb, duration=None, location=None) -> None:
        self.name = 'Key combination'
        self.interval = interval
        self.keyComb = keyComb
        self.location = location
        self.duration  = duration

    def execute(self,region,confidence):
        keys = self.keyComb.split(',')
        time.sleep(float(self.interval))
        pyautogui.hotkey(*keys)

class HoldaKey:
    def __init__(self, interval, duration, key, location=None) -> None:
        self.name = 'Hold a key'
        self.interval =interval
        self.duration = duration
        self.key = key
        self.location = location

    def execute(self,region,confidence):
        print(self.key)
        time.sleep(float(self.interval))
        pyautogui.keyDown(self.key)
        time.sleep(float(self.duration))
        pyautogui.keyUp(self.key)

class TypeaString:
    def __init__(self, interval, duration, string, location = None) -> None:
        self.name = 'Type a string'
        self.interval =interval
        self.duration = duration
        self.string = string
        self.location = location
    def execute(self,region,confidence):
        intervalEachLetter = float(self.interval)/len(self.string)
        time.sleep(float(self.interval))
        pyautogui.write(self.string,intervalEachLetter)

class Capture:
    def __init__(self,interval, topleft, botright,path, duration = None, location = None) -> None:
        self.name = 'Capture screenshot'
        self.interval =interval
        self.topleft = topleft
        self.botright = botright
        self.pathtoSave = path
        self.location = location
        self.duration = duration
    
    def execute(self,region,confidence):
        time.sleep(float(self.interval))
        topleft = ast.literal_eval(self.topleft)
        botright = ast.literal_eval(self.botright)

        reg = (topleft[0],topleft[1],botright[0]-topleft[0],botright[1]-topleft[1])
        pyautogui.screenshot(self.pathtoSave,reg)

class DragandDrop:
    def __init__(self,interval,choosePosSource,source,choosePosDes,des,duration,isLeft) -> None:
        self.name = 'Drag and drop'
        self.interval =interval
        self.choosePosSource = choosePosSource
        self.source = source
        self.choosePosDes = choosePosDes
        self.des = des
        self.duration = duration
        self.isLeft = isLeft
        self.location = (source,des)
    
    def execute(self,region,confidence):
        source = ''
        destination = ''
        mouse = ''
        if self.choosePosSource == 1:
            source = ast.literal_eval(self.source)
        elif self.choosePosSource == 2:
            source = getPositionFromImage(self.source,region)
            source[0]
        if self.choosePosDes == 1:
            destination = ast.literal_eval(self.des)
        elif self.choosePosDes == 2:
            destination = getPositionFromImage(self.des,region)
            destination[0]
        if self.isLeft:
            mouse = 'left'
        elif self.isLeft == 2:
            mouse = 'right'
        time.sleep(float(self.interval))
        pyautogui.moveTo(source[0],source[1])
        pyautogui.dragTo(destination[0],destination[1],duration=float(self.duration),button=mouse)
        

