import tkinter as tk
import os, json
from tkinter import filedialog, ttk

NORMAL_FONT = ("Helvetica", 12)

# Settings definitions
libraryroot_location = "/steamui/css/libraryroot.css"
#default_card_hover_colors = "    filter: brightness(1.1) contrast(0.95) saturate(1);\n"
#custom_card_hover_colors = "    filter: brightness(1.1) contrast(1) saturate(1);\n"

searchStrings = {
    "  .appportrait_HoversEnabled_54PuC .appportrait_LibraryItemBox_WYgDg:hover:not(.appportrait_Landscape_3VOR2) {\n" : {
        "configName" : "disableTilt",
        "default" : "    transform: rotateX(3deg) translateZ(15px);\n",
        "edited" : "    transform: translateZ(15px);\n"
    },
    ".appportrait_LibraryItemBoxShine_MyNb5 {\n" : {
        "configName" : "disableShine",
        "default" : "  opacity: 0.1;\n",
        "edited" : "  opacity: 0.0;\n"
    },
    "  .appportrait_HoversEnabled_54PuC .appportrait_LibraryItemBox_WYgDg:hover .appportrait_LibraryItemBoxShine_MyNb5 {\n" : {
        "configName" : "disableHoverShine",
        "default" : "    opacity: 0.2;\n",
        "edited" : "    opacity: 0.0;\n"
    }
}

# Create folder in users app data to store config file
appdataPath = os.getenv('APPDATA')
if not os.path.exists(appdataPath + "\\Custom-Steam-Library"):
    os.makedirs(appdataPath + "\\Custom-Steam-Library")
appdataPath += "\\Custom-Steam-Library\\"

# Default config JSON
configData = {
    "configVersion" : 0.1,
    "steamDirectory": "",
    "disableTilt": False,
    "disableShine": False,
    "disableHoverShine": False,
    "roundCartCorners": False
}

# Check if config exists. If it doesn't, write configData to new file
if not os.path.exists(appdataPath + "config.json"):
    with open(appdataPath + "config.json", "w") as outfile:
        json.dump(configData, outfile, indent=4)

# Loads the config file
with open(appdataPath + "config.json") as jsonFile:
    config = json.load(jsonFile)

class ConfigureTool(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Wm.title(self, "Steam Library Config")
        container = tk.Frame(self)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Add additional pages here
        for F in (StartPage, AboutPage, LogPage):
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

        # Variables
        disableTilt = tk.BooleanVar()
        disableTilt.set(config["disableTilt"])
        disableShine = tk.BooleanVar()
        disableShine.set(config["disableShine"])
        disableHoverShine = tk.BooleanVar()
        disableHoverShine.set(config["disableHoverShine"])

        # Page Items
        global lblStatus
        lblStatus = ttk.Label(self, text="", font=NORMAL_FONT)
        btnSave = ttk.Button(self, text="Save", command=lambda: SavePressed())
        btnLog = ttk.Button(self, text="Logs", command=lambda: controller.show_frame(LogPage))
        btnSteam = ttk.Button(self, text="Set Steam Directory", command=lambda: AskForSteamDirectory(steamDirBox))
        steamDirBox = tk.Text(self, height=1)

        chkDisableTilt = ttk.Checkbutton(self, text="Disable library cart tilt", variable=disableTilt, command=lambda: CheckboxPressed("disableTilt", disableTilt.get()))
        chkDisableShine = ttk.Checkbutton(self, text="Disable library cart shine", variable=disableShine, command=lambda: CheckboxPressed("disableShine", disableShine.get()))
        chkDisableHoverShine = ttk.Checkbutton(self, text="Disable library cart hover shine", variable=disableHoverShine, command=lambda: CheckboxPressed("disableHoverShine", disableHoverShine.get()))

        # Grid / Pack
        chkDisableTilt.pack(side=tk.TOP, expand=True, anchor=tk.CENTER)
        chkDisableShine.pack(side=tk.TOP, expand=True, anchor=tk.CENTER)
        chkDisableHoverShine.pack(side=tk.TOP, expand=True, anchor=tk.CENTER)
        lblStatus.pack(side=tk.TOP, expand=True, anchor=tk.S)
        btnSave.pack(side=tk.BOTTOM, anchor=tk.S, fill=tk.X)
        btnLog.pack(side=tk.BOTTOM, anchor=tk.S, fill=tk.X)
        btnSteam.pack(side=tk.LEFT, anchor=tk.NW)
        steamDirBox.pack(side=tk.LEFT, pady=1, anchor=tk.NW, expand=True, fill=tk.X)

        # Config
        steamDirBox.insert(tk.END, config["steamDirectory"])
        steamDirBox.config(state=tk.DISABLED)     
        

class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text ="About page", font=NORMAL_FONT)
        label.pack(side=tk.TOP, anchor=tk.NW)

class LogPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Page items
        scroll = ttk.Scrollbar(self)
        textbox = tk.Text(self)
        btnBack = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))

        # Grid
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        btnBack.pack(side=tk.BOTTOM, anchor=tk.S , fill=tk.X)
        textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Config
        scroll.config(command=textbox.yview)
        textbox.config(yscrollcommand=scroll.set)     

def SavePressed():
    if(config["steamDirectory"] != ""):
        with open(appdataPath + "config.json", "w") as outfile:
            json.dump(config, outfile, indent=4)
        EditLibrary()
        UpdateStatus("Library changes saved!")
    else:
        UpdateStatus("Steam Directory Not Set!")

def AskForSteamDirectory(steamDirBox):
    steamDirectory = tk.filedialog.askdirectory()
    config["steamDirectory"] = steamDirectory
    steamDirBox.config(state=tk.NORMAL)
    steamDirBox.delete(1.0 , tk.END)
    steamDirBox.insert(tk.END, steamDirectory)
    steamDirBox.config(state=tk.DISABLED)

def CheckboxPressed(text, value):
    config[text] = value

def UpdateStatus(status):
    lblStatus.configure(text=status)

def EditLibrary():
    with open(config["steamDirectory"] + libraryroot_location, 'r') as file:
        data = file.readlines()
    
    for line in data:
        if line in searchStrings:
            index = data.index(line)
            if (config[searchStrings[line]["configName"]] == True):
                data[index + 1] = searchStrings[line]["edited"]
            elif (config[searchStrings[line]["configName"]] == False):
                data[index + 1] = searchStrings[line]["default"]
            else:
                #Log it
                print("Error?")

    with open(config["steamDirectory"] + libraryroot_location, 'w') as file:
        file.writelines(data)


app = ConfigureTool()
#app.geometry("400x250")
app.mainloop()
