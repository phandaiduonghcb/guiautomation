from tkinter import *
import ast
import pyautogui
from pynput.keyboard import KeyCode,Listener
from tkinter import messagebox

class WindowforAuto(LabelFrame):
    def __init__(self,parent,text):
        super(WindowforAuto,self).__init__(master=parent,text=text)
        self.windowLeftBtn = Button(self,text='Top left corner',command = self.topLeftCommand)
        self.windowLeftLbl = Label(self,text='')
        self.windowLeftLbl.grid(sticky='w',column=2,row=0,pady=5)
        self.windowLeftBtn.grid(sticky='w',column=1,row=0,pady=5)
        self.windowRightBtn = Button(self,text='Bottom right corner',command = self.botRightCommand)
        self.windowRightBtn.grid(sticky='w',column=1,row=1,pady=5)
        self.windowRightLbl = Label(self,text='')
        self.windowRightLbl.grid(sticky='w',column=2,row=1,pady=5)
    
    def choosePostitionManually(self):
        def on_press(key):
            if key == KeyCode(char='s'):
                listener.stop()
        with Listener(on_press=on_press) as listener:
            listener.join()
        result = str(tuple(pyautogui.position()))
        return result

    def topLeftCommand(self):
        self.windowLeftLbl['text'] = self.choosePostitionManually()
    def botRightCommand(self):
        self.windowRightLbl['text'] = self.choosePostitionManually()
class SettingResult:
    def __init__(self,choice,conf,defInterval,defDuration,left,right) -> None:
        self.choice = choice
        self.conf = conf
        self.defInterval = defInterval
        self.defDuration = defDuration
        self.left = left
        self.right = right

class settingsForm:
    def __init__(self):
        self.root = Toplevel()
        self.setting = None
        self.root.columnconfigure(0,weight=1)
        self.root.columnconfigure(1,weight=1)
        self.root.rowconfigure(6,weight=1)
        self.root.rowconfigure(7,weight=1)
        self.root.title('Setting')
        self.root.resizable(width=False,height=False)
        self.vcmdFloat = (self.root.register(self.validateFloat),"%P")
        self.vcmdConf = (self.root.register(self.validateConf),"%P")
        self.r = IntVar()
        self.imgLbl = Label(self.root,text='When an image can not be located:')
        self.imgLbl.grid(sticky='w',row=0,column=0)
        self.stopRbtn = Radiobutton(self.root,variable=self.r,value=1,text='Stop')
        self.stopRbtn.grid(sticky='w',row=0,column=1,padx=10)
        self.runRbtn = Radiobutton(self.root,variable=self.r,value=2,text='Keep running')
        self.runRbtn.grid(sticky='w',row=1,column=1,padx=10)
        self.waitRbtn = Radiobutton(self.root,variable=self.r,value=3,text='Wait until the image is located')
        self.waitRbtn.grid(sticky='w',row=2,column=1,padx=10)

        self.confidenceLbl = Label(self.root,text='Confidence for locating images :')
        self.confidenceLbl.grid(sticky='w',row=3,column=0,pady=10)
        self.confidenceTxtbox = Entry(self.root,validatecommand=self.vcmdConf,validate='key')
        self.confidenceTxtbox.grid(sticky='w',row=3,column=1)

        self.defaultIntervalLbl = Label(self.root,text='Default interval:')
        self.defaultIntervalLbl.grid(sticky='w',row=4,column=0,pady=10)
        self.defaultIntervalTxtbox = Entry(self.root,validate='key',validatecommand=self.vcmdFloat)
        self.defaultIntervalTxtbox.grid(sticky='w',row=4,column=1)

        self.defaultDurationLbl = Label(self.root,text='Default duration:')
        self.defaultDurationLbl.grid(sticky='w',row=5,column=0,pady=10)
        self.defaultDurationTxtbox = Entry(self.root,validate='key',validatecommand=self.vcmdFloat)
        self.defaultDurationTxtbox.grid(sticky='w',row=5,column=1)

        self.chooseRegion = WindowforAuto(self.root,'Region')
        self.chooseRegion.grid(row=6,column=0,columnspan=2,sticky='wesn')

        self.buttonFrame = LabelFrame(self.root,text='Button')
        self.buttonFrame.grid(row=7,column=0,sticky='wesn',columnspan=2)
        self.buttonFrame.rowconfigure(0,weight=1)
        self.buttonFrame.columnconfigure(0,weight=1)
        self.button = Button(self.buttonFrame,text='OK',command=self.doneCommand)
        self.button.grid(row=0,column=0,sticky='wesn')
        self.open()
    def show(self):
        self.root.wm_deiconify()
        self.root.wait_window()
        return self.setting
    def save(self):
        choice = self.r.get()
        conf = self.confidenceTxtbox.get()
        defInterval = self.defaultIntervalTxtbox.get()
        defDuration = self.defaultDurationTxtbox.get()
        left = self.chooseRegion.windowLeftLbl['text']
        right = self.chooseRegion.windowRightLbl['text']
        setting = SettingResult(choice,conf,defInterval,defDuration,left,right)
        with open('settings.txt','w') as f:
            f.write(str(setting.__dict__))
        self.setting =  setting
    def open(self):
        f = open('settings.txt','r')
        setting = f.read()
        f.close()
        dic = ast.literal_eval(setting)
        choice = dic['choice']
        conf = dic['conf']
        defInterval = dic['defInterval']
        defDuration = dic['defDuration']
        windowLeftLbl = dic['left']
        windowRightLbl = dic['right']

        self.confidenceTxtbox.delete(0,END)
        self.confidenceTxtbox.insert(0,conf)
        self.r.set(choice)
        self.defaultDurationTxtbox.delete(0,END)
        self.defaultDurationTxtbox.insert(0,defDuration)
        self.defaultIntervalTxtbox.delete(0,END)
        self.defaultIntervalTxtbox.insert(0,defInterval)
        self.chooseRegion.windowRightLbl['text'] = windowRightLbl
        self.chooseRegion.windowLeftLbl['text'] = windowLeftLbl
        self.setting = SettingResult(choice,conf,defInterval,defDuration,windowLeftLbl,windowRightLbl)
    def doneCommand(self):
        if ast.literal_eval(self.chooseRegion.windowLeftLbl['text']) > ast.literal_eval(self.chooseRegion.windowRightLbl['text']):
                messagebox.showwarning('Warning','Invalid top left and bottom right position')
        else:
            self.save()
            self.root.destroy()
    def validateFloat(self,S):
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
    
    def validateConf(self,S):
        if S == '':
            return True
        try:
            if float(S) <= 1 and float(S) >= 0:
                return True
            else:
                return False
        except:
            try:
                int(S[:-1])
                if int(S[:-1]) ==0 or int(S[:-1]) == 1 and S[-1] == '.':
                    return True
                else:
                    return False
            except:
                return False