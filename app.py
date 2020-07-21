from flask import Flask, render_template, request
import json
from teachers import Teacher, Teachers
from booking import Booking, TeacherRequest
from forms import BookingForm, RequestForm

app = Flask(__name__)

app.secret_key = 'noneofthemwouldgeas19203332'
t = Teachers()


@app.route('/')
def main():
    return render_template('index.html', teachers_list=t.get_random())


@app.route('/goals/<goal>/')
def get_goal(goal):
    goal_title = t.goals[goal]
    teachers_list = [
        teacher for teacher in t.teachers if goal in teacher['goals']]
    return render_template('goal.html', teachers_list=teachers_list, goal_title=goal_title)


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
        if form.validate_on_submit():
            booking.save()
            return render_template('booking_done.html',
                                   clientWeekday=clientWeekday,
                                   clientTime=clientTime,
                                   clientName=clientName,
                                   clientPhone=clientPhone
                                   )
        return render_template('booking.html',
                               form=form,
                               name=Teacher(clientTeacher).name,
                               day=clientWeekday,
                               hour=clientTime,
                               picture=Teacher(clientTeacher).picture,
                               id=clientTeacher)


if __name__ == "__main__":
    app.run(debug=True)
