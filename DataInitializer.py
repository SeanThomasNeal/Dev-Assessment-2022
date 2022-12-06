import sqlite3
import DatabaseManager
import StringManager

def CreateTestMeetings():
    TestList = ["TestData1", "TestData2", "TestData3"]
    TestString = ", ".join(TestList)
    MeetingTestData = "('T1', 'TestType', '2022.12.04', '12:00', '" + TestString + "')"
    DatabaseManager.InsertData("Meeting", MeetingTestData)

    TestList2 = ["TestData4", "TestData5", "TestData6"]
    TestString2 = ", ".join(TestList2)
    MeetingTestData2 = "('T2', 'TestType', '2022.12.04', '14:00', '" + TestString2 + "')"
    DatabaseManager.InsertData("Meeting", MeetingTestData2)

    TestList3 = ["TestData7", "TestData8", "TestData9"]
    TestString3 = ", ".join(TestList3)
    MeetingTestData3 = "('T3', 'TestType', '2022.12.04', '16:00', '" + TestString3 + "')"
    DatabaseManager.InsertData("Meeting", MeetingTestData3)
#Creates 3 Test meetings

def CreateFinanceMeetings():
    FMeetingItems1 = ", ".join(["Item1", "Item2", "Item3"])
    FMeetingData1 = "('F1', 'Finance', '2022-12-02', '10:00', '" + FMeetingItems1 + "')"
    DatabaseManager.InsertData("Meeting", FMeetingData1)

    FMeetingItems2 = ", ".join(["Item1", "Item4"])
    FMeetingData2 = "('F2', 'Finance', '2022-12-03', '10:00', '" + FMeetingItems2 + "')"
    DatabaseManager.InsertData("Meeting", FMeetingData2)

    FMeetingItems3 = ", ".join(["Item1", "Item4", "Item5"])
    FMeetingData3 = "('F3', 'Finance', '2022-12-04', '10:00', '" + FMeetingItems3 + "')"
    DatabaseManager.InsertData("Meeting", FMeetingData3)
#Creates 3 Finance meetings

def CreateMancoMeetings():
    MMeetingItems1 = ", ".join(["Item1", "Item2", "Item3"])
    MMeetingData1 = "('M1', 'MANCO', '2022-12-02', '11:00', '" + MMeetingItems1 + "')"
    DatabaseManager.InsertData("Meeting", MMeetingData1)

    MMeetingItems2 = ", ".join(["Item2", "Item6"])
    MMeetingData2 = "('M2', 'MANCO', '2022-12-03', '11:00', '" + MMeetingItems2 + "')"
    DatabaseManager.InsertData("Meeting", MMeetingData2)

    MMeetingItems3 = ", ".join(["Item2", "Item6", "Item7"])
    MMeetingData3 = "('M3', 'MANCO', '2022-12-04', '11:00', '" + MMeetingItems3 + "')"
    DatabaseManager.InsertData("Meeting", MMeetingData3)
#Creates 3 MANCO meetings

def CreatePtlMeetings():
    PMeetingItems1 = ", ".join(["Item1", "Item2", "Item3"])
    PMeetingData1 = "('P1', 'PTL', '2022-12-02', '12:00', '" + PMeetingItems1 + "')"
    DatabaseManager.InsertData("Meeting", PMeetingData1)

    PMeetingItems2 = ", ".join(["Item3", "Item8"])
    PMeetingData2 = "('P2', 'PTL', '2022-12-03', '12:00', '" + PMeetingItems2 + "')"
    DatabaseManager.InsertData("Meeting", PMeetingData2)

    PMeetingItems3 = ", ".join(["Item3", "Item8", "Item9"])
    PMeetingData3 = "('P3', 'PTL', '2022-12-04', '12:00', '" + PMeetingItems3 + "')"
    DatabaseManager.InsertData("Meeting", PMeetingData3)
#Creates 3 PTL meetings

def CreateItems():
    MeetingData = DatabaseManager.FetchAllData("Meeting")
    FullItemList = []
    for Meeting in MeetingData:
        ItemList = StringManager.CreateMeetingItemList(Meeting)
        for Item in ItemList:
            if Item not in FullItemList:
                FullItemList.append(Item)
    for i in range(len(FullItemList)):
        ItemData = "('" + FullItemList[i] + "', 'ItemName" + str(i+1) + "', 'ItemDecription" + str(i+1) + "')"
        DatabaseManager.InsertData("Meeting Item", ItemData)    
#Creates Initial Items

def GenerateInitialMIS():
    Action = ["Action1", "Action2", "Action3", "Action4", "Action5"]
    Status = ["Open", "Closed"]
    DueDate = ["2022-12-02", "2022-12-04", "2022-12-06"]
    DateCompleted = ["Incomplete", "2022-11-27", "2022-11-29", "2022-12-01"]
    PersonResponsible = ["William Smith", "Susan Harris", "James Wilde"]
    MeetingData = DatabaseManager.FetchAllData("Meeting")
    MeetingItemData = DatabaseManager.FetchAllData("Meeting Item")
    index = 0
    for i in range(len(MeetingData)):
        Meeting = MeetingData[i]
        MeetingItemList = StringManager.CreateMeetingItemList(Meeting)
        for Item in MeetingItemList:
            MeetingID = Meeting[0]
            ItemAction = Action[index%len(Action)]
            ItemStatus = Status[index%len(Status)]
            ItemDD = DueDate[index%len(DueDate)]
            ItemDC = DateCompleted[index%len(DateCompleted)]
            ItemPR = PersonResponsible[index%len(PersonResponsible)]
            index += 1
            MeetingItemStatus = StringManager.CreateMeetingItemStatus(MeetingID, Item, ItemAction, ItemStatus, ItemDD, ItemDC, ItemPR)
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
#Resets Database to initial data
