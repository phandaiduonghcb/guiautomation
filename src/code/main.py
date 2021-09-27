from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from pyscreeze import center
from settings_form import settingsForm, SettingResult
import threading
from keyCombimation_form import ChooseOneKeyForm, keyCombinationForm
from operationClasses import *
from pynput.keyboard import GlobalHotKeys,Listener, KeyCode
import pyautogui
import ast
import time
class myMenubar:
    def __init__(self,root) -> None:
        self.menuBar = Menu(root)
        self.fileMenu = Menu(self.menuBar)
        self.settingsMenu = Menu(self.menuBar)
        self.addMenu = Menu(self.menuBar)
        self.mouseMenu = Menu(self.addMenu)
        self.keyboardMenu = Menu(self.addMenu)
        self.runMenu = Menu(self.menuBar)
        self.addFrametoChange = None
        self.buttonFrame = None
        self.app = None
        self.fileName = ''
    def addCommand(self):
        print(self)
    def OpenCommand(self):
        path = filedialog.askopenfilename(initialdir='.',title='Open a file',filetypes=(('AUTO files','*.auto'),))
        if path == '' or isinstance(path,tuple):
            return
        self.fileName = path
        filename = path.split('/')[-1]
        data = []
        self.app.root.title('AutomationGUI - ' + filename)
        file = open(path,'r')
        for opStr in file.read().split('\n')[:-1]:
            opDict = ast.literal_eval(opStr)
            name = opDict['name']
            if name == 'Left click' or name == 'Middle click' or name == 'Right click':
                data.append(Click(name,opDict['interval'],opDict['choosePos'],opDict['location']))
            elif name == 'Scroll up' or name == 'Scroll down':
                data.append(Scroll(name,opDict['interval'],opDict['clicks'],opDict['location'],opDict['duration']))
            elif name == 'Press a key':
                data.append(KeyPress(opDict['interval'],opDict['key'],opDict['location'],opDict['duration']))
            elif name == 'Key combination':
                data.append(KeyCombination(opDict['interval'],opDict['keyComb'],opDict['duration'],opDict['location']))
            elif name == 'Hold a key':
                data.append(HoldaKey(opDict['interval'],opDict['duration'],opDict['key'],opDict['location']))
            elif name == 'Type a string':
                data.append(TypeaString(opDict['interval'],opDict['duration'],opDict['string'],opDict['location']))
            elif name == 'Capture screenshot':
                data.append(Capture(opDict['interval'],opDict['topleft'],opDict['botright'],opDict['duration'],opDict['location']))
            elif name == 'Drag and drop':
                data.append(DragandDrop(opDict['interval'],opDict['choosePosSource'],opDict['source'],opDict['choosePosDes'],opDict['des'],opDict['duration'],opDict['isLeft']))
            else:
                print(name)
        
        self.buttonFrame.data = data
        self.buttonFrame.updateTreeView()
        file.close()
    def NewCommand(self):
        answer = ''
        if self.buttonFrame.dataChanged:
            answer = messagebox.askyesnocancel('Save?','Save changes before closing?')
        if answer is None:
            return
        elif answer:
            if self.fileName != '':
                self.SaveCommand()
            else:
                self.SaveAsCommand()
        self.buttonFrame.dataChanged = False
        self.fileName = ''
        self.app.root.title('AutomationGUI - Untitled')
        self.buttonFrame.data = []
        self.buttonFrame.updateTreeView()
    def SaveAsCommand(self):
        path = filedialog.asksaveasfilename(initialdir='.',title='Save as',defaultextension='.auto')
        if path == '' or isinstance(path,tuple):
            return
        self.fileName = path
        filename = path.split('/')[-1]
        self.app.root.title('AutomationGUI - ' + filename)
        file = open(path,'w')
        for op in self.buttonFrame.data:
            file.write(str(op.__dict__) + '\n')
        file.close()
        self.buttonFrame.dataChanged = False
    def SaveCommand(self):
        path = self.fileName
        if path =='':
            path = filedialog.asksaveasfilename(initialdir='.',title='Save as',defaultextension='.auto')
        if path == '' or isinstance(path,tuple):
            self.fileName = ''
            return
        filename = path.split('/')[-1]
        self.app.root.title('AutomationGUI - ' + filename)
        self.fileName = path
        file = open(path,'w')
        for op in self.buttonFrame.data:
            file.write(str(op.__dict__) + '\n')
        file.close()
        self.buttonFrame.dataChanged = False
    def startCommand(self,event=None):
        print('Auto...')
        #self.app.auto.start_auto()
        self.app.conf = self.addFrametoChange.setting.conf
        self.app.choice = self.addFrametoChange.setting.choice
        self.app.start_auto()
    def stopCommand(self,event=None):
        try:
            self.app.auto.stop_auto()
            self.app.listener.stop()
        except:
            return
    def pauseCommand(self,event=None):
        try:
            self.app.auto.pause_auto()
        except:
            return
    def add(self):
        self.menuBar.add_cascade(label='File',menu=self.fileMenu) # FILE
        self.fileMenu.add_command(label='New...',command=self.NewCommand)
        self.fileMenu.add_command(label='Open...',command=self.OpenCommand)
        self.fileMenu.add_command(label='Save as...',command=self.SaveAsCommand)
        self.fileMenu.add_command(label='Save',command=self.SaveCommand)

        self.menuBar.add_command(label='Settings',command=self.open_settings) # SETTINGS

        self.menuBar.add_cascade(label='Run...',menu=self.runMenu)
        self.runMenu.add_command(label='Start',command=self.startCommand,accelerator='Ctrl+Alt+S')
        self.runMenu.add_command(label='Stop',command=self.stopCommand,accelerator='Ctrl+Alt+E')
        self.runMenu.add_command(label='Pause/Resume',command=self.pauseCommand,accelerator='Ctrl+Alt+P')
        self.runMenu.bind_all('<Control-Alt-s>',self.startCommand)
        self.runMenu.bind_all('<Control-Alt-e>',self.stopCommand)
        self.runMenu.bind_all('<Control-Alt-p>',self.pauseCommand)

        self.menuBar.add_cascade(label='Add...',menu=self.addMenu) # ADD
        self.mouseMenu.add_command(label='Left click',command=lambda :self.addCommand('Left click'))
        self.mouseMenu.add_command(label='Right click',command=lambda :self.addCommand('Right click'))
        self.mouseMenu.add_command(label='Double left click',command=lambda :self.addCommand('Double left click'))
        self.mouseMenu.add_command(label='Middle click',command=lambda :self.addCommand('Middle click'))
        self.mouseMenu.add_command(label='Drag and drop',command=lambda :self.addCommand('Drag and drop'))
        self.mouseMenu.add_command(label='Scroll up',command=lambda :self.addCommand('Scroll up'))
        self.mouseMenu.add_command(label='Scroll down',command=lambda :self.addCommand('Scroll down'))
        self.addMenu.add_cascade(label='Mouse',menu=self.mouseMenu)

        self.keyboardMenu.add_command(label='Press a key',command=lambda :self.addCommand('Press a key'))
        self.keyboardMenu.add_command(label='Hold a key',command=lambda :self.addCommand('Hold a key'))
        self.keyboardMenu.add_command(label='Key combination',command=lambda :self.addCommand('Key combination'))
        self.keyboardMenu.add_command(label='Type a string',command=lambda :self.addCommand('Type a string'))
        self.addMenu.add_cascade(label='Keyboard',menu=self.keyboardMenu)
        self.addMenu.add_command(label='Capture screenshot',command=lambda :self.addCommand('Capture screenshot'))
    def open_settings(self):
        g = self.app.root.geometry()
        size = tuple(int(_) for _ in self.app.root.geometry().split('+')[0].split('x'))
        pos = tuple(int(_) for _ in self.app.root.geometry().split('+')[1:])
        centerPoint = (pos[0] + size[0]/2,pos[1] + size[1]/2)
        self.addFrametoChange.setting = settingsForm(centerPoint).show()
    def addCommand(self,text):
        self.addFrametoChange.optionMenuEvent(self.addFrametoChange,selected=text)

class myAddFrame():
    def optionMenuEvent(self,event=None, selected=None):
        if selected is None:
            selected = self.clicked.get()
        else:
            self.clicked.set(selected)
        print(selected)

        if selected == 'Left click' or selected == 'Right click' or selected == 'Middle click' or selected == 'Double left click':
            self.locationDesLbl['text'] = ''
            self.locationPosLbl['text'] = ''
            self.posLabel.config(text='Position')
            self.desLabel.grid_remove()
            self.imRbtn1.grid_remove()
            self.posRbtn1.grid_remove()
            self.browsebtn1.grid_remove()
            self.choosePosbtn1.grid_remove()
            self.stringLabel.grid_remove()
            self.stringTxtbox.grid_remove()
            self.durTxtbox.grid_remove()
            self.durLabel.grid_remove()
            self.mouseLabel.grid_remove()
            self.leftRbtn.grid_remove()
            self.rightRbtn.grid_remove()
            self.clicksLabel.grid_remove()
            self.clicksTxtbox.grid_remove()
            self.windowRightBtn.grid_remove()
            self.windowLeftBtn.grid_remove()
            self.windowLabel.grid_remove()
            self.chooseKeyComb.grid_remove()
            self.desLabel.grid_remove()
            self.locationDesLbl.grid_remove()
            self.windowLeftLbl.grid_remove()
            self.windowRightLbl.grid_remove()
            self.browseSaveBtn.grid_remove()
            self.pathtoSaveLbl.grid_remove()
            self.saveToLbl.grid_remove()

            self.intervalTxtbox.grid()
            self.intervalLabel.grid()
            self.posLabel.grid()
            self.posRbtn.grid()
            self.imRbtn.grid()
            self.choosePosbtn.grid()
            self.browsebtn.grid()
            self.locationPosLbl.grid()
        
        elif selected == 'Drag and drop':
            self.locationDesLbl['text'] = ''
            self.locationPosLbl['text'] = ''
            self.posLabel.config(text='Source')
            self.stringLabel.grid_remove()
            self.stringTxtbox.grid_remove()
            self.clicksLabel.grid_remove()
            self.clicksTxtbox.grid_remove()
            self.windowRightBtn.grid_remove()
            self.windowLeftBtn.grid_remove()
            self.windowLabel.grid_remove()
            self.chooseKeyComb.grid_remove()
            self.windowLeftLbl.grid_remove()
            self.windowRightLbl.grid_remove()
            self.browseSaveBtn.grid_remove()
            self.pathtoSaveLbl.grid_remove()
            self.saveToLbl.grid_remove()

            self.intervalTxtbox.grid()
            self.durLabel.grid()
            self.durTxtbox.grid()
            self.mouseLabel.grid()
            self.leftRbtn.grid()
            self.rightRbtn.grid()
            self.desLabel.grid()
            self.imRbtn1.grid()
            self.posRbtn1.grid()
            self.browsebtn1.grid()
            self.choosePosbtn1.grid()
            self.intervalLabel.grid()
            self.posLabel.grid()
            self.posRbtn.grid()
            self.imRbtn.grid()
            self.choosePosbtn.grid()
            self.browsebtn.grid()
            self.locationPosLbl.grid()
            self.locationDesLbl.grid()

        elif selected == 'Scroll up' or selected == 'Scroll down':
            self.locationDesLbl['text'] = ''
            self.locationPosLbl['text'] = ''
            self.desLabel.grid_remove()
            self.imRbtn1.grid_remove()
            self.posRbtn1.grid_remove()
            self.browsebtn1.grid_remove()
            self.choosePosbtn1.grid_remove()
            self.stringLabel.grid_remove()
            self.stringTxtbox.grid_remove()
            self.durTxtbox.grid_remove()
            self.durLabel.grid_remove()
            self.mouseLabel.grid_remove()
            self.leftRbtn.grid_remove()
            self.rightRbtn.grid_remove()
            self.windowRightBtn.grid_remove()
            self.windowLeftBtn.grid_remove()
            self.windowLabel.grid_remove()
            self.posLabel.grid_remove()
            self.posRbtn.grid_remove()
            self.imRbtn.grid_remove()
            self.choosePosbtn.grid_remove()
            self.browsebtn.grid_remove()
            self.chooseKeyComb.grid_remove()
            self.locationDesLbl.grid_remove()
            self.locationPosLbl.grid_remove()
            self.windowLeftLbl.grid_remove()
            self.windowRightLbl.grid_remove()
            self.browseSaveBtn.grid_remove()
            self.pathtoSaveLbl.grid_remove()
            self.saveToLbl.grid_remove()

            self.clicksLabel.grid()
            self.clicksTxtbox.grid()
            self.intervalTxtbox.grid()
            self.intervalLabel.grid()
        elif selected == 'Press a key' or selected == 'Key combination':
            if selected == 'Press a key':
                self.stringLabel.config(text='Key:')
                self.chooseKeyComb.config(command=self.openChooseOneKeyForm)
            elif selected == 'Key combination':
                self.stringLabel.config(text='Key combination:')
                self.chooseKeyComb.config(command=self.open_keyCombinationForm)
            self.locationDesLbl['text'] = ''
            self.locationPosLbl['text'] = ''
            self.posLabel.config(text='Position')
            self.desLabel.grid_remove()
            self.imRbtn1.grid_remove()
            self.posRbtn1.grid_remove()
            self.browsebtn1.grid_remove()
            self.choosePosbtn1.grid_remove()
            self.mouseLabel.grid_remove()
            self.leftRbtn.grid_remove()
            self.rightRbtn.grid_remove()
            self.clicksLabel.grid_remove()
            self.clicksTxtbox.grid_remove()
            self.posLabel.grid_remove()
            self.posRbtn.grid_remove()
            self.imRbtn.grid_remove()
            self.choosePosbtn.grid_remove()
            self.browsebtn.grid_remove()
            self.durTxtbox.grid_remove()
            self.durLabel.grid_remove()
            self.windowRightBtn.grid_remove()
            self.windowLeftBtn.grid_remove()
            self.windowLabel.grid_remove()
            self.locationDesLbl.grid_remove()
            self.locationPosLbl.grid_remove()
            self.windowLeftLbl.grid_remove()
            self.windowRightLbl.grid_remove()
            self.browseSaveBtn.grid_remove()
            self.pathtoSaveLbl.grid_remove()
            self.saveToLbl.grid_remove()

            self.intervalTxtbox.grid()
            self.intervalLabel.grid()
            self.stringLabel.grid()

            self.stringTxtboxChanged = True
            self.stringTxtbox.delete(0,END)
            self.stringTxtboxChanged = False
            self.stringTxtbox.grid()

            self.chooseKeyComb.grid()

        elif selected == 'Hold a key' or selected == 'Type a string':
            if selected == 'Hold a key':
                self.stringLabel.config(text='Key:')
            elif selected == 'Type a string':
                self.stringLabel.config(text='String:')
            self.locationDesLbl['text'] = ''
            self.locationPosLbl['text'] = ''
            self.posLabel.config(text='Position')
            self.desLabel.grid_remove()
            self.imRbtn1.grid_remove()
            self.posRbtn1.grid_remove()
            self.browsebtn1.grid_remove()
            self.choosePosbtn1.grid_remove()
            self.mouseLabel.grid_remove()
            self.leftRbtn.grid_remove()
            self.rightRbtn.grid_remove()
            self.clicksLabel.grid_remove()
            self.clicksTxtbox.grid_remove()
            self.posLabel.grid_remove()
            self.posRbtn.grid_remove()
            self.imRbtn.grid_remove()
            self.choosePosbtn.grid_remove()
            self.browsebtn.grid_remove()
            self.windowRightBtn.grid_remove()
            self.windowLeftBtn.grid_remove()
            self.windowLabel.grid_remove()
            self.chooseKeyComb.grid_remove()
            self.locationDesLbl.grid_remove()
            self.locationPosLbl.grid_remove()
            self.windowLeftLbl.grid_remove()
            self.windowRightLbl.grid_remove()
            self.browseSaveBtn.grid_remove()
            self.pathtoSaveLbl.grid_remove()
            self.saveToLbl.grid_remove()

            self.intervalTxtbox.grid()
            self.intervalLabel.grid()
            self.stringLabel.grid()

            self.stringTxtboxChanged = True
            self.stringTxtbox.delete(0,END)
            self.stringTxtboxChanged = False
            self.stringTxtbox.grid()

            self.durTxtbox.grid()
            self.durLabel.grid()
            if selected == 'Hold a key':
                self.chooseKeyComb.config(command=self.openChooseOneKeyForm)
                self.chooseKeyComb.grid()
                self.stringTxtboxChanged = False
            else:
                self.stringTxtboxChanged = True
        elif selected == 'Capture screenshot':
            self.locationDesLbl['text'] = ''
            self.locationPosLbl['text'] = ''
            self.windowLeftLbl['text'] = ''
            self.windowRightLbl['text'] = ''
            self.posLabel.config(text='Position')
            self.desLabel.grid_remove()
            self.imRbtn1.grid_remove()
            self.posRbtn1.grid_remove()
            self.browsebtn1.grid_remove()
            self.choosePosbtn1.grid_remove()
            self.mouseLabel.grid_remove()
            self.leftRbtn.grid_remove()
            self.rightRbtn.grid_remove()
            self.clicksLabel.grid_remove()
            self.clicksTxtbox.grid_remove()
            self.posLabel.grid_remove()
            self.posRbtn.grid_remove()
            self.imRbtn.grid_remove()
            self.choosePosbtn.grid_remove()
            self.browsebtn.grid_remove()
            self.durTxtbox.grid_remove()
            self.durLabel.grid_remove()
            self.windowRightBtn.grid_remove()
            self.windowLeftBtn.grid_remove()
            self.windowLabel.grid_remove()
            self.stringTxtbox.grid_remove()
            self.stringLabel.grid_remove()
            self.chooseKeyComb.grid_remove()
            self.locationDesLbl.grid_remove()
            self.locationPosLbl.grid_remove()
            

            self.intervalTxtbox.grid()
            self.intervalLabel.grid()
            self.windowRightBtn.grid()
            self.windowLeftBtn.grid()
            self.windowLabel.grid()
            self.windowLeftLbl.grid()
            self.windowRightLbl.grid()
            self.browseSaveBtn.grid()
            self.pathtoSaveLbl.grid()
            self.saveToLbl.grid()
        
        self.updateDefault()
            
    def __init__(self,root) -> None:
        self.addFrame = LabelFrame(root,text='Add')
        options = ['Left click', 'Right click','Double left click', 'Middle click', 'Drag and drop', 'Scroll up', 'Scroll down', 'Press a key',
            'Hold a key', 'Key combination', 'Type a string', 'Capture screenshot']

        self.vcmdFloat = (self.addFrame.register(self.validateFloat),"%P",'%s')
        self.stringTxtboxChanged = False
        self.vcmdKeyorString = (self.addFrame.register(lambda: self.validateKeys(self.stringTxtboxChanged)))
        self.clicked = StringVar()
        self.clicked.set('                              ')
        self.drop = OptionMenu(self.addFrame,self.clicked,*options,command=self.optionMenuEvent)
        self.opsLabel = Label(self.addFrame,text='Operation:')
        self.drop.grid(sticky='w',column=1,row=0,columnspan=3)
        self.opsLabel.grid(sticky='w',column=0,row=0)

        self.intervalLabel = Label(self.addFrame,text='Interval (s):')
        self.intervalLabel.grid(sticky='w',column=0,row=1,pady=5)

        self.intervalTxtbox = Entry(self.addFrame, validate='key',validatecommand=self.vcmdFloat)
        self.intervalTxtbox.grid(sticky='w',column=1,row=1,pady=5,columnspan=3)

        self.posLabel = Label(self.addFrame,text='Position:')
        self.posLabel.grid(sticky='w',column=0,row=2,pady=5)
        self.r=IntVar()
        self.r.set(0)
        self.posRbtn = Radiobutton(self.addFrame,variable=self.r,value=1,text='Choose position',command=lambda: self.enableBtn(self.r,self.choosePosbtn,self.browsebtn))
        self.posRbtn.grid(sticky='w',row=2,column=1)
        self.imRbtn = Radiobutton(self.addFrame,variable=self.r,value=2,text='Locate image',command=lambda: self.enableBtn(self.r,self.choosePosbtn,self.browsebtn))
        self.imRbtn.grid(sticky='w',row=3,column=1)
        self.choosePosbtn = Button(self.addFrame,text='Choose',command=self.choosePosition,state='disabled')
        self.choosePosbtn.grid(sticky='w',column=2,row=2)
        self.browsebtn = Button(self.addFrame, text='Browse',command=self.browse,state='disabled')
        self.browsebtn.grid(sticky='w',column=2,row=3)

        self.desLabel = Label(self.addFrame,text='Destination:')
        self.desLabel.grid(sticky='w',column=0,row=4,pady=5)
        self.r1=IntVar()
        self.r1.set(0)
        self.posRbtn1 = Radiobutton(self.addFrame,variable=self.r1,value=1,text='Choose position',command=lambda: self.enableBtn(self.r1,self.choosePosbtn1,self.browsebtn1))
        self.posRbtn1.grid(sticky='w',row=4,column=1)
        self.imRbtn1 = Radiobutton(self.addFrame,variable=self.r1,value=2,text='Locate image',command=lambda: self.enableBtn(self.r1,self.choosePosbtn1,self.browsebtn1))
        self.imRbtn1.grid(sticky='w',row=5,column=1)
        self.choosePosbtn1 = Button(self.addFrame,text='Choose',command=self.choosePosition1,state='disabled')
        self.choosePosbtn1.grid(sticky='w',column=2,row=4)
        self.browsebtn1 = Button(self.addFrame, text='Browse',command=self.browse1,state='disabled')
        self.browsebtn1.grid(sticky='w',column=2,row=5)

        self.stringLabel = Label(self.addFrame,text='String:')
        self.stringLabel.grid(sticky='w',column=0,row=6,pady=5)

        self.stringTxtbox = Entry(self.addFrame,validate='key',validatecommand =self.vcmdKeyorString)
        self.stringTxtbox.grid(sticky='w',column=1,row=6,pady=5,columnspan=3)
        self.chooseKeyComb = Button(self.addFrame,text='...')
        self.chooseKeyComb.grid(sticky='w',column=4,row=6,pady=5)

        self.durLabel = Label(self.addFrame,text='Duration (s):')
        self.durLabel.grid(sticky='w',column=0,row=7,pady=5)
        self.durTxtbox = Entry(self.addFrame, validate='key',validatecommand=self.vcmdFloat)
        self.durTxtbox.grid(sticky='w',column=1,row=7,pady=5,columnspan=3)

        self.mouseLabel = Label(self.addFrame,text='Mouse:')
        self.mouseLabel.grid(sticky='w',column=0,row=8,pady=5)
        self.rMouse=IntVar()
        self.rMouse.set(0)
        self.leftRbtn = Radiobutton(self.addFrame,variable=self.rMouse,value=1,text='Left mouse')
        self.leftRbtn.grid(sticky='w',row=8,column=1)
        self.rightRbtn = Radiobutton(self.addFrame,variable=self.rMouse,value=2,text='Right mouse')
        self.rightRbtn.grid(sticky='w',row=9,column=1)

        self.clicksLabel = Label(self.addFrame,text='Clicks:')
        self.clicksLabel.grid(sticky='w',column=0,row=10,pady=5)
        self.clicksTxtbox = Entry(self.addFrame)
        self.clicksTxtbox.grid(sticky='w',column=1,row=10,pady=5,columnspan=3)

        self.windowLabel = Label(self.addFrame,text='Window: ')
        self.windowLabel.grid(sticky='w',column=0,row=11,pady=5)
        self.windowLeftBtn = Button(self.addFrame,text='Top left corner',command = self.topLeftCommand)
        self.windowLeftLbl = Label(self.addFrame,text='')
        self.windowLeftLbl.grid(sticky='w',column=2,row=11,pady=5)
        self.windowLeftBtn.grid(sticky='w',column=1,row=11,pady=5)
        self.windowRightBtn = Button(self.addFrame,text='Bottom right corner',command = self.botRightCommand)
        self.windowRightBtn.grid(sticky='w',column=1,row=12,pady=5)
        self.windowRightLbl = Label(self.addFrame,text='')
        self.windowRightLbl.grid(sticky='w',column=2,row=12,pady=5)

        self.saveToLbl = Label(self.addFrame,text='Save to: ')
        self.saveToLbl.grid(sticky='w',column=0,row=13,pady=5)
        self.pathtoSaveChanged = False
        self.vcmdPathtoSave = (self.addFrame.register(lambda: self.validateKeys(self.pathtoSaveChanged)))
        self.pathtoSaveLbl = Entry(self.addFrame,validate='key',validatecommand=self.vcmdPathtoSave)
        self.pathtoSaveLbl.grid(sticky='w',column=1,row=13,pady=5,columnspan=3)
        self.browseSaveBtn = Button(self.addFrame,text='Browse',command=self.browseSaveCommand)
        self.browseSaveBtn.grid(sticky='w',column=2,row=13,pady=5,padx=10)

        self.locationPosLbl = Label(self.addFrame,text='')
        self.locationPosLbl.grid(sticky='w',column=5,row=2,pady=5)
        self.locationDesLbl = Label(self.addFrame,text='')
        self.locationDesLbl.grid(sticky='w',column=5,row=4,pady=5)

        self.app_root = None

        #open setting
        f = open('settings.txt','r')
        setting = f.read()
        f.close()
        dic = ast.literal_eval(setting)
        choice = dic['choice']
        conf = dic['conf']
        defInterval = dic['defInterval']
        defDuration = dic['defDuration']
        left = dic['left']
        right = dic['right']
        self.setting = SettingResult(choice,conf,defInterval,defDuration,left,right)
        # HIDE ALL WIDGETS:
        self.posLabel.config(text='Position')
        self.desLabel.grid_remove()
        self.imRbtn1.grid_remove()
        self.posRbtn1.grid_remove()
        self.browsebtn1.grid_remove()
        self.choosePosbtn1.grid_remove()
        self.mouseLabel.grid_remove()
        self.leftRbtn.grid_remove()
        self.rightRbtn.grid_remove()
        self.clicksLabel.grid_remove()
        self.clicksTxtbox.grid_remove()
        self.posLabel.grid_remove()
        self.posRbtn.grid_remove()
        self.imRbtn.grid_remove()
        self.choosePosbtn.grid_remove()
        self.browsebtn.grid_remove()
        self.durTxtbox.grid_remove()
        self.durLabel.grid_remove()
        self.windowRightBtn.grid_remove()
        self.windowLeftBtn.grid_remove()
        self.windowLabel.grid_remove()
        self.intervalTxtbox.grid_remove()
        self.intervalLabel.grid_remove()
        self.windowRightBtn.grid_remove()
        self.windowLeftBtn.grid_remove()
        self.windowLabel.grid_remove()
        self.stringTxtbox.grid_remove()
        self.stringLabel.grid_remove()
        self.chooseKeyComb.grid_remove()
        self.locationPosLbl.grid_remove()
        self.locationDesLbl.grid_remove()
        self.windowLeftLbl.grid_remove()
        self.windowRightLbl.grid_remove()
        self.browseSaveBtn.grid_remove()
        self.pathtoSaveLbl.grid_remove()
        self.saveToLbl.grid_remove()

    def updateDefault(self):
        self.durTxtbox.delete(0,END)
        self.durTxtbox.insert(0,self.setting.defDuration)
        self.intervalTxtbox.delete(0,END)
        self.intervalTxtbox.insert(0,self.setting.defInterval)
    def browseSaveCommand(self):
        self.pathtoSaveChanged = True
        path = filedialog.asksaveasfilename(initialdir='.',title='Save as',defaultextension='.jpg')
        self.pathtoSaveLbl.delete(0,END)
        self.pathtoSaveLbl.insert(0,path)
        self.pathtoSaveChanged = False
    def enableBtn(self,r,btnChoose,btnBrowse):
        if r.get()==1:
            btnChoose['state'] = 'normal'
            btnBrowse['state'] = 'disabled'
        elif r.get()==2:
            btnChoose['state'] = 'disabled'
            btnBrowse['state'] = 'normal'
    def choosePostitionManually(self):
        def on_press(key):
            if key == KeyCode(char='s'):
                listener.stop()
        with Listener(on_press=on_press) as listener:
            listener.join()
        result = str(tuple(pyautogui.position()))
        return result
    def browse(self):
        path = filedialog.askopenfilename(initialdir='.',title='Select an image',filetypes=(('PNG files','*.png'),))
        self.locationPosLbl['text'] = path
    def choosePosition(self):
        self.locationPosLbl['text'] = self.choosePostitionManually()
    def browse1(self):
        path = filedialog.askopenfilename(initialdir='.',title='Select an image',filetypes=(('PNG files','*.png'),))
        self.locationDesLbl['text'] = path
    def choosePosition1(self):
        self.locationDesLbl['text'] = self.choosePostitionManually()
    def topLeftCommand(self):
        self.windowLeftLbl['text'] = self.choosePostitionManually()
    def botRightCommand(self):
        self.windowRightLbl['text'] = self.choosePostitionManually()

    def open_keyCombinationForm(self):
        size = tuple(int(_) for _ in self.app_root.geometry().split('+')[0].split('x'))
        pos = tuple(int(_) for _ in self.app_root.geometry().split('+')[1:])
        centerPoint = (pos[0] + size[0]/2,pos[1] + size[1]/2)
        text = keyCombinationForm(self.stringTxtbox.get(),centerPoint).show()
        self.stringTxtboxChanged = True
        self.stringTxtbox.delete(0,END)
        self.stringTxtbox.insert(0,text)
        self.stringTxtboxChanged = False
    def openChooseOneKeyForm(self):
        size = tuple(int(_) for _ in self.app_root.geometry().split('+')[0].split('x'))
        pos = tuple(int(_) for _ in self.app_root.geometry().split('+')[1:])
        centerPoint = (pos[0] + size[0]/2,pos[1] + size[1]/2)
        text = ChooseOneKeyForm(self.stringTxtbox.get(),centerPoint).show()
        self.stringTxtboxChanged = True
        self.stringTxtbox.delete(0,END)
        self.stringTxtbox.insert(0,text)
        self.stringTxtboxChanged = False
    def validateFloat(self,S,s):
        if S == '':
            return True
        try:
            float(S)
            return True
        except:
            try:
                int(S[:-1])
                if S[-1] == '.':
                    return True
                else:
                    return False
            except:
                return False
                
    def validateKeys(self,changed):
        return changed
class myTableFrame():
    def __init__(self,root) -> None:
        self.tableFrame = LabelFrame(root,text='Table')
        self.tableFrame.rowconfigure(0,weight=1)
        self.tableFrame.columnconfigure(0,weight=1)
        # Scrollbar
        self.scrollbar = Scrollbar(self.tableFrame)
        self.scrollbar.grid(column=1,row=0,sticky='sn')

        # Treeview
        self.treeView = ttk.Treeview(self.tableFrame,yscrollcommand=self.scrollbar.set)
        self.treeView['column'] = ('ops','interval','pos','duration')
        self.treeView.column('#0',width=70,anchor=CENTER)
        self.treeView.column('ops',width=150,anchor=CENTER)
        self.treeView.column('interval',width=100,anchor=CENTER)
        self.treeView.column('pos',width=400,anchor=CENTER)
        self.treeView.column('duration',width=100,anchor=CENTER)

        self.treeView.heading('#0',text='id',anchor=CENTER)
        self.treeView.heading('ops',text='ops',anchor=CENTER)
        self.treeView.heading('interval',text='interval',anchor=CENTER)
        self.treeView.heading('pos',text='position',anchor=CENTER)
        self.treeView.heading('duration',text='duration',anchor=CENTER)
        self.treeView.grid(row=0,column=0,sticky='nsew')
class myButtonFrame():
    def __init__(self,root) -> None:
        self.buttonFrame = LabelFrame(root,text='Buttons')
        self.buttonFrame.rowconfigure(0,weight=1)
        self.buttonFrame.columnconfigure(0,weight=1)
        self.buttonFrame.columnconfigure(1,weight=1)
        self.buttonFrame.columnconfigure(2,weight=1)
        self.addFrame = None
        self.tableFrame = None
        self.data = []

        self.addBtn = Button(self.buttonFrame,command=self.AddEvent,text='Add')
        self.addBtn.grid(column=0,row=0,sticky='we')

        self.insertBtn = Button(self.buttonFrame,command=self.InsertEvent,text='Insert')
        self.insertBtn.grid(column=1,row=0,sticky='we')

        self.deleteBtn = Button(self.buttonFrame,command=self.DeleteEvent,text='Delete')
        self.deleteBtn.grid(column=2,row=0,sticky='we')
        self.dataChanged = False
        
    def raiseNotFilledMessage(self,text):
        messagebox.showwarning('Warning','Please complete:\n' + text)
    def DeleteEvent(self):
        curItem = self.tableFrame.treeView.focus()
        id = self.tableFrame.treeView.item(curItem)['text']
        if id=='':
            return
        self.data = self.data[:int(id)] + self.data[int(id)+1:]
        self.dataChanged = True
        self.updateTreeView()
    
    def InsertEvent(self):
        selected = self.addFrame.clicked.get()
        notFilled = []
        item = ''
        if selected == 'Left click' or selected == 'Middle click' or selected == 'Right click' or selected == 'Double left click':
            interval = self.addFrame.intervalTxtbox.get()
            choosePos = self.addFrame.r.get()
            location = self.addFrame.locationPosLbl['text']
            if interval == '':
                notFilled.append('"Interval"')
            if choosePos ==0:
                notFilled.append('"Position"')
            elif choosePos==1 and location == '':
                notFilled.append('"Position: Choose"')
            elif choosePos==2 and location =='':
                notFilled.append('"Position: Browse')
            if notFilled:
                self.raiseNotFilledMessage('\n'.join(notFilled))
                return
            item = (Click(selected,interval, choosePos, location))

        elif selected == 'Scroll up' or selected == 'Scroll down':
            interval = self.addFrame.intervalTxtbox.get()
            clicks = self.addFrame.clicksTxtbox.get()

            if interval == '':
                notFilled.append('"Interval"')
            if clicks == '':
                notFilled.append('"Clicks"')
            if notFilled:
                self.raiseNotFilledMessage('\n'.join(notFilled))
                return
            item = (Scroll(name=selected,interval=interval,clicks=clicks))
        
        elif selected == 'Press a key':
            interval = self.addFrame.intervalTxtbox.get()
            key = self.addFrame.stringTxtbox.get()

            if interval =='':
                notFilled.append('"Interval"')
            if key == '':
                notFilled.append('"Key"')
            if notFilled:
                self.raiseNotFilledMessage('\n'.join(notFilled))
                return
            
            item = (KeyPress(interval,key))
        
        elif selected == 'Drag and drop':
            interval = self.addFrame.intervalTxtbox.get()
            choosePosSource = self.addFrame.r.get()
            source = self.addFrame.locationPosLbl['text']
            choosePosDes = self.addFrame.r1.get()
            des = self.addFrame.locationDesLbl['text']
            duration = self.addFrame.durTxtbox.get()
            isLeft = self.addFrame.rMouse.get()
            if interval=='':
                notFilled.append('"Interval"')
            if choosePosSource == 0:
                notFilled.append('"Source"')
            elif choosePosSource == 1 and source == '':
                notFilled.append('"Source: Choose"')
            elif choosePosSource == 2 and source == '':
                notFilled.append('"Source: Browse"')
            if choosePosDes == 0:
                notFilled.append('"Destination"')
            elif choosePosDes == 1 and source == '':
                notFilled.append('"Destination: Choose"')
            elif choosePosDes == 2 and source == '':
                notFilled.append('"Destination: Browse"')
            if duration == '':
                notFilled.append('"Duration"')
            if isLeft == 0:
                notFilled.append('"Mouse"')
            if notFilled:
                self.raiseNotFilledMessage('\n'.join(notFilled))
                return
            item = (DragandDrop(interval,choosePosSource,source,choosePosDes,des,duration,isLeft))
        
        elif selected == 'Key combination':
            interval = self.addFrame.intervalTxtbox.get()
            keyComb = self.addFrame.stringTxtbox.get()

            if interval == '':
                notFilled.append('"Interval"')
            if keyComb == '':
                notFilled.append('"Key combination"')
            if notFilled:
                self.raiseNotFilledMessage('\n'.join(notFilled))
                return
            item = (KeyCombination(interval,keyComb))

        elif selected == 'Hold a key':
            interval = self.addFrame.intervalTxtbox.get()
            key = self.addFrame.stringTxtbox.get()
            duration = self.addFrame.durTxtbox.get()

            if interval == '':
                notFilled.append('"Interval"')
            if key == '':
                notFilled.append('"Key"')
            if duration =='':
                notFilled.append('"Duration')
            if notFilled:
                self.raiseNotFilledMessage('\n'.join(notFilled))
                return
            item = (HoldaKey(interval,duration,key))

        elif selected == 'Type a string':
            interval = self.addFrame.intervalTxtbox.get()
            string = self.addFrame.stringTxtbox.get()
            duration = self.addFrame.durTxtbox.get()

            if interval == '':
                notFilled.append('"Interval"')
            if string == '':
                notFilled.append('"String"')
            if duration =='':
                notFilled.append('"Duration')
            if notFilled:
                self.raiseNotFilledMessage('\n'.join(notFilled))
                return
            item = (TypeaString(interval=interval,duration=duration,string=string))

        elif selected == 'Capture screenshot':
            interval = self.addFrame.intervalTxtbox.get()
            topleft = self.addFrame.windowLeftLbl['text']
            botright = self.addFrame.windowRightLbl['text']
            path = self.addFrame.pathtoSaveLbl.get()

            if interval == '':
                notFilled.append('"Interval"')
            if topleft == '':
                notFilled.append('"Top left corner"')
            if botright == '':
                notFilled.append('"Bottom right corner"')
            if path == '':
                notFilled.append('"Save to"')
            if notFilled:
                self.raiseNotFilledMessage('\n'.join(notFilled))
                return
            if ast.literal_eval(topleft) > ast.literal_eval(botright):
                messagebox.showwarning('Warning','Invalid top left and bottom right position')
                return
            item = (Capture(interval,topleft,botright,path,location=(topleft,botright)))
        else:
            return

        self.dataChanged = True
        curItem = self.tableFrame.treeView.focus()
        id = self.tableFrame.treeView.item(curItem)['text']
        if id=='':
            return
        if id == 0:
            self.data = [item] + self.data
        else:
            self.data = self.data[:int(id)] + [item] + self.data[int(id):]
        self.dataChanged = True
        self.updateTreeView()
        
    def AddEvent(self):
        # options = ['Left click', 'Right click', 'Drag and drop', 'Middle click', 'Scroll up', 'Scroll down', 'Press a key',
        #     'Hold a key', 'Key combination', 'Type a string', 'Capture screenshot']
        selected = self.addFrame.clicked.get()
        notFilled = []
        if selected == 'Left click' or selected == 'Middle click' or selected == 'Right click' or selected == 'Double left click':
            interval = self.addFrame.intervalTxtbox.get()
            choosePos = self.addFrame.r.get()
            location = self.addFrame.locationPosLbl['text']
            if interval == '':
                notFilled.append('"Interval"')
            if choosePos ==0:
                notFilled.append('"Position"')
            elif choosePos==1 and location == '':
                notFilled.append('"Position: Choose"')
            elif choosePos==2 and location =='':
                notFilled.append('"Position: Browse')
            if notFilled:
                self.raiseNotFilledMessage('\n'.join(notFilled))
                return
            self.data.append(Click(selected,interval, choosePos, location))

        elif selected == 'Scroll up' or selected == 'Scroll down':
            interval = self.addFrame.intervalTxtbox.get()
            clicks = self.addFrame.clicksTxtbox.get()

            if interval == '':
                notFilled.append('"Interval"')
            if clicks == '':
                notFilled.append('"Clicks"')
            if notFilled:
                self.raiseNotFilledMessage('\n'.join(notFilled))
                return
            self.data.append(Scroll(name=selected,interval=interval,clicks=clicks))
        
        elif selected == 'Press a key':
            interval = self.addFrame.intervalTxtbox.get()
            key = self.addFrame.stringTxtbox.get()

            if interval =='':
                notFilled.append('"Interval"')
            if key == '':
                notFilled.append('"Key"')
            if notFilled:
                self.raiseNotFilledMessage('\n'.join(notFilled))
                return
            
            self.data.append(KeyPress(interval,key))
        
        elif selected == 'Drag and drop':
            interval = self.addFrame.intervalTxtbox.get()
            choosePosSource = self.addFrame.r.get()
            source = self.addFrame.locationPosLbl['text']
            choosePosDes = self.addFrame.r1.get()
            des = self.addFrame.locationDesLbl['text']
            duration = self.addFrame.durTxtbox.get()
            isLeft = self.addFrame.rMouse.get()
            if interval=='':
                notFilled.append('"Interval"')
            if choosePosSource == 0:
                notFilled.append('"Source"')
            elif choosePosSource == 1 and source == '':
                notFilled.append('"Source: Choose"')
            elif choosePosSource == 2 and source == '':
                notFilled.append('"Source: Browse"')
            if choosePosDes == 0:
                notFilled.append('"Destination"')
            elif choosePosDes == 1 and source == '':
                notFilled.append('"Destination: Choose"')
            elif choosePosDes == 2 and source == '':
                notFilled.append('"Destination: Browse"')
            if duration == '':
                notFilled.append('"Duration"')
            if isLeft == 0:
                notFilled.append('"Mouse"')
            if notFilled:
                self.raiseNotFilledMessage('\n'.join(notFilled))
                return
            self.data.append(DragandDrop(interval,choosePosSource,source,choosePosDes,des,duration,isLeft))
        
        elif selected == 'Key combination':
            interval = self.addFrame.intervalTxtbox.get()
            keyComb = self.addFrame.stringTxtbox.get()

            if interval == '':
                notFilled.append('"Interval"')
            if keyComb == '':
                notFilled.append('"Key combination"')
            if notFilled:
                self.raiseNotFilledMessage('\n'.join(notFilled))
                return
            self.data.append(KeyCombination(interval,keyComb))

        elif selected == 'Hold a key':
            interval = self.addFrame.intervalTxtbox.get()
            key = self.addFrame.stringTxtbox.get()
            duration = self.addFrame.durTxtbox.get()

            if interval == '':
                notFilled.append('"Interval"')
            if key == '':
                notFilled.append('"Key"')
            if duration =='':
                notFilled.append('"Duration')
            if notFilled:
                self.raiseNotFilledMessage('\n'.join(notFilled))
                return
            self.data.append(HoldaKey(interval,duration,key))

        elif selected == 'Type a string':
            interval = self.addFrame.intervalTxtbox.get()
            string = self.addFrame.stringTxtbox.get()
            duration = self.addFrame.durTxtbox.get()

            if interval == '':
                notFilled.append('"Interval"')
            if string == '':
                notFilled.append('"String"')
            if duration =='':
                notFilled.append('"Duration')
            if notFilled:
                self.raiseNotFilledMessage('\n'.join(notFilled))
                return
            self.data.append(TypeaString(interval=interval,duration=duration,string=string))

        elif selected == 'Capture screenshot':
            interval = self.addFrame.intervalTxtbox.get()
            topleft = self.addFrame.windowLeftLbl['text']
            botright = self.addFrame.windowRightLbl['text']
            path = self.addFrame.pathtoSaveLbl.get()

            if interval == '':
                notFilled.append('"Interval"')
            if topleft == '':
                notFilled.append('"Top left corner"')
            if botright == '':
                notFilled.append('"Bottom right corner"')
            if path == '':
                notFilled.append('"Save to"')
            if notFilled:
                self.raiseNotFilledMessage('\n'.join(notFilled))
                return
            if ast.literal_eval(topleft) > ast.literal_eval(botright):
                messagebox.showwarning('Warning','Invalid top left and bottom right position')
                return
            self.data.append(Capture(interval,topleft,botright,path,location=(topleft,botright)))
        else:
            return

        self.dataChanged = True
        self.updateTreeView()


    def updateTreeView(self):

        # DELETE ALL
        for item in self.tableFrame.treeView.get_children():
            self.tableFrame.treeView.delete(item)

        # INSERT ALL
        for index,element in enumerate(self.data):
            name = element.name
            self.tableFrame.treeView.insert(parent='',index='end',iid=index,text=str(index),values=(name,element.interval,element.location,element.duration))

class AutoThread(threading.Thread):
    def __init__(self,data,region,listener,setting):
        super(AutoThread,self).__init__()
        self.data = data
        self.region =region
        self.paused = False
        self.stopped = False
        self.listener = listener
        self.setting = setting
    
    def start_auto(self):
        self.paused = False
        print('START')
    def pause_auto(self):
        self.paused = not self.paused# True
        print('PAUSE: ',self.paused)
    
    def stop_auto(self):
        print('STOP')
        self.paused = True
        self.stopped = True

    def run(self):

        i=0
        while not self.stopped:
            while not self.paused:
                print('Operation: {}'.format(i))
                op = self.data[i]
                try:
                    self.region
                    op.execute(self.region,self.setting.conf)
                except TypeError:
                    if self.setting.choice == 1:
                        print('Stop')
                        self.stop_auto()
                        self.listener.stop()
                    elif self.setting.choice == 2:
                        print('Keep running')
                    elif self.setting.choice == 3:
                        print('Waiting...')
                        i-=1
                i+=1
                # Done:
                if i == len(self.data):
                    self.stop_auto()
                    self.listener.stop()

class AutoApp():
    def getCenter(self,toplevel):
        size = (839,348)
        screenSize = pyautogui.size()
        x = int(screenSize[0]/2 - size[0]/2)
        y = int(screenSize[1]/2 - size[1]/2)-100
        return '+{}+{}'.format(x,y)


    def init_UI(self):
        self.root = Tk()
        self.screenSize = pyautogui.size()
        self.root.title('AutomationGUI - Untitled')

        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)
        self.root.rowconfigure(1,weight=1)
        self.root.rowconfigure(2,weight=1)
        self.root.rowconfigure(3,weight=1)
        self.root.geometry(self.getCenter(self.root))

        self.menu = myMenubar(self.root)
        self.root.config(menu=self.menu.menuBar)

        self.addFrame = myAddFrame(self.root)
        self.addFrame.addFrame.grid(row=0,column=0,sticky='nesw')

        self.buttonFrame = myButtonFrame(self.root)
        self.buttonFrame.buttonFrame.grid(row=1,column=0,sticky='news')

        self.tableFrame = myTableFrame(self.root)
        self.tableFrame.tableFrame.grid(row=2,column=0,sticky='nesw')
        
        self.data = self.buttonFrame.data
        self.choice = None
        self.conf = None
        self.auto = None
        def on_closing(dataChanged):
            if dataChanged:
                result = messagebox.askyesnocancel('Save?','Save changes before closing?')
                if result is None:
                    return
                elif result:
                    self.menu.SaveCommand()
                    self.root.destroy()
                else:
                    self.root.destroy()
            else:
                self.root.destroy()
        self.root.protocol("WM_DELETE_WINDOW", lambda :on_closing(self.buttonFrame.dataChanged))
    def connectMenuAndAddFrame(self):
        self.menu.addFrametoChange = self.addFrame
        self.menu.add()
    def connectButtonAndAddFrame(self):
        self.buttonFrame.addFrame = self.addFrame
    def connectButtonAndTableFrame(self):
        self.buttonFrame.tableFrame = self.tableFrame
    def connectMenuAndButton(self):
        self.menu.buttonFrame =self.buttonFrame
    def connectAppandMenu(self):
        self.menu.app = self
    def start_auto(self):
        if not self.buttonFrame.data:
            return
        self.data = self.buttonFrame.data
        def on_activate_s():
            self.auto.start_auto()
        def on_activate_e():
            self.auto.stop_auto()
            self.listener.stop()
        def on_activate_p():
            self.auto.pause_auto()
        self.listener = GlobalHotKeys({
        '<ctrl>+<alt>+s': on_activate_s,
        '<ctrl>+<alt>+e': on_activate_e,
        '<ctrl>+<alt>+p': on_activate_p})
        self.listener.start()
        left = ast.literal_eval(self.addFrame.setting.left)
        right = ast.literal_eval(self.addFrame.setting.right)
        self.auto = AutoThread(self.data,(left[0],left[1],right[0]-left[0],right[1]-left[1]),self.listener,self.addFrame.setting)
        self.auto.start()

    def run(self):
        self.connectMenuAndAddFrame()
        self.connectButtonAndAddFrame()
        self.connectButtonAndTableFrame()
        self.connectMenuAndButton()
        self.connectAppandMenu()
        self.addFrame.app_root = self.root
        self.root.mainloop()
    

if __name__ == '__main__':
    application = AutoApp()
    application.init_UI()
    application.run()
