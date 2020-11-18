import os

from TCP.readini import ReadIni,WriteIni
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox as messagebox

class SelectFile:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('My window')
        self.window.geometry('500x400')
        label = tkinter.Label(self.window,text='文件保存地址',bg='green',width=30,height=2)
        label.pack()
        self.text = tkinter.Text(self.window,width = 30 ,height=2)
        self.text.pack()
        self.text.insert('end',ReadIni(r'TCP\conf.ini','load_path'))
        self.test()

        self.window.mainloop()
    def FileOpen(self):
        try:
            file_name = tk.filedialog.askdirectory()
        except Exception as e:
            pass
        self.text.delete('1.0', 'end')
        self.text.insert('end',file_name)
        if os.path.isdir(file_name):
            WriteIni(r'TCP\conf.ini','load_path',file_name)
        else:
            messagebox.showinfo('error','路径错误！！！')
    def CloseWindows(self):
        self.window.quit()
    def test(self):
        b1 = tkinter.Button(self.window, text='open', width=10, height=2, command=self.FileOpen)
        b1.pack()
        b2 = tkinter.Button(self.window, text='quit', width=10, height=2, command=self.CloseWindows)
        b2.pack()

if __name__ == '__main__':
    a = SelectFile()


