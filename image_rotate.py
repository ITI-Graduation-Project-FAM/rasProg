import tkinter as tk
from PIL import ImageTk
from PIL import Image
import time

class SimpleApp(object):
    def __init__(self, master, filename, **kwargs):
        self.master = master
        self.filename = filename
        self.canvas = tk.Canvas(master, width=20, height=20)
        global angle
        angle=0
        #self.canvas.place(relx=0.15, rely=0.35, relheight=0.25, relwidth=0.10)
        #self.update = self.draw().__next__
        #master.after(10, self.update)
    def changefilename(self,filename1):
        self.filename = filename1
        
    
    def start_rotate(self,filenamePara):
        #self.update = self.draw().__next__
        #self.master.after(10, self.update)
        self.draw(angle=0,filename1=filenamePara)

    def draw(self,angle,filename1):
        image = Image.open(filename1)
        self.angle = angle
        d=True
        self.canvas.place(relx=0.1, rely=0.3, height=150, width=150)
        tkimage = ImageTk.PhotoImage(image.rotate(self.angle))
        canvas_obj = self.canvas.create_image(75, 75, image=tkimage)
        # while True:
        # #if(True):
        #     self.canvas.place(relx=0.1, rely=0.3, height=150, width=150)
        #     tkimage = ImageTk.PhotoImage(image.rotate(self.angle))
        #     canvas_obj = self.canvas.create_image(75, 75, image=tkimage)
        #     time.sleep(0.1)
    
#root = tk.Tk()
#app = SimpleApp(root, 'D:\Picture4.png')
#root.mainloop()