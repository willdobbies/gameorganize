from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerRangeField
from wtforms.validators import DataRequired
from gameorganize.model.game import GameEntry, Completion, Priority

class GameEntryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    platform = SelectField('Platform', choices=[], validators=[DataRequired()])
    completion = SelectField('Completion', choices=[type.name for type in Completion], validators=[DataRequired()])
    priority = SelectField('Priority', choices=[type.name for type in Priority], validators=[DataRequired()])
    cheev = IntegerRangeField('Achievements', validators=[DataRequired()])
    notes = StringField('Notes', validators=[DataRequired()])