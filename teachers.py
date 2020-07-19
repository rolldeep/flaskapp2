import json
import random

class Teachers:
    def __init__(self):
        with open('base.json', encoding='utf8') as f:
            self.teachers = json.load(f)['teachers']
    
    def get_random(self):
        return random.sample(self.teachers, 6)

class Teacher:
    def __init__(self, id):
        self.id = id
        with open('base.json') as f:
            teachers = json.load(f)['teachers']
        self.name = teachers[self.id]['name']
        self.about = teachers[self.id]['about']
        self.rating = teachers[self.id]['rating']
        self.picture = teachers[self.id]['picture']
        self.price = teachers[self.id]['price']
        self.goals = teachers[self.id]['goals']
        self.free = teachers[self.id]['free']
        
    def get_shedule(self):
        tab = []
        for day, shedule in self.free.items():
            availability = []
            res = dict()
            for timeslot, available in shedule.items():
                if available:
                    availability.append(timeslot)
            if day == 'mon':
                res['Понедельник'] = availability
            elif day == 'tue':
                res['Вторник'] = availability
            elif day == 'wed':
                res['Среда'] = availability
            elif day == 'thu':
                res['Четверг'] = availability
            elif day == 'fri':
                res['Пятница'] = availability
            elif day == 'sat':
                res['Суббота'] = availability
            elif day == 'sun':
                res['Воскресенье'] = availability
            tab.append(res)
        return tab


if __name__ == "__main__":
    t = Teacher(1)
    
    
    print(t.get_shedule())