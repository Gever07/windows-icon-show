import tkinter as tk
from tkinter import messagebox
import win32gui, win32process, commctrl, ctypes, random, time, math, pyautogui, win32com.client
import winreg

def set_desktop_grid(enabled):
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
        val = 1 if enabled else 0
        winreg.SetValueEx(key, "IconsOnly", 0, winreg.REG_DWORD, val) 
        win32gui.SendMessage(win32gui.GetDesktopWindow(), win32con.WM_SETTINGCHANGE, 0, 0)
        winreg.CloseKey(key)
    except Exception as e:
        pass

class BossDesktopShow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.screen_width, self.screen_height = pyautogui.size()
        self.original_positions = {}
        self.start_show()

    def show_timer(self, stage, time_left):
        if not hasattr(self, 'hud'):
            self.hud = tk.Toplevel()
            self.hud.overrideredirect(True)
            self.hud.attributes('-topmost', True)
            self.hud.geometry("400x120+100+100")
            self.hud.configure(bg='black')
            self.label = tk.Label(self.hud, text="", font=('Impact', 30), fg='red', bg='black', borderwidth=5, relief="ridge")
            self.label.pack(fill='both', expand=True)
        self.label.config(text=f"{stage}\n{time_left:.1f}s")
        self.hud.update()

    def start_show(self):
        win32com.client.Dispatch("Shell.Application").MinimizeAll()
        
        set_desktop_grid(False)
        time.sleep(1.0)
        
        hwnd = win32gui.FindWindowEx(win32gui.FindWindowEx(win32gui.FindWindow("Progman", "Program Manager"), 0, "SHELLDLL_DefView", None), 0, "SysListView32", None)
        icon_count = win32gui.SendMessage(hwnd, commctrl.LVM_GETITEMCOUNT, 0, 0)
        
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        ph = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, pid)
        p_mem = ctypes.windll.kernel32.VirtualAllocEx(ph, 0, 8, 0x1000, 0x04)
        
        for i in range(icon_count):
            win32gui.SendMessage(hwnd, commctrl.LVM_GETITEMPOSITION, i, p_mem)
            pos = (ctypes.c_long * 2)()
            ctypes.windll.kernel32.ReadProcessMemory(ph, p_mem, ctypes.byref(pos), 8, None)
            self.original_positions[i] = (pos[0], pos[1])

        cx, cy = self.screen_width // 2, self.screen_height // 2
        
        stages = [
            ("CHAOS", 5, lambda i, t: (random.randint(50, self.screen_width-50), random.randint(50, self.screen_height-50))),
            ("SMILE", 4, lambda i, t: (cx - 100 + (i%2)*200, cy - 100) if i < 4 else (cx + 200*math.cos(math.pi*((i-4)/(icon_count-4)) + math.pi), cy + 150*math.sin(math.pi*((i-4)/(icon_count-4))))),
            ("HEART", 4, lambda i, t: (cx + 20*(16*math.sin((i/icon_count)*2*math.pi)**3), cy - 20*(13*math.cos((i/icon_count)*2*math.pi) - 5*math.cos(2*(i/icon_count)*2*math.pi) - 2*math.cos(3*(i/icon_count)*2*math.pi) - math.cos(4*(i/icon_count)*2*math.pi)))),
            ("STAR", 4, lambda i, t: (cx + 200*math.cos(5*(i/icon_count)*2*math.pi)*math.cos((i/icon_count)*2*math.pi), cy + 200*math.cos(5*(i/icon_count)*2*math.pi)*math.sin((i/icon_count)*2*math.pi))),
            ("INFINITY", 4, lambda i, t: (cx + 250*math.cos((i/icon_count)*2*math.pi)/(1 + math.sin((i/icon_count)*2*math.pi)**2), cy + 250*math.cos((i/icon_count)*2*math.pi)*math.sin((i/icon_count)*2*math.pi)/(1 + math.sin((i/icon_count)*2*math.pi)**2)))
        ]

        for name, duration, shape_func in stages:
            start = time.time()
            while time.time() - start < duration:
                self.show_timer(name, duration - (time.time() - start))
                elapsed = time.time() - start
                for i in range(icon_count):
                    tx, ty = shape_func(i, elapsed)
                    ctypes.windll.user32.SendMessageW(hwnd, commctrl.LVM_SETITEMPOSITION, i, (int(ty) << 16) | (int(tx) & 0xFFFF))
                time.sleep(0.05)

        self.hud.destroy()
        if messagebox.askyesno("Finish", "Boss, the show is over! Restore icons to their original positions?"):
            for i, pos in self.original_positions.items():
                ctypes.windll.user32.SendMessageW(hwnd, commctrl.LVM_SETITEMPOSITION, i, (pos[1] << 16) | (pos[0] & 0xFFFF))
        
        set_desktop_grid(True)
        self.root.destroy()

if __name__ == "__main__":
    BossDesktopShow()