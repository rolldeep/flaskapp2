import json
class Booking():
    def __init__(self, clientWeekday, clientTime, clientTeacher, clientName, clientPhone):
        self.clientWeekday = clientWeekday
        self.clientTime = clientTime
        self.clientTeacher = clientTeacher
        self.clientName = clientName
        self.clientPhone = clientPhone
    
    def save(self):
        record = dict()

        record[self.clientTeacher] = {
            'clientWeekday': self.clientWeekday,
            'clientTime': self.clientTime,
            'clientName': self.clientName,
            'clientPhone': self.clientPhone
        }
        
        with open('booking.json', 'a', encoding='utf8') as f:
            json.dump(record, f, ensure_ascii=False)
