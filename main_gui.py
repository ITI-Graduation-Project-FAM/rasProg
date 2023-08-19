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
         def closeinfoWindow(self,newWindow):
                newWindow.destroy()
                self.btn_info.configure(state='normal')
         
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
         text ="Model:64V \nFirmware version:V1.1 \nSystem Status:Good \nCreator: FAM_TEAM  \nID:VEH982496354").pack()
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
         #make the button close the window
         self.stop_button.configure(command=lambda :closeinfoWindow(self,newWindow=newWindow))
        

        #update button function
    def update_button_fn(self,state):
            self.consolFrame.configure(text=self.consolFrame["text"]+" \n")
            if (state=="Check for update"):
                 self.btn_updates.configure(text='''Checking....''',background="yellow")
                 #reintialize the thread var to start thread again
                 update_thread_var=threading.Thread(target=self.thread_update_fn,args=(1,),daemon=True)
                 update_thread_var.start()
            else:
                pass
             


    def btn_shutdown_fn(self):
        # get the current firmware version number from the st1 and st2
        self.mycan.send(0x10,"",False)
        self.mycan.send(0x15,"",False)
        # check if the version number is the same as the latest version number in the current files ,if not update
        # send the stop app signal to st1
        # self.mycan.send(0x33,"",False)
        

    

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
        
#------------------------------------------------------------------
#add images here for battery
        self.LabetempValue.configure(text=self.batteryTemp)
        if(self.batteryVoltage<=20):
            Ximg=tk.PhotoImage(file="battery20.png")
            Ximg=Ximg.subsample(3)
        elif(self.batteryVoltage<=40 and self.batteryVoltage>20):
            Ximg=tk.PhotoImage(file="battery40.png")
            Ximg=Ximg.subsample(3)
        elif(self.batteryVoltage<=60 and self.batteryVoltage>40):
            Ximg=tk.PhotoImage(file="battery60.png")
            Ximg=Ximg.subsample(3)
        elif(self.batteryVoltage<=80 and self.batteryVoltage>60):
            Ximg=tk.PhotoImage(file="battery80.png")
            Ximg=Ximg.subsample(3)
        elif(self.batteryVoltage<=100 and self.batteryVoltage>80):
            Ximg=tk.PhotoImage(file="battery100.png")
            Ximg=Ximg.subsample(3)

        
        # Ximg=Ximg.zoom(2)
        XimgLabel=tk.Label(image=Ximg)
        XimgLabel.configure(background="#d9d9d9")
        XimgLabel.place(relx=0.2,rely=0.5,anchor=tk.CENTER)
#------------------------------------------------------------------

        time.sleep(0.5)  

    def thread_restart_Mcu(self):
        #restart st and update if firmaewre is not the same
        if(self.st1Version!=self.st1Version):
            self.mycan.send(0x33,"",False)
            # request the st1 to update mode
            self.mycan.st1requestedstate=3
            # wait for the st1 to enter bootloader mode
            while(self.mycan.ST1currentstate!=2):
                time.sleep(0.1)
            # send the update file to the st1
            
        self.mycan.send(0x33,"",False)
        time.sleep(1)


    def CAN_SYNC(self,msg=can.Message):
        print("msg received \n ID:",hex(msg.arbitration_id),"  ","Data:",msg.data[0])
        #temp value messege
        if(msg.arbitration_id==0x11):
            self.batteryTemp=msg.data[0]
            self.LabetempValue.configure(text=msg.data[0])  

        #st1 version number
        elif(msg.arbitration_id==0x10):
            self.st1Version=msg.data[0]

        #st1 version number
        elif(msg.arbitration_id==0x15):
            self.st2Version=msg.data[0]

        #st1 battery voltage
        elif(msg.arbitration_id==0x13):
            self.batteryVoltage=msg.data[0]
            self.LabeVoltageValue.configure(text=msg.data[0])

            
        
        #st1 battery current
        elif(msg.arbitration_id==0x12):
            self.batteryCurrent=msg.data[0]
            self.LabeCurrentValue.configure(text=msg.data[0])
        
        #st1 pwm value
        elif(msg.arbitration_id==0x14):
            self.PWMValue=msg.data[0]
        
        #st1 start signal received ,send the required state
        elif(msg.arbitration_id==0x19):
            # assign the current state localy
            self.mycan.ST1currentstate=2
            # check the requested state and send the required state
            # st must be in state 2 to send the hex file
            # if(self.mycan.st1requestedstate==3 and self.mycan.ST1currentstate==2):
            #     self.mycan.send(0x16,"",False)
            #     # if no update is needed send the start signal
            # elif(self.mycan.st1requestedstate==1):
            #     self.mycan.send(0x22,"",False)
        
        #st2 start signal received ,send the required state
        elif(msg.arbitration_id==0x20):
            # assign the current state localy
            self.mycan.ST2currentstate=2
            # check the requested state and send the required state
            # st must be in state 2 to send the hex file
            # if(self.mycan.st2requestedstate==3 and self.mycan.ST2currentstate==2):
            #     self.mycan.send(0x17,"",False)
            #     # if no update is needed send the start signal
            # elif(self.mycan.st2requestedstate==1):
            #     self.mycan.send(0x21,"",False)
        
            # st1 firmware version number received
        elif(msg.arbitration_id==0x15):
            self.st1Version=msg.data[0]

            # st2 firmware version number received
        elif(msg.arbitration_id==0x10):
            self.st2Version=msg.data[0]


        
            

        
        


        
        
        
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


        
        self.battrey_satues=20
        
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
        self.LabeCurrent = tk.Label(self.top)
        self.LabeCurrentValue = tk.Label(self.top)
        self.LabeVoltage = tk.Label(self.top)
        self.LabeVoltageValue = tk.Label(self.top)
        self.txt = scrolledtext.ScrolledText(self.top, undo=True)
        self.btnShutdown=tk.Button()
        self.st1Version=1.0
        self.st2Version=1.0


        self.batteryVoltage=20
        self.batteryCurrent=0
        self.batteryTemp=50
        


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
        

    #configure the Diagnose button
        self.btn_Diagnose.place(relx=0.17, rely=0.805, height=44, width=147)
        self.btn_Diagnose.configure(activebackground="#ececec")
        self.btn_Diagnose.configure(background="#d9d9d9")
        self.btn_Diagnose.configure(compound='left')
        self.btn_Diagnose.configure(disabledforeground="#a3a3a3")
        self.btn_Diagnose.configure(text='''Diagnose''')
        self.btn_Diagnose.configure(command=lambda : self.Diagnose_fn(state=self.btn_Diagnose["text"]) )

        #configure the start button
        self.btnShutdown.configure(activebackground="#ececec",background="#d9d9d9",text="Shutdown",command=lambda :self.top.destroy())
        self.btnShutdown.place(relx=0.4, rely=0.805, height=44, width=77)

        self.LabelBox_status.place(relx=0.26, rely=0.086, height=31, width=544)
        self.LabelBox_status.configure(activebackground="#ffffff")
        self.LabelBox_status.configure(highlightbackground="#d9d9d9",foreground="#400040",disabledforeground="#a3a3a3",compound='left',background="#ffffff",anchor='w',activeforeground="black",highlightcolor="black")
        self.LabelBox_status.configure(text='''Every Thing is OK & Ready To Go''')

        self.Label2.place(relx=0.215, rely=0.086, height=31, width=35)
        self.Label2.configure(activebackground="#f9f9f9",activeforeground="black",anchor='w',background="#d9d9d9")
        self.Label2.configure(compound='left',disabledforeground="#a3a3a3",foreground="#000000",highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black",text='''State:''')

        #configure temp label and value
        self.Labetemp.configure(activebackground="#f9f9f9",activeforeground="black",anchor='w',background="#d9d9d9")
        self.Labetemp.configure(compound='left',disabledforeground="#a3a3a3",foreground="#000000",highlightbackground="#d9d9d9")
        self.Labetemp.configure(highlightcolor="black",text="Temp:")
        self.Labetemp.place(relx=0.30, rely=0.25, height=31, width=100)
        self.LabetempValue.configure(activebackground="#f9f9f9",activeforeground="black",anchor='w',background="#d9d9d9")
        self.LabetempValue.configure(compound='left',disabledforeground="#a3a3a3",foreground="#000000",highlightbackground="#d9d9d9")
        self.LabetempValue.configure(highlightcolor="black",text=str(self.batteryTemp))
        self.LabetempValue.place(relx=0.345, rely=0.25, height=31, width=35)

        #configure current label and value
        self.LabeCurrent.configure(activebackground="#f9f9f9",activeforeground="black",anchor='w',background="#d9d9d9")
        self.LabeCurrent.configure(compound='left',disabledforeground="#a3a3a3",foreground="#000000",highlightbackground="#d9d9d9")
        self.LabeCurrent.configure(highlightcolor="black",text="Current:")
        self.LabeCurrent.place(relx=0.30, rely=0.35, height=31, width=110)
        self.LabeCurrentValue.configure(activebackground="#f9f9f9",activeforeground="black",anchor='w',background="#d9d9d9")
        self.LabeCurrentValue.configure(compound='left',disabledforeground="#a3a3a3",foreground="#000000",highlightbackground="#d9d9d9")
        self.LabeCurrentValue.configure(highlightcolor="black",text=str(self.batteryCurrent))
        self.LabeCurrentValue.place(relx=0.352, rely=0.35, height=31, width=35)


        #configure voltage label and value but with bigger font
        self.LabeVoltage.configure(activebackground="#f9f9f9",activeforeground="black",anchor='w',background="#d9d9d9")
        self.LabeVoltage.configure(compound='left',disabledforeground="#a3a3a3",foreground="#000000",highlightbackground="#d9d9d9")
        self.LabeVoltage.configure(highlightcolor="black",text="Voltage:")
        self.LabeVoltage.place(relx=0.30, rely=0.45, height=31, width=110)
        self.LabeVoltageValue.configure(activebackground="#f9f9f9",activeforeground="black",anchor='w',background="#d9d9d9")
        self.LabeVoltageValue.configure(compound='left',disabledforeground="#a3a3a3",foreground="#000000",highlightbackground="#d9d9d9")
        self.LabeVoltageValue.configure(highlightcolor="black",text=str(self.batteryVoltage))
        self.LabeVoltageValue.place(relx=0.355, rely=0.45, height=31, width=35)

        



        #self.Text1 = tk.Text(self.top)
        #self.Text1.place(relx=0.057, rely=0.287, relheight=0.328, relwidth=0.162)
        


#---------------------------------------------------------
# -------------------comment this part to run on pc----------
        self.mycan=CanModule.CANOBJ()
        self.mycan.addListener(Callable=self.CAN_SYNC)
        
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
    




