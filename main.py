import threading
import time
import random
import sys
import os
import download


ftpdownload=download.Update_Ftp()

update_thread = threading.Thread(target=ftpdownload.get_update,daemon=1)

update_thread.start()
while(1):
    time.sleep(1)
    if(update_thread.is_alive()==False):
        print("update thread finished")
        break
