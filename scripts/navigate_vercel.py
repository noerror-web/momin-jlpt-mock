import ctypes
import time
import subprocess

# Set clipboard
url = "https://vercel.com/new/import?s=https%3A%2F%2Fgithub.com%2Fnoerror-web%2Fmomin-jlpt-mock"
subprocess.run(['powershell', '-Command', f'Set-Clipboard -Value "{url}"'])

user32 = ctypes.windll.user32

def switch_chrome():
    def cb(hwnd, extra):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            title = buff.value
            if 'Chrome' in title or 'Vercel' in title or 'Netflix' in title or 'Google' in title:
                print(f"Restoring window: {title}")
                user32.ShowWindow(hwnd, 9) # SW_RESTORE
                user32.ShowWindow(hwnd, 3) # SW_MAXIMIZE
                user32.SetForegroundWindow(hwnd)
                user32.SwitchToThisWindow(hwnd, True)
                return False
        return True
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    user32.EnumWindows(EnumWindowsProc(cb), 0)

switch_chrome()
time.sleep(1.0)

code = '''
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.SendKeys]::SendWait('^l')
Start-Sleep -Milliseconds 300
[System.Windows.Forms.SendKeys]::SendWait('^v')
Start-Sleep -Milliseconds 300
[System.Windows.Forms.SendKeys]::SendWait('{ENTER}')
'''
subprocess.run(['powershell', '-Command', code])
print('Restored Chrome and navigated to exact Vercel import URL!')
