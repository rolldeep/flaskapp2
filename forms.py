from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField
from wtforms.validators import InputRequired, Length


class BookingForm(FlaskForm):
    clientWeekday = StringField()
    clientTime = StringField()
    clientTeacher = IntegerField()
    clientName = StringField(
        'Вас зовут', [InputRequired(), Length(min=1, max=20)])
    clientPhone = StringField(
        'Ваш телефон', [InputRequired(), Length(min=6, max=12)])


class RequestForm(FlaskForm):
    goals = RadioField('goal',
                       choices=[
                           ("goal1", "Для путешествий"),
                           ("goal2", "Для школы"),
                           ("goal3", "Для работы"),
                           ("goal4", "Для переезда")
                       ])
    availability = RadioField('time',
                              choices=[
                                  ('time1', '1-2 часа в неделю'),
                                  ('time2', '3-5 часов в неделю'),
                                  ('time3', '5-7 часов в неделю'),
                                  ('time4', '7-10 часов в неделю')
                              ])
