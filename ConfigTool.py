import tkinter as tk
import os, json
from tkinter import filedialog, ttk

NORMAL_FONT = ("Helvetica", 12)

# Settings definitions
libraryroot_location = "/steamui/css/libraryroot.css"
default_tilt = "    transform: rotateX(3deg) translateZ(15px);\n"
disable_tilt = "    transform: translateZ(15px);\n"
default_card_hover_colors = "    filter: brightness(1.1) contrast(0.95) saturate(1);\n"
custom_card_hover_colors = "    filter: brightness(1.1) contrast(1) saturate(1);\n"

class ConfigureTool(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.wm_title(self, "Steam Library Config")
        tk.Wm.title(self, "Steam Library Config")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Add additional pages here
        for F in (StartPage, AboutPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column = 0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        lblStatus = tk.Label(self, text ="yoyoyo", font=NORMAL_FONT)
        lblStatus.pack(pady=10, expand=True)
        lblInfo = tk.Label(self, text ="", font=NORMAL_FONT)
        lblInfo.pack(expand=True)

        disableTilt = tk.BooleanVar()
        disableTilt.set(False)
        chkDisableTilt = ttk.Checkbutton(self, text="Disable library cart tilt", variable=disableTilt, command=lambda: RemoveTilt(disableTilt.get()))
        chkDisableTilt.pack(side="top", expand=True, anchor="s")

        btnSteam = ttk.Button(self, text="Set Steam Directory", command=lambda: AskForSteamDirectory(lblInfo))
        btnSteam.pack()

class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text ="About page", font=NORMAL_FONT)
        label.pack(side="top", anchor="nw")

def AskForSteamDirectory(label):
    global steamDirectory
    steamDirectory = tk.filedialog.askdirectory()
    label.configure(text=steamDirectory)

#TODO: Completely redo this.
# Use the data index to change the values (get index)
# Use generic function to edit the lines
def RemoveTilt(value):       
    if (value == True):
        with open(steamDirectory + libraryroot_location, 'r') as file:
            data = file.readlines()
        for line in data:
            if (line == "  .appportrait_HoversEnabled_54PuC .appportrait_LibraryItemBox_WYgDg:hover:not(.appportrait_Landscape_3VOR2) {\n"):
                data[13731] = disable_tilt
        with open(steamDirectory + libraryroot_location, 'w') as file:
            file.writelines(data)

app = ConfigureTool()
app.geometry("400x250")
app.mainloop()
