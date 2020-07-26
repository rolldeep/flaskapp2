import os
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
app.config['SECRET_KEY'] = 'noneofthemwouldgeas19203332'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    about = db.Column(db.String(4000))
    rating = db.Column(db.Float)
    picture = db.Column(db.String(255))
    price = db.Column(db.Integer)
    goals = db.Column(db.Text)
    free = db.Column(JSON)


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    weekday = db.Column(db.DateTime(), nullable=False)
    time = db.Column(db.Time(), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)

    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    teacher = db.relationship('Teacher')


class TeacherRequest(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(30), nullable=False)
    availability = db.Column(db.String(30), nullable=False)
    clientName = db.Column(db.String(30), nullable=False)
    clientPhone = db.Column(db.String(30), nullable=False)


def get_random_teachers(qnt):
    teachers = list()
    for _ in range(qnt):
        random_index = random.randint(1, 24)
        row = db.session.query(Teacher).get(random_index)
        teachers.append(row)
    return teachers


@app.route('/')
def main():
    teachers_list = get_random_teachers(6)
    return render_template('index.html', teachers_list=teachers_list)


@app.route('/goals/<goal>/')
def get_goal(goal):
    goal_title = goal
    teachers_list = db.session.query(Teacher)\
        .filter(goal in Teacher.goals)\
        .order_by(Teacher.rating.desc())
    return render_template('goal.html',
                           teachers_list=teachers_list,
                           goal_title=goal_title)


@app.route('/profiles/<id>/')
def get_teacher(id):
    teacher = db.session.query(Teacher).get_or_404(int(id))
    goals_string = ', '.join(teacher.goals)
    return render_template('profile.html',
                           name=teacher.name,
                           goals=goals_string,
                           rating=teacher.rating,
                           price=teacher.price,
                           picture=teacher.picture,
                           description=teacher.about,
                           free=teacher.free,
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
                           id=id)


@app.route('/booking/', methods=['POST'])
def save_booking():
    if request.method == 'POST':
        form = BookingForm()
        booking = Booking(clientWeekday=form.clientWeekday.data,
                          clientTime=form.clientTime.data,
                          clientTeacher=form.clientTeacher.data,
                          clientName=form.clientName.data,
                          clientPhone=form.clientPhone.data)
        if form.validate_on_submit():
            db.session.query.add(booking)
            return render_template('booking_done.html',
                                   clientWeekday=booking.clientWeekday,
                                   clientTime=booking.clientTime,
                                   clientName=booking.clientName,
                                   clientPhone=booking.clientPhone)
        return render_template('booking.html',
                               form=form,
                               name=db.session.query(Teacher).get(booking.clientTeacher).name,
                               day=booking.clientWeekday,
                               hour=booking.clientTime,
                               picture=db.session.query(Teacher).get(booking.clientTeacher).picture,
                               id=booking.clientTeacher)

# Убрал route, для воспроизведения корректной валидации формы
# @app.route('/booking_done/', methods=['POST'])


if __name__ == "__main__":
    app.run(debug=True)
