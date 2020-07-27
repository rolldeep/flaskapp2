import os
import re
import json
import random
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from flask_migrate import Migrate
from forms import BookingForm, RequestForm


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config['SECRET_KEY'] = 'noneofthemwouldgeas19203332'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

WEEK = {
    'mon': 'Понедельник',
    'tue': 'Вторник',
    'wed': 'Среда',
    'thu': 'Четверг',
    'fri': 'Пятница',
    'sat': 'Суббота',
    'san': 'Воскресенье',
}
GOALS = {"travel": "Для путешествий",
         "study": "Для учебы",
         "work": "Для работы",
         "relocate": "Для переезда",
         "programming": "Для программирования"}


goals_association = db.Table('teachers_goals',
                             db.Column('teacher_id', db.Integer, db.ForeignKey(
                                 'teachers.id'), primary_key=True),
                             db.Column('goal_id', db.Integer, db.ForeignKey(
                                 'goals.id'), primary_key=True)
                             )


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    about = db.Column(db.String(4000))
    rating = db.Column(db.Float)
    picture = db.Column(db.String(255))
    price = db.Column(db.Integer)
    free = db.Column(JSON)

    goals = db.relationship(
        'Goal', secondary=goals_association, back_populates='teachers')


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    weekday = db.Column(db.String(255), nullable=False)
    time = db.Column(db.Time(), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)

    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    teacher = db.relationship('Teacher')


class TeacherRequest(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(255), nullable=False)
    availability = db.Column(db.String(255), nullable=False)
    clientName = db.Column(db.String(255), nullable=False)
    clientPhone = db.Column(db.String(255), nullable=False)


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(255), nullable=False)
    goal_ru = db.Column(db.String(255), nullable=False)

    teachers = db.relationship(
        'Teacher', secondary=goals_association, back_populates="goals"
    )


def get_random_teachers(qnt):
    teachers = list()
    random_index = random.sample(range(1, 13), qnt)
    for i in random_index:
        row = db.session.query(Teacher).get(i)
        teachers.append(row)
    return teachers


@app.route('/')
def main():
    teachers_list = get_random_teachers(6)
    return render_template('index.html', teachers_list=teachers_list)


@app.route('/goals/<goal>/')
def get_goal(goal):
    goal_title = GOALS[goal]
    goals = db.session.query(Goal).filter(Goal.goal == goal)
    teachers_list = []
    teachers_id = []
    for g in goals:
        for t in g.teachers:
            if t.id in teachers_id:
                continue
            else:
                teachers_list.append(t)
                teachers_id.append(t.id)
    return render_template('goal.html',
                           teachers_list=teachers_list,
                           goal_title=goal_title,
                           teachers_id=teachers_id)


@app.route('/profiles/<id>/')
def get_teacher(id):
    teacher = db.session.query(Teacher).get_or_404(int(id))
    return render_template('profile.html',
                           name=teacher.name,
                           goals=teacher.goals,
                           rating=teacher.rating,
                           price=teacher.price,
                           picture=teacher.picture,
                           description=teacher.about,
                           free=teacher.free,
                           week=WEEK,
                           goals_dict=GOALS,
                           teacher_id=id)


@app.route('/request/', methods=['GET', 'POST'])
def make_request():
    form = RequestForm()
    if request.method == 'GET':
        return render_template('request.html', form=form)
    if request.method == 'POST':
        form = RequestForm()
        if form.validate_on_submit():
            tr = TeacherRequest(goal=form.goals.data,
                                availability=form.availability.data,
                                clientName=form.clientName.data,
                                clientPhone=form.clientPhone.data)
            db.session.add(tr)
            db.session.commit()
            return render_template('request_done.html',
                                   goal=tr.goal,
                                   availability=tr.availability,
                                   clientName=tr.clientName,
                                   clientPhone=tr.clientPhone)
        return render_template('request.html', form=form)


@app.route('/booking/<id>/<booking_day>/<booking_time>/')
def booking(id, booking_day, booking_time):
    form = BookingForm()
    teacher = db.session.query(Teacher).get(int(id))
    return render_template('booking.html',
                           form=form,
                           name=teacher.name,
                           day=booking_day,
                           hour=booking_time,
                           picture=teacher.picture,
                           week=WEEK,
                           id=id)


@app.route('/booking/', methods=['POST'])
def save_booking():
    if request.method == 'POST':
        form = BookingForm()
        booking = Booking(weekday=form.clientWeekday.data,
                          time=form.clientTime.data,
                          teacher_id=form.clientTeacher.data,
                          name=form.clientName.data,
                          phone=form.clientPhone.data)
        if form.validate_on_submit():
            db.session.add(booking)
            db.session.commit()
            return render_template('booking_done.html',
                                   clientWeekday=booking.weekday,
                                   clientTime=booking.time,
                                   clientName=booking.name,
                                   clientPhone=booking.phone,
                                   week=WEEK)
        return render_template('booking.html',
                               form=form,
                               name=db.session.query(Teacher).get(
                                   booking.teacher_id).name,
                               day=booking.weekday,
                               hour=booking.time,
                               picture=db.session.query(Teacher).get(
                                   booking.teacher_id).picture,
                               id=booking.teacher_id,
                               week=WEEK)

def add_goals():
    with open('base.json') as f:
        data = json.load(f)
    for g in data['goals']:
        gl = Goal(
            goal=g,
            goal_ru=GOALS[g]
        )
        db.session.add(gl)
    for t in data['teachers']:
        t_db = Teacher(
            name=t['name'],
            about=t['about'],
            rating=t['rating'],
            picture=t['picture'],
            price=t['price'],
            free=t['free']
        )
        db.session.add(t_db)
        goals_list = t['goals']
        for g in goals_list:
            goal = db.session.query(Goal).filter(Goal.goal == g).first()
            t_db.goals.append(goal)
    
    db.session.commit()

if __name__ == "__main__":
    app.run()
