class Event:

    def __init__(self,name,eventID,startDate,endDate,description,price,location,type,status,ticketNum):
        self.name = name
        self.eventId = eventID
        self.startDate = startDate
        self.endDate = endDate
        self.description = description
        self.price = price
        self.location = location
        self.type = type
        self.status = status
        self.ticketNum = ticketNum
    