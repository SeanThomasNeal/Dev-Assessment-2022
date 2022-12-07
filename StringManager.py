def CreateMeetingItemStatus(meeting, meeting_item, action="", status="", due_date="", completed_date="", person_responsible=""):
    MeetingItemStatus = "('"+meeting+"', '"+meeting_item+"', '"+action+"', '"+status+"', '"+due_date+"', '"+completed_date+"', '"+person_responsible+"')"
    return MeetingItemStatus
#Generates meeting item status data string

def CreateMeetingData(meeting, meeting_type, date, time):
    MeetingData = "('"+meeting+"', '"+meeting_type+"', '"+date+"', '"+time+"')"
    return MeetingData
#Generates meeting data string
