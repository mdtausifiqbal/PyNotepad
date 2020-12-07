from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename

class NotePad(Tk):

    DEFAULT_FILENAME = "Untitled"
    DEFAULT_WINDOW_SIZE = "500x600"
    DEFAULT_CONTENT = ""
    DEFAULT_FILE_TYPES = (
        ("Text Document", "*.txt*"),
        ("All Files", "*.*")
    )

    def __init__(self):
        Tk.__init__(self)
        self.setCurrentFileName("")
        self.geometry(NotePad.DEFAULT_WINDOW_SIZE)

        self.initMenuBar()
        self.initTextAreaWithScrollBar()

    def initMenuBar(self):
        #Create Menubar
        menubar = MenuBar(self)
        self.configure(menu = menubar)

    def initTextAreaWithScrollBar(self):
        #Create Scrollbar
        yscrollbar = Scrollbar(self)
        yscrollbar.pack( side = RIGHT, fill = Y )

        self.text_area = Text(self, yscrollcommand=yscrollbar.set)
        self.text_area.pack(expand=True, fill=BOTH, side=LEFT)

        yscrollbar.config( command = self.text_area.yview )
        self.setText(NotePad.DEFAULT_CONTENT)

    def setText(self, value):
        self.text_area.delete(1.0, END)
        self.text_area.insert(END, value)

    def getText(self):
        return self.text_area.get(1.0, END)

    def setCurrentFileName(self, value):
        self.currentfilename = value
        filename = NotePad.DEFAULT_FILENAME if value == "" else value
        self.title(filename + " - " + "Notepad")


    def getCurrentFileName(self):
        return self.currentfilename

class MenuBar(Menu):
    
    def __init__(self, parent):
        self.parent = parent
        self.notepad = parent
        Menu.__init__(self, parent)
        self.add_cascade(label = "File", menu = FileMenu(self))


class FileMenu(Menu):
    
    def __init__(self, parent):
        self.parent = parent
        self.notepad = parent.parent
        Menu.__init__(self, parent, tearoff = 0)
        self.add_command(label = "New", command = self.newFile)
        self.add_command(label = "New Window", command = self.newWindow)
        self.add_command(label = "Open...", command = self.openFile)
        self.add_command(label = "Save", command = self.saveFile)
        self.add_command(label = "Save As", command = self.saveAsFile)
        self.add_separator()
        self.add_command(label = "Exit", command = self.exit)


    def newFile(self):
        self.notepad.setText(NotePad.DEFAULT_CONTENT)

    def newWindow(self):
        new_notepad = NotePad()
        new_notepad.mainloop()

    def openFile(self):
        filename = askopenfilename(initialdir = "/", title="Open", filetypes=NotePad.DEFAULT_FILE_TYPES)
        with open(filename, mode="r") as file:
            self.newFile()
            self.notepad.setText(file.read())
            self.notepad.setCurrentFileName(filename)

    def saveFile(self):
        if self.notepad.getCurrentFileName() == "":
            self.saveAsFile()
        else:
            self._writeFile(self.notepad.getCurrentFileName(), self.notepad.getText())


    def saveAsFile(self):
        files = NotePad.DEFAULT_FILE_TYPES
        filename = asksaveasfilename(filetypes=files, defaultextension=files)
        self.notepad.setCurrentFileName(filename)
        self.saveFile()

    
    def _writeFile(self, filename, content):
        with open(filename, mode="w") as file:
            file.write(content)
            file.close()

    def exit(self):
        self.notepad.quit()


window = NotePad()
window.mainloop()