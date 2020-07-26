from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from flask_migrate import Migrate
import json
from booking import TeacherRequest
from forms import BookingForm, RequestForm
import os

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
    rating = db.Column(db.Integer)
    picture = db.Column(db.String(255))
    price = db.Column(db.Float)
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


@app.route('/')
def main():
    return render_template('index.html', teachers_list=t.get_random())


# @app.route('/goals/<goal>/')
# def get_goal(goal):
#     goal_title = t.goals[goal]
#     teachers_list = [
#         teacher for teacher in t.teachers if goal in teacher['goals']]
#     return render_template('goal.html', teachers_list=teachers_list, goal_title=goal_title)


@app.route('/profiles/<id>/')
def get_teacher(id):
    teacher = Teacher(int(id))
    goals_string = ', '.join(teacher.goals)
    return render_template('profile.html',
                           name=teacher.name,
                           goals=goals_string,
                           rating=teacher.rating,
                           price=teacher.price,
                           picture=teacher.picture,
                           description=teacher.about,
                           free=teacher.get_shedule(),
                           teacher_id=id)


@app.route('/request/', methods=['GET', 'POST'])
def make_request():
    form = RequestForm()
    if request.method == 'GET':
        return render_template('request.html', form=form)
    if request.method == 'POST':
        form = RequestForm()
        if form.validate_on_submit():
            tr = TeacherRequest(form.goals.data, form.availability.data,
                                form.clientName.data, form.clientPhone.data)
            tr.save()
            return render_template('request_done.html',
                                   goal=tr.goal,
                                   availability=tr.availability,
                                   clientName=tr.clientName,
                                   clientPhone=tr.clientPhone)
        return render_template('request.html', form=form)

# Убрал route, для воспроизведения корректной валидации формы
# @app.route('/request_done/', methods=['POST'])


@app.route('/booking/<id>/<booking_day>/<booking_time>/')
def booking(id, booking_day, booking_time):
    form = BookingForm()
    if request.method == 'GET':
        teacher = Teacher(int(id))
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
        clientWeekday = form.clientWeekday.data
        clientTime = form.clientTime.data
        clientTeacher = form.clientTeacher.data
        clientName = form.clientName.data
        clientPhone = form.clientPhone.data
        booking = Booking(clientWeekday, clientTime,
                          clientTeacher, clientName, clientPhone)
        if form.validate_on_submit():
            booking.save()
            return render_template('booking_done.html',
                                   clientWeekday=clientWeekday,
                                   clientTime=clientTime,
                                   clientName=clientName,
                                   clientPhone=clientPhone)
        return render_template('booking.html',
                               form=form,
                               name=Teacher(clientTeacher).name,
                               day=clientWeekday,
                               hour=clientTime,
                               picture=Teacher(clientTeacher).picture,
                               id=clientTeacher)

# Убрал route, для воспроизведения корректной валидации формы
# @app.route('/booking_done/', methods=['POST'])

def fill_db():
    with open('base.json') as f:
        teachers = json.load(f)['teachers']
    for t in teachers:
        t_db = Teacher(
            name=t['name'],
            about=t['about'],
            rating=t['rating'],
            picture=t['picture'],
            price=t['price'],
            goals=t['goals'],
            free=t['free']
        )
        db.session.add(t_db)
        db.session.commit()

if __name__ == "__main__":
    fill_db()
    app.run(debug=True)
