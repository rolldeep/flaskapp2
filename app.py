from flask import Flask, render_template, request

from teacher import Teacher
from booking import Booking
from forms import BookingForm, RequestForm

app = Flask(__name__)

app.secret_key = 'noneofthemwouldgeas19203332'


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/goals/<goal>/')
def get_goal(goal):
    return render_template('goal.html')


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


@app.route('/request/')
def make_request():
    form = RequestForm()
    return render_template('request.html', form=form)


@app.route('/request_done/', methods=['POST'])
def get_request():
    if request.method == 'POST':
        form = RequestForm()
        return render_template('request_done.html',
                               goal=form.goals.data,
                               availability=form.availability.data,
                               clientName=form.clientName.data,
                               clientPhone=form.clientPhone.data)


@app.route('/booking/<id>/<booking_day>/<booking_time>/')
def booking(id, booking_day, booking_time):
    form = BookingForm()
    teacher = Teacher(int(id))
    return render_template('booking.html',
                           form=form,
                           name=teacher.name,
                           day=booking_day,
                           hour=booking_time,
                           picture=teacher.picture,
                           id=id)


@app.route('/booking_done/', methods=['POST'])
def get_booking():
    if request.method == 'POST':
        form = BookingForm()
        clientWeekday = form.clientWeekday.data
        clientTime = form.clientTime.data
        clientTeacher = form.clientTeacher.data
        clientName = form.clientName.data
        clientPhone = form.clientPhone.data
        booking = Booking(clientWeekday, clientTime,
                          clientTeacher, clientName, clientPhone)
        booking.save()
        return render_template('booking_done.html',
                               clientWeekday=clientWeekday,
                               clientTime=clientTime,
                               clientName=clientName,
                               clientPhone=clientPhone
                               )


if __name__ == "__main__":
    app.run(debug=True)
