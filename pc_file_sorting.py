import sys
import re
import os
from tkinter import*
import tkinter.filedialog
import tkinter.messagebox
root = Tk()
root.withdraw()
temp_file = tkinter.filedialog.askdirectory(parent= root, initialdir =os.getcwd(),title="Select Folder to "
 "be Cleanly Sorted")
#print(temp_file)
path = temp_file+"/"#Your path here
#print(path)
files = os.listdir(path)
#print(os.listdir(path))
ext = []
for k in files:
 file_ext = os.path.splitext(k)[1]
 #print(file_ext)
 pattern = r'([\w]+)'
 match = re.search(pattern,file_ext)
 if match:
 folder_name = match.group().upper()
 path1 = path + folder_name
 #print(file_ext)
 if not os.path.exists(path1):
 os.mkdir(path1)
 os.chdir(path)
 os.system("move "+'"'+k+'"'+" "+path1)#double quote embed in single colon
 ext.append(folder_name)
if len(temp_file) > 0:
 tkinter.messagebox.showinfo(title="Processing Done",message="Files are cleanly sorted.")
