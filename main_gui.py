from tkinter import *
from tkinter.ttk import *
import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as scrolledtext
from tkinter.constants import *
import threading
#import unknown_support
import time
import image_rotate
import download
import CanModule
import can

class Toplevel1:
    
    #function and variable for controlling the update thread
    def thread_update_fn(self,Toplevel):
            update_Ftp_var.get_update(consolBox_update=self.txt)

    def info_fn(self):
            # Toplevel object which will
             # be treated as a new window
         self.btn_info.configure(state='disabled')
         newWindow = Toplevel(self.top)
 
         # sets the title of the
         # Toplevel widget
         newWindow.title("Info")
 
         # sets the geometry of toplevel
         newWindow.geometry("200x200")
         self.stop_button = tk.Button(newWindow)
         
 
         # A Label widget to show in toplevel
         Label(newWindow,
         text ="Model:64V \nFirmware version:V1.1 \nSystem Status:Good \nCreator: Mansoura Universitey \nID:VEH982496354").pack()
         #self.stop_button.pack()
         self.stop_button.configure(activebackground="#ececec")
         self.stop_button.configure(activeforeground="#000000")
         self.stop_button.configure(background="red")
         self.stop_button.configure(compound='left')
         self.stop_button.configure(disabledforeground="#a3a3a3")
         self.stop_button.configure(foreground="#000000")
         self.stop_button.configure(highlightbackground="#d9d9d9")
         self.stop_button.configure(highlightcolor="black")
         self.stop_button.configure(pady="0")
         self.stop_button.configure(text='''Close''')
         self.stop_button.place(relx=0.306, rely=0.7, height=30, width=70)

        #update button function
    def update_button_fn(self,state):
            self.battrey_satues=60
            self.consolFrame.configure(text=self.consolFrame["text"]+" \n")
            if (state=="Check for update"):
                 self.btn_updates.configure(text='''Checking....''',background="yellow")
                 #reintialize the thread var to start thread again
                 update_thread_var=threading.Thread(target=self.thread_update_fn,args=(1,),daemon=True)
                 update_thread_var.start()
            else:
                pass
             



    def Diagnose_fn(self,state):
        if(state=="Diagnose"):
            self.btn_Diagnose.configure(text='''Diagnosing''',background="yellow",state='disabled')
            self.txt.configure(state='normal')
            self.txt.insert(tk.END,"Cooling is not Responding. \n")
        else:
            pass



    
    def btn_start_algo_fn(self):
        state="Start AutoDrive"
        if(state=="Start AutoDrive"):
            self.btn_start_algo.configure(text='''Stop AutoDrive''',background="red")
            #self.icon_image.angle=180;
            self.cntrol_var_thread.start()
        else:
            self.btn_start_algo.configure(text='''Start AutoDrive''',background="#80ff80")
            pass
        pass

    #a function used in thread to check other threads for changes to update the gui based on it
    def gui_update_events(self):
       global update_Ftp_var
       while(True):
        if(update_Ftp_var.IS_RUNNING):
           self.btn_updates.configure( text="Checking.." ,background="yellow",default=tk.DISABLED)
        elif (update_Ftp_var.IS_RUNNING==False):
           self.btn_updates.configure(text='''Check for update''',background="orange",default=tk.DISABLED)
        print(self.battrey_satues)
#------------------------------------------------------------------
#add images here for battery
        self.LabetempValue.configure(text=self.batteryTemp)
        if(self.battrey_satues==70):

            Ximg=tk.PhotoImage(file="picture6.png")
            XimgLabel=tk.Label(image=Ximg)
            XimgLabel.place(relx=0.2,rely=0.5,anchor=tk.CENTER)

        elif(self.battrey_satues==60):

            Ximg=tk.PhotoImage(file="picture3.png")
            # Ximg=Ximg.subsample(2)
            # Ximg=Ximg.zoom(2)
            XimgLabel=tk.Label(image=Ximg)
            XimgLabel.place(relx=0.2,rely=0.5,anchor=tk.CENTER)
            
#------------------------------------------------------------------

        time.sleep(0.5)  


    def CAN_SYNC(self,msg=can.Message):
        if(True):
            self.batteryTemp=msg.data[0]
        self.LabetempValue.configure(text=msg.data[0])
        print("msg received \n ID:",msg.arbitration_id,"  ","Data:",msg.data)
        
        
        pass
        
#-------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'


        
        self.battrey_satues=70
        global update_thread_var
        update_thread_var=threading.Thread(target=self.thread_update_fn,args=(1,),daemon=True)

 
        global gui_thread_var
        gui_thread_var=threading.Thread(target=self.gui_update_events,daemon=True)
        
        global update_Ftp_var
        update_Ftp_var=download.Update_Ftp()

        global CANSyncThread_var
        CanSyncThread_var=threading.Thread(target=self.CAN_SYNC,daemon=True)


        self.top = top
        self.btn_start_algo = tk.Button(self.top)
        self.btn_info = tk.Button(self.top)
        self.btn_camera = tk.Button(self.top)
        self.btn_Diagnose = tk.Button(self.top)
        self.btn_updates = tk.Button(self.top)
        self.LabelBox_status = tk.Label(self.top)
        self.Label2 = tk.Label(self.top)
        self.Labetemp = tk.Label(self.top)
        self.LabetempValue = tk.Label(self.top)
        self.consolFrame = tk.LabelFrame(self.top)
        self.txt = scrolledtext.ScrolledText(self.top, undo=True)

        self.batteryVoltage=0
        self.batteryCurrent=0
        self.batteryTemp=0
        


        top.geometry("883x348+275+270")
        #top.minsize(120, 1)
        #top.maxsize(1540, 845)
        top.resizable(1,  1)
        top.title("Adas SubSystem")
        top.configure(highlightbackground="#d9d9d9",highlightcolor="black",background="#d9d9d9")



        


        
        self.btn_info.place(relx=0.781, rely=0.805, height=44, width=77)
        self.btn_info.configure(background="#d9d9d9",highlightbackground="#d9d9d9",highlightcolor="black",text='''Info''')
        self.btn_info.configure(command=lambda :self.info_fn())
        

        self.btn_updates.place(relx=0.578, rely=0.805, height=44, width=137)
        self.btn_updates.configure(text='''Check for update''',background="#d9d9d9",activebackground="#ececec",activeforeground="#000000")
        self.btn_updates.configure(disabledforeground="#a3a3a3")
        #self.btn_updates.configure(command=update_button_fn)
        self.btn_updates.configure(command=lambda :self.update_button_fn(self.btn_updates['text'] ))
        


        self.btn_Diagnose.place(relx=0.17, rely=0.805, height=44, width=147)
        self.btn_Diagnose.configure(activebackground="#ececec")
        self.btn_Diagnose.configure(background="#d9d9d9")
        self.btn_Diagnose.configure(compound='left')
        self.btn_Diagnose.configure(disabledforeground="#a3a3a3")
        self.btn_Diagnose.configure(text='''Diagnose''')
        self.btn_Diagnose.configure(command=lambda : self.Diagnose_fn(state=self.btn_Diagnose["text"]) )

        self.LabelBox_status.place(relx=0.26, rely=0.086, height=31, width=544)
        self.LabelBox_status.configure(activebackground="#ffffff")
        self.LabelBox_status.configure(highlightbackground="#d9d9d9",foreground="#400040",disabledforeground="#a3a3a3",compound='left',background="#ffffff",anchor='w',activeforeground="black",highlightcolor="black")
        self.LabelBox_status.configure(text='''Every Thing is OK & Ready To Go''')

        self.Label2.place(relx=0.215, rely=0.086, height=31, width=35)
        self.Label2.configure(activebackground="#f9f9f9",activeforeground="black",anchor='w',background="#d9d9d9")
        self.Label2.configure(compound='left',disabledforeground="#a3a3a3",foreground="#000000",highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black",text='''State:''')

        self.Labetemp.place(relx=0.45, rely=0.5, height=31, width=35)
        self.Labetemp.configure(activebackground="#f9f9f9",activeforeground="black",anchor='w',background="#d9d9d9")
        self.Labetemp.configure(compound='left',disabledforeground="#a3a3a3",foreground="#000000",highlightbackground="#d9d9d9")
        self.Labetemp.configure(highlightcolor="black",text='''Temp:''')
        self.LabetempValue.place(relx=0.45, rely=0.5, height=31, width=35)
        self.LabetempValue.configure(activebackground="#f9f9f9",activeforeground="black",anchor='w',background="#d9d9d9")
        self.LabetempValue.configure(compound='left',disabledforeground="#a3a3a3",foreground="#000000",highlightbackground="#d9d9d9")
        self.LabetempValue.configure(highlightcolor="black",text='''0''')



        #self.Text1 = tk.Text(self.top)
        #self.Text1.place(relx=0.057, rely=0.287, relheight=0.328, relwidth=0.162)
        


#---------------------------------------------------------
# -------------------comment this part to run on pc----------
        mycan=CanModule.CANOBJ()
        mycan.addListener(Callable=self.CAN_SYNC)
#----------------------------------------------------------------------
        self.txt['font'] = ('consolas', '9')
        self.txt.insert(tk.END,"\n")
        self.txt.insert(tk.END,"\n")
        self.txt.configure(state='disabled',wrap="word")
        self.txt.place(relx=0.557, rely=0.207, relheight=0.428, relwidth=0.362)
        self.txt.see("end")

        bg = PhotoImage(file = "picture3.png")
        # Create Canvas
        canvas1 = Canvas( self.top, width = 800,height = 400)
        #canvas1.pack(fill = "both", expand = True)
        #canvas1.place(x=50,y=50)
        # Display image
        canvas1.create_image( 0, 0, image = bg, anchor = "nw")

        gui_thread_var.start()
        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)
        canvas1.create_text( 200, 250, text = "Welcome")
        # Create Buttons
        button1 = Button( self.top, text = "Exit")
        button3 = Button( self.top, text = "Start")
        button2 = Button( self.top, text = "Reset")
        # Display Buttons
        button1_canvas = canvas1.create_window( 100, 10, anchor = "nw",window = button1)
        button2_canvas = canvas1.create_window( 100, 40,anchor = "nw",window = button2)
        button3_canvas = canvas1.create_window( 100, 70, anchor = "nw",window = button3)
        



if __name__ == '__main__':
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    
    _w1 = Toplevel1(_top1)
    root.mainloop()
    




