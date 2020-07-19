import json


class Booking:
    row_id = 0

    def __init__(self, clientWeekday, clientTime, clientTeacher, clientName, clientPhone):
        self.clientWeekday = clientWeekday
        self.clientTime = clientTime
        self.clientTeacher = clientTeacher
        self.clientName = clientName
        self.clientPhone = clientPhone

    def save(self):
        record = dict()

        record[Booking.row_id] = {
            'clientTeacherId': self.clientTeacher,
            'clientWeekday': self.clientWeekday,
            'clientTime': self.clientTime,
            'clientName': self.clientName,
            'clientPhone': self.clientPhone
        }

        with open('booking.json', 'a', encoding='utf8') as f:
            json.dump(record, f, ensure_ascii=False)

        Booking.row_id += 1


class TeacherRequest:
    row_id = 0

    def __init__(self, goal, availability, clientName, clientPhone):
        self.goal = goal
        self.availability = availability
        self.clientName = clientName
        self.clientPhone = clientPhone

    def save(self):
        record = dict()

        record[TeacherRequest.row_id] = {
            'goal': self.goal,
            'availability': self.availability,
            'clientName': self.clientName,
            'clientPhone': self.clientPhone
        }

        with open('request.json', 'a', encoding='utf8') as f:
            json.dump(record, f, ensure_ascii=False)

        TeacherRequest.row_id += 1
