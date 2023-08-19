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
               #init the server file name and version number
             server_version_str1=0
             server_version_str2=0
             if(server_connected):
                   file_names= myftp.nlst()
                   for i in range(0,len(file_names)):
                       
                        # print("server"+file_names[i])  #list the server existing files
                        #check if the file name is update+version number using regex
                        # the file name should be st1update+version number,version number range is 0 to 99
                        #example st1update10.bin
                        
                        if(bool(re.match("st1update\d+\d+.hex",file_names[i]))):
                           server_file_name1=file_names[i]
                           server_version_str1=server_file_name1[9:-4]
                           server_file_found=True
                           print("server file version is st1 ",int(server_version_str1))
                           self.append_consol_outer(consolBox=consolBox_update,passed_text="server file version is st1 "+server_version_str1+"\n")
                           
                        #find if there is update for st2
                        
                        if(bool(re.match("st2update\d+\d+.hex",file_names[i]))):
                           server_file_name2=file_names[i]
                           server_version_str2=server_file_name2[9:-4]
                           server_file_found=True
                           print("server file version is st2 ",int(server_version_str2))
                           self.append_consol_outer(consolBox=consolBox_update,passed_text="server file version is st2 "+server_version_str2+"\n")
                        

       
       
               #find the local version number and store it in local_version_str
             local_files = os.listdir(os.getcwd())
             local_version_str1="0"
             local_version_str2="0"
             local_file_found=False
             for i in range(0,len(local_files)):
                   if(bool(re.match("st1update\d+\d+.hex",local_files[i]))):  
                       local_version_str1=local_files[i][9:-4]
                       print("local file version is st1. "+local_version_str1)
                       local_file_found=True
                       
                   elif(bool(re.match("st2update\d+\d+.hex",local_files[i]))):
                           local_version_str2=local_files[i][9:-4]
                           print("local file version is st2."+local_version_str2)
                           local_file_found=True
       
               #asssume the update file name Consists of "update"+version number so the program
               #will compare the local file with the server file to check if there is an update
       
               #compare between the server file and the local file
             if(server_file_found):
                   if((not local_file_found ) or((int(server_version_str1)>int(local_version_str1))) or (int(server_version_str2)>int(local_version_str2))):
                    with open(server_file_name1, "wb") as file:
                        # use FTP's RETR command to download the file
                       myftp.retrbinary(f"RETR {server_file_name1}", file.write)
                       print("Local file st1 updated sucssfuly to "+server_version_str1+"\n");
                    with open(server_file_name2, "wb") as file:
                        # use FTP's RETR command to download the file
                       myftp.retrbinary(f"RETR {server_file_name2}", file.write)
                       print("Local file st1 updated sucssfuly to "+server_version_str1+"\n");
                   self.append_consol_outer(consolBox_update,passed_text="Local file updated sucssfuly \n")
                  #      self.append_consol_outer(consolBox_update,passed_text="sending reset request ... "+server_version_str1+"\n")
                  #      time.sleep(0.2)
                  #      self.append_consol_outer(consolBox_update,passed_text="flashing firmware.... "+server_version_str1+"\n")
                  #      time.sleep(2)
                  #      self.append_consol_outer(consolBox_update,passed_text="flashing firmware succeeded"+server_version_str1+"\n")
             else:
                        print("no update available")
                        self.append_consol_outer(consolBox_update,passed_text="no update available\n")
             server_file_found=False
             local_file_found=False
             self.IS_RUNNING = False
             if(server_connected):
                    myftp.close();
                    server_connected=False
             self.IS_RUNNING = False
       def get_current_latest_version_number_st1(self):
            pass

