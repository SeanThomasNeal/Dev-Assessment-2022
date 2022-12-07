import DatabaseManager
import DataInitializer
import StringManager
import ValidateLib
from tkinter import *
import os

#####MAIN#####

path = os.getcwd()
file_path = path + "/Main.db"
isExist = os.path.exists(file_path)
if isExist == False:
    DataInitializer.InitializeDatabase()

def ClearFrame():
    for widget in RootFrame.winfo_children():
        widget.destroy()
#Clears Frame

def DisplayPrevMeet(meeting_type, output, listbox):
    output.delete(0.0, END)
    listbox.delete(0, END)
    if meeting_type == "-type-":
        output.insert(END, "Please select meeting type")
    else:
        LastMeeting = DatabaseManager.FetchLastMeeting(meeting_type)
        if LastMeeting == []:
            output.insert(END, "No previous items to fetch"+"\n"+"Click Create Meeting to make\nempty meeting")
        else:
            LastMeetingID = LastMeeting[0]
            output.insert(END, "Meeting: "+LastMeetingID+"\n"+"Select items to carry forward:")
            MeetingItems = DatabaseManager.FetchMeetingItems(LastMeetingID)
            for Item in MeetingItems:
                listbox.insert(END, Item)
#Displays previous meeting of specific type and creates listbox of items

def GenerateMeetingListbox(menu, listbox):
    listbox.delete(0, END)
    meeting_type = menu.get()
    if meeting_type == "-type-":
        listbox.insert(END, "Please select meeting type")
    else:
        MeetingIDList = []
        MeetingList = DatabaseManager.FetchAllMeetings(meeting_type)
        for Meeting in MeetingList:
            MeetingID = Meeting[0]
            MeetingIDList.append(MeetingID)
        for ID in MeetingIDList:
            listbox.insert(END, ID)
#Generates list from meeting type and inputs into chosen listbox
    
def DisplayMeet(meeting, output):
    output.delete(0.0, END)
    meeting_display = (
    "Meeting ID: " + meeting[0] + "\n" +
    "Meeting Type: " + meeting[1] + "\n" +
    "Date: " + meeting[2] + "\n" +
    "Time: " + meeting[3]
    )
    output.insert(END, meeting_display)
#Formats and displays chosen meeting to chosen output

def CreateMeet(meeting_type, date, time, output, listbox):
    output.delete(0.0, END)
    ValidDate = ValidateLib.ValidateDate(date)
    ValidTime = ValidateLib.ValidateTime(time)
    if meeting_type == "-type-":
        output.insert(END, "Please select meeting type")
    elif ValidDate is None:
        output.insert(END, "Please input valid date\n")
        output.insert(END, "Format: (yyyy-mm-dd)")
    elif ValidTime is None:
        output.insert(END, "Please input valid time\n")
        output.insert(END, "Format: (hh:mm)")
    else:
        ItemList = []
        for i in listbox.curselection():
            ItemList.append(listbox.get(i))
        MeetingID = DatabaseManager.GenerateNewMeetingID(meeting_type)
        for Item in ItemList:
            MeetingItemStatus = StringManager.CreateMeetingItemStatus(MeetingID, Item)
            DatabaseManager.InsertData("Meeting Item Status", MeetingItemStatus)
        MeetingData = StringManager.CreateMeetingData(MeetingID, meeting_type, date, time)
        DatabaseManager.InsertData("Meeting", MeetingData)
#Creates and inserts meeting into database from input data.
        Meeting = DatabaseManager.FetchMeeting(MeetingID)
        RaiseViewMeetingFrame(Meeting)
#Views created meeting

def ViewSelectedMeet(listbox):
    CurSelection = listbox.curselection()
    if CurSelection == ():
        return None
    else:
        MeetingID = listbox.get(CurSelection)
        if MeetingID == "Please select meeting type":
            return None
        else:
            Meeting = DatabaseManager.FetchMeeting(MeetingID)
            RaiseViewMeetingFrame(Meeting)
#Views meeting selected in chosen listbox

def UpdateSelectedItem(meeting_id, listbox):
    CurSelection = listbox.curselection()
    if CurSelection == ():
        return None
    else:
        Item = listbox.get(CurSelection)
        RaiseUpdateMISFrame(meeting_id, Item)
    
#Raises frame for updating selected Item

def UpdateMISButton(meeting_id, item_id, action, status, DDate, CDate, Person, output):
    output.delete(0.0, END)
    ValidDD = ValidateLib.ValidateDate(DDate)
    ValidCD = ValidateLib.ValidateDate(CDate)
    if ValidDD is None:
        output.insert(END, "Please input valid due date\n")
        output.insert(END, "yyyy-mm-dd")
    elif ValidCD is None:
        output.insert(END, "Please input valid completed date\n")
        output.insert(END, "yyyy-mm-dd")
    else:
        DatabaseManager.UpdateMISData(meeting_id, item_id, action, status, ValidDD, ValidCD, Person)
        OutputString = "Updated Meeting Item Status:\nMeeting: " +meeting_id+", "+item_id
        output.insert(END, OutputString)
#Validates inputs then updates Meeting Item Status if valid

root = Tk()
root.title(" ")

RootFrame = Frame(root)
RootFrame.grid(row=0, column=0, sticky="news")

###Root Frame###
def RaiseRootFrame():
    ClearFrame()
    Label(RootFrame, text="Choose Task").grid(row=0, column=0, sticky=N)
    Button(RootFrame, text="Capture New Meeting", width=30, command=lambda:RaiseCreateMeetingFrame()).grid(row=2, column=0, sticky=N)
    Button(RootFrame, text="Select Meeting",width=30, command=lambda:RaiseSelectMeetingFrame()).grid(row=3, column=0, sticky=N)
    Button(RootFrame, text="Roll back to Initial Data", width=30, command=lambda:DataInitializer.InitializeDatabase()).grid(row=4, column=0, sticky=N)
    RootFrame.tkraise()

###Create Meeting Frame###
def RaiseCreateMeetingFrame():
    ClearFrame()
    Label(RootFrame, text="Select Meeting Type:").grid(row=0, column=0, sticky=N)
    MeetingTypeMenu = StringVar()
    MeetingTypeMenu.set("-type-")
    OptionMenu(RootFrame, MeetingTypeMenu, "MANCO", "Finance", "PTL").grid(row=1, column=0, sticky=N)
#Creates Option Menu from set meeting types
    Label(RootFrame, text="Input Date:").grid(row=2, column=0, sticky=N)
    DateEntry = Entry(RootFrame, width=30, bg="light blue")
    DateEntry.grid(row=3, column=0, sticky=N)
#Date Input
    Label(RootFrame, text="Input Time:").grid(row=4, column=0, sticky=N)
    TimeEntry = Entry(RootFrame, width=30, bg="light blue")
    TimeEntry.grid(row=5, column=0, sticky=N)
#Time Input
    Label(RootFrame, text="").grid(row=10, column=0, sticky=N)
    Output = Text(RootFrame, width=30, height=3, bg="light gray")
    Output.grid(row=11, column=0, sticky=N)
#Creates display
    Label(RootFrame, text="Previous Meeting Items:").grid(row=12, column=0, sticky=N)
    MeetItemListbox = Listbox(RootFrame, selectmode = "multiple", width=30, height=5)
    MeetItemListbox.grid(row=13, column=0, sticky=N)
#Creates Listbox for previous meeting items
    Button(RootFrame, text="Get Previous Meeting Items", width=30, command=lambda:DisplayPrevMeet(MeetingTypeMenu.get(), Output, MeetItemListbox)).grid(row=14, column=0, sticky=N)
#Fetches and displays last meeting of chosen type
    Button(RootFrame, text="Create Meeting", width=30, command=lambda:CreateMeet(MeetingTypeMenu.get(), DateEntry.get(), TimeEntry.get(), Output, MeetItemListbox)).grid(row=20, column=0, sticky=N)
    Button(RootFrame, text="Back", width=30, command=lambda:RaiseRootFrame()).grid(row=99, column=0, sticky=N)
#Creates Buttons

###Select Meeting Frame###
def RaiseSelectMeetingFrame():
    ClearFrame()
    Label(RootFrame, text="Select Meeting Type:").grid(row=0, column=0, sticky=N)
    MeetingTypeMenu = StringVar()
    MeetingTypeMenu.set("-type-")
    OptionMenu(RootFrame, MeetingTypeMenu, "MANCO", "Finance", "PTL").grid(row=1, column=0, sticky=N)
#Creates Option Menu from set meeting types
    MeetingListbox = Listbox(RootFrame, selectmode = "single", width=30, height=5)
    MeetingListbox.grid(row=12, column=0, sticky=N)
#Creates Listbox for meetings
    Button(RootFrame, text="Fetch Meeting List", command=lambda:GenerateMeetingListbox(MeetingTypeMenu, MeetingListbox)).grid(row=10, column=0, sticky=N)
#Generates Listbox options
    Button(RootFrame, text="View Meeting", width=30, command=lambda:ViewSelectedMeet(MeetingListbox)).grid(row=20, column=0, sticky=N)
    Button(RootFrame, text="Back", width=30, command=lambda:RaiseRootFrame()).grid(row=99, column=0, sticky=N)
#Creates buttons

###View Meeting Frame###
def RaiseViewMeetingFrame(meeting):
    ClearFrame()
    Label(RootFrame, text="Current Meeting").grid(row=0, column=0, sticky=N)
    CurrentMeetDataOutput = Text(RootFrame, width=30, height=3, bg="light gray")
    CurrentMeetDataOutput.grid(row=2, column=0, sticky=N)
    DisplayMeet(meeting, CurrentMeetDataOutput)
#Displays Meeting
    Label(RootFrame, text="Select Item:").grid(row=3, column=0, sticky=N)
    ItemListbox = Listbox(RootFrame, selectmode = "single", width=30, height=5)
    ItemListbox.grid(row=4, column=0, sticky=N)
#Creates Listbox
    ItemList = DatabaseManager.FetchMeetingItems(meeting[0])
    for Item in ItemList:
        ItemListbox.insert(END, Item)
#Fetches items to be options in listbox
    Button(RootFrame, text="Print Meeting Minutes", width=30, command=lambda:RaisePrintMeetingFrame()).grid(row=10, column=0, sticky=N)
    Button(RootFrame, text="Add Meeting Item", width=30, command=lambda:RaiseAddItemFrame()).grid(row=11, column=0, sticky=N)
    Button(RootFrame, text="Edit Meeting Item", width=30, command=lambda:RaiseEditItemFrame()).grid(row=12, column=0, sticky=N)
    Button(RootFrame, text="Update Meeting Item Status", width=30, command=lambda:UpdateSelectedItem(meeting[0], ItemListbox)).grid(row=13, column=0, sticky=N)
    Button(RootFrame, text="View Meeting Item History", width=30, command=lambda:RaiseViewItemHistoryFrame()).grid(row=14, column=0, sticky=N)
    Button(RootFrame, text="Back", width=30, command=lambda:RaiseRootFrame()).grid(row=99, column=0, sticky=N)
#Creates Buttons

###SelectItemFrame###

###Update MIS Frame###
def RaiseUpdateMISFrame(meeting_id, item_id):
    ClearFrame()
    CurrentMIS = "Meeting "+meeting_id+": "+item_id
    Label(RootFrame, text=CurrentMIS).grid(row=0, column=0, sticky=N)
    Meeting = DatabaseManager.FetchMeeting(meeting_id)
    Output = Text(RootFrame, width=30, height=2, bg="light gray")
    Output.grid(row=1, column=0, sticky=N)
#Creates display
    Label(RootFrame, text="Input Action:").grid(row=10, column=0, sticky=N)
    UpdAction = Entry(RootFrame, width=30, bg="light blue")
    UpdAction.grid(row=11, column=0, sticky=N)
#Update Action Input
    Label(RootFrame, text="Input Status:").grid(row=12, column=0, sticky=N)
    UpdStatus = Entry(RootFrame, width=30, bg="light blue")
    UpdStatus.grid(row=13, column=0, sticky=N)
#Update Status Input
    Label(RootFrame, text="Input Due Date:").grid(row=14, column=0, sticky=N)
    UpdDD = Entry(RootFrame, width=30, bg="light blue")
    UpdDD.grid(row=15, column=0, sticky=N)
#Update Due Date Input
    Label(RootFrame, text="Input Completed Date:").grid(row=16, column=0, sticky=N)
    UpdCD = Entry(RootFrame, width=30, bg="light blue")
    UpdCD.grid(row=17, column=0, sticky=N)
#Update Completed Date Input
    Label(RootFrame, text="Input Person Responsible:").grid(row=18, column=0, sticky=N)
    UpdPR = Entry(RootFrame, width=30, bg="light blue")
    UpdPR.grid(row=19, column=0, sticky=N)
#Update Person Responsible Input
    Button(RootFrame, text="Update", command=lambda:UpdateMISButton(meeting_id, item_id, UpdAction.get(), UpdStatus.get(), UpdDD.get(), UpdCD.get(), UpdPR.get(), Output)).grid(row=30, column=0, sticky=N)
    Button(RootFrame, text="Back", command=lambda:RaiseViewMeetingFrame(Meeting)).grid(row=31, column=0, sticky=N)
#Creates Buttons

###Print Meeting Frame###
def RaisePrintMeetingFrame():
    ClearFrame()
    Button(RootFrame, text="Back", width=30, command=lambda:RaiseRootFrame()).grid(row=99, column=0, sticky=W)

###Add Item Frame###
def RaiseAddItemFrame():
    ClearFrame()
    Button(RootFrame, text="Back", width=30, command=lambda:RaiseRootFrame()).grid(row=99, column=0, sticky=W)

###Edit Item Frame###
def RaiseEditItemFrame():
    ClearFrame()
    Button(RootFrame, text="Back", width=30, command=lambda:RaiseRootFrame()).grid(row=99, column=0, sticky=W)

###View Item History Frame###
def RaiseViewItemHistoryFrame():
    ClearFrame()
    Button(RootFrame, text="Back", width=30, command=lambda:RaiseRootFrame()).grid(row=99, column=0, sticky=W)


RaiseRootFrame()

root.mainloop()



















