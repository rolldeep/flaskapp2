import json
import data

base = dict()
base['goals'] = data.goals
base['teachers'] = data.teachers

with open('base.json', 'w', encoding='utf8') as f:
    json.dump(base, f, ensure_ascii=False)


