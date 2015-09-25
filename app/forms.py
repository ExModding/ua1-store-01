from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SubmitField, IntegerField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, NumberRange


class AddPC(Form):
    cpu = StringField('CPU', description="Описание CPU", validators=[DataRequired()])

    mb = StringField('Motherboard', description="Описание материнской платы", validators=[DataRequired()])

    video = StringField('Video', description="Video card", validators=[DataRequired()])

    ram = IntegerField('RAM', description="Значение в GB. Только цыфры",
                       validators=[DataRequired(message="Should be integer!"),
                                   NumberRange(min=1, max=64, message="Should be in range [1-64]")])

    hdd = IntegerField('HDD', description="Значение в GB. Только цыфры",
                       validators=[DataRequired(message="Should be integer!"),
                                   NumberRange(min=100, max=5000, message="Should be in range [100-5000]")])

    price = IntegerField('Price', description="Цена в грн. Только цыфры",
                         validators=[DataRequired(message="Should be integer!"),
                                              NumberRange(min=50, max=10000, message="Should be in range [50-10000]")])
    comment = TextAreaField('Description', description="Опционально",)
    pc_id = HiddenField('pc_id')
    submit = SubmitField('Submit')


class AddMonitor(Form):
    manufacturer = StringField('Производитель', validators=[DataRequired()])

    monitor_model = StringField('Модель', validators=[DataRequired()])

    size = IntegerField('Диагональ', validators=[DataRequired(message="Should be integer!"),
                                                 NumberRange(min=15, max=40, message="Should be in range [15-40]")])

    price = IntegerField('Price', description="Цена в грн. Только цыфры",
                         validators=[DataRequired(message="Should be integer!"),
                                              NumberRange(min=10, max=10000, message="Should be in range [10-10000]")])
    comment = TextAreaField('Description', description="Опционально",)
    monitor_id = HiddenField('pc_id')
    submit = SubmitField('Submit')