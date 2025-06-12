
import customtkinter
import json
import os
import sys
from CTkMessagebox import CTkMessagebox
from CTkMenuBar import *
from customtkinter import filedialog
from update import check_for_updates

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

APPDATA_DIR = os.path.join(os.getenv("APPDATA"), "AccountManager")
os.makedirs(APPDATA_DIR, exist_ok=True)

LOCAL_JSON = os.path.join(APPDATA_DIR, "local.json")
GLIST_JSON = os.path.join(APPDATA_DIR, "glist.json")
MERGED_JSON = os.path.join(APPDATA_DIR, "merged.json")

if not os.path.exists(LOCAL_JSON):
    with open(LOCAL_JSON, "w") as file:
        json.dump({"games": {}}, file, indent=4)

if not os.path.exists(GLIST_JSON):
    with open(GLIST_JSON, "w") as file:
        json.dump({"games": {}}, file, indent=4)

check_for_updates()

def mergeFiles():
    with open(GLIST_JSON, 'r') as constFile:
        uploadedList = json.load(constFile)
    with open(LOCAL_JSON, "r") as localFile:
        localList = json.load(localFile)
    for game, accounts in localList['games'].items():
        if game in uploadedList['games']:
            uploadedList['games'][game].extend(accounts)
        else:
            uploadedList['games'][game] = accounts
    with open(MERGED_JSON, 'w') as finalFile:
        json.dump(uploadedList, finalFile, indent=4)

#Root Configs
root = customtkinter.CTk()
root.geometry("600x180")
root.resizable(False,False)
root.iconbitmap("kando2.ico")  #Comment this if you are in linux
customtkinter.set_default_color_theme("dark-blue")

def clear():
    for ele in root.winfo_children():
        ele.destroy()

def gameComboBoxGameGet():
    global gameValue
    with open(MERGED_JSON, "r") as jsonFile:
        data = json.load(jsonFile)
    gameValue = list(data["games"].keys())

def menuBar():
    menuBar = customtkinter.CTkFrame(root, fg_color="gray20", height=40)
    menuBar.grid(row=0, column=0, columnspan=4, sticky="ew")

    btnSelection = customtkinter.CTkButton(menuBar, text="Selection Page", command=selectionPage, fg_color="gray30", hover_color="gray50")
    btnSelection.grid(row=0, column=0, padx=5, pady=5)

    btnAdd = customtkinter.CTkButton(menuBar, text="New", command=gameAddPage, fg_color="gray30", hover_color="gray50")
    btnAdd.grid(row=0, column=1, padx=5, pady=5)

    btnLocation = customtkinter.CTkButton(menuBar, text="Location", command=locationPage, fg_color="gray30", hover_color="gray50")
    btnLocation.grid(row=0, column=2, padx=5, pady=5)

    btnRemove = customtkinter.CTkButton(menuBar, text="Remove", command=removePage, fg_color="gray30", hover_color="gray50")
    btnRemove.grid(row=0, column=3, padx=5, pady=5)

def selectionPage():
    mergeFiles()
    def getInfo(choice):
        with open(MERGED_JSON,'r') as jsonFile:
            data = json.load(jsonFile)
            gameID = data["games"][choice][0]["ID"]
            gamePW = data["games"][choice][0]["PW"]
            gamePlatform = data["games"][choice][0]["Platform"]            
            idLabel.configure(text = gameID)
            pwLabel.configure(text = gamePW)
            platformLabel.configure(text=gamePlatform)

    def copyID():
        id = idLabel.cget("text")
        root.clipboard_clear()
        root.clipboard_append(id)
        root.update()
        
    def copyPW():
        pw = pwLabel.cget("text")
        root.clipboard_clear()
        root.clipboard_append(pw)
        root.update()

    def startGame():
        game = comboBox.get()
        if game != "Choose a Game":
            with open(MERGED_JSON,'r') as files:
                data = json.load(files)
                location = data['games'][game][0]['LC']
                if (location != ""):
                    os.startfile(location)
                else:
                    CTkMessagebox(title="Error",message="No location added for this game.",icon="warning")
        else:
            CTkMessagebox(title="Error",message="Choose a game before you start.",icon="warning")


    clear()
    gameComboBoxGameGet()
    root.title("Game List")
    root.resizable(False,False)

    menuBar()

    #GAMELIST COMBOBOX

    comboBox = customtkinter.CTkComboBox(root,values=gameValue,state="readonly",width=250,command=getInfo)
    comboBox.set("Choose a Game")
    comboBox.grid(row=1,column = 1,padx = 10,pady = 15)

    #ID&PW&PLATFORM LABELS
    idLabel = customtkinter.CTkLabel(master=root,text="")
    idLabel.grid(row = 3,column = 0)
    pwLabel = customtkinter.CTkLabel(master=root,text="")
    pwLabel.grid(row = 3,column = 1)
    platformLabel = customtkinter.CTkLabel(master=root,text="")
    platformLabel.grid(row = 3,column = 2,padx=15)

    #ID&PW COPY BUTTONS
    idCopyButton = customtkinter.CTkButton(master=root,text="Copy",command=copyID)
    idCopyButton.grid(row =4,column = 0)

    pwCopyButton = customtkinter.CTkButton(master=root,text="Copy",command=copyPW)
    pwCopyButton.grid(row =4,column = 1)

    #START GAME BUTTON
    startGameButton = customtkinter.CTkButton(master=root,text="Start Game",command=startGame)
    startGameButton.grid(row=4,column=2)

def gameAddPage():
    clear()
    menuBar()
    
    def getEntry():
        name = newGameEntry.get()
        userID = userIDEntry.get()
        userPW = userPWEntry.get()
        gamePlatform = platformComboBox.get()

        if (name == "NewGameName" or userID == "User ID" or userPW == "User PW" or gamePlatform == "Choose a Platform"):
            CTkMessagebox(title="Error",message="Enter full information about game!",icon="warning")
        else:

            mainfile = open(LOCAL_JSON)
            data = json.load(mainfile)

            data["games"][name] = [{"ID":userID,"PW":userPW,"Platform":gamePlatform,"LC":""}]

            with open(LOCAL_JSON,'w') as jsonfile:
                json.dump(data,jsonfile,
                        indent=4,
                        separators=(',',': '))
            CTkMessagebox(title="Game Added",message="Game is added to library successfully!",icon="check")

    #Got to return first page here 
    root.title("Add Game/Account")
    root.geometry("600x180")
    root.resizable(False,False)
    
    #New Game Entry
    newGameEntry = customtkinter.CTkEntry(master=root,width=150)
    newGameEntry.insert(0,"New Game Name")
    newGameEntry.grid(row=1,column=0,padx=20,pady=10)
    
    userIDEntry = customtkinter.CTkEntry(master=root,width=150)
    userIDEntry.insert(0,"User ID")
    userIDEntry.grid(row=2,column=0,padx=20,pady=10)

    userPWEntry = customtkinter.CTkEntry(master=root,width=150)
    userPWEntry.insert(0,"User PW")
    userPWEntry.grid(row=4,column=0,padx=20,pady=10)

    platformComboBox = customtkinter.CTkComboBox(master=root,width=175,state="readonly",values=("Steam","Epic Games","Ubisoft","Ea Play","Other"))
    platformComboBox.set("Choose a Platform")
    platformComboBox.grid(row= 1, column=1,columnspan = 1,padx=20,pady=10)
    
    #Buttons
    addButton = customtkinter.CTkButton(master=root,text="Add",command=getEntry,width=175)
    addButton.grid(row=2,column=1)

def locationPage():
    
    def open_text_file(): 
        global fileLocation
        filetypes = (('All files', '*.*'),) 
        f = filedialog.askopenfile(filetypes=filetypes, 
                        initialdir="D:/Downloads") 
        
        fileLocationStr = str(f)
        fileLocation = fileLocationStr.split("'")[1]

        #test
        locationLabel.configure(text=fileLocation,wraplength = 400)

    def replace():
        game = combobox.get()
        if game != "Choose a Game":
            try : 
                fileLocation
            except NameError:
                CTkMessagebox(title="Error",message="You need to choose location also.",icon="warning")

            else:
                with open(MERGED_JSON,'r') as files:
                    data = json.load(files)
                #game  = combobox.get()
                data["games"][game][0]['LC'] = fileLocation

                with open(MERGED_JSON,'w') as files:
                    json.dump(data,files,indent=2)
                CTkMessagebox(title="Successful!",message="Location replaced successfully!",icon="check")
        else:CTkMessagebox(title="Error",message="Choose a game to replace location.",icon= 'warning')

    clear()
    
    root.title("Game Location")
    root.geometry("600x180")
    root.resizable(False,False)
    gameComboBoxGameGet()
    menuBar()

    #GameComboBox
    combobox = customtkinter.CTkComboBox(master=root,state="readonly",values=gameValue,width=250)
    combobox.set("Choose a Game")
    combobox.grid(row = 1,column = 0, padx = 5,pady = 20)

    #Location Label
    locationLabel = customtkinter.CTkLabel(master=root,text="",width=3)
    locationLabel.grid(row = 2,column = 0,padx=5,pady =10 )

    #Browse Button
    browseButton = customtkinter.CTkButton(master=root,text="Browse",command=open_text_file)
    browseButton.grid(row = 1,column = 1)

    #Replace Button
    replaceButton = customtkinter.CTkButton(master=root,text="Replace",command=replace)
    replaceButton.grid(row = 2,column =1 )

def removePage():
    clear()
    gameComboBoxGameGet()
    menuBar()
    root.title("Remove Game")
    root.resizable(False,False)

    def removeGame():
        gameName = gameToRemove.get()
        if (gameName != "Choose a Game To Remove"):
            lastChance = CTkMessagebox(title="Are you sure ?",message=f"Are you sure to remove {gameName}?",option_1="No",option_2="Yes")
            ans = lastChance.get()
            if (ans == "Yes"):
 
                try:
                    with open(LOCAL_JSON, 'r') as file:
                        data = json.load(file)

                    if gameName in data["games"]:
                        del data["games"][gameName]

                        with open(LOCAL_JSON, 'w') as file:
                            json.dump(data, file, indent=4)
                        CTkMessagebox(title="Successful",message=f"{gameName} removed successfully.",icon="check")
                    else:
                        CTkMessagebox(title="Error,",message=f"{gameName} is not able to remove.",icon="warning")

                    gameComboBoxGameGet()
                    gameToRemove['values'] = gameValue
                    gameToRemove.set("Choose a Game To Remove")

                except FileNotFoundError:
                    print("One or both of the files (local.json) couldn't be found.")
                except json.JSONDecodeError:
                    print("local.json file is broken.")
            else:pass
        else:
            CTkMessagebox(title="Error",message="Choose a game first to remove.",icon='warning')
    #Game ComboBox 
    gameToRemove = customtkinter.CTkComboBox(master=root,values=gameValue,state="readonly",width=250)
    gameToRemove.set("Choose a Game To Remove")
    gameToRemove.grid(row = 1,column = 0, padx = 5,pady = 40)


    #RemoveButton
    removeButton = customtkinter.CTkButton(master=root,text="Remove",command=removeGame)
    removeButton.grid(row = 1,column = 1,padx = 5,pady = 30)

selectionPage()
root.mainloop()