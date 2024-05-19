import tkinter

from ui_interface import UIInterface


class Application:

    def start(self):
        root = tkinter.Tk()
        root.wm_minsize(200, 100)
        app = UIInterface(root)
        app.mainloop()
