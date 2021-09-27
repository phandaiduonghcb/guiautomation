from tkinter import *

class keyCombinationForm:
    def __init__(self,keyComb,centerPoint):
        self.root = Toplevel()
        self.root.title('Choose keys')
        self.root.resizable(width=False,height=False)
        self.root.rowconfigure(0,weight=1)
        self.root.rowconfigure(1,weight=1)
        self.root.columnconfigure(0,weight=1)
        size = (243,326)
        self.root.geometry('+{}+{}'.format(int(centerPoint[0] - size[0]/2),int(centerPoint[1] - size[1]/2)))
        self.keyComb=keyComb
        
        
        # Check Frame
        self.checkFrame = Frame(self.root)
        self.checkFrame.grid(column=0,row=0)
        self.specialKeyStrings = 'Esc,Tab,Capslock,Shift,Ctrl,Alt,Space,F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11,F12,Enter,PrtScr,Insert,Delete,PageDown,PageUp,Win,Left,Right,Down,Up'.split(',')
        self.specialKeyVars = [IntVar() for i in range(30)]
        self.specialKeyCbtn = []
        col=0
        row=0
        for i in range(30):
            if col==3:
                col=0
                row+=1
            var = self.specialKeyVars[i]
            text = self.specialKeyStrings[i]
            cbtn = Checkbutton(self.checkFrame,text=text,command=lambda text=text: self.checkCommand(text),variable=var)
            cbtn.grid(row=row,column=col,sticky='w')
            self.specialKeyCbtn.append(cbtn)
            col+=1

        if self.keyComb:
            temp = self.keyComb.split(',')
            for key in temp:
                try:
                    index = self.specialKeyStrings.index(key)
                    self.specialKeyVars[index].set(1)
                except:
                    pass
        # Entry Frame
        self.entryFrame = LabelFrame(self.root,text='Key combinations')
        self.entryFrame.grid(row=1,column=0,sticky='we')
        self.entryFrame.rowconfigure(0,weight=1)
        self.entryFrame.columnconfigure(0,weight=1)

        vdcm = (self.entryFrame.register(self.validateKey),'%s','%P')
        self.keyCombTxtbox = Entry(self.entryFrame,validate='key',validatecommand=vdcm)
        self.keyCombTxtbox.grid(row=0,column=0,sticky='wesn')
        #Button Frame
        self.buttonFrame = LabelFrame(self.root)
        self.buttonFrame.rowconfigure(0,weight=1)
        self.buttonFrame.columnconfigure(0,weight=1)
        self.buttonFrame.grid(row=2,column=0,padx=20)

        self.doneButton = Button(self.buttonFrame,text='OK',height=2,width=4,command=self.doneButtonClicked)
        self.doneButton.grid(row=0,column=0,columnspan=2)

        self.keyCombTxtbox.delete(0,END)
        self.keyCombTxtbox.insert(0,self.keyComb)
    def show(self):
        self.root.wm_deiconify()
        self.root.wait_window()
        return self.keyComb
    def doneButtonClicked(self):
        print(self.root.geometry())
        self.keyComb = self.keyCombTxtbox.get()
        self.root.destroy()
    def checkCommand(self,text):
        keyComb = self.keyCombTxtbox.get()

        def add_text(entry,entryText, addText):
            if entryText=='':
                entry.insert(0,addText)
            else:
                entry.delete(0,END)
                entry.insert(0,','.join([entryText,addText]))

        def delete_text(entry,entryText,deleteText):
            keys = entryText.split(',')
            try:
                keys.remove(text)
            except:
                print(text)
                print(keys)
                raise ValueError
            entry.delete(0,END)
            entry.insert(0,','.join(keys))

        textPos = self.specialKeyStrings.index(text)
        varValue = self.specialKeyVars[textPos].get()
        entry = self.specialKeyCbtn[textPos]
        if varValue:
            add_text(self.keyCombTxtbox,keyComb,text)
        else:
            delete_text(self.keyCombTxtbox,keyComb,text)

    def validateKey(self, S, P):
        keys = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
        ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
        'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
        'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
        'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
        'browserback', 'browserfavorites', 'browserforward', 'browserhome',
        'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
        'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
        'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
        'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
        'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
        'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
        'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
        'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
        'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
        'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
        'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
        'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
        'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
        'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
        'command', 'option', 'optionleft', 'optionright']
        if P=='':
            return True
        temp = P.split(',')
        if temp.count('') > 1:
            return False
        for key in temp:
            if key.lower() not in keys and key != '':
                return False
        return True


class ChooseOneKeyForm(keyCombinationForm):
    def __init__(self,keyComb,centerPoint):
        super().__init__(keyComb,centerPoint)
    def checkCommand(self, text):

        textPos = self.specialKeyStrings.index(text)
        entryVal = self.keyCombTxtbox.get()
        if self.specialKeyVars[textPos].get():
            if entryVal:
                self.specialKeyVars[textPos].set(0)
            else:
                self.keyCombTxtbox.insert(0,text)
        else:
            self.keyCombTxtbox.delete(0,END)

    def validateKey(self, S, P):
        keys = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
        ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
        'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
        'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
        'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
        'browserback', 'browserfavorites', 'browserforward', 'browserhome',
        'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
        'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
        'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
        'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
        'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
        'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
        'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
        'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
        'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
        'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
        'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
        'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
        'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
        'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
        'command', 'option', 'optionleft', 'optionright']
        if P.lower() in keys or P == '':
            return True
        return False