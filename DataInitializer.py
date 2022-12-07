import sqlite3
import DatabaseManager
import StringManager

def CreateTestMeetings():
    MeetingTestData = "('T1', 'TestType', '2022.12.04', '12:00')"
    DatabaseManager.InsertData("Meeting", MeetingTestData)

    MeetingTestData2 = "('T2', 'TestType', '2022.12.04', '14:00')"
    DatabaseManager.InsertData("Meeting", MeetingTestData2)

    MeetingTestData3 = "('T3', 'TestType', '2022.12.04', '16:00')"
    DatabaseManager.InsertData("Meeting", MeetingTestData3)
#Creates 3 Test meetings

def CreateFinanceMeetings():
    FMeetingData1 = "('F1', 'Finance', '2022-12-02', '10:00')"
    DatabaseManager.InsertData("Meeting", FMeetingData1)

    FMeetingData2 = "('F2', 'Finance', '2022-12-03', '10:00')"
    DatabaseManager.InsertData("Meeting", FMeetingData2)
    
    FMeetingData3 = "('F3', 'Finance', '2022-12-04', '10:00')"
    DatabaseManager.InsertData("Meeting", FMeetingData3)
#Creates 3 Finance meetings

def CreateMancoMeetings():
    MMeetingData1 = "('M1', 'MANCO', '2022-12-02', '11:00')"
    DatabaseManager.InsertData("Meeting", MMeetingData1)

    MMeetingData2 = "('M2', 'MANCO', '2022-12-03', '11:00')"
    DatabaseManager.InsertData("Meeting", MMeetingData2)

    MMeetingData3 = "('M3', 'MANCO', '2022-12-04', '11:00')"
    DatabaseManager.InsertData("Meeting", MMeetingData3)
#Creates 3 MANCO meetings

def CreatePtlMeetings():
    PMeetingData1 = "('P1', 'PTL', '2022-12-02', '12:00')"
    DatabaseManager.InsertData("Meeting", PMeetingData1)

    PMeetingData2 = "('P2', 'PTL', '2022-12-03', '12:00')"
    DatabaseManager.InsertData("Meeting", PMeetingData2)

    PMeetingData3 = "('P3', 'PTL', '2022-12-04', '12:00')"
    DatabaseManager.InsertData("Meeting", PMeetingData3)
#Creates 3 PTL meetings

def CreateItems():
    ItemList = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "Item 7", "Item 8", "Item 9"]
    for i in range(len(ItemList)):
        ItemData = "('" + ItemList[i] + "', 'ItemName" + str(i+1) + "', 'ItemDecription" + str(i+1) + "')"
        DatabaseManager.InsertData("Meeting Item", ItemData)    
#Creates Initial Items

def GenerateInitialMIS():
    Action = ["Action1", "Action2", "Action3", "Action4", "Action5"]
    Status = ["Open", "Closed"]
    DueDate = ["2022-12-02", "2022-12-04", "2022-12-06"]
    DateCompleted = ["Incomplete", "2022-11-27", "2022-11-29", "2022-12-01"]
    PersonResponsible = ["William Smith", "Susan Harris", "James Wilde"]
    Meetings = ["M1", "M2", "M3", "F1", "F2", "F3", "P1", "P2", "P3"]
    MeetingItemArray = [["Item 1", "Item 2", "Item 3"], ["Item 1", "Item 4"], ["Item 1", "Item 4", "Item 5"],
                     ["Item 1", "Item 2", "Item 3"], ["Item 2", "Item 6"], ["Item 2", "Item 6", "Item 7"],
                     ["Item 1", "Item 2", "Item 3"], ["Item 3", "Item 8"], ["Item 3", "Item 8", "Item 9"]]
    index = 0
    for i in range(len(Meetings)):
        Meeting = Meetings[i]
        MeetingItemList = MeetingItemArray[i]
        for Item in MeetingItemList:
            ItemAction = Action[index%len(Action)]
            ItemStatus = Status[index%len(Status)]
            ItemDD = DueDate[index%len(DueDate)]
            ItemDC = DateCompleted[index%len(DateCompleted)]
            ItemPR = PersonResponsible[index%len(PersonResponsible)]
            index += 1
            MeetingItemStatus = StringManager.CreateMeetingItemStatus(Meeting, Item, ItemAction, ItemStatus, ItemDD, ItemDC, ItemPR)
            DatabaseManager.InsertData("Meeting Item Status", MeetingItemStatus)
#Fetch all meetings
#Fetch all meeting items
#Generate MIS for each combination

def InitializeDatabase():
    DatabaseManager.DropTable("Meeting")
    DatabaseManager.DropTable("Meeting Item")
    DatabaseManager.DropTable("Meeting Item Status")
    DatabaseManager.CreateTables()
    CreateTestMeetings()
    CreateFinanceMeetings()
    CreateMancoMeetings()
    CreatePtlMeetings()
    CreateItems()
    GenerateInitialMIS()
    print("success")
#Resets Database to initial data
