from ftplib import FTP
import ftplib
import re
import os
from datetime import datetime
import time
import threading
import tkinter as tk
import tkinter.ttk as ttk

class Update_Ftp(object):
        
       IS_RUNNING=False;  

       def __init__(self):
           self.temp_str=""
           #is_running is a variable used to indcate if the the thread is still running
           self.IS_RUNNING = False
      
       

       
       #CONSOLE box is the text box in GUI that will be updated with the update process
       #this function is used to update the console box from the thread
       def append_consol_outer(self,consolBox=None,passed_text=""):
                if(consolBox!= None):
                       consolBox.configure(state='normal')
                       consolBox.insert(tk.END,passed_text)
                       consolBox.configure(state='disabled')
                       consolBox.see("end")

       #CONSOLE box is the text box in GUI that will be updated with the update process
       #this function is used to connect to the server and check for updates 
       def get_update(self,consolBox_update=None):
             server_file_found=False
             local_file_found=False
             server_connected=False
             try:
                  self.IS_RUNNING = True
                  print("trying to connect to update server...")
                  self.append_consol_outer(consolBox=consolBox_update,passed_text="trying to connect to update server...\n")
                 
                  #init the ftp server
                  myftp=FTP('ftp.byethost32.com',timeout=50)
                  myftp.login(user='b32_34585717',passwd='123456789');
                  server_connected=True
             except ftplib.all_errors:
                   print("error connecting server")
                   self.append_consol_outer(consolBox=consolBox_update,passed_text="error connecting server \n")
                   #IS_RUNNING = False
       
             # myftp.retrlines('LIST');
               #search for the update file in the server
             if(server_connected):
                   file_names= myftp.nlst()
                   for i in range(0,len(file_names)):
                       
                        print("server"+file_names[i])  #list the server existing files
                        #check if the file name is update+version number using regex
                        if(bool(re.match("update\d+\.\d+.bin",file_names[i]))):
                           server_file_name=file_names[i]
                           server_version_str=server_file_name[6:-4]
                           server_file_found=True
                           print("server file version is "+server_version_str)
                           self.append_consol_outer(consolBox=consolBox_update,passed_text="server file version is "+server_version_str+"\n")
                           break
       
               #asssume the update file name Consists of "update"+version number so the program
               #will compare the local file with the server file to check if there is an update
       
       
       
               #find the local version number and store it in local_version_str
             local_files = os.listdir(os.getcwd())
             local_version_str="0"
             for i in range(0,len(local_files)):
                   if(bool(re.match("update\d+\.\d+.binary",local_files[i]))):  
                       local_version_str=local_files[i][6:-4]
                       print("local file version is "+local_version_str)
                       local_file_found=True
                       break
       
       
               #compare between the server file and the local file
             if(server_file_found):
                   if((not local_file_found ) or((float(server_version_str)>float(local_version_str)))):
                    with open(server_file_name, "wb") as file:
                        # use FTP's RETR command to download the file
                       myftp.retrbinary(f"RETR {server_file_name}", file.write)
                       print("Local file updated sucssfuly to "+server_version_str+"\n");
                       self.append_consol_outer(consolBox_update,passed_text="Local file updated sucssfuly to "+server_version_str+"\n")
                       self.append_consol_outer(consolBox_update,passed_text="sending reset request ... "+server_version_str+"\n")
                       time.sleep(0.2)
                       self.append_consol_outer(consolBox_update,passed_text="flashing firmware.... "+server_version_str+"\n")
                       time.sleep(2)
                       self.append_consol_outer(consolBox_update,passed_text="flashing firmware succeeded"+server_version_str+"\n")
             server_file_found=False
             local_file_found=False
             self.IS_RUNNING = False
             if(server_connected):
                    myftp.close();
                    server_connected=False
             self.IS_RUNNING = False
       

