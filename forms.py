from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField
from wtforms.validators import InputRequired, Length


class BookingForm(FlaskForm):
    clientWeekday = StringField()
    clientTime = StringField()
    clientTeacher = IntegerField()
    clientName = StringField(
        'Вас зовут', [InputRequired(message='Заполните имя'), Length(min=1, max=20, message='Размер имени не должен превышать 20 символов')])
    clientPhone = StringField(
        'Ваш телефон', [InputRequired(message='Введите свой телефон'), Length(min=6, max=12)])


class RequestForm(FlaskForm):
    goals = RadioField('goal',
                       choices=[
                           ('Для путешествий', 'Для путешествий'),
                           ('Для школы', 'Для школы'),
                           ('Для работы', 'Для работы'),
                           ('Для переезда', 'Для переезда'),
                           ('Для программирования', 'Для программирования')
                       ])
    availability = RadioField('time',
                              choices=[
                                  ('1-2 часа в неделю', '1-2 часа в неделю'),
                                  ('3-5 часов в неделю', '3-5 часов в неделю'),
                                  ('5-7 часов в неделю', '5-7 часов в неделю'),
                                  ('7-10 часов в неделю', '7-10 часов в неделю')
                              ])
    clientName = StringField(
        'Вас зовут',
        [InputRequired(message='Заполните имя'),
         Length(min=1, max=20, message='Имя не должно превышать 20-ти символов')])
    clientPhone = StringField(
        'Ваш телефон', [InputRequired(message='Введите свой телефон'), Length(min=6, max=12, message='Введите валидный телефон')])
