def CreateMeetingItemList(meeting):
    MeetingItems = meeting[4]
    MeetingItemList = MeetingItems.split(", ")
    return MeetingItemList
#Creates a list of meeting items from a specific meeting

def CreateItemListString(item_list):
    ItemListString = ", ".join(item_list)
    return ItemListString
#Creates an item list string from an item list

def CreateMeetingItemStatus(meeting, meeting_item, action="", status="", due_date="", completed_date="", person_responsible=""):
    MeetingItemStatus = "('"+meeting+"', '"+meeting_item+"', '"+action+"', '"+status+"', '"+due_date+"', '"+completed_date+"', '"+person_responsible+"')"
    return MeetingItemStatus
#Generates meeting item status data string

def CreateMeetingData(meeting, meeting_type, date, time, meeting_items):
    MeetingData = "('"+meeting+"', '"+meeting_type+"', '"+date+"', '"+time+"', '"+meeting_items+"')"
    return MeetingData
#Generates meeting data string
