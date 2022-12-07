import sqlite3

def CursorDecorator(func):
    def wrapper(*args, **kwargs):
        MainDB = sqlite3.connect("Main.db")
        MainCursor = MainDB.cursor()
        result = func(MainCursor, *args, **kwargs)
        MainDB.commit()
        MainCursor.close()
        MainDB.close()
        return result
    return wrapper

@CursorDecorator
def CreateTables(MainCursor):
    MainCursor.execute("CREATE TABLE IF NOT EXISTS 'Meeting' (MeetingID TEXT, MeetingType TEXT, Date TEXT, Time TEXT)")
    MainCursor.execute("CREATE TABLE IF NOT EXISTS 'Meeting Item' (MeetingItemID TEXT, ItemName TEXT, ItemDescription TEXT)")
    MainCursor.execute("CREATE TABLE IF NOT EXISTS 'Meeting Item Status' (MeetingID TEXT, MeetingItemID TEXT, Action TEXT, Status TEXT, DueDate TEXT, DateCompleted TEXT, PersonResponsible TEXT)")
#Creates tables if they dont exist

@CursorDecorator
def DropTable(MainCursor, table):
    MainCursor.execute(
        "DROP TABLE IF EXISTS '"+table+"'"
    )
#Drops table if it exists

@CursorDecorator
def InsertData(MainCursor, table_name, data):
    MainCursor.execute(
        "INSERT INTO '" + table_name + "' VALUES " + data,
    )
#Inserts data into specific table

@CursorDecorator
def DeleteData(MainCursor, table_name, field, data):
    MainCursor.execute(
        "DELETE FROM '" + table_name + "' WHERE " + field + " = ?",
        (data,)
    )
#Deletes data from specific table based on matching field data

@CursorDecorator    
def ReadAllData(MainCursor, table_name):
    Data = MainCursor.execute(
        "SELECT * FROM '" + table_name + "'",
    ).fetchall()
    for i in Data:
        print(i)
#Reads all data in specific table

@CursorDecorator
def FetchAllData(MainCursor, table_name, field = "*"):
    Data = MainCursor.execute(
        "SELECT " + field + " FROM '" + table_name + "'",
    ).fetchall()
    return Data

@CursorDecorator
def FetchMeeting(MainCursor, meeting_id):
    Meeting = MainCursor.execute(
        "SELECT * FROM Meeting WHERE MeetingID = ?",
        (meeting_id,)
    ).fetchall()
    return Meeting[0]
#Fetches specific meeting

@CursorDecorator
def FetchAllMeetings(MainCursor, meeting_type):
    Meetings = MainCursor.execute(
        "SELECT * FROM Meeting WHERE MeetingType = ?",
        (meeting_type,)
    ).fetchall()
    return Meetings
#Fetches all meeting of specific type

@CursorDecorator
def FetchLastMeeting(MainCursor, meeting_type):
    Meetings = FetchAllMeetings(meeting_type)
    if Meetings == []:
        return Meetings
    else:
        LastMeeting = Meetings[-1]
        return LastMeeting
#Fetches last meeting of specific type

@CursorDecorator
def FetchMeetingItems(MainCursor, meeting_id):
    List = []
    LastMeetingItems = MainCursor.execute(
        "SELECT MeetingItemID FROM 'Meeting Item Status' WHERE MeetingID = ?",
        (meeting_id,)
    ).fetchall()
    for Item in LastMeetingItems:
        List.append(Item[0])
    return List

@CursorDecorator
def GenerateNewMeetingID(MainCursor, meeting_type):
    Letter = meeting_type[0]
    LastMeeting = FetchLastMeeting(meeting_type)
    if LastMeeting == []:
        NewMeetingNum = 1
    else:
        LastMeetingID = LastMeeting[0]
        LastMeetingNum = int(LastMeetingID[1:])
        NewMeetingNum = LastMeetingNum + 1
    NewMeetingID = Letter + str(NewMeetingNum)
    return NewMeetingID
#Creates ID for new meeting of specific type

@CursorDecorator
def ViewLastMeeting(MainCursor, meeting_type):
    LastMeeting = FetchLastMeeting(meeting_type)
    print(LastMeeting)
#Displays last meeting of specific type

@CursorDecorator
def ViewAllMeetings(MainCursor, meeting_type):
    Meetings = FetchAllMeetings(meeting_type)
    for i in Meetings:
        print(i)
#Displays all meetings of specific type

@CursorDecorator
def UpdateMISData(MainCursor, meeting_id, item_id, action, status, DDate, CDate, Person):
    MainCursor.execute(
        "UPDATE 'Meeting Item Status' SET Action = ? WHERE MeetingID = ? AND MeetingItemID = ?",
        (action, meeting_id, item_id)
    )
    MainCursor.execute(
        "UPDATE 'Meeting Item Status' SET Status = ? WHERE MeetingID = ? AND MeetingItemID = ?",
        (status, meeting_id, item_id)
    )
    MainCursor.execute(
        "UPDATE 'Meeting Item Status' SET DueDate = ? WHERE MeetingID = ? AND MeetingItemID = ?",
        (DDate, meeting_id, item_id)
    )
    MainCursor.execute(
        "UPDATE 'Meeting Item Status' SET DateCompleted = ? WHERE MeetingID = ? AND MeetingItemID = ?",
        (CDate, meeting_id, item_id)
    )
    MainCursor.execute(
        "UPDATE 'Meeting Item Status' SET PersonResponsible = ? WHERE MeetingID = ? AND MeetingItemID = ?",
        (Person, meeting_id, item_id)
    )
#Udates Meeting Item Status linked to specific MeetingID and MeetingItemID





















