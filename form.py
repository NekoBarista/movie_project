from flask_wtf import FlaskForm
from wtforms import Form, SubmitField, StringField, validators, FloatField

class ReviewForm(FlaskForm):
    rating= FloatField('Your rating out of 10', [validators.DataRequired()])
    review = StringField('Your Review', [validators.Length(min=6, max=35), validators.DataRequired()])
    submit = SubmitField('Submit')

class AddMovie(FlaskForm):
    title = StringField("Title", [validators.DataRequired()])
    add = SubmitField("Add Movie")