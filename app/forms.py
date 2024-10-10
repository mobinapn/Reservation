from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DecimalField, DateField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class EventFilterForm(FlaskForm):
    place = StringField('Place')
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    min_price = DecimalField('Min Price')
    max_price = DecimalField('Max Price')
    min_rate = DecimalField('Min Rate')
    max_rate = DecimalField('Max Rate')
    min_capacity = IntegerField('Min Capacity')
    max_capacity = IntegerField('Max Capacity')
    submit = SubmitField('Filter')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    parent_id = HiddenField('Parent ID')  # This field is hidden and filled dynamically for replies
    submit = SubmitField('Post Comment')
